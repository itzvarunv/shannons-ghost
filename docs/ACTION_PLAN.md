# Relations — Action Plan

Nov 17, 2026 · companion to BUILD_PLAN.md

How we go from plan to a first 100-pair run. No code is written until you approve the step it belongs to. Each step ends at a gate: a check that has to pass before the next step starts.

## Run rules (decided Nov 17)

- **Where it runs:** the existing Oracle Always Free VM (1 GB RAM) that runs EV, not Azure. Relations is its own systemd service with a memory cap (about 300 MB), so if it overruns only Relations is killed and EV keeps running.
- **Gemini key:** a new Google project with its own key, so Relations never eats EV's daily free-tier limit.
- **Batches of 10:** the job works in batches of 10 actions. After each batch, every result, failures included, is saved as a JSONL file on the server, and EV sends a short WhatsApp summary. The file comes to Relations/logs/ and we analyse it before the next batch.
- **Test first, then the main model:** every stage runs on test data before it touches real data.
- **Code stays on this computer:** nothing goes to GitHub for now.
- **Problems:** when something blocks, stop and decide together from a list of options and what each one affects.

## Step 0 — Decide and check (no code)

- [x] LLM API: Gemini free tier.
- [x] Where the code lives: this folder, on this computer. No GitHub yet.
- [x] Where it runs: the Oracle VM, as a capped separate service (see Run rules).
- [x] New Google project "Relations" in AI Studio. Limits are per model, each with its own counter.
- [x] Models (option A): Gemma 4 31B extracts (30 req/min, 16K tokens/min, 14,400 req/day); Gemini 3.5 Flash Lite judges (15 req/min, 250K tokens/min, 500 req/day). Gemini 3.1 Flash Lite is the backup judge (same limits, separate counter).
- [x] Oracle VM memory checked (Nov 17, EV running): 954 MB total, 510 MB available, 2,047 MB swap (89 MB used). The 300 MB cap fits with about 210 MB spare. Server reached by ssh with the ev_oracle key; the Oracle console password is still lost but not needed for this project.
- [x] 8 hidden pairs: keep the BUILD_PLAN table as is.
- [x] Time: Steps 1–5 on Nov 17. From Step 3, Claude writes the code and explains it; Varun reviews and approves each file before it is saved.

**Gate:** every box above ticked.

## Step 1 — Learn just enough (no project code)

**Status (Nov 18):** skipped at Varun's request; building continues and questions get answered as they come up.

The checker needs two things you haven't used yet:

- **sympy basics:** symbols, equations, `subs`, `simplify`.
- **What an ODE (ordinary differential equation) is:** at the level of "which derivatives appear and in what order". No solving needed.

**Gate:** you can explain why m·ẍ + c·ẋ + k·x = F and L·q̈ + R·q̇ + q/C = V have the same form.

## Step 2 — Project skeleton

**Status (Nov 18):** passed. Key works; Gemma 4 31B, Gemini 3.5 Flash Lite and 3.1 Flash Lite all answer (`check_setup.py`).

Proposed folder layout inside Relations/:

| Folder | Holds |
| --- | --- |
| docs/ | BUILD_PLAN.md, ACTION_PLAN.md, run notes |
| assets/ | flowchart and screenshots for the README |
| checker/ | the sympy form check and mapping check |
| benchmark/ | the 16 disguised pairs + hidden answers, stored separately |
| smoke_test/ | the invented-maths text file |
| feeder/ | the arXiv / Wikipedia fetcher and formality score |
| logs/ | JSONL logs of every attempt, dropped ones included |
| archive/ | earlier versions and dead ends, kept on purpose |

**Gate:** a script runs, sends one prompt to Gemini and saves the reply to logs/.

## Step 3 — Checker, no AI

**Status (Nov 18):** passed. 8/8 known pairs accepted, 0/8 decoys; wrong mappings are rejected too (`tests/gate_step3.py`).

Build the form check and mapping check. Test them on the 8 known pairs in their normal names, plus the 8 decoys.

**Gate:** 8/8 known pairs pass, 0/8 decoys pass.

## Step 4 — Disguised benchmark

**Status (Nov 18):** passed. 25 topics renamed into invented words; all 16 disguised pairs get the same verdict as the plain ones (`tests/gate_step4.py`).

Write the 16 pairs in fictional vocabulary, with the answers kept in a separate file.

**Gate:** the checker gives the same results on the disguised versions as on the originals.

## Step 5 — Extractor + judge on the benchmark

**Status (Nov 18):** passed. Run `logs/20261118-130024_benchmark`, 7 batches:
- Extraction: 25/25 topics match the reference equations (Gemma 4 31B, 37–84 s per batch).
- Form check: 8 hidden pairs passed, 7 of 8 decoys dropped with no AI call; the OR-vs-XOR decoy passed (same shape), as designed.
- Judge (Gemini 3.5 Flash Lite, one call, 59 s): all 8 hidden pairs related with score 10 and mappings the checker verified; the OR-vs-XOR decoy rejected.
- Score: 8/8 hidden found, 0/8 decoys accepted (recall 1.0, precision 1.0).

