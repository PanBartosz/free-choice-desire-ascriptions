from collections import namedtuple, deque, Counter
import random
import json
import os
try:
    import pandas as pd
    HAS_PANDAS = True
except Exception:
    pd = None
    HAS_PANDAS = False

# Exp5b generator:
# - Only want/prefer items (no modals or "does not mind").
# - Emits two JSON files: stimuli_experimental.json (main, 114 items) and stimuli_practice.json (training, 32 items).

Triplet = namedtuple("Triplet", ["Sweet", "Fruit", "Meat"])

sweets = [
    "a chocolate", "a cookie", "a biscuit", "a lollipop", "a cupcake",
    "a cake", "a muffin", "caramel", "a donut", "a brownie",
]

fruits = [
    "a strawberry", "a grapefruit", "a cranberry", "an apple", "a pear",
    "a cherry", "an orange", "a mango", "a plum", "a peach",
]

meats = [
    "a steak", "a burger", "a kebab", "a meatball", "a sausage",
    "a meatloaf", "a hotdog", "ribs", "pork", "beef",
]

names = [
    # Male
    "James", "John", "Robert", "Michael", "William",
    "David", "Richard", "Joseph", "Thomas", "Charles",
    "Christopher", "Daniel", "Matthew", "Anthony", "Mark",
    "Donald", "Steven", "Paul", "Andrew", "Joshua",
    # Female
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth",
    "Barbara", "Susan", "Jessica", "Sarah", "Karen",
    "Nancy", "Lisa", "Margaret", "Betty", "Sandra",
    "Ashley", "Dorothy", "Kimberly", "Emily", "Donna",
]

random.Random(42).shuffle(names)

qs = [Triplet(Sweet=s, Fruit=f, Meat=m) for s, f, m in zip(sweets, fruits, meats)]

# rotated list for pairing (double controls)
qsr = deque(qs)
qsr.rotate(1)
qsr = list(qsr)

# Tribe-specific preferences (strict order)
preferences = {
    "Urbanite": {"wants": "Sweet", "accepts": "Meat", "dislikes": "Fruit"},
    "Nomad": {"wants": "Fruit", "accepts": "Meat", "dislikes": "Sweet"},
}

preference_rank = {"dislikes": 0, "accepts": 1, "wants": 2}
category_labels = {"Sweet": "sweets", "Fruit": "fruit", "Meat": "meat"}


def category_label_for(region, kind):
    """Return category label (e.g., sweets/fruit/meat) for a tribe-kind pair."""
    return category_labels[preferences[region][kind]]


def seg(firstname, region, parts):
    """Build SEGMENTS array from a list of (text, duration_ms or None)."""
    out = [{"text": f"{firstname}-the-{region}", "duration": 750}]
    for t, d in parts:
        segm = {"text": t}
        if d is not None:
            segm["duration"] = d
        out.append(segm)
    return out


def make_sentence(firstname, region, text):
    return f"{firstname}-the-{region} {text}"


def pick_item(q, region, kind):
    return getattr(q, preferences[region][kind])


def preference_relation(kind_left, kind_right):
    r1 = preference_rank[kind_left]
    r2 = preference_rank[kind_right]
    if r1 > r2:
        return "gt"  # left item strictly preferred to right
    if r1 < r2:
        return "lt"  # left item strictly worse than right
    return "eq"  # equally liked


def build_feedback_strings(name, region, verb, kind_left, kind_right=None, rel=None, item_left=None, item_right=None):
    subj = f"{name}-the-{region}"
    cat1 = category_label_for(region, kind_left)
    cat2 = category_label_for(region, kind_right) if kind_right else None
    if verb == "prefer":
        if rel == "gt":
            base = f"{subj} always prefers {cat1} to {cat2}"
        elif rel == "lt":
            base = f"{subj} never prefers {cat1} to {cat2}"
        else:
            if item_left is not None and item_right is not None:
                base = f"{subj} equally likes {item_left} and {item_right}"
            elif cat1 == cat2:
                base = f"{subj} likes both options equally"
            else:
                base = f"{subj} equally likes {cat1} and {cat2}"
        return (f"Your answer is correct. {base}.", f"Your answer is incorrect. {base}.")
    # want feedback (training only)
    if kind_left == "wants":
        base = f"{subj} always wants to eat {cat1}"
    else:
        base = f"{subj} never wants to eat {cat1}"
    return (f"Your answer is correct. {base}.", f"Your answer is incorrect. {base}.")


