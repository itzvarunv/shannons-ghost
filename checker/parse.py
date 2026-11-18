"""Turn a topic (a small dict describing one equation) into sympy objects.

A topic looks like:
    {"id": "msd", "kind": "ode", "independent": ["t"], "dependent": ["x"],
     "params": ["m", "c", "k", "F"], "equation": "m*D(x, t, 2) + c*D(x, t, 1) + k*x = F"}

kind:
    ode       - one independent variable (usually time), derivatives written D(f, var, n)
    pde       - several independent variables, same D() syntax
    algebraic - no derivatives; "dependent" lists the changing quantities
    logic     - true/false expressions; "variables" lists the inputs and
                "semantics" says what each named operator means (And, Or, Xor, ...)

The equation "lhs = rhs" is stored as the expression lhs - rhs (meaning "= 0").
Every name used must be declared, so a typo is caught instead of silently
turning into a new symbol (or into sympy's built-in E or I).
"""
import re

import sympy as sp
from sympy.core.function import AppliedUndef
from sympy.parsing.sympy_parser import convert_xor, parse_expr, standard_transformations

KINDS = ("ode", "pde", "algebraic", "logic")

LOGIC_OPS = {
    "And": sp.And, "Or": sp.Or, "Not": sp.Not, "Xor": sp.Xor,
    "Nand": sp.Nand, "Nor": sp.Nor, "Implies": sp.Implies, "Equivalent": sp.Equivalent,
}

# The only names an equation may use besides its own declared names.
SAFE_GLOBALS = {
    "Integer": sp.Integer, "Float": sp.Float, "Rational": sp.Rational,
    "Symbol": sp.Symbol, "Function": sp.Function,
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "exp": sp.exp, "log": sp.log,
    "sqrt": sp.sqrt, "Abs": sp.Abs, "pi": sp.pi,
}

MATH_TRANSFORMS = standard_transformations + (convert_xor,)   # ^ means power in maths
LOGIC_TRANSFORMS = standard_transformations                   # ^ means Xor in logic


# Maths symbols models often write instead of plain ASCII.
UNICODE_MATH = {"·": "*", "×": "*", "−": "-", "–": "-", "÷": "/", "²": "**2", "³": "**3", "⁴": "**4"}
UNICODE_LOGIC = {"∧": "&", "∨": "|", "¬": "~", "⊕": "^"}


def _plain(text, table):
    text = str(text)
    for k, v in table.items():
        text = text.replace(k, v)
    return text


class TopicError(ValueError):
    """The topic's equation cannot be parsed, or it uses names it never declared."""


class Parsed:
    """A parsed topic.

    kind    : one of KINDS
    expr    : sympy expression meaning "expr = 0" (for logic: the logic expression itself)
    indep   : independent-variable Symbols, in declared order (ode/pde only)
    funcs   : name -> the changing quantity (applied function for ode/pde,
              Symbol for algebraic, input variable for logic)
    params  : name -> constant Symbol
    names   : every declared name -> its sympy object
    """

    def __init__(self, kind, expr, indep, funcs, params, names):
        self.kind = kind
        self.expr = expr
        self.indep = indep
        self.funcs = funcs
        self.params = params
        self.names = names


def D(f, var, n=1):
    """D(x, t, 2) is the 2nd derivative of x with respect to t."""
    return sp.Derivative(f, (var, int(n)))


def parse_topic(topic):
    kind = topic.get("kind")
    if kind not in KINDS:
        raise TopicError(f"unknown kind {kind!r}; expected one of {KINDS}")
    if "equation" not in topic or not str(topic["equation"]).strip():
        raise TopicError("topic has no equation")
    if kind == "logic":
        return _parse_logic(topic)
    return _parse_math(topic, kind)


