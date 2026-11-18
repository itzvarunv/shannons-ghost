"""Step 2 gate: the key works, the chosen models exist, and one prompt to each
comes back and is saved to logs/."""
import json
import sys
import time

import config
import llm


def main():
    print("Listing models this key can use...")
    try:
        models = llm.list_models()
    except llm.LLMError as e:
        print(f"FAILED: {e}")
        return 1
    wanted = [config.EXTRACTOR_MODEL, config.JUDGE_MODEL, config.BACKUP_JUDGE_MODEL]
    for w in wanted:
        print(f"  {w:<28} {'found' if w in models else 'NOT FOUND'}")
    missing = [w for w in wanted if w not in models]
    if missing:
        print("\nClosest available names:")
        for m in sorted(models):
            if any(part in m for part in ("gemma-4", "flash-lite")):
                print(f"  {m}")
        print("Set the right names in .env (RELATIONS_*_MODEL) and run again.")
        return 1

    config.LOG_DIR.mkdir(exist_ok=True)
    path = config.LOG_DIR / f"setup_{time.strftime('%Y%m%d-%H%M%S')}.jsonl"
    ok = True
    with open(path, "w", encoding="utf-8") as f:
        for model in wanted:
            try:
                text, meta = llm.generate(model, 'Reply with exactly this JSON and nothing else: {"ok": true}')
                status = "ok"
            except llm.LLMError as e:
                text, meta, status, ok = str(e), {"model": model}, "failed", False
            f.write(json.dumps({"status": status, "reply": text, **meta}) + "\n")
            print(f"  {model:<28} {status}: {text.strip()[:60]}")
    print(f"\nSaved to {path.relative_to(config.ROOT)}")
    print("GATE PASSED" if ok else "GATE FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