Changes made while building (Nov 18):
- The judge proposes the mapping and the score in one call (the build plan had a separate theory builder); halves the calls.
- Gemma's thinking set to "minimal": by default it spent about 3,600 thinking tokens and 137 s on 2 topics.
- "Model busy" errors (HTTP 503) are retried twice, 20 s apart; if Gemma 4 31B is still busy, the batch falls back to Gemma 4 26B (Varun's choice). Batch 2 failed this way before the fallback existed; its report is kept.
- The runner saves progress after every batch and can resume, so each batch runs as its own command; failed topics are retried on resume.
- The parser accepts maths symbols models write (∧ ∨ · − ²).

Caveats: 16 pairs is a small benchmark, and the judge scored every true pair 10/10, so it adds little beyond the checker here. Its reason for one pair named "Ohm's law", so disguises can still leak recognisable forms.

Gemini extracts purpose, mechanism, variables and equation. The checker filters, and the judge returns batched JSON (related, score, reason under 15 words).

**Gate:** recall ≥ 6/8 and at most 1 decoy accepted.

## Fencer (built Nov 18, at Varun's request, ahead of Steps 6–7)

`fencer.py` collects topics from Wikipedia science categories in 14 fields, fences out pages that cannot be compared, anchors each topic to a partner from a different field with the same equation form, and has the judge rate each pair. Step 6 is deferred; the fencer runs on this Mac for now, not yet on the Oracle server.

**Run 1** (`logs/20261118-131605_fencer`): 550 pages checked, 200 kept, 350 fenced off (0–1 equations, list pages). Gemma extracted a usable equation from 128; the rest used integrals, sums, matrices or abstract functions, or had no single central equation. Anchor pairing gave 46 pairs (target was 100), and the judge accepted 0. Cause: the v1 form check only looked at the changing quantities, so "y = anything" matched "y = anything else". Kept in `archive/signature_v1_too_loose.py`.

**Run 2** (`logs/20261118-131605_fencer_v2_strict_form`, same 128 extractions, no new calls): a stricter form check (the whole equation shape) and a judge note that constants may absorb signs and factors. 19 pairs, 2 accepted, both valid but trivial (velocity = dr/dt ↔ group delay = −dφ/dω; one ratio ↔ another ratio).

**Finding:** Lotka–Volterra (prey) ↔ SIR (infected) is an exact match with x → I, y → S, α → −γ, β → −β/N; verified by the checker after a fix (it wrongly demanded mappings for constants the equation never uses). The judge rejected it with "both are population models, but the specific equations differ". The judge leans on the topics' fields rather than the maths, which defeats the purpose of cross-field search.

Fixes made while running: Wikipedia pacing and back-off; forgiving parser for `Dv(t, 1)`, chained `a = b = c` and undeclared names (fencer only); unparseable equations count as final drops instead of endless retries; a backup judge on "busy" errors; pair IDs matched even when the model writes "pair F011".


**Run 3** (`logs/20261118-131605_fencer_v3_score_only`, same 19 pairs, Varun's decision): the judge no longer says yes or no. It always proposes its best mapping and scores 0–10; a score of 7 or more is flagged for human review, and the checker reports whether the mapping holds. Old judge kept in `archive/judge_v1_yes_no.py`. Result: 9 of 19 flagged, 6 of those with a verified mapping. Top flags: optimal forest rotation age ↔ logistic growth (9, verified); Lotka–Volterra ↔ SIR (8; the judge's own mapping was wrong, β → 0, but the hand mapping above verifies). Several flags are simple ratios or differences: true but uninteresting.

Benchmark re-run with the new judge (`logs/20261118-130024_benchmark_v2_score_judge`): 8/8 hidden, 0/8 decoys, after telling the judge that mapping keys must be single names (it had written "g/l").

**Open ideas, not decided:** let the checker search for mappings itself when the judge flags a pair but its mapping fails (would have caught Lotka–Volterra ↔ SIR); push simple ratio and difference formulas lower in the ranking.

## Step 6 — Smoke test: invented maths, grounding only

One file with 30–50 invented definitions and theorems, 2 hidden connections and a few decoys. The model may only cite passages from this file.

**Gate:** both hidden connections found, no decoy accepted, and every claim cites a passage.

## Step 7 — Feeder + fence on the Oracle VM

**Memory cap:** start throttling Relations at 250 MB and kill it at 300 MB, so EV always keeps its share (checked Nov 17: 510 MB available with EV running).

Fetch from arXiv and Wikipedia categories only, apply the formality score, and pair only across fields with matching equation signatures. This runs on the Oracle VM as the capped Relations service, reporting every 10 actions (see Run rules).

**Gate:** the pool holds enough pages that the form check yields 100 candidate pairs, with no off-topic pages getting in (spot-check 20 by hand).

## Step 8 — The 100-pair run and review

Send the 100 pairs to Gemini as 10 batches of 10, and analyse each batch report (failures included) before the next one goes.

**Gate (your call):** what changes before any longer run, and whether a longer run is worth it at all.

## Checkpoints with you

Each step starts only after you say go. After each gate, the result goes into docs/ as a short note, including what failed.
