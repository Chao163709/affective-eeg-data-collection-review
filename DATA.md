# Rating input preparation and access

Inputs are local derived representations, not necessarily provider filenames. Each entry contains one rating per observed participant/stimulus/dimension. Missing observations remain NaN. Dimensions are fitted separately.

| Dataset | Access starting point | Required local file | Representation |
|---|---|---|---|
| DEAP | https://doi.org/10.1109/T-AFFC.2011.15 | deap_subj32_8d65c6_y.npy | First two rating columns; reshape 32 × 40 × 2 (valence, arousal). |
| MAHNOB-HCI | https://doi.org/10.1109/T-AFFC.2011.25 | mahnob_meta.csv | subject, media, valence, arousal; pivot to 27 × 20. |
| DENS | https://openneuro.org/datasets/ds003751 | dens_ratings.csv | subject, stimulus, dim, y; remove identical duplicate keys, reject conflicts; 34 × 20, 367 observed per dimension. |
| FACED | https://doi.org/10.1038/s41597-023-02650-w | faced_ratings_long.csv | subject, video_index, item, score; use Valence/Arousal; exclude five fully missing IDs, retain nine incomplete participants; 118 × 28. |
| MET | https://openneuro.org/datasets/ds008701 | met_ratings.tsv | participant_id, song_id, Valence, Arousal; pivot to 20 × 20. |

## Preparation steps

1. Request or download each dataset through its provider access route identified by the descriptor or repository above. Follow the provider terms; a DOI is a descriptor starting point, not a promise of an unrestricted download. Record provider release version and download date in any new reconstruction.
2. Extract the rating records, retaining participant and stimulus identifiers to align observations. Keep valence and arousal separate; do not replace individual ratings with stimulus-assigned categories.
3. For MAHNOB-HCI, pivot the subject/media table separately for valence and arousal. For MET, strip column-name whitespace and pivot participant_id/song_id separately for Valence and Arousal. Preserve missing cells as NaN.
4. For DENS, reject conflicting repeated subject/stimulus/dimension keys, remove identical duplicate export rows (22 across both dimensions), and align the two dimensions on common keys. The frozen representation contains 34 participants, 20 clips and 367 observed cells per dimension.
5. For FACED, pivot the Valence and Arousal questionnaire items by subject/video_index, then exclude only IDs missing both dimensions throughout. The frozen representation has 123 source IDs, 118 retained participants, 109 complete records and 3158 observed cells per dimension.
6. For DEAP, retain the first two columns of the frozen rating array and reshape them to participant × trial × dimension (32 × 40 × 2); confirm participant/trial ordering before reshaping. The original eight-column local representation is not supplied here, and cannot be inferred to be a provider-native export.
7. Save the five named representations under `cache/`. Verify SHA-256 against the frozen input manifest. A newly generated but semantically equivalent CSV can differ byte-for-byte; such a reconstruction needs its own manifest and is not an exact frozen-input reproduction.

Source access remains subject to provider terms. The frozen derived input SHA-256 identities are supplied, but correspondence to specific original provider release versions has not been fully reconstructed. No EEG files, trial-level rating tables or participant identifiers from these matrices are included.
