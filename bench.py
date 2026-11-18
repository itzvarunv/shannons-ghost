"""Load benchmark files and score a set of verdicts against the hidden answers."""
import json

import config
from checker import TopicError, check_mapping, form_check


def load(name):
    with open(config.BENCH_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def check_pairs_with_answers(topics, pairs, answers):
    """No AI: run the form check, then the stored true mapping, on every pair."""
    by_id = {t["id"]: t for t in topics}
    rows = []
    for p in pairs:
        a, b = by_id[p["a"]], by_id[p["b"]]
        ans = answers[p["pair_id"]]
        try:
            same_form, sa, sb = form_check(a, b)
        except TopicError as e:
            same_form, sa, sb = False, f"parse error: {e}", ""
        if not same_form:
            map_ok, why = False, "form check failed"
        elif ans.get("mapping") is None:
            map_ok, why = False, "form passed, no mapping on file"
        else:
            map_ok, why = check_mapping(a, b, ans["mapping"])
        rows.append({"pair_id": p["pair_id"], "a": p["a"], "b": p["b"], "label": ans["label"],
                     "form_ok": same_form, "mapping_ok": map_ok, "accepted": same_form and map_ok,
                     "reason": why, "sig_a": str(sa), "sig_b": str(sb)})
    return rows


def score(rows):
    """rows need 'label' (hidden/decoy) and 'accepted' (bool)."""
    tp = sum(1 for r in rows if r["label"] == "hidden" and r["accepted"])
    fn = sum(1 for r in rows if r["label"] == "hidden" and not r["accepted"])
    fp = sum(1 for r in rows if r["label"] == "decoy" and r["accepted"])
    tn = sum(1 for r in rows if r["label"] == "decoy" and not r["accepted"])
    recall = tp / (tp + fn) if tp + fn else 0.0
    precision = tp / (tp + fp) if tp + fp else 0.0
    return {"TP": tp, "FN": fn, "FP": fp, "TN": tn, "recall": round(recall, 3), "precision": round(precision, 3)}


def print_rows(rows):
    for r in rows:
        mark = "ACCEPT" if r["accepted"] else "reject"
        print(f"  {r['pair_id']}  {r['label']:<6}  {mark:<6}  {r['a']} vs {r['b']}: {r['reason']}")
