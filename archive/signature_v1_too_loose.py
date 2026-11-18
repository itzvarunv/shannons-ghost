"""The form check: reduce an equation to a 'signature' and compare signatures.

Different signatures mean the two topics cannot be the same maths, so the pair
is dropped without spending any AI call.

Signatures by kind:
    ode/pde   : ("diff", number of independent variables,
                 the derivative orders that appear, linear?, has a source term?)
                e.g. m*x'' + c*x' + k*x = F  ->  ("diff", 1, ((0,), (1,), (2,)), True, True)
    algebraic : ("algebraic", number of changing quantities,
                 for each term the powers of the changing quantities in it)
                e.g. U = k*x**2/2  ->  ("algebraic", 2, (("1",), ("2",)))
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
    expr = sp.expand(p.expr)
    deps = set(p.funcs.values())
    replace, order = {}, {}
    for d in expr.atoms(sp.Derivative):
        if d.expr in deps:
            ph = sp.Dummy()
            counts = dict(d.variable_count)
            replace[d] = ph
            order[ph] = tuple(int(counts.get(v, 0)) for v in p.indep)
    for f in deps:
        ph = sp.Dummy()
        replace[f] = ph
        order[ph] = tuple(0 for _ in p.indep)
    e2 = expr.xreplace(replace)
    if e2.atoms(AppliedUndef):
        raise ValueError(f"could not reduce {expr} to placeholders")
    present = [ph for ph in order if ph in e2.free_symbols]
    try:
        linear = sp.Poly(e2, *present).total_degree() <= 1
    except sp.PolynomialError:      # e.g. sin(x): not a polynomial in x
        linear = False
    rest = e2.xreplace({ph: 0 for ph in present})
    has_source = sp.simplify(rest) != 0
    orders = tuple(sorted({order[ph] for ph in present}))
    return ("diff", len(p.indep), orders, linear, bool(has_source))


def _algebraic_signature(p):
    expr = sp.expand(p.expr)
    quantities = list(p.funcs.values())
    terms = []
    for term in sp.Add.make_args(expr):
        inside_function = any(q in f.free_symbols for f in term.atoms(sp.Function) for q in quantities)
        if inside_function:
            terms.append(("nonpoly",))
            continue
        powers = term.as_powers_dict()
        terms.append(tuple(sorted(str(powers[q]) for q in quantities if powers.get(q, 0) != 0)))
    return ("algebraic", len(quantities), tuple(sorted(terms)))
