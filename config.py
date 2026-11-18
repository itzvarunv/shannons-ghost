"""Settings. Secrets and model names come from Relations/.env (see .env.example)."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _load_env(path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env(ROOT / ".env")

API_KEY = os.environ.get("GEMINI_API_KEY", "")
EXTRACTOR_MODEL = os.environ.get("RELATIONS_EXTRACTOR_MODEL", "gemma-4-31b-it")
FALLBACK_EXTRACTOR_MODEL = os.environ.get("RELATIONS_FALLBACK_EXTRACTOR_MODEL", "gemma-4-26b-a4b-it")  # used when 31B is busy
JUDGE_MODEL = os.environ.get("RELATIONS_JUDGE_MODEL", "gemini-3.5-flash-lite")
BACKUP_JUDGE_MODEL = os.environ.get("RELATIONS_BACKUP_JUDGE_MODEL", "gemini-3.1-flash-lite")

GEMMA_THINKING = os.environ.get("RELATIONS_GEMMA_THINKING", "minimal")  # Gemma thinks ~3,600 tokens per call otherwise

BATCH_SIZE = 10          # actions per batch; a report is written after every batch
REVIEW_SCORE = 7         # judge score (0-10) at or above which a pair is flagged for human review
MIN_GAP_SECONDS = {      # spacing between calls to stay under per-minute limits
    "gemma": 15.0,       # Gemma: 30 req/min but only 16K tokens/min
    "default": 5.0,      # Flash Lite: 15 req/min
}

LOG_DIR = ROOT / "logs"
BENCH_DIR = ROOT / "benchmark"
