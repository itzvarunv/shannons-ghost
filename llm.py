"""Minimal Gemini API client (plain HTTPS, no extra packages).

Both Gemini and Gemma models are called through the same endpoint with the key
from .env. Errors are raised as LLMError (or RateLimited for HTTP 429) so the
caller can log them as failed actions instead of crashing.
"""
import json
import re
import time
import urllib.error
import urllib.request

import config

BASE = "https://generativelanguage.googleapis.com/v1beta"
_last_call = {}


class LLMError(RuntimeError):
    pass


class RateLimited(LLMError):
    pass


def _request(method, url, body=None):
    if not config.API_KEY:
        raise LLMError("GEMINI_API_KEY is missing: add it to Relations/.env (see .env.example)")
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "x-goog-api-key": config.API_KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:600]
        if e.code == 429:
            raise RateLimited(f"HTTP 429 (rate limited): {detail}") from e
        raise LLMError(f"HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise LLMError(f"network error: {e.reason}") from e


def list_models():
    names, token = [], None
    while True:
        url = f"{BASE}/models?pageSize=1000" + (f"&pageToken={token}" if token else "")
        r = _request("GET", url)
        names += [m["name"].split("/", 1)[1] for m in r.get("models", [])]
        token = r.get("nextPageToken")
        if not token:
            return names


def _pace(model):
    gap = config.MIN_GAP_SECONDS["gemma" if model.startswith("gemma") else "default"]
    wait = _last_call.get(model, 0) + gap - time.time()
    if wait > 0:
        time.sleep(wait)
    _last_call[model] = time.time()


def generate(model, prompt, want_json=True):
    """Send one prompt. Returns (reply_text, meta)."""
    _pace(model)
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0}}
    if want_json and not model.startswith("gemma"):   # Gemma does not take the JSON switch
        body["generationConfig"]["responseMimeType"] = "application/json"
    if model.startswith("gemma") and config.GEMMA_THINKING:
        body["generationConfig"]["thinkingConfig"] = {"thinkingLevel": config.GEMMA_THINKING}
    t0 = time.time()
    for attempt in range(3):              # retry only "model busy" (HTTP 503), up to 2 times
        try:
            r = _request("POST", f"{BASE}/models/{model}:generateContent", body)
            break
        except LLMError as e:
            if "HTTP 503" not in str(e) or attempt == 2:
                raise
            time.sleep(20)
    candidates = r.get("candidates") or []
    if not candidates:
        raise LLMError(f"no reply: {json.dumps(r)[:400]}")
    parts = candidates[0].get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    meta = {"model": model, "seconds": round(time.time() - t0, 2), "retries": attempt,
            "finish": candidates[0].get("finishReason"), "usage": r.get("usageMetadata", {})}
    return text, meta


def parse_json(text):
    """Pull JSON out of a reply, tolerating ``` fences and stray prose around it."""
    t = text.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)```", t, re.S)
    if fenced:
        t = fenced.group(1).strip()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        pass
    for open_, close in (("[", "]"), ("{", "}")):
        i, j = t.find(open_), t.rfind(close)
        if i != -1 and j > i:
            try:
                return json.loads(t[i:j + 1])
            except json.JSONDecodeError:
                continue
    raise LLMError("reply is not valid JSON")
