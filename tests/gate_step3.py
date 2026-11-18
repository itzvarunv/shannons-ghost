"""Step 3 gate (no AI): the 8 known pairs must pass, the 8 decoys must fail."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bench import check_pairs_with_answers, load, print_rows, score  # noqa: E402

rows = check_pairs_with_answers(load("topics_plain.json"), load("pairs_plain.json"), load("answers_plain.json"))
print("Step 3 gate: checker on plain-named pairs")
print_rows(rows)
s = score(rows)
print(f"\nknown pairs accepted: {s['TP']}/8   decoys accepted: {s['FP']}/8")
passed = s["TP"] == 8 and s["FP"] == 0
print("GATE PASSED" if passed else "GATE FAILED")
sys.exit(0 if passed else 1)