def want_single(q, firstname, region, kind):
    item1 = pick_item(q, region, kind)
    parts = [("wants to", 500), ("eat", 250), (item1, None)]
    correct = "Y" if kind == "wants" else "N"
    fc, fi = build_feedback_strings(firstname, region, "want", kind)
    return {
        "SEGMENTS": seg(firstname, region, parts),
        "SENTENCE": make_sentence(firstname, region, f"wants to eat {item1}"),
        "VERB": "want",
        "CONDITION": "SINGLE_CONTROL",
        "STRUCTURE": "single",
        "SUBCONDITION": kind,
        "ORDER": "single",
        "CORRECT": correct,
        "LOGICAL_TRUTH": correct,
        "TRIBE": region,
        "ITEM": None,
        "ITEM1": item1,
        "ITEM1_TYPE": kind,
        "ITEM2": None,
        "ITEM2_TYPE": None,
        "RELATION": None,
        "FEEDBACK_CORRECT": fc,
        "FEEDBACK_INCORRECT": fi,
    }


def want_double(q1, q2, firstname, region, kind, order="AB"):
    item_a = pick_item(q1, region, kind)
    item_b = pick_item(q2, region, kind)
    if order == "BA":
        item_a, item_b = item_b, item_a
    parts = [("wants to", 500), ("eat", 250), (f"{item_a} or {item_b}", None)]
    correct = "Y" if kind == "wants" else "N"
    fc, fi = build_feedback_strings(firstname, region, "want", kind)
    return {
        "SEGMENTS": seg(firstname, region, parts),
        "SENTENCE": make_sentence(firstname, region, f"wants to eat {item_a} or {item_b}"),
        "VERB": "want",
        "CONDITION": "DOUBLE_CONTROL",
        "STRUCTURE": "disjunction",
        "SUBCONDITION": f"{kind}|{kind}",
        "ORDER": order,
        "CORRECT": correct,
        "LOGICAL_TRUTH": correct,
        "TRIBE": region,
        "ITEM": None,
        "ITEM1": item_a,
        "ITEM1_TYPE": kind,
        "ITEM2": item_b,
        "ITEM2_TYPE": kind,
        "RELATION": None,
        "FEEDBACK_CORRECT": fc,
        "FEEDBACK_INCORRECT": fi,
    }


def want_experimental(q, firstname, region, kinds, order="AB"):
    k_left, k_right = kinds if order == "AB" else (kinds[1], kinds[0])
    item1 = pick_item(q, region, k_left)
    item2 = pick_item(q, region, k_right)
    parts = [("wants to", 500), ("eat", 250), (f"{item1} or {item2}", None)]
    fc, fi = build_feedback_strings(firstname, region, "want", k_left)
    return {
        "SEGMENTS": seg(firstname, region, parts),
        "SENTENCE": make_sentence(firstname, region, f"wants to eat {item1} or {item2}"),
        "VERB": "want",
        "CONDITION": "EXPERIMENTAL",
        "STRUCTURE": "disjunction",
        "SUBCONDITION": f"{kinds[0]}|{kinds[1]}",
        "ORDER": order,
        "CORRECT": "Y/N",  # main block, no feedback
        "LOGICAL_TRUTH": "NA",
        "TRIBE": region,
        "ITEM": None,
        "ITEM1": item1,
        "ITEM1_TYPE": k_left,
        "ITEM2": item2,
        "ITEM2_TYPE": k_right,
        "RELATION": None,
        "FEEDBACK_CORRECT": fc,
        "FEEDBACK_INCORRECT": fi,
    }


def prefer_statement(q1, q2, firstname, region, kind_left, kind_right, order="AB", condition="PREFER_DIFFERENT"):
    item_a = pick_item(q1, region, kind_left)
    item_b = pick_item(q2, region, kind_right)
    if order == "BA":
        item_a, item_b = item_b, item_a
        kind_left, kind_right = kind_right, kind_left
    rel = preference_relation(kind_left, kind_right)
    correct = "Y" if rel == "gt" else "N"
    parts = [("prefers to", 500), ("eat", 250), (f"{item_a} rather than {item_b}", None)]
    fc, fi = build_feedback_strings(
        firstname,
        region,
        "prefer",
        kind_left,
        kind_right,
        rel,
        item_left=item_a,
        item_right=item_b,
    )
    return {
        "SEGMENTS": seg(firstname, region, parts),
        "SENTENCE": make_sentence(firstname, region, f"prefers to eat {item_a} rather than {item_b}"),
        "VERB": "prefer",
        "CONDITION": condition,
        "STRUCTURE": "preference",
        "SUBCONDITION": f"{kind_left}_vs_{kind_right}",
        "ORDER": order,
        "CORRECT": correct,
        "LOGICAL_TRUTH": correct,
        "TRIBE": region,
        "ITEM": None,
        "ITEM1": item_a,
        "ITEM1_TYPE": kind_left,
        "ITEM2": item_b,
        "ITEM2_TYPE": kind_right,
        "RELATION": rel,
        "FEEDBACK_CORRECT": fc,
        "FEEDBACK_INCORRECT": fi,
    }


