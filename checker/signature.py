"""The form check: reduce an equation to a 'signature' and compare signatures.

Different signatures mean the two topics cannot be the same maths, so the pair
is dropped without spending any AI call.

Signatures by kind:
    ode/pde   : ("diff", number of independent variables, shape of the equation with
                 derivatives as d<orders>, the quantity as f, constants merged into c)
                e.g. m*x'' + c*x' + k*x = F  ->  ("diff", 1, "add(c,mul(c,d1),mul(c,d2),mul(c,f))")
    algebraic : ("algebraic", shape with every name as v and number factors as n)
                e.g. U = k*x**2/2  ->  ("algebraic", "add(mul(n,pow(v,2),v),v)")
    (v1 of this file, which only looked at the changing quantities, was far too loose
     on real data; it is kept in archive/signature_v1_too_loose.py)
    logic     : ("logic", number of inputs, shape of the expression tree with
                 operator names hidden), e.g. x & (y | z) -> ("logic", 3, "op2(op2(v,v),v)")
"""
import sympy as sp
from sympy.core.function import AppliedUndef

from .parse import parse_topic


def signature(parsed):
    if parsed.kind == "logic":
        return ("logic", len(parsed.funcs), _shape(parsed.expr))
    if parsed.kind in ("ode", "pde"):
        return _diff_signature(parsed)
    return _algebraic_signature(parsed)


def form_check(topic_a, topic_b):
    """Return (same_form, signature_a, signature_b)."""
    sa = signature(parse_topic(topic_a))
    sb = signature(parse_topic(topic_b))
    return sa == sb, sa, sb


def _shape(e):
    if e.is_Symbol:
        return "v"
    kids = sorted(_shape(a) for a in e.args)
    return f"op{len(kids)}(" + ",".join(kids) + ")"


def _diff_signature(p):
    """Shape of the whole equation. Derivatives become d(orders), the changing quantity f;
    inside each product all constant factors merge into one 'c' (so k*x and x/C match),
    and every term without the changing quantity merges into one source 'c'."""
    expr = sp.expand(p.expr)
    deps = set(p.funcs.values())
    leaves = {}
    for d in expr.atoms(sp.Derivative):
        if d.expr in deps:
            counts = dict(d.variable_count)
            leaves[d] = "d" + "".join(str(int(counts.get(v, 0))) for v in p.indep)
    for f in deps:
        leaves[f] = "f"
    if not leaves:
        raise ValueError("no changing quantity found")
    return ("diff", len(p.indep), _shape_diff(expr, leaves))


def _has_leaf(e, leaves):
    return any(a in leaves for a in e.atoms(sp.Derivative, AppliedUndef))


def _shape_diff(e, leaves):
    if e in leaves:
        return leaves[e]
    if not _has_leaf(e, leaves):
        return "c"
    if e.is_Add:
        parts = [_shape_diff(a, leaves) for a in e.args if _has_leaf(a, leaves)]
        if any(not _has_leaf(a, leaves) for a in e.args):
            parts.append("c")
        return "add(" + ",".join(sorted(parts)) + ")"
    if e.is_Mul:
        var = sorted(_shape_diff(a, leaves) for a in e.args if _has_leaf(a, leaves))
        const = any(not _has_leaf(a, leaves) for a in e.args)
        return "mul(" + ",".join((["c"] if const else []) + var) + ")"
    if e.is_Pow:
        base, ex = e.args
        return f"pow({_shape_diff(base, leaves)},{ex if ex.is_Number else _shape_diff(ex, leaves)})"
    return f"{type(e).__name__}(" + ",".join(sorted(_shape_diff(a, leaves) for a in e.args)) + ")"


def _algebraic_signature(p):
    """Shape of the whole formula. Every name is a leaf 'v' (models often mislabel which
    names are constants), number factors become 'n'; powers are kept exactly."""
    return ("algebraic", _shape_alg(sp.expand(p.expr)))


def _shape_alg(e):
    if e.is_Number:
        return "n"
    if e.is_Symbol:
        return "v"
    if e.is_Add:
        return "add(" + ",".join(sorted(_shape_alg(a) for a in e.args)) + ")"
    if e.is_Mul:
        parts = sorted(_shape_alg(a) for a in e.args if not a.is_Number)
        if any(a.is_Number for a in e.args):
            parts = ["n"] + parts
        return "mul(" + ",".join(parts) + ")"
    if e.is_Pow:
        base, ex = e.args
        return f"pow({_shape_alg(base)},{ex if ex.is_Number else _shape_alg(ex)})"
    return f"{type(e).__name__}(" + ",".join(sorted(_shape_alg(a) for a in e.args)) + ")"
