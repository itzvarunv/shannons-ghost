"""Build the disguised benchmark from the plain one.

Every name, field and description is replaced with invented vocabulary so the
model cannot recognise a famous link; the equations keep their exact form.

Writes three files:
    topics_disguised.json   - what the AI sees: id, invented field, description text
    pairs_disguised.json    - which topics are compared (no labels)
    answers_disguised.json  - hidden: labels, true mappings, reference equations,
                              and which plain topic each disguised one came from

Re-running gives the same output (fixed random seed).
"""
import json
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 2026

FIELDS = {
    "mechanics": "tessel lore", "electrical": "vorn craft", "thermal": "glim studies",
    "chemistry": "murk studies", "mathematics": "glyph reckoning", "fluids": "brine works",
    "structures": "girder lore", "nuclear": "mote counting", "ecology": "swarm lore",
    "acoustics": "ripple craft", "astronomy": "orb lore", "coding theory": "oddness tallying",
}

# Descriptions in invented words. {name} is replaced by that name's disguised spelling.
# A ' after a quantity means one rate of change with respect to the clock reading.
TEXT = {
    "msd": "A tessel slides along a groove. Its offset from rest is {x}, which changes with the clock reading {t}. "
           "The tessel's heft is {m}, the groove's sluggishness coefficient is {c}, the tessel's rebound coefficient is {k}, "
           "and an outside shove {F} acts on it. Observation gives {m}·{x}'' + {c}·{x}' + {k}·{x} = {F}, "
           "where each ' is one rate of change with respect to {t}.",
    "rlc": "A vorn loop holds a charge-like amount {q} that varies with the clock reading {t}. The loop has an inertness {L}, "
           "a hindrance {R} and a holding capacity {C}, and a driving urge {V} is applied. "
           "The loop obeys {L}·{q}'' + {R}·{q}' + {q}/{C} = {V}, where each ' is one rate of change with respect to {t}.",
    "heat": "Along a glim bar, the glim level {u} depends on the clock reading {t} and on the position {x} along the bar. "
            "With spreading coefficient {alpha}, the bar obeys ∂{u}/∂{t} = {alpha}·∂²{u}/∂{x}².",
    "diffusion": "In a murk channel, the murk density {n} depends on the clock reading {t} and the position {x}. "
                 "With seep coefficient {Dm}, the channel obeys ∂{n}/∂{t} = {Dm}·∂²{n}/∂{x}².",
    "boolean": "In glyph reckoning every glyph is either lit or dark. The compound glyph {x} ∧ ({y} ∨ {z}) is studied, "
               "where ∧ is lit only when both sides are lit and ∨ is lit when at least one side is lit.",
    "relay": "A clatter board has three clatters {a}, {b} and {c}, each open or shut. The board lets a token through when "
             "{series}({a}, {parallel}({b}, {c})) holds. A {series} link lets the token through only when all of its inputs do; "
             "a {parallel} link lets it through when at least one input does.",
    "spring_energy": "A tessel bent by an amount {x} holds a reserve {U}. With rebound coefficient {k}, the reserve follows {U} = {k}·{x}²/2.",
    "capacitor_energy": "A vorn reservoir under an urge {V} holds a stock {W}. With holding capacity {C}, the stock follows {W} = {C}·{V}²/2.",
    "pipe": "Brine runs through a narrow sluice. The sluice rate {Qf} depends on the push difference {dP} across it and on "
            "the sluice's choke {Rh}: {Qf} = {dP}/{Rh}.",
    "ohm": "A vorn trickle {I} runs along a strand when an urge {V} is applied across it. The strand's hindrance is {R}, and {I} = {V}/{R}.",
    "truss_node": "At a girder knot, two girder pulls {F1} and {F2} together balance the knot's burden {P}: {F1} + {F2} = {P}.",
    "kcl": "At a vorn junction, two incoming trickles {I1} and {I2} together equal the outgoing trickle {Is}: {I1} + {I2} = {Is}.",
    "decay": "A heap of fading motes has count {N}, which changes with the clock reading {t}. With fade rate {lam}, "
             "the heap obeys {N}' = −{lam}·{N}, where ' is the rate of change with respect to {t}.",
    "rc": "A vorn reservoir holding a stock {Q} drains through a strand. With hindrance {R} and holding capacity {C}, "
          "{Q}' = −{Q}/({R}·{C}), where ' is the rate of change with respect to the clock reading {t}.",
    "pendulum_small": "A swing-weight hangs from a cord of length {l} in a pull-field of strength {g}. For small swings its tilt {th} "
                      "obeys {th}'' + ({g}/{l})·{th} = 0, where each ' is one rate of change with respect to the clock reading {t}.",
    "lc": "A vorn loop with inertness {L} and holding capacity {C} sloshes a charge-like amount {q} back and forth: "
          "{q}'' + {q}/({L}·{C}) = 0, where each ' is one rate of change with respect to the clock reading {t}.",
    "quad_drag": "A pellet of heft {m} sinks through brine in a pull-field of strength {g}. The brine resists in proportion to the "
                 "square of the sinking speed {v}, with resistance coefficient {c}: {m}·{v}' + {c}·{v}² = {m}·{g}, "
                 "where ' is the rate of change with respect to the clock reading {t}.",
    "logistic": "A swarm of size {P} grows with the clock reading {t}. With breeding rate {r} and crowding ceiling {K}, "
                "{P}' = {r}·{P}·(1 − {P}/{K}), where ' is the rate of change with respect to {t}.",
    "pendulum_full": "A swing-weight on a cord of length {l} in a pull-field of strength {g} swings through wide arcs. Its tilt {th} "
                     "obeys {th}'' + ({g}/{l})·sin({th}) = 0, where each ' is one rate of change with respect to the clock reading {t}.",
    "wave": "A taut ripple string has a sideways offset {w} that depends on the clock reading {t} and the position {x}. "
            "With ripple speed {cw}, it obeys ∂²{w}/∂{t}² = {cw}²·∂²{w}/∂{x}².",
    "stefan": "A glowing slab at warmth {T} sheds glow at a rate {Pw}. With shedding constant {sigma} and face size {A}, "
              "{Pw} = {sigma}·{A}·{T}⁴.",
    "grav": "Two orbs of heft {M} and {m} at separation {r} share a pull reserve {Ug}. With pull constant {G}, {Ug} = −{G}·{M}·{m}/{r}.",
    "boolean_or": "In glyph reckoning every glyph is either lit or dark. The compound glyph {x} ∨ {y} is lit when at least one of "
                  "{x} and {y} is lit.",
    "parity": "In oddness tallying, each mark {p} and {s} is either set or unset. The tally {mod2sum}({p}, {s}) is set exactly when "
              "one, and only one, of its two marks is set.",
    "freefall": "A pellet drops freely in a pull-field of strength {g}. Its height {z} obeys {z}'' = −{g}, "
                "where each ' is one rate of change with respect to the clock reading {t}.",
}