def build_experimental():
    items = []
    iid = 0
    name_idx = 0
    q_idx = 0

    # 1) SINGLE CONTROL want (18): 2 tribes x 3 categories x 3 items
    for region in ("Urbanite", "Nomad"):
        for kind in ("dislikes", "accepts", "wants"):
            for _ in range(3):
                it = want_single(qs[q_idx % len(qs)], names[name_idx % len(names)], region, kind)
                it["ITEM"] = f"SC{iid}"
                items.append(it)
                iid += 1
                name_idx += 1
                q_idx += 1

    # 2) DOUBLE CONTROL want (36): 2 tribes x 3 categories x 2 order x 3 items
    for region in ("Urbanite", "Nomad"):
        for kind in ("dislikes", "accepts", "wants"):
            for order in ("AB", "BA"):
                for _ in range(3):
                    it = want_double(
                        qs[q_idx % len(qs)],
                        qsr[q_idx % len(qsr)],
                        names[name_idx % len(names)],
                        region,
                        kind=kind,
                        order=order,
                    )
                    it["ITEM"] = f"DC{iid}"
                    items.append(it)
                    iid += 1
                    name_idx += 1
                    q_idx += 1

    # 3) PREFER with different categories (24): 2 tribes x 2 comparisons x 2 order x 3 items
    diff_pairs = (("accepts", "dislikes"), ("wants", "accepts"))
    for region in ("Urbanite", "Nomad"):
        for kinds in diff_pairs:
            for order in ("AB", "BA"):
                for _ in range(3):
                    it = prefer_statement(
                        qs[q_idx % len(qs)],
                        qsr[q_idx % len(qsr)],
                        names[name_idx % len(names)],
                        region,
                        kinds[0],
                        kinds[1],
                        order=order,
                        condition="PREFER_DIFFERENT",
                    )
                    it["ITEM"] = f"PD{iid}"
                    items.append(it)
                    iid += 1
                    name_idx += 1
                    q_idx += 1

    # 4) PREFER with same categories (12): 2 tribes x 2 comparisons x 3 items
    same_pairs = (("accepts", "accepts"), ("wants", "wants"))
    for region in ("Urbanite", "Nomad"):
        for kinds in same_pairs:
            for _ in range(3):
                it = prefer_statement(
                    qs[q_idx % len(qs)],
                    qsr[q_idx % len(qsr)],
                    names[name_idx % len(names)],
                    region,
                    kinds[0],
                    kinds[1],
                    order="AB",
                    condition="PREFER_SAME",
                )
                it["ITEM"] = f"PS{iid}"
                items.append(it)
                iid += 1
                name_idx += 1
                q_idx += 1

    # 5) Experimental want OR (24): 2 tribes x 2 subconditions x 2 order x 3 items
    exp_pairs = (("wants", "dislikes"), ("wants", "accepts"))
    for region in ("Urbanite", "Nomad"):
        for kinds in exp_pairs:
            for order in ("AB", "BA"):
                for _ in range(3):
                    it = want_experimental(
                        qs[q_idx % len(qs)],
                        names[name_idx % len(names)],
                        region,
                        kinds=kinds,
                        order=order,
                    )
                    it["ITEM"] = f"EX{iid}"
                    items.append(it)
                    iid += 1
                    name_idx += 1
                    q_idx += 1

    # Do not pre-shuffle: keep logical grouping for inspection.
    return items


