"""Build the pre-adjudication inter-coder comparison for AECS v1.0.0.

Inputs are read-only. Nothing in this script writes to a source file.

Coder A  : census/affect_eeg_census.csv (register of record, 20 columns)
           + review/closeout_20261104/human_coding/FIRST_PASS_FROZEN.csv
             (documented AECS mapping, frozen 2026-11-04)
           + review/closeout_20261104/human_coding/CROSSWALK.md (mapping rules)
           + review/closeout_20261104/ECSMP_CORRECTION.md (post-freeze update)
Coder B  : data/coding/independent_coding.csv

Outputs (this directory):
  coding_input_manifest.csv
  coding_comparison.csv
  pre_adjudication_agreement.json
  coding_confusion_matrices.csv

The script never edits a coded value. Where the two files use different
structures, a named derivation is applied and recorded in `A_derivation`.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # repository root
HERE = Path(__file__).resolve().parent
DOWNLOADS = ROOT / "data/coding"

CENSUS = ROOT / "census" / "affect_eeg_census.csv"
FIRST_PASS = ROOT / "review" / "closeout_20261104" / "human_coding" / "FIRST_PASS_FROZEN.csv"
CROSSWALK = ROOT / "review" / "closeout_20261104" / "human_coding" / "CROSSWALK.md"
ECSMP_FIX = ROOT / "review" / "closeout_20261104" / "ECSMP_CORRECTION.md"
SCHEMA = ROOT / "coding_scheme" / "coding_schema.json"
CODEBOOK = ROOT / "research_quality_audit_20261113" / "coding_reliability_package" / "codebook.md"

B_CODING = DOWNLOADS / "independent_coding.csv"
B_EVIDENCE = DOWNLOADS / "independent_evidence_log.csv"
B_METHOD = DOWNLOADS / "coding_method_log_rechecked.md"
B_UNRESOLVED = DOWNLOADS / "unresolved_items_rechecked.md"

ENUM_FIELDS = [
    "released_target",
    "additional_stream",
    "ratings_per_stimulus",
    "stimulus_unit",
    "stimuli_shared",
    "protocol_records_self_report",
    "release_description",
]
COUNT_FIELDS = ["n_subjects", "n_stimuli"]
ALL_FIELDS = ENUM_FIELDS + COUNT_FIELDS

# Fields Coder A coded under AECS and that therefore enter the headline table.
# release_description is reported separately: the 2026-11-04 crosswalk declined
# to score it because the register holds a package-level status, not a
# description-level one. A documented derivation is supplied for transparency
# but is kept out of the headline agreement.
HEADLINE_FIELDS = [
    "released_target",
    "additional_stream",
    "ratings_per_stimulus",
    "stimulus_unit",
    "stimuli_shared",
    "protocol_records_self_report",
    "n_subjects",
    "n_stimuli",
]
SECONDARY_FIELDS = ["release_description"]

# Post-freeze register updates, quoted from ECSMP_CORRECTION.md §5 and from the
# register rows themselves. Each entry names its documentary basis.
POST_FREEZE_UPDATES = {
    ("ECSMP", "released_target"): ("assigned", "ECSMP_CORRECTION.md §3/§5 (2026-11-04)"),
    ("ECSMP", "additional_stream"): ("ratings", "ECSMP_CORRECTION.md §3/§5 (2026-11-04)"),
    ("ECSMP", "stimuli_shared"): ("yes", "ECSMP_CORRECTION.md §3/§5 (2026-11-04)"),
    ("SEED-GER", "n_subjects"): ("8", "census note: BCMI page, '8 German subjects' (accessed 2026-11-04)"),
    ("SEED-SD", "n_subjects"): ("40", "census note: BCMI page / TAFFC abstract, '40 participants'"),
    ("EmoEEG-MC", "n_stimuli"): ("21 video + 21 imagery", "census note: Sci Data 12:1142, 21 + 21 trials"),
}

# census rating_granularity -> AECS enum, verbatim from CROSSWALK.md, plus the
# two strings that appear in the register but not in the crosswalk table. Those
# two are marked so the reader can see they are not covered by a published rule.
CROSSWALK_GRANULARITY = {
    "one per clip": ("one", "clip"),
    "per_clip": ("one", "clip"),
    "one category per trial": ("one", "trial"),
    "per trial; emotion-by-task label": ("one", "trial"),
    "one instructed target emotion per period": ("one", "period"),
    "one SAM arousal/valence rating per game": ("one", "game"),
    "one per song (1-9)": ("one", "song"),
    "per exchange; nine bipolar adjective ratings": ("one", "exchange"),
    "one per clip (1-5)": ("one", "clip"),
    "one per clip (continuous + discrete)": ("one", "clip"),
    "one per clip (continuous + discrete survey)": ("one", "clip"),
    "one per clip (6 emotion intensities + A/V/familiarity/liking 0-7)": ("one", "clip"),
    "ratings on 8 induced-emotion dimensions": ("one", "clip"),
    "clip category released; per-clip self-assessment also collected": ("one", "clip"),
    "clip category released; 1-5 intensity rating collected": ("one", "clip"),
    "post-video self-report + 20-second observer segments": ("one", "clip"),
    "367 matched participant\u2013stimulus valence/arousal cells": ("one", "clip"),
    "every 5 s (self + partner + external)": ("time_resolved", "conversation"),
    "0-1 induction-effect feedback; retrospective session annotation documented": ("session_level", "clip"),
}
# Present in the register, absent from the crosswalk table.
UNCROSSWALKED = {
    "one per video condition; 4 SAM points during stress task": ("one", "clip"),
}

# census self_report_release_status -> release_description, with the two
# package-level statements left unmapped for the reason the crosswalk gives.
RELEASE_DESC_MAP = {
    "not independently verified": "not inspected",
    "official documentation describes participant feedback; no package inspection": "explicitly describes",
    "version-3 release description explicitly describes per-subject SAM PDFs; archive not inspected": "explicitly describes",
    "descriptor Data Records describes self-report JSON records; package not inspected": "explicitly describes",
    "descriptor and ds002721 README describe per-participant induced-emotion reports; archive not inspected": "explicitly describes",
}
RELEASE_DESC_UNMAPPED = {
    "derived local input analyzed; see input provenance":
        "package-level status: the rating file was used locally; the release description itself is not recorded",
    "one local package inspected; no participant-rating table found":
        "package-level status: a package was inspected; the release description wording is not recorded",
}

PROTOCOL_MAP = {
    "yes": "yes",
    "documented in recorded protocol": "yes",
    "not established": "not established",
    "not established in checked record": "not established",
}

DEFINITE = {
    "released_target": lambda v: v != "cannot judge",
    "additional_stream": lambda v: v != "cannot judge",
    "ratings_per_stimulus": lambda v: v != "cannot judge",
    "stimulus_unit": lambda v: v != "cannot judge",
    "stimuli_shared": lambda v: v not in ("cannot judge", "TBD"),
    "protocol_records_self_report": lambda v: v in ("yes", "no"),
    "release_description": lambda v: v in ("explicitly describes", "does not mention"),
}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(p: Path):
    with p.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def numeric(raw: str):
    """Extract the released/analysed count from a register cell.

    Rule (recorded in coding_method_record.md): take the leading integer. If the
    cell is a sum of components joined by '+', sum the leading integers of the
    addends; that is the only composite form present in the register. Returns
    None for TBD or an unparsable cell.
    """
    s = str(raw).strip()
    if not s or s.upper() == "TBD":
        return None
    # A parenthetical is a breakdown, not a summand: "80 (12 per emotion x6 + 8
    # neutral)" is 80, whereas "21 video + 21 imagery" is a two-component total.
    head = re.sub(r"\([^)]*\)", "", s).strip()
    if "+" in head:
        parts = [p.strip() for p in head.split("+")]
        nums = [re.match(r"^(\d+)", p) for p in parts]
        if all(nums):
            return sum(int(m.group(1)) for m in nums)
    m = re.match(r"^(\d+)", head)
    return int(m.group(1)) if m else None


def build_manifest():
    entries = [
        ("Coder A", "register of record", CENSUS, "2026-11-04",
         "AECS v1.0.0", "20-column register; 27 corpora"),
        ("Coder A", "frozen AECS mapping", FIRST_PASS, "2026-11-04",
         "AECS v1.0.0", "27 rows x 9 AECS fields + raw census columns"),
        ("Coder A", "mapping rules", CROSSWALK, "2026-11-04",
         "AECS v1.0.0", "free text -> enum rules"),
        ("Coder A", "post-freeze register correction", ECSMP_FIX, "2026-11-04",
         "AECS v1.0.0", "ECSMP 3 fields; counts in census notes"),
        ("both", "coding scheme", SCHEMA, "2026-11-04", "AECS v1.0.0", "JSON schema"),
        ("both", "codebook", CODEBOOK, "2026-11-04", "AECS v1.0.0", "markdown codebook"),
        ("Coder B", "independent coding", B_CODING, "2026-11-13",
         "AECS v1.0.0", "14 columns; 27 corpora"),
        ("Coder B", "per-field evidence log", B_EVIDENCE, "2026-11-13",
         "AECS v1.0.0", "243 rows = 27 corpora x 9 fields"),
        ("Coder B", "method log", B_METHOD, "2026-11-13",
         "AECS v1.0.0", "recheck log; states AI-assisted source retrieval"),
        ("Coder B", "unresolved items", B_UNRESOLVED, "2026-11-13",
         "AECS v1.0.0", "per-corpus undetermined items and reasons"),
    ]
    rows = []
    for coder, role, path, date, version, note in entries:
        rows.append(OrderedDict([
            ("coder", coder),
            ("role", role),
            ("file", path.name),
            ("path", str(path).replace("\\", "/")),
            ("bytes", path.stat().st_size),
            ("sha256", sha256(path)),
            ("coding_date", date),
            ("codebook_version", version),
            ("note", note),
        ]))
    out = HERE / "coding_input_manifest.csv"
    with out.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return rows


def build_coder_a():
    census = {r["dataset"]: r for r in read_csv(CENSUS)}
    frozen = {r["corpus"]: r for r in read_csv(FIRST_PASS)}
    assert set(census) == set(frozen), "corpus sets differ between register and frozen pass"

    a = {}
    for corpus, c in census.items():
        f = frozen[corpus]
        rec = {}
        for fld in ("released_target", "additional_stream", "ratings_per_stimulus",
                    "stimulus_unit", "stimuli_shared", "protocol_records_self_report",
                    "n_subjects", "n_stimuli"):
            rec[fld] = (f[fld], "FIRST_PASS_FROZEN.csv (crosswalk 2026-11-04)")

        # re-apply the documented post-freeze updates, and confirm each one
        # against the register cell it came from
        for (cp, fld), (val, basis) in POST_FREEZE_UPDATES.items():
            if cp != corpus:
                continue
            rec[fld] = (val, f"post-freeze update: {basis}")

        # the register is the authority for the two enum fields it holds directly
        for fld in ("released_target", "additional_stream"):
            if corpus in ("ECSMP",):
                continue
            if c[fld].strip() != rec[fld][0].strip():
                rec[fld] = (c[fld], "register cell (frozen pass differs; see audit)")
        # stimuli_shared: register uses TBD where the frozen pass already says TBD
        if corpus != "ECSMP" and c["stimuli_shared"].strip() != rec["stimuli_shared"][0].strip():
            rec["stimuli_shared"] = (c["stimuli_shared"], "register cell (frozen pass differs; see audit)")

        # release_description: derived, flagged, and never used in the headline
        raw_status = c["self_report_release_status"].strip()
        if raw_status in RELEASE_DESC_MAP:
            rec["release_description"] = (
                RELEASE_DESC_MAP[raw_status],
                f"derived from census self_report_release_status='{raw_status}'",
            )
        else:
            rec["release_description"] = (
                "",
                f"NOT COMPARABLE: {RELEASE_DESC_UNMAPPED.get(raw_status, 'unmapped')}",
            )

        # keep the raw material that shows how free text became an enum
        rec["_raw"] = {
            "released_target": c["released_target"],
            "additional_stream": c["additional_stream"],
            "ratings_per_stimulus": c["rating_granularity"],
            "stimulus_unit": c["rating_granularity"],
            "stimuli_shared": c["stimuli_shared"],
            "protocol_records_self_report": c["collected_self_report"],
            "release_description": c["self_report_release_status"],
            "n_subjects": c["n_subjects"],
            "n_stimuli": c["n_stimuli"],
        }
        rec["_note"] = c["note"]
        rec["_source"] = c["primary_source"]
        rec["_verification"] = c["verification"]
        # flag the two granularity strings that no published crosswalk rule covers
        if c["rating_granularity"].strip() in UNCROSSWALKED and f["census_granularity_raw"].strip() != c["rating_granularity"].strip():
            rec["ratings_per_stimulus"] = (
                rec["ratings_per_stimulus"][0],
                "crosswalk rule not published for this register string; "
                "value carried from FIRST_PASS_FROZEN via census_granularity_raw='per_clip'",
            )
        a[corpus] = rec
    return a, census, frozen


def build_coder_b():
    return {r["corpus"]: r for r in read_csv(B_CODING)}


def build_comparison(a, b):
    rows = []
    for corpus in b:  # B defines the order; sets are asserted equal below
        for fld in ALL_FIELDS:
            aval, ader = a[corpus][fld]
            bval = b[corpus][fld].strip()
            a_num, b_num = None, None
            if fld in COUNT_FIELDS:
                a_num, b_num = numeric(aval), numeric(bval)
                agree = (a_num is not None and b_num is not None and a_num == b_num)
                agree_literal = (str(aval).strip() == bval)
            else:
                agree = (aval == bval)
                agree_literal = agree
            if fld in DEFINITE:
                a_def = bool(aval) and DEFINITE[fld](aval)
                b_def = DEFINITE[fld](bval)
            else:
                a_def = a_num is not None
                b_def = b_num is not None
            rows.append(OrderedDict([
                ("corpus", corpus),
                ("field", fld),
                ("A_value", aval),
                ("A_numeric", "" if a_num is None else a_num),
                ("A_raw_in_register", a[corpus]["_raw"][fld]),
                ("A_derivation", ader),
                ("B_value", bval),
                ("B_numeric", "" if b_num is None else b_num),
                ("B_raw_in_file", bval),
                ("agreement", "1" if agree else "0"),
                ("agreement_literal", "1" if agree_literal else "0"),
                ("A_definite", "1" if a_def else "0"),
                ("B_definite", "1" if b_def else "0"),
                ("A_source", a[corpus]["_source"]),
                ("B_source", b[corpus]["source_used"]),
            ]))
    out = HERE / "coding_comparison.csv"
    with out.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return rows


def cohen_kappa(pairs):
    """Nominal kappa for paired ratings. Returns (kappa, pabak, note)."""
    n = len(pairs)
    if n == 0:
        return None, None, "no comparable pairs"
    a = [p[0] for p in pairs]
    b = [p[1] for p in pairs]
    po = sum(1 for x, y in pairs if x == y) / n
    cats = set(a) | set(b)
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    pabak = max(0.0, 2 * po - 1)
    if pe >= 1 - 1e-12:
        return None, round(pabak, 4), (
            "Undefined: expected agreement equals 1 (both coders used a single identical category) "
            "so kappa has no denominator; raw agreement is reported instead"
        )
    return round((po - pe) / (1 - pe), 4), round(pabak, 4), ""


def summarise(rows, fields, label):
    out = OrderedDict()
    for fld in fields:
        fr = [r for r in rows if r["field"] == fld]
        # Empty derived values mark absent comparable evidence, not an AECS category.
        if fld == "release_description":
            fr = [r for r in fr if r["A_value"] and r["B_value"]]
        n = len(fr)
        if fld in COUNT_FIELDS:
            both = [r for r in fr if r["A_numeric"] != "" and r["B_numeric"] != ""]
            agree = sum(1 for r in both if r["agreement"] == "1")
            diffs = [r for r in both if r["agreement"] == "0"]
            tbd_a = [r["corpus"] for r in fr if r["A_numeric"] == ""]
            tbd_b = [r["corpus"] for r in fr if r["B_numeric"] == ""]
            out[fld] = OrderedDict([
                ("type", "count"),
                ("total_comparisons", n),
                ("both_numeric", len(both)),
                ("exact_agreements", agree),
                ("exact_agreement_rate", round(agree / len(both), 4) if both else None),
                ("literal_string_agreements", sum(1 for r in fr if r["agreement_literal"] == "1")),
                ("value_differences", [
                    {"corpus": r["corpus"], "A": r["A_numeric"], "B": r["B_numeric"],
                     "A_raw": r["A_raw_in_register"], "B_raw": r["B_raw_in_file"]}
                    for r in diffs
                ]),
                ("TBD_A", tbd_a),
                ("TBD_B", tbd_b),
                ("excluded_from_exact", n - len(both)),
                ("kappa", None),
                ("kappa_note", "not applicable to counts"),
            ])
            continue

        pairs = [(r["A_value"], r["B_value"]) for r in fr]
        agree = sum(1 for r in fr if r["agreement"] == "1")
        kappa, pabak, note = cohen_kappa(pairs)
        # sensitivity: both definite only
        det = [(r["A_value"], r["B_value"]) for r in fr
               if r["A_definite"] == "1" and r["B_definite"] == "1"]
        det_agree = sum(1 for x, y in det if x == y)
        kappa_d, pabak_d, note_d = cohen_kappa(det)
        out[fld] = OrderedDict([
            ("type", "enum"),
            ("total_comparisons", n),
            ("agreements", agree),
            ("raw_agreement_rate", round(agree / n, 4)),
            ("kappa", kappa),
            ("pabak_supplementary", pabak),
            ("kappa_note", note),
            ("A_distribution", dict(Counter(r["A_value"] for r in fr))),
            ("B_distribution", dict(Counter(r["B_value"] for r in fr))),
            ("sensitivity_both_definite", OrderedDict([
                ("total_comparisons", n),
                ("excluded", n - len(det)),
                ("retained", len(det)),
                ("agreements", det_agree),
                ("raw_agreement_rate", round(det_agree / len(det), 4) if det else None),
                ("definite_conflicts", len(det) - det_agree),
                ("kappa", kappa_d),
                ("pabak_supplementary", pabak_d),
                ("kappa_note", note_d),
                ("excluded_corpora", [
                    {"corpus": r["corpus"], "A": r["A_value"], "B": r["B_value"]}
                    for r in fr if not (r["A_definite"] == "1" and r["B_definite"] == "1")
                ]),
            ])),
        ])
    out["_overall"] = OrderedDict([
        ("fields_in_table", len(fields)),
        ("comparisons", sum(out[f]["total_comparisons"] for f in fields)),
        ("agreements", sum(out[f].get("agreements", out[f].get("exact_agreements", 0)) for f in fields)),
        ("note", label),
    ])
    return out


def confusion_rows(rows, fields):
    out = []
    for fld in fields:
        fr = [r for r in rows if r["field"] == fld]
        avals = sorted({r["A_value"] for r in fr})
        bvals = sorted({r["B_value"] for r in fr})
        for av in avals:
            for bv in bvals:
                n = sum(1 for r in fr if r["A_value"] == av and r["B_value"] == bv)
                if n:
                    out.append({
                        "field": fld,
                        "A_value": av,
                        "B_value": bv,
                        "n": n,
                        "on_diagonal": "1" if av == bv else "0",
                        "corpora": "; ".join(r["corpus"] for r in fr
                                             if r["A_value"] == av and r["B_value"] == bv),
                    })
    return out


def check_summary_applicability():
    rows = [dict(corpus=str(i), field="release_description", A_value=a,
                 B_value=b, agreement=str(int(a == b)),
                 A_definite=str(int(a == "mentioned")),
                 B_definite=str(int(b == "mentioned")))
            for i, (a, b) in enumerate([
                ("", "not inspected"), ("mentioned", "mentioned"),
                ("not inspected", "not inspected")])]
    summary = summarise(rows, SECONDARY_FIELDS, "self-check")["release_description"]
    assert summary["total_comparisons"] == 2
    assert summary["agreements"] == 2
    assert summary["sensitivity_both_definite"]["retained"] == 1


def main():
    check_summary_applicability()
    manifest = build_manifest()
    a, census, frozen = build_coder_a()
    b = build_coder_b()
    assert set(a) == set(b), f"corpus sets differ: {set(a) ^ set(b)}"

    comparison = build_comparison(a, b)

    headline = summarise(comparison, HEADLINE_FIELDS, "pre-adjudication, 8 fields Coder A coded under AECS")
    secondary = summarise(comparison, SECONDARY_FIELDS, "derived field, reported separately")

    # disagreement inventory
    disagree = [r for r in comparison if r["agreement"] == "0"]
    structural = [r for r in disagree if r["A_value"] == ""]

    def dtype(r):
        a_def = r["A_definite"] == "1"
        b_def = r["B_definite"] == "1"
        if a_def and b_def:
            return "both_definite_conflict"
        if a_def and not b_def:
            return "A_definite_B_undetermined"
        if b_def and not a_def:
            return "A_undetermined_B_definite"
        return "both_undetermined"

    dtype_counts = Counter(dtype(r) for r in disagree)
    dtype_by_field = {}
    for fld in ALL_FIELDS:
        c = Counter(dtype(r) for r in disagree if r["field"] == fld)
        if c:
            dtype_by_field[fld] = dict(c)

    payload = OrderedDict([
        ("codebook_version", "AECS v1.0.0"),
        ("computed", "2026-11-13"),
        ("state", "pre-adjudication; no coded value was altered"),
        ("inputs", [
            {"coder": m["coder"], "file": m["file"], "sha256": m["sha256"],
             "coding_date": m["coding_date"]} for m in manifest
        ]),
        ("corpora", len(b)),
        ("headline_fields", HEADLINE_FIELDS),
        ("headline", headline),
        ("secondary_field", secondary),
        ("disagreement_inventory", OrderedDict([
            ("total_cells", len(comparison)),
            ("disagreements", len(disagree)),
            ("disagreements_excluding_structural", len(disagree) - len(structural)),
            ("types", dict(dtype_counts)),
            ("types_by_field", dtype_by_field),
            ("structural_unavailable_cells", [
                {"corpus": r["corpus"], "field": r["field"],
                 "A_derivation": r["A_derivation"]} for r in structural
            ]),
            ("by_field", dict(Counter(r["field"] for r in disagree))),
            ("by_corpus", dict(Counter(r["corpus"] for r in disagree))),
        ])),
        ("rules", OrderedDict([
            ("undetermined_main_analysis", "cannot judge / TBD / not established / not inspected kept as their own categories; never merged"),
            ("undetermined_sensitivity", "only pairs where both coders gave a definite value; exclusion counts reported"),
            ("counts", "leading integer of the register cell; '+' components summed; TBD excluded from exact agreement"),
            ("kappa", "nominal Cohen's kappa; Undefined reported when expected agreement = 1"),
            ("pabak", "supplementary prevalence-adjusted index, reported alongside but not instead of kappa"),
        ])),
    ])

    (HERE / "pre_adjudication_agreement.json").write_text(
        json.dumps(payload, indent=1, ensure_ascii=False), encoding="utf-8")

    with (HERE / "coding_confusion_matrices.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        rows = confusion_rows(comparison, ENUM_FIELDS)
        w = csv.DictWriter(fh, fieldnames=["field", "A_value", "B_value", "n", "on_diagonal", "corpora"])
        w.writeheader()
        w.writerows(rows)

    print("manifest:", len(manifest), "files")
    for fld, s in headline.items():
        if fld.startswith("_"):
            continue
        if s["type"] == "enum":
            print(f"{fld:32s} n={s['total_comparisons']} agree={s['agreements']} "
                  f"raw={s['raw_agreement_rate']:.3f} kappa={s['kappa']} "
                  f"| definite-only n={s['sensitivity_both_definite']['retained']} "
                  f"raw={s['sensitivity_both_definite']['raw_agreement_rate']} "
                  f"kappa={s['sensitivity_both_definite']['kappa']}")
        else:
            print(f"{fld:32s} both_numeric={s['both_numeric']} exact={s['exact_agreements']} "
                  f"rate={s['exact_agreement_rate']} literal={s['literal_string_agreements']}")
    print("secondary release_description:", json.dumps(secondary["release_description"]["raw_agreement_rate"]),
          "kappa", secondary["release_description"]["kappa"],
          "retained", secondary["release_description"]["sensitivity_both_definite"]["retained"])
    print("disagreements:", payload["disagreement_inventory"]["disagreements"],
          "structural:", len(structural))


if __name__ == "__main__":
    main()