TOKEN = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")


def topic_names(t):
    names = list(t.get("independent") or []) + list(t.get("dependent") or []) + list(t.get("variables") or [])
    names += list(t.get("params") or []) + list((t.get("semantics") or {}).keys())
    return names


def make_namer(rng):
    used = set()
    consonants, vowels = "bdfghjklmnprstvwz", "aeiou"

    def new():
        while True:
            name = rng.choice(consonants) + rng.choice(vowels) + str(rng.randint(1, 9))
            if name not in used:
                used.add(name)
                return name
    return new


def rename_text(text, table):
    return TOKEN.sub(lambda m: table.get(m.group(0), m.group(0)), text)


def main():
    rng = random.Random(SEED)
    new_name = make_namer(rng)
    plain = json.loads((HERE / "topics_plain.json").read_text(encoding="utf-8"))
    pairs = json.loads((HERE / "pairs_plain.json").read_text(encoding="utf-8"))
    answers = json.loads((HERE / "answers_plain.json").read_text(encoding="utf-8"))

    order = [t["id"] for t in plain]
    rng.shuffle(order)
    new_id = {pid: f"T{i + 1:02d}" for i, pid in enumerate(order)}

    tables, visible, reference = {}, [], {}
    for t in plain:
        table = {n: new_name() for n in topic_names(t)}
        tables[t["id"]] = table
        did = new_id[t["id"]]
        visible.append({"id": did, "field": FIELDS[t["field"]], "description": TEXT[t["id"]].format(**table)})
        ref = {"id": did, "kind": t["kind"], "equation": rename_text(t["equation"], table)}
        for key in ("independent", "dependent", "variables", "params"):
            if key in t:
                ref[key] = [table[n] for n in t[key]]
        if "semantics" in t:
            ref["semantics"] = {table[k]: v for k, v in t["semantics"].items()}
        reference[did] = ref

    visible.sort(key=lambda v: v["id"])
    pair_order = list(pairs)
    rng.shuffle(pair_order)
    new_pairs, new_answers = [], {"topics": reference, "pairs": {}, "plain_ids": {v: k for k, v in new_id.items()}}
    for i, p in enumerate(pair_order):
        pid = f"Q{i + 1:02d}"
        a, b = new_id[p["a"]], new_id[p["b"]]
        new_pairs.append({"pair_id": pid, "a": a, "b": b})
        ans = answers[p["pair_id"]]
        mapping = None
        if ans.get("mapping") is not None:
            ta, tb = tables[p["a"]], tables[p["b"]]
            mapping = {ta[k]: rename_text(v, tb) for k, v in ans["mapping"].items()}
        new_answers["pairs"][pid] = {"label": ans["label"], "mapping": mapping, "plain_pair": p["pair_id"]}
    new_pairs.sort(key=lambda p: p["pair_id"])

    (HERE / "topics_disguised.json").write_text(json.dumps(visible, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (HERE / "pairs_disguised.json").write_text(json.dumps(new_pairs, indent=2) + "\n", encoding="utf-8")
    (HERE / "answers_disguised.json").write_text(json.dumps(new_answers, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(visible)} topics and {len(new_pairs)} pairs")


if __name__ == "__main__":
    main()