def build_practice():
    items = []
    iid = 0
    name_idx = 0
    q_idx = 0

    # Single controls (only wants/dislikes): 2 tribes x 2 categories x 2 items = 8
    for region in ("Urbanite", "Nomad"):
        for kind in ("wants", "dislikes"):
            for _ in range(2):
                it = want_single(qs[q_idx % len(qs)], names[name_idx % len(names)], region, kind)
                it["ITEM"] = f"PR{iid}"
                items.append(it)
                iid += 1
                name_idx += 1
                q_idx += 1

    # Double controls (wants/dislikes), keep order factor with one exemplar per order: 2 x 2 x 2 x 1 = 8
    for region in ("Urbanite", "Nomad"):
        for kind in ("wants", "dislikes"):
            for order in ("AB", "BA"):
                it = want_double(
                    qs[q_idx % len(qs)],
                    qsr[q_idx % len(qsr)],
                    names[name_idx % len(names)],
                    region,
                    kind=kind,
                    order=order,
                )
                it["ITEM"] = f"PR{iid}"
                items.append(it)
                iid += 1
                name_idx += 1
                q_idx += 1

    # Prefer different (accept vs dislike, want vs accept), one exemplar per order: 2 x 2 x 2 x 1 = 8
    diff_pairs = (("accepts", "dislikes"), ("wants", "accepts"))
    for region in ("Urbanite", "Nomad"):
        for kinds in diff_pairs:
            for order in ("AB", "BA"):
                it = prefer_statement(
                    qs[q_idx % len(qs)],
                    qsr[q_idx % len(qsr)],
                    names[name_idx % len(names)],
                    region,
                    kinds[0],
                    kinds[1],
                    order=order,
                    condition="PREFER_DIFFERENT",
                )
                it["ITEM"] = f"PR{iid}"
                items.append(it)
                iid += 1
                name_idx += 1
                q_idx += 1

    # Prefer same (accept vs accept, want vs want), two exemplars per comparison: 2 x 2 x 2 = 8
    same_pairs = (("accepts", "accepts"), ("wants", "wants"))
    for region in ("Urbanite", "Nomad"):
        for kinds in same_pairs:
            for _ in range(2):
                it = prefer_statement(
                    qs[q_idx % len(qs)],
                    qsr[q_idx % len(qsr)],
                    names[name_idx % len(names)],
                    region,
                    kinds[0],
                    kinds[1],
                    order="AB",
                    condition="PREFER_SAME",
                )
                it["ITEM"] = f"PR{iid}"
                items.append(it)
                iid += 1
                name_idx += 1
                q_idx += 1

    # Ordered for easy inspection.
    return items


def write_json(items, fname):
    with open(fname, "w") as f:
        json.dump(items, f, indent=4)


def write_js_var_json(items, fname, varname):
    with open(fname, "w") as f:
        f.write(f"var {varname} = ")
        json.dump(items, f, indent=4)


def write_xlsx(items, fname):
    if HAS_PANDAS:
        df = pd.DataFrame(items)
        df.to_excel(fname, index=False)
        return True
    return False


def write_csv(items, fname):
    # Minimal CSV fallback for manual review if pandas is unavailable
    import csv
    keys = set()
    for it in items:
        keys.update(it.keys())
    keys = sorted(keys)
    with open(fname, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for it in items:
            w.writerow(it)


def validate_and_report(items, expected_counts, label):
    """Print condition counts and assert they match the spec."""
    counts = Counter([it["CONDITION"] for it in items])
    total_expected = sum(expected_counts.values())
    total_actual = len(items)
    print(f"[{label}] total: {total_actual} (expected {total_expected})")
    for cond, expected in expected_counts.items():
        actual = counts.get(cond, 0)
        print(f"  {cond}: {actual} (expected {expected})")
        if actual != expected:
            raise ValueError(f"{label} condition count mismatch for {cond}: {actual} vs {expected}")
    if total_actual != total_expected:
        raise ValueError(f"{label} total mismatch: {total_actual} vs {total_expected}")


def main():
    exp = build_experimental()
    prac = build_practice()
    # Validation and quick report for debugging/refinement
    validate_and_report(
        exp,
        {
            "SINGLE_CONTROL": 18,
            "DOUBLE_CONTROL": 36,
            "PREFER_DIFFERENT": 24,
            "PREFER_SAME": 12,
            "EXPERIMENTAL": 24,
        },
        label="Experimental",
    )
    validate_and_report(
        prac,
        {
            "SINGLE_CONTROL": 8,
            "DOUBLE_CONTROL": 8,
            "PREFER_DIFFERENT": 8,
            "PREFER_SAME": 8,
        },
        label="Practice",
    )
    basedir = os.path.dirname(__file__)
    # Excel (or CSV fallback) for manual review
    if not write_xlsx(exp, os.path.join(basedir, "stimuli_experimental.xlsx")):
        write_csv(exp, os.path.join(basedir, "stimuli_experimental.csv"))
    if not write_xlsx(prac, os.path.join(basedir, "stimuli_practice.xlsx")):
        write_csv(prac, os.path.join(basedir, "stimuli_practice.csv"))

    # Also copy into experiment/ for direct loading
    outdir = os.path.join(basedir, "experiment")
    os.makedirs(outdir, exist_ok=True)
    write_js_var_json(exp, os.path.join(outdir, "stimuli_experimental.json"), "stimuli_experimental")
    write_js_var_json(prac, os.path.join(outdir, "stimuli_practice.json"), "stimuli_practice")
    if not write_xlsx(exp, os.path.join(outdir, "stimuli_experimental.xlsx")):
        write_csv(exp, os.path.join(outdir, "stimuli_experimental.csv"))
    if not write_xlsx(prac, os.path.join(outdir, "stimuli_practice.xlsx")):
        write_csv(prac, os.path.join(outdir, "stimuli_practice.csv"))


if __name__ == "__main__":
    main()