def _parse_math(topic, kind):
    indep = [sp.Symbol(n) for n in topic.get("independent") or []]
    if kind in ("ode", "pde") and not indep:
        raise TopicError(f"a {kind} needs at least one independent variable")
    if kind == "ode" and len(indep) != 1:
        raise TopicError("an ode has exactly one independent variable; use kind 'pde' for more")

    names = {s.name: s for s in indep}
    funcs = {}
    for n in topic.get("dependent") or []:
        obj = sp.Function(n)(*indep) if kind in ("ode", "pde") else sp.Symbol(n)
        funcs[n] = obj
        names[n] = obj
    if not funcs:
        raise TopicError("topic declares no dependent quantity")
    params = {}
    for n in topic.get("params") or []:
        params[n] = sp.Symbol(n)
        names[n] = params[n]

    expr = parse_math_text(topic["equation"], names)

    declared_symbols = {o for o in names.values() if isinstance(o, sp.Symbol)}
    undeclared = expr.free_symbols - declared_symbols
    if undeclared:
        raise TopicError(f"undeclared names: {sorted(s.name for s in undeclared)}")
    allowed_funcs = set(funcs.values()) if kind in ("ode", "pde") else set()
    stray = {f for f in expr.atoms(AppliedUndef) if f not in allowed_funcs}
    if stray:
        raise TopicError(f"undeclared functions: {sorted(str(f) for f in stray)}")
    if kind in ("ode", "pde") and not (expr.atoms(AppliedUndef) & allowed_funcs):
        raise TopicError("the dependent quantity never appears in the equation")
    return Parsed(kind, expr, indep, funcs, params, names)


def parse_math_text(text, names):
    """Parse 'lhs = rhs' (or a bare expression) using only the given names."""
    text = _plain(text, UNICODE_MATH)
    # a common slip: Dv(t, 1) for D(v, t, 1)
    text = re.sub(r"\bD([A-Za-z_]\w*)\(\s*([A-Za-z_]\w*)\s*,\s*(\d+)\s*\)", r"D(\1, \2, \3)", text)
    parts = re.split(r"(?<![<>=!])=(?!=)", text)
    if len(parts) > 2:                      # chained a = b = c: keep the outer relation a = c
        parts = [parts[0], parts[-1]]
    local = dict(names)
    local["D"] = D
    try:
        sides = [parse_expr(p, local_dict=local, global_dict=dict(SAFE_GLOBALS),
                            transformations=MATH_TRANSFORMS) for p in parts]
    except Exception as e:  # sympy raises many different error types here
        raise TopicError(f"cannot parse {text!r}: {e}") from e
    return sp.expand(sides[0] - sides[1]) if len(sides) == 2 else sp.expand(sides[0])


def _parse_logic(topic):
    variables = [sp.Symbol(n) for n in (topic.get("variables") or topic.get("dependent") or [])]
    if not variables:
        raise TopicError("logic topic declares no variables")
    names = {s.name: s for s in variables}
    expr = parse_logic_text(topic["equation"], names, topic.get("semantics") or {})
    undeclared = expr.free_symbols - set(variables)
    if undeclared:
        raise TopicError(f"undeclared names: {sorted(s.name for s in undeclared)}")
    return Parsed("logic", expr, [], dict(names), {}, names)


def parse_logic_text(text, names, semantics):
    local = dict(names)
    local.update(LOGIC_OPS)
    for op, meaning in semantics.items():
        if not str(op).isidentifier():      # e.g. {"∧": "And"}: symbols are handled by UNICODE_LOGIC
            continue
        if meaning not in LOGIC_OPS:
            raise TopicError(f"operator {op!r} has unknown meaning {meaning!r}; use one of {list(LOGIC_OPS)}")
        local[op] = LOGIC_OPS[meaning]
    try:
        expr = parse_expr(_plain(text, UNICODE_LOGIC), local_dict=local, global_dict=dict(SAFE_GLOBALS),
                          transformations=LOGIC_TRANSFORMS)
    except Exception as e:
        raise TopicError(f"cannot parse {text!r}: {e}") from e
    if not isinstance(expr, sp.logic.boolalg.Boolean):
        raise TopicError(f"{text!r} is not a true/false expression")
    return expr
