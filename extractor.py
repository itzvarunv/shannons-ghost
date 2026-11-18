"""Extractor: an LLM reads topic descriptions and writes each one's equation in
the checker's format. Up to 10 topics per call (one call = one batch)."""
import json
import re

import config
import llm
from checker import TopicError, parse_topic

PROMPT = """You turn short scientific descriptions into structured equations.

For each topic below, return one JSON object with these keys:
  "topic_id"   : the topic's id, copied exactly
  "kind"       : "ode" (rates of change in one variable), "pde" (rates of change in several variables),
                 "algebraic" (no rates of change) or "logic" (true/false statements)
  "independent": for ode/pde, the variables things change with, e.g. ["s"]; otherwise []
  "dependent"  : the changing quantities (ode/pde/algebraic), e.g. ["h"]
  "variables"  : for logic only, the true/false inputs, e.g. ["p", "q"]
  "params"     : the constants, e.g. ["b", "f"]
  "semantics"  : for logic only, what each NAMED operator means, using And, Or, Xor or Not, e.g. {{"blend": "And"}}; otherwise {{}}
  "equation"   : the equation as text, using these rules:
       - use exactly the names from the description; never rename anything
       - * for multiply, / for divide, ** for powers (x² is x**2)
       - a rate of change is D(quantity, variable, order): h' with respect to s is D(h, s, 1), h'' is D(h, s, 2),
         ∂²u/∂x² is D(u, x, 2)
       - write "left side = right side" exactly as the description states it
       - logic: & for "and", | for "or", ~ for "not", ^ for "exactly one"; keep named operators as functions, e.g. blend(p, q)

Examples (not part of the task):
  "A tank level h changes with time s; inflow f and leak constant b give h' = f − b·h"
    -> {{"topic_id": "X1", "kind": "ode", "independent": ["s"], "dependent": ["h"], "variables": [], "params": ["f", "b"], "semantics": {{}}, "equation": "D(h, s, 1) = f - b*h"}}
  "The yield y of a crop with feed h and constant b follows y = b·h³"
    -> {{"topic_id": "X2", "kind": "algebraic", "independent": [], "dependent": ["y", "h"], "variables": [], "params": ["b"], "semantics": {{}}, "equation": "y = b*h**3"}}
  "blend(p, q) holds only when both p and q hold"
    -> {{"topic_id": "X3", "kind": "logic", "independent": [], "dependent": [], "variables": ["p", "q"], "params": [], "semantics": {{"blend": "And"}}, "equation": "blend(p, q)"}}

Reply with only a JSON list of objects, one per topic, in the same order.

Topics:
{topics}
"""


def extract_batch(topics, prompt_template=PROMPT, lenient=False):
    """topics: list of {"id", "field", "description"}.
    Returns (records, call_meta). Each record has status ok/skipped/failed and, if ok, a topic dict."""
    listing = "\n".join(f'- id {t["id"]} ({t["field"]}): {t["description"]}' for t in topics)
    prompt = prompt_template.format(topics=listing)
    try:
        text, meta = llm.generate(config.EXTRACTOR_MODEL, prompt)
    except llm.LLMError as e:
        if "HTTP 503" not in str(e) or not config.FALLBACK_EXTRACTOR_MODEL:
            return [{"action": "extract", "topic_id": t["id"], "status": "failed", "error": str(e)} for t in topics], {}
        try:                                  # main model busy: same batch on the fallback model
            text, meta = llm.generate(config.FALLBACK_EXTRACTOR_MODEL, prompt)
            meta["fallback_from"] = config.EXTRACTOR_MODEL
        except llm.LLMError as e2:
            return [{"action": "extract", "topic_id": t["id"], "status": "failed",
                     "error": f"main: {e} | fallback: {e2}"} for t in topics], {}
    try:
        items = llm.parse_json(text)
        if isinstance(items, dict):
            items = [items]
    except llm.LLMError as e:
        return [{"action": "extract", "topic_id": t["id"], "status": "failed", "error": str(e),
                 "raw": text[:2000]} for t in topics], meta

    by_id = {str(i.get("topic_id")): i for i in items if isinstance(i, dict)}
    records = []
    for t in topics:
        item = by_id.get(t["id"])
        if item is None:
            records.append({"action": "extract", "topic_id": t["id"], "status": "failed", "error": "missing from reply"})
            continue
        if item.get("skip") or item.get("kind") == "skip":
            records.append({"action": "extract", "topic_id": t["id"], "status": "skipped",
                            "why": str(item.get("why", ""))[:200]})
            continue
        topic = {"id": t["id"], "kind": item.get("kind"), "equation": item.get("equation", "")}
        for key in ("independent", "dependent", "variables", "params"):
            topic[key] = list(item.get(key) or [])
        topic["semantics"] = dict(item.get("semantics") or {})
        if topic["kind"] == "algebraic" and not topic["dependent"] and topic["params"]:
            # the model put everything under params: treat all names as changing quantities
            topic["dependent"], topic["params"] = topic["params"], []
            topic["dependent_guessed"] = True
        try:
            try:
                parse_topic(topic)
            except TopicError as e:
                missing = re.search(r"undeclared names: \[(.*)\]", str(e))
                if not (lenient and missing):
                    raise
                # lenient mode (real data): names the model used but forgot to declare become constants
                extra = [n.strip().strip("'\"") for n in missing.group(1).split(",")]
                topic["params"] = topic["params"] + extra
                topic["auto_declared"] = extra
                parse_topic(topic)
            records.append({"action": "extract", "topic_id": t["id"], "status": "ok", "topic": topic})
        except TopicError as e:
            records.append({"action": "extract", "topic_id": t["id"], "status": "failed",
                            "error": f"unparseable: {e}", "topic": topic})
    return records, meta


def describe(topic):
    """Compact text of an extracted topic, for the judge."""
    parts = [f'kind {topic["kind"]}', f'equation: {topic["equation"]}']
    for key in ("independent", "dependent", "variables", "params"):
        if topic.get(key):
            parts.append(f'{key}: {", ".join(topic[key])}')
    if topic.get("semantics"):
        parts.append("operators: " + json.dumps(topic["semantics"]))
    return "; ".join(parts)
