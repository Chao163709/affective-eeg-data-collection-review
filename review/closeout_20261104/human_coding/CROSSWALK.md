# Crosswalk: census free text → codebook values (frozen first pass)

The register (`census/affect_eeg_census.csv`) records some fields as free text. `FIRST_PASS_FROZEN.csv` maps them onto the codebook vocabulary with the rules below. Every mapping is one-to-one and auditable; nothing was inferred beyond the wording of the census entry. Raw entries are kept in the `census_*_raw` columns of the frozen file so any mapping can be checked against the original.

## `ratings_per_stimulus` and `stimulus_unit`

| Census `rating_granularity` | `ratings_per_stimulus` | `stimulus_unit` |
|---|---|---|
| one per clip | one | clip |
| per_clip | one | clip |
| one category per trial | one | trial |
| per trial; emotion-by-task label | one | trial |
| one instructed target emotion per period | one | period |
| one SAM arousal/valence rating per game | one | game |
| one per song (1-9) | one | song |
| per exchange; nine bipolar adjective ratings | one | exchange |
| one per clip (1-5) | one | clip |
| one per clip (continuous + discrete) | one | clip |
| one per clip (continuous + discrete survey) | one | clip |
| one per clip (6 emotion intensities + A/V/familiarity/liking 0-7) | one | clip |
| ratings on 8 induced-emotion dimensions | one | clip |
| clip category released; per-clip self-assessment also collected | one | clip |
| clip category released; 1-5 intensity rating collected | one | clip |
| post-video self-report + 20-second observer segments | one | clip |
| 367 matched participant–stimulus valence/arousal cells | one | clip |
| every 5 s (self + partner + external) | time_resolved | conversation |
| 0-1 induction-effect feedback; retrospective session annotation documented | session_level | clip |

Two rules matter for interpretation:

1. `per song`, `per trial`, `per period` and `per game` are **not** collapsed into a generic "fine granularity". They differ in what one observation covers, so the unit is kept separate from the count.
2. `every 5 s` is the only entry coded `time_resolved`, and it is coded so because the release states a fixed five-second annotation interval. A post-session summary score is `session_level`, not `time_resolved`. A single row (`0-1 induction-effect feedback; retrospective session annotation documented`) is coded `session_level` for that documented annotation, while its 0–1 feedback score is recorded as an additional stream, not as a rating count.

## `protocol_records_self_report`

| Census `collected_self_report` | Codebook |
|---|---|
| yes | yes |
| documented in recorded protocol | yes |
| not established | not established |
| not established in checked record | not established |

## Not mapped

`self_report_release_status` is retained as free text (`census_release_desc_raw`). It mixes "not independently verified", "derived local input analysed" and "release description explicitly describes…" — three different claims. The codebook's `release_description` field is therefore collected from the human coder for Table V but **not** scored against the first pass; scoring it would compare two different questions.

## Sampling

The eight corpora used in the earlier partial kit (IESD, SEED-IV, SEED-MYA, FACED, DREAMER, ECSMP, MAHNOB-HCI, MET) are a **prespecified** subset. No random-sampling record exists for them, so any agreement computed on those eight describes those eight corpora only and must not be described as a random sample of the register.
