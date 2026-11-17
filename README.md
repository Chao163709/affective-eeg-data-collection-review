# Affective EEG data collection review

Code and documentary coding records for **What Can an Affective EEG Corpus Support? A Review of Collection Objectives, Labels, Paradigms, and Evaluation Targets**. This is an associated research repository, not a claim of journal acceptance.

## Contents

- `scripts/`: one-way ICC(1), crossed participant/stimulus REML, held-out-participant consensus, and descriptive shuffle analyses.
- `results/`: frozen aggregate outputs and input identities. Participant-level loss records are omitted from the public consensus summary.
- `register/`: adjudicated 27-dataset register, including unresolved and provisional status.
- `coding/`, `data/coding/`, `review/`, and `research_quality_audit_20261113/`: codebook, blank template, two coding records, field evidence and pre-adjudication comparison. Both records used AI-assisted retrieval; agreement is not unaided independent human reliability.
- `MANIFEST.json`: identity of every distributed file.

## Required publication materials

| Material | Repository path |
|---|---|
| Adjudicated register | `register/AECS_final_27_corpus_register.csv` |
| Codebook and blank template | `coding/codebook.md`, `coding/blind_coding_sheet.csv` |
| Coding record A | `review/closeout_20261104/human_coding/FIRST_PASS_FROZEN.csv` |
| Coding record B and field evidence | `data/coding/independent_coding.csv`, `data/coding/independent_evidence_log.csv` |
| Analysis scripts | `scripts/` |
| Frozen rating input SHA-256 | `results/rating_input_manifest_20261108.json` |
| Provider access and matrix preparation | `DATA.md` |

Repository: https://github.com/Chao163709/affective-eeg-data-collection-review. Use an exact commit identifier when citing or reproducing this release.


The register status columns follow the revised 2026-11-14 workbook. `register/provisional_fields.csv` lists the nine candidate fields; their status is distinct from the two frozen pre-adjudication coding records. The 2026-11-17 documentary check did not promote any of these fields to human-confirmed status.

## Quick verification without restricted data

Python 3.12 was used for the rating analyses. Install `requirements.txt`, then run:

```sh
python scripts/verify_release.py
python -c "import sys; sys.path.insert(0, 'scripts'); from crossed_rating_reml import check; check(); print('REML numerical checks passed')"
python research_quality_audit_20261113/intercoder_agreement/build_intercoder_analysis.py
```

The coding script recomputes outputs in its own folder. Run manifest verification before recomputation; regenerated outputs can differ in software metadata.
The secondary `release_description` comparison excludes six empty derived values for Coder A: these indicate that description-level evidence was not recorded. Explicit undetermined codes remain categories in the all-comparable analysis; the both-definite sensitivity analysis filters them separately. This yields 21 comparable pairs, not 27.

## Rating reproduction

Third-party raw EEG and derived rating matrices are **not distributed**. Obtain access from the providers and prepare the representations described in `DATA.md`. Place the five inputs under `cache/`; the loader requires exact agreement with `results/rating_input_manifest_20261108.json` before analysis.

```sh
python scripts/verified_analysis.py --bootstrap 2000
python scripts/crossed_rating_reml.py
python scripts/consensus_transfer.py
python scripts/share_permutation_null.py
```

The archive does not reconstruct every provider release automatically. Different exports will not match the frozen input hashes; do not disable identity checks to call such a run an exact reproduction.

## Reading the results

Main Table V's Crossed columns are REML point estimates. Its One-way columns and supplementary S2 use one-way ICC(1); S2's crossed bootstrap resamples participants and stimuli and is not a REML confidence interval. Consensus Q is computed from held-out losses, with fixed-prediction descriptive intervals. Shuffling is a descriptive reference, not a calibrated significance test. No classification bound or EEG decoder result is claimed here.

## Citation and versions

The associated manuscript is under preparation for submission. No article DOI or repository archive DOI has been assigned here. Cite the repository URL and the exact commit used. Public availability does not grant rights to third-party datasets. No software reuse license has yet been selected by the authors.
