"""The mapping check: does topic A's equation become topic B's under a proposed mapping?

mapping is a dict {name in A: expression written in B's names}, for example
    {"x": "q", "m": "L", "c": "R", "k": "1/C", "F": "V"}
A name left out maps to the same name in B, if B has one. Independent variables
left out map in order (A's 1st to B's 1st, ...).

The link holds when A-after-mapping divided by B simplifies to a non-zero
constant (equal up to an overall factor). For logic, the two expressions must
agree on every possible input.
"""
import sympy as sp
from sympy.core.function import AppliedUndef

from .parse import TopicError, parse_logic_text, parse_math_text, parse_topic


def _family(kind):
    return "diff" if kind in ("ode", "pde") else kind


def check_mapping(topic_a, topic_b, mapping):
    """Return (ok, reason)."""
    try:
        pa, pb = parse_topic(topic_a), parse_topic(topic_b)
    except TopicError as e:
        return False, f"parse error: {e}"
    if _family(pa.kind) != _family(pb.kind):
        return False, f"different kinds ({pa.kind} vs {pb.kind})"
    mapping = {str(k): str(v) for k, v in (mapping or {}).items()}
    try:
        if pa.kind == "logic":
            return _check_logic(pa, pb, mapping, topic_b.get("semantics") or {})
        return _check_math(pa, pb, mapping)
    except TopicError as e:
        return False, f"bad mapping value: {e}"


def _target(name, mapping, pb):
    if name in mapping:
        return mapping[name]
    if name in pb.names:
        return name
    return None


def _check_math(pa, pb, mapping):
    # 1. give every A name a private spelling so A and B names can never collide
    private = {obj: sp.Symbol("__A__" + name) for name, obj in pa.names.items()
               if isinstance(obj, sp.Symbol)}
    expr = pa.expr.xreplace(private)

    # 2. independent variables (time, position)
    indep_sub = {}
    for i, s in enumerate(pa.indep):
        if s.name in mapping:
            indep_sub[private[s]] = parse_math_text(mapping[s.name], pb.names)
        elif i < len(pb.indep):
            indep_sub[private[s]] = pb.indep[i]
        else:
            return False, f"no independent variable in B for {s.name}"
    expr = expr.xreplace(indep_sub)

    used_symbols = pa.expr.free_symbols
    used_funcs = pa.expr.atoms(AppliedUndef)

    # 3. the changing quantities (only those that appear in the equation need a mapping)
    for name, obj in pa.funcs.items():
        if obj not in used_symbols and obj not in used_funcs:
            continue
        target = _target(name, mapping, pb)
        if target is None:
            return False, f"no mapping for {name}"
        value = parse_math_text(target, pb.names)
        if pa.kind in ("ode", "pde"):
            applied = obj.func(*[indep_sub[private[s]] for s in pa.indep])
            expr = expr.xreplace({applied: value})
        else:
            expr = expr.xreplace({private[obj]: value})

    # 4. constants
    const_sub = {}
    for name, obj in pa.params.items():
        if obj not in used_symbols:
            continue
        target = _target(name, mapping, pb)
        if target is None:
            return False, f"no mapping for parameter {name}"
        const_sub[private[obj]] = parse_math_text(target, pb.names)
    expr = expr.xreplace(const_sub).doit()

    leftovers = sorted(s.name[5:] for s in expr.free_symbols if s.name.startswith("__A__"))
    if leftovers:
        return False, f"unmapped names: {leftovers}"
    if pb.expr == 0:
        return False, "B's equation is empty"
    ratio = sp.simplify(expr / pb.expr)
    if ratio == 0 or ratio.free_symbols or ratio.atoms(AppliedUndef) or ratio.is_finite is False:
        return False, f"A does not become B (A/B = {ratio})"
    return True, f"A becomes B (A/B = {ratio})"


def _check_logic(pa, pb, mapping, semantics_b):
    private = {obj: sp.Symbol("__A__" + name) for name, obj in pa.funcs.items()}
    expr = pa.expr.xreplace(private)
    sub = {}
    for name, obj in pa.funcs.items():
        target = _target(name, mapping, pb)
        if target is None:
            return False, f"no mapping for {name}"
        sub[private[obj]] = parse_logic_text(target, pb.names, semantics_b)
    expr = expr.xreplace(sub)
    leftovers = sorted(s.name[5:] for s in expr.free_symbols if s.name.startswith("__A__"))
    if leftovers:
        return False, f"unmapped names: {leftovers}"
    if sp.satisfiable(sp.Xor(expr, pb.expr)) is False:
        return True, "same truth table"
    return False, "truth tables differ"
