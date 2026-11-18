"""Fencer: collect real topics from Wikipedia, fence out what can't be compared,
anchor each topic to a partner from a different field with the same equation form,
and have the judge rate every pair.

Stages (each saves progress; every batch of up to 10 actions writes its own report):
    1. collect  - list candidate articles from the field categories below (no AI)
    2. fence    - fetch each article; keep it only if it has enough equations and isn't
                  a list/history page (no AI)
    3. extract  - Gemma picks each kept article's governing equation (10 per call)
    4. pair     - anchor pairing: each topic looks for an unused topic from a DIFFERENT
                  field with the SAME equation form (no AI)
    5. judge    - Gemini rates each pair and proposes a mapping; the checker verifies it

    python3 fencer.py                                    # pauses after every batch
    python3 fencer.py --no-pause --max-batches 2         # stop after 2 batches
    python3 fencer.py --resume logs/<run> --no-pause     # continue a saved run

Output: pairs.md (readable) and result.json in the run folder.
"""
import argparse
import json
import random
import sys
from pathlib import Path

import config
import wiki
from batching import Run, chunks
from checker import TopicError, check_mapping, parse_topic, signature
from extractor import extract_batch
from judge import judge_batch

TARGET_TOPICS = 200        # topics that must pass the fence and extraction
TARGET_PAIRS = 100
MIN_EQUATIONS = 2          # a page needs at least this many equations (3 dropped real models like the Hassell model)
PER_CATEGORY = 60          # candidates taken from each category
SEED = 2026

# The fence's first layer: only these fields are ever fetched. Everything here is
# formal (written in equations), so Shakespeare or Napoleon can never get in.
FIELDS = {
    "mechanics": ["Classical mechanics", "Oscillation", "Rigid bodies"],
    "electrical": ["Electrical circuits", "Electronic filters", "Electromagnetism"],
    "thermal": ["Heat transfer", "Thermodynamics"],
    "fluids": ["Fluid dynamics", "Hydraulics"],
    "chemistry": ["Chemical kinetics", "Physical chemistry"],
    "population biology": ["Population dynamics", "Population ecology"],
    "epidemiology": ["Epidemiology", "Mathematical modeling of infectious disease"],
    "economics": ["Mathematical economics", "Economics models"],
    "finance": ["Mathematical finance"],
    "acoustics": ["Acoustics"],
    "optics": ["Optics"],
    "nuclear": ["Radioactivity", "Nuclear physics"],
    "control": ["Control theory"],
    "pharmacology": ["Pharmacokinetics"],
}

BAD_TITLE_STARTS = ("List of", "Lists of", "Outline of", "Timeline of", "History of", "Glossary of", "Index of")

WIKI_PROMPT = """You read short excerpts from encyclopedia articles. Each excerpt has the article's opening
text and some of its equations (in LaTeX, marked [EQUATION]).

For each topic, pick the ONE equation that best captures what the topic is about: its governing law or
defining relation. Write it in the structured format below. If no single equation is central (only unit
definitions, lists of values, or many unrelated formulas), return {{"topic_id": "<id>", "skip": true, "why": "<short reason>"}}.

Keys for a kept topic:
  "topic_id"   : the topic's id, copied exactly
  "kind"       : "ode" (rates of change in one variable), "pde" (rates of change in several variables),
                 "algebraic" (no rates of change) or "logic" (true/false statements)
  "independent": for ode/pde, the variables things change with, e.g. ["t"]; otherwise []
  "dependent"  : the changing quantities, e.g. ["x"]
  "variables"  : for logic only, the true/false inputs; otherwise []
  "params"     : the constants
  "semantics"  : for logic only, named operators mapped to And, Or, Xor or Not; otherwise {{}}
  "equation"   : the equation as text:
       - names must be plain ASCII identifiers: spell Greek letters (omega, alpha), use _ for subscripts
         (omega_0, R_h), never use the word lambda (write lam), never use e for Euler's number (write exp(1))
       - every name in the equation must appear in independent, dependent or params
       - * for multiply, / for divide, ** for powers
       - rates of change: dx/dt or x-dot is D(x, t, 1); second derivative D(x, t, 2); partial ∂u/∂x is D(u, x, 1)
       - vectors: write the magnitude only (F instead of vector F)
       - write exactly one "=": "left side = right side" (no chains like a = b = c)
       - "dependent" must never be empty: list the quantities that change or are being solved for;
         "params" are only the fixed constants
       - write D(v, t, 1), never Dv(t, 1)

Reply with only a JSON list of objects, one per topic, in the same order.

Topics:
{topics}
"""


def load_state(run):
    path = run.dir / "state.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"candidates": [], "next_candidate": 0, "kept": {}, "fenced": 0,
            "extract_done": [], "extracted": {}, "pairs": None, "judged": {}, "batch_no": 0}


