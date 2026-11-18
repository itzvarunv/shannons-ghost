"""Step 5: run extractor + judge on the disguised benchmark and score it.

    python3 run_benchmark.py                     # full run, pauses after every batch
    python3 run_benchmark.py --no-pause          # full run, no pauses
    python3 run_benchmark.py --max-batches 1     # do one batch, save progress, stop
    python3 run_benchmark.py --resume logs/<run> --max-batches 1   # continue a saved run

Progress is saved after every batch (state.json in the run folder), so a run can be
stopped and resumed at any point. Every batch of up to 10 actions writes its own report.

Gate: recall >= 6/8 and at most 1 decoy accepted.
"""
import argparse
import json
import sys
from pathlib import Path

import config
from bench import load, score
from batching import Run, chunks
from checker import TopicError, check_mapping, form_check
from extractor import extract_batch
from judge import judge_batch


class Budget:
    def __init__(self, n):
        self.left = n

    def take(self):
        if self.left is None:
            return True
        if self.left <= 0:
            return False
        self.left -= 1
        return True


def load_state(run):
    path = run.dir / "state.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"extracted": {}, "extract_done": [], "form_done": False, "to_judge": [],
            "verdicts": {}, "judged": [], "batch_no": 0, "extract_records": []}


def save_state(run, state):
    state["batch_no"] = run.batch_no
    (run.dir / "state.json").write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pause", action="store_true")
    ap.add_argument("--max-batches", type=int, default=None, help="stop after this many AI batches")
    ap.add_argument("--resume", default=None, help="run folder to continue")
    args = ap.parse_args()

    topics = load("topics_disguised.json")
    pairs = load("pairs_disguised.json")
    answers = load("answers_disguised.json")      # only used for scoring, never shown to a model
    descriptions = {t["id"]: t["description"] for t in topics}

    run = Run("benchmark", pause=not args.no_pause, existing=Path(args.resume) if args.resume else None)
    state = load_state(run)
    run.batch_no = state["batch_no"]
    budget = Budget(args.max_batches)

    # 1. extract equations, 10 topics per call
    todo = [t for t in topics if t["id"] not in state["extract_done"]]
    for batch in chunks(todo):
        if not budget.take():
            save_state(run, state)
            print(f"stopped after the batch limit; resume with: python3 run_benchmark.py --resume {run.dir.relative_to(config.ROOT)}")
            return 2
        records, meta = extract_batch(batch)
        for r in records:
            r["call"] = meta
            if r["status"] == "ok":
                ref = answers["topics"][r["topic_id"]]
                same, why = check_mapping(ref, r["topic"], {})
                r["matches_reference"] = same
                if not same:
                    r["reference_check"] = why
                # used even when wrong: a bad extraction is a real failure mode we want to measure
                state["extracted"][r["topic_id"]] = r["topic"]
            if r["status"] == "ok":         # failed topics stay in the to-do list and are retried on resume
                state["extract_done"].append(r["topic_id"])
                state["extract_records"].append({"topic_id": r["topic_id"], "status": r["status"],
                                                 "matches_reference": r.get("matches_reference", False)})
        run.write_batch("extract", records)
        save_state(run, state)

    # 2. form check (no AI) on every pair whose two topics were extracted
    if not state["form_done"]:
        extracted = state["extracted"]
        form_records = []
        for p in pairs:
            rec = {"action": "form_check", "pair_id": p["pair_id"], "a": p["a"], "b": p["b"]}
            if p["a"] not in extracted or p["b"] not in extracted:
                rec.update(status="failed", error="a topic failed extraction")
                state["verdicts"][p["pair_id"]] = False
            else:
                try:
                    same, sa, sb = form_check(extracted[p["a"]], extracted[p["b"]])
                    rec.update(status="ok", same_form=same, sig_a=str(sa), sig_b=str(sb))
                    if same:
                        state["to_judge"].append(p)
                    else:
                        state["verdicts"][p["pair_id"]] = False
                except TopicError as e:
                    rec.update(status="failed", error=str(e))
                    state["verdicts"][p["pair_id"]] = False
            form_records.append(rec)
        for batch in chunks(form_records):
            run.write_batch("form_check", batch)
        state["form_done"] = True
        save_state(run, state)

    # 3. judge the survivors, 10 pairs per call; the checker verifies each mapping
    todo = [p for p in state["to_judge"] if p["pair_id"] not in state["judged"]]
    for batch in chunks(todo):
        if not budget.take():
            save_state(run, state)
            print(f"stopped after the batch limit; resume with: python3 run_benchmark.py --resume {run.dir.relative_to(config.ROOT)}")
            return 2
        records, meta = judge_batch(batch, state["extracted"], descriptions)
        for r in records:
            r["call"] = meta
            state["verdicts"][r["pair_id"]] = bool(r.get("accepted"))
            state["judged"].append(r["pair_id"])
        run.write_batch("judge", records)
        save_state(run, state)

    # 4. score against the hidden answers
    rows = [{"pair_id": p["pair_id"], "label": answers["pairs"][p["pair_id"]]["label"],
             "plain_pair": answers["pairs"][p["pair_id"]]["plain_pair"],
             "accepted": state["verdicts"].get(p["pair_id"], False)} for p in pairs]
    s = score(rows)
    ex_ok = sum(1 for r in state["extract_records"] if r["matches_reference"])
    run.save("result.json", {"score": s, "extraction_correct": f"{ex_ok}/{len(topics)}", "rows": rows})

    print(f"\nextraction matched the reference: {ex_ok}/{len(topics)}")
    print(f"pairs judged: {len(state['to_judge'])}/{len(pairs)} (the rest failed the form check or extraction)")
    print(f"known pairs found: {s['TP']}/8   decoys accepted: {s['FP']}/8   "
          f"recall {s['recall']}   precision {s['precision']}")
    passed = s["TP"] >= 6 and s["FP"] <= 1
    print("GATE PASSED" if passed else "GATE FAILED")
    print(f"reports: {run.dir.relative_to(config.ROOT)}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
