"""Judge: for each pair that passed the form check, an LLM says whether the two
topics are the same maths, proposes the name mapping, and scores it 0-10.
The mapping is then verified by the checker, so a confident wrong answer is caught."""
import config
import llm
from checker import check_mapping
from extractor import describe

PROMPT = """You check whether two topics from different fields are secretly the same mathematics.

Two topics are RELATED only if topic A's equation turns exactly into topic B's equation after renaming:
every quantity, constant and variable of A is replaced by a name (or a simple expression of names) from B.
Look-alikes are common and must be rejected: same words or similar shape is not enough.
Constants are free to absorb signs and number factors: a constant of A may map to a negative or scaled
expression of B's constants (e.g. {{"alpha": "-gamma", "k": "2/C"}}). Quantities must map to quantities.

For each pair return one JSON object:
  "pair_id" : copied exactly
  "related" : true or false
  "score"   : 0-10, how sure you are that a method for A would solve B's problem unchanged
  "mapping" : if related, an object from EVERY name in A (quantities, constants, variables) to an expression
              in B's names, e.g. {{"h": "y", "b": "1/k"}}; if not related, {{}}
  "reason"  : at most 15 words

Reply with only a JSON list, one object per pair, in the same order.

Pairs:
{pairs}
"""


def judge_batch(pairs, extracted, descriptions, model=None):
    """pairs: list of {"pair_id", "a", "b"}; extracted: topic_id -> topic dict;
    descriptions: topic_id -> description text. Returns (records, call_meta)."""
    model = model or config.JUDGE_MODEL
    blocks = []
    for p in pairs:
        a, b = extracted[p["a"]], extracted[p["b"]]
        blocks.append(
            f'- pair {p["pair_id"]}\n'
            f'  A ({p["a"]}): {descriptions[p["a"]]}\n  A structured: {describe(a)}\n'
            f'  B ({p["b"]}): {descriptions[p["b"]]}\n  B structured: {describe(b)}')
    prompt = PROMPT.format(pairs="\n".join(blocks))
    try:
        try:
            text, meta = llm.generate(model, prompt)
        except llm.LLMError as e:
            if "HTTP 503" not in str(e) or not config.BACKUP_JUDGE_MODEL or model == config.BACKUP_JUDGE_MODEL:
                raise
            text, meta = llm.generate(config.BACKUP_JUDGE_MODEL, prompt)   # main judge busy
            meta["fallback_from"] = model
        items = llm.parse_json(text)
        if isinstance(items, dict):
            items = [items]
    except llm.LLMError as e:
        return [{"action": "judge", "pair_id": p["pair_id"], "status": "failed", "error": str(e)} for p in pairs], {}

    # models sometimes copy the label too ("pair F011"): keep only the last word
    by_id = {str(i.get("pair_id", "")).split()[-1] if str(i.get("pair_id", "")).split() else "": i
             for i in items if isinstance(i, dict)}
    records = []
    for p in pairs:
        item = by_id.get(p["pair_id"])
        if item is None:
            records.append({"action": "judge", "pair_id": p["pair_id"], "status": "failed", "error": "missing from reply",
                            "raw": text[:1500]})
            continue
        related = bool(item.get("related"))
        try:
            score = float(item.get("score", 0))
        except (TypeError, ValueError):
            score = 0.0
        mapping = item.get("mapping") or {}
        map_ok, why = (check_mapping(extracted[p["a"]], extracted[p["b"]], mapping)
                       if related and mapping else (False, "judge said not related"))
        accepted = related and score >= config.ACCEPT_SCORE and map_ok
        records.append({"action": "judge", "pair_id": p["pair_id"], "status": "ok", "related": related,
                        "score": score, "mapping": mapping, "reason": item.get("reason", ""),
                        "mapping_ok": map_ok, "mapping_check": why, "accepted": accepted})
    return records, meta
