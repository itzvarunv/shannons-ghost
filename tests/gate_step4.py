"""Step 4 gate (no AI): the checker must give the same verdict on every disguised pair
as on the plain pair it came from."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bench import check_pairs_with_answers, load, print_rows, score  # noqa: E402

plain = {r["pair_id"]: r for r in check_pairs_with_answers(
    load("topics_plain.json"), load("pairs_plain.json"), load("answers_plain.json"))}

ans = load("answers_disguised.json")
topics = list(ans["topics"].values())
rows = check_pairs_with_answers(topics, load("pairs_disguised.json"), ans["pairs"])
print("Step 4 gate: checker on disguised pairs")
print_rows(rows)

mismatch = [r["pair_id"] for r in rows
            if r["accepted"] != plain[ans["pairs"][r["pair_id"]]["plain_pair"]]["accepted"]]
s = score(rows)
print(f"\nknown pairs accepted: {s['TP']}/8   decoys accepted: {s['FP']}/8   disagreements with plain: {mismatch or 'none'}")
passed = not mismatch and s["TP"] == 8 and s["FP"] == 0
print("GATE PASSED" if passed else "GATE FAILED")
sys.exit(0 if passed else 1)
