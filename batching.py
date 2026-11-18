"""Batches of 10 actions, each saved as its own report (failures included)."""
import json
import time

import config


def chunks(items, n=config.BATCH_SIZE):
    for i in range(0, len(items), n):
        yield items[i:i + n]


class Run:
    """One run = one folder in logs/. Every batch writes batch_NNN_<stage>.jsonl
    and adds a line to summary.jsonl."""

    def __init__(self, name, pause=True, existing=None):
        if existing is not None:
            self.dir = existing if existing.is_absolute() else config.ROOT / existing
        else:
            self.dir = config.LOG_DIR / f"{time.strftime('%Y%m%d-%H%M%S')}_{name}"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.pause = pause
        self.batch_no = 0

    def write_batch(self, stage, records):
        self.batch_no += 1
        path = self.dir / f"batch_{self.batch_no:03d}_{stage}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
        ok = sum(1 for r in records if r.get("status") == "ok")
        summary = {"batch": self.batch_no, "stage": stage, "actions": len(records),
                   "ok": ok, "failed": len(records) - ok, "file": path.name}
        with open(self.dir / "summary.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(summary) + "\n")
        print(f"[batch {self.batch_no:03d} · {stage}] {len(records)} actions: {ok} ok, "
              f"{len(records) - ok} failed -> {path.relative_to(config.ROOT)}")
        if self.pause:
            input("    Saved. Analyse it, then press Enter for the next batch (Ctrl+C stops)... ")
        return path

    def save(self, filename, obj):
        (self.dir / filename).write_text(json.dumps(obj, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
