"""Judge: for each pair that passed the form check, an LLM says whether the two
topics are the same maths, proposes the name mapping, and scores it 0-10.
The mapping is then verified by the checker, so a confident wrong answer is caught."""
import config
import llm
from checker import check_mapping
from extractor import describe

PROMPT = """You compare pairs of topics, usually from DIFFERENT fields, looking for mathematics they secretly share.
Different fields is expected and is never a reason for a low score: finding links across fields is the whole point.

For every pair, do two things:
1. Propose your best mapping: an object from every name in A's equation (quantities, constants, variables)
   to a name or simple expression of B's names, so that A's equation turns into B's. Constants are free to
   absorb signs and number factors (e.g. {{"alpha": "-gamma", "k": "2/C"}}); quantities map to quantities.
   Every key must be ONE name from A, never an expression: to match a ratio like g/l with 1/(L*C),
   write {{"g": "1", "l": "L*C"}}, not {{"g/l": "1/(L*C)"}}.
   Always give your best attempt, even if you doubt it.
2. Score 0-10: how strongly the two share the same mathematics, so that a method or result for A would
   carry over to B. 10 = identical structure, 0 = nothing in common. Judge the equations, not the topics' fields.

Return one JSON object per pair:
  "pair_id" : copied exactly (just the id, e.g. "F011")
  "score"   : 0-10
  "mapping" : your best mapping (never empty)
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
        try:
            score = float(item.get("score", 0))
        except (TypeError, ValueError):
            score = 0.0
        mapping = item.get("mapping") or {}
        map_ok, why = (check_mapping(extracted[p["a"]], extracted[p["b"]], mapping)
                       if mapping else (False, "no mapping given"))
        review = score >= config.REVIEW_SCORE          # flagged for a human to look at
        accepted = review and map_ok                   # used for benchmark scoring
        records.append({"action": "judge", "pair_id": p["pair_id"], "status": "ok", "review": review,
                        "score": score, "mapping": mapping, "reason": item.get("reason", ""),
                        "mapping_ok": map_ok, "mapping_check": why, "accepted": accepted})
    return records, meta
