# Reproduction notes

## Resolved: release_description denominator

The summary previously counted all 27 rows even though six Coder A values were empty and marked NOT COMPARABLE by the derivation step. The corrected summary excludes empty derived values only for this secondary field. Explicit undetermined categories remain in the all-comparable analysis and are filtered separately in the both-definite sensitivity analysis. No coded value was changed.

The corrected result is 21 comparisons, 6 agreements, raw agreement 0.2857 and kappa 0.1463 (0.15 at the manuscript precision). The both-definite subset remains 5 pairs, 4 agreements, raw agreement 0.80 and kappa 0.00. The six main categorical fields and two numeric-count comparisons are unchanged. A built-in regression check distinguishes empty derived values from explicitly coded undetermined values.

No restricted rating-input run was performed in this release check. Provider-version reconstruction is incomplete. The public repository is https://github.com/Chao163709/affective-eeg-data-collection-review. No archive DOI has been assigned.