def save_state(run, state):
    state["batch_no"] = run.batch_no
    (run.dir / "state.json").write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")


def collect(state, run):
    """Round-robin over fields so anchors come from every field, not one at a time.
    Each field's list is saved as soon as it is fetched, so a rate limit loses nothing."""
    rng = random.Random(SEED)
    per_field = state.setdefault("per_field", {})
    seen = {t for titles in per_field.values() for t in titles}
    for field, cats in FIELDS.items():
        if field in per_field:
            continue
        titles = []
        for cat in cats:
            for t in wiki.category_pages(cat, PER_CATEGORY):
                if t not in seen and not t.startswith(BAD_TITLE_STARTS):
                    seen.add(t)
                    titles.append(t)
        rng.shuffle(titles)
        per_field[field] = titles
        save_state(run, state)
        print(f"  {field:<20} {len(titles)} candidates")
    per_field = {f: list(t) for f, t in per_field.items()}
    order = []
    while any(per_field.values()):
        for field in FIELDS:
            if per_field[field]:
                order.append({"title": per_field[field].pop(), "field": field})
    state["candidates"] = order


def is_trivial(sig):
    """Short plain formulas (y = a*x, y = a/b) match many unrelated things: pair them last."""
    if sig[0] != "algebraic":
        return False
    shape = sig[1]
    return shape.count("v") <= 3 and "pow" not in shape.replace("pow(v,-1)", "")


def anchor_pairs(state):
    topics = state["kept"]
    sigs, records = {}, []
    for tid, topic in state["extracted"].items():
        try:
            sigs[tid] = signature(parse_topic(topic))
        except (TopicError, ValueError) as e:
            records.append({"action": "pair", "anchor": tid, "status": "failed", "error": str(e)})
    order = [tid for tid in topics if tid in sigs]            # kept order = round-robin over fields
    order = [t for t in order if not is_trivial(sigs[t])] + [t for t in order if is_trivial(sigs[t])]
    used, pairs = set(), []
    for anchor in order:
        if anchor in used or len(pairs) >= TARGET_PAIRS:
            continue
        partner = next((c for c in order if c not in used and c != anchor
                        and topics[c]["field"] != topics[anchor]["field"] and sigs[c] == sigs[anchor]), None)
        if partner is None:
            records.append({"action": "pair", "anchor": anchor, "status": "ok", "result": "no partner",
                            "signature": str(sigs[anchor])})
            continue
        used.update({anchor, partner})
        pid = f"F{len(pairs) + 1:03d}"
        pairs.append({"pair_id": pid, "a": anchor, "b": partner, "trivial": is_trivial(sigs[anchor])})
        records.append({"action": "pair", "anchor": anchor, "status": "ok", "result": "paired", "pair_id": pid,
                        "partner": partner, "signature": str(sigs[anchor]), "trivial": is_trivial(sigs[anchor])})
    return pairs, records


def write_markdown(run, state):
    topics, ex = state["kept"], state["extracted"]
    lines = ["# Fencer run", "", f"Topics kept: {len(topics)} · extracted: {len(ex)} · pairs: {len(state['pairs'] or [])}", ""]
    judged = state["judged"]
    flagged = [p for p in state["pairs"] or [] if judged.get(p["pair_id"], {}).get("review")]
    lines.append(f"Flagged for review (judge score >= {config.REVIEW_SCORE}): {len(flagged)}, "
                 f"of which the checker verified the mapping: {sum(1 for p in flagged if judged[p['pair_id']].get('mapping_ok'))}")
    lines.append("")
    ordered = sorted(state["pairs"] or [], key=lambda p: -float(judged.get(p["pair_id"], {}).get("score", -1)))
    for p in ordered:
        j = state["judged"].get(p["pair_id"], {})
        a, b = topics[p["a"]], topics[p["b"]]
        mark = ("REVIEW" if j.get("review") else "low score") + (" · mapping verified" if j.get("mapping_ok") else "")
        lines += [f"## {p['pair_id']} · {mark}{' · trivial form' if p.get('trivial') else ''}",
                  f"- **A:** [{a['title']}](https://en.wikipedia.org/wiki/{a['title'].replace(' ', '_')}) ({a['field']}): `{ex[p['a']]['equation']}`",
                  f"- **B:** [{b['title']}](https://en.wikipedia.org/wiki/{b['title'].replace(' ', '_')}) ({b['field']}): `{ex[p['b']]['equation']}`",
                  f"- judge score: {j.get('score')}/10 · {j.get('reason', '')}",
                  f"- mapping: `{json.dumps(j.get('mapping', {}))}` → {j.get('mapping_check', j.get('error', ''))}", ""]
    (run.dir / "pairs.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pause", action="store_true")
    ap.add_argument("--max-batches", type=int, default=None)
    ap.add_argument("--resume", default=None)
    args = ap.parse_args()

    run = Run("fencer", pause=not args.no_pause, existing=Path(args.resume) if args.resume else None)
    state = load_state(run)
    run.batch_no = state["batch_no"]
    left = [args.max_batches]

    def take():
        if left[0] is None:
            return True
        if left[0] <= 0:
            save_state(run, state)
            print(f"stopped at the batch limit; resume: python3 fencer.py --resume {run.dir.relative_to(config.ROOT)}")
            return False
        left[0] -= 1
        return True

    # 1. collect
    if not state["candidates"]:
        print("Collecting candidates from Wikipedia categories...")
        collect(state, run)
        save_state(run, state)

    # 2. fence: fetch 10 articles per batch until enough topics are kept
    while len(state["kept"]) < TARGET_TOPICS and state["next_candidate"] < len(state["candidates"]):
        if not take():
            return 2
        batch = state["candidates"][state["next_candidate"]:state["next_candidate"] + config.BATCH_SIZE]
        state["next_candidate"] += len(batch)
        records = []
        try:
            pages = wiki.wikitext([c["title"] for c in batch])
        except Exception as e:
            pages, err = {}, str(e)
        for c in batch:
            raw = pages.get(c["title"])
            rec = {"action": "fence", "title": c["title"], "field": c["field"]}
            if raw is None:
                rec.update(status="failed", error="page not fetched" if pages else f"fetch error: {err}")
            elif raw.lstrip().upper().startswith("#REDIRECT") or "{{disambiguation" in raw.lower():
                rec.update(status="ok", kept=False, why="redirect or disambiguation page")
            else:
                text, n_eq = wiki.excerpt(raw)
                if n_eq < MIN_EQUATIONS:
                    rec.update(status="ok", kept=False, why=f"only {n_eq} equations")
                else:
                    tid = f"W{len(state['kept']) + 1:03d}"
                    state["kept"][tid] = {"title": c["title"], "field": c["field"], "excerpt": text, "equations": n_eq}
                    rec.update(status="ok", kept=True, topic_id=tid, equations=n_eq)
            if rec.get("kept") is False:
                state["fenced"] += 1
            records.append(rec)
        run.write_batch("fence", records)
        save_state(run, state)

    # 3. extract: Gemma picks each topic's governing equation, 10 per call
    todo = [tid for tid in state["kept"] if tid not in state["extract_done"]]
    for ids in chunks(todo):
        if not take():
            return 2
        batch = [{"id": tid, "field": state["kept"][tid]["field"],
                  "description": f'{state["kept"][tid]["title"]}. {state["kept"][tid]["excerpt"]}'} for tid in ids]
        records, meta = extract_batch(batch, prompt_template=WIKI_PROMPT, lenient=True)
        for r in records:
            r["call"] = meta
            r["title"] = state["kept"][r["topic_id"]]["title"]
            # unparseable output is final (the topic is outside what the checker handles, e.g. integrals);
            # only network / busy / missing-reply failures are retried on resume
            final_failure = r["status"] == "failed" and str(r.get("error", "")).startswith("unparseable")
            if r["status"] in ("ok", "skipped") or final_failure:
                state["extract_done"].append(r["topic_id"])
            if r["status"] == "ok":
                state["extracted"][r["topic_id"]] = r["topic"]
        run.write_batch("extract", records)
        save_state(run, state)

    # 4. anchor pairing (no AI)
    if state["pairs"] is None:
        pairs, records = anchor_pairs(state)
        state["pairs"] = pairs
        for batch in chunks(records):
            run.write_batch("pair", batch)
        save_state(run, state)
        print(f"anchor pairing: {len(pairs)} pairs from {len(state['extracted'])} extracted topics")

    # 5. judge: 10 pairs per call, mapping verified by the checker
    descriptions = {tid: f'{t["title"]} ({t["field"]}): {t["excerpt"][:500]}' for tid, t in state["kept"].items()}
    todo = [p for p in state["pairs"] if p["pair_id"] not in state["judged"]]
    for batch in chunks(todo):
        if not take():
            return 2
        records, meta = judge_batch(batch, state["extracted"], descriptions)
        for r in records:
            r["call"] = meta
            if r["status"] == "ok":
                state["judged"][r["pair_id"]] = r
        run.write_batch("judge", records)
        save_state(run, state)

    write_markdown(run, state)
    accepted = sum(1 for j in state["judged"].values() if j.get("review"))
    result = {"candidates_seen": state["next_candidate"], "kept": len(state["kept"]), "fenced": state["fenced"],
              "extracted": len(state["extracted"]), "pairs": len(state["pairs"]), "judged": len(state["judged"]),
              "flagged_for_review": accepted,
              "flagged_and_verified": sum(1 for j in state["judged"].values() if j.get("review") and j.get("mapping_ok"))}
    run.save("result.json", result)
    print(json.dumps(result, indent=1))
    print(f"readable report: {(run.dir / 'pairs.md').relative_to(config.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
