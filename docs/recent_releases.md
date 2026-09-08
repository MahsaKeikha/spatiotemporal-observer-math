# Earlier recent releases

This page preserves the compact records for releases 0.32.0 through 0.35.0.

For releases 0.37.0 and later, use the canonical [Recent Release History](recent_release_history.md). Release 0.36.0 and earlier are also recorded in the root [`CHANGELOG.md`](../CHANGELOG.md).

## 0.35.0 - 2026-09-08

**Main result:** Proposition 47 and Experiment AG.

- Added direct matrix-Laplace concentration for weighted Gaussian Wishart covariance.
- Replaced the previous sphere-net operator-norm reduction by an exact rank-one Gaussian matrix exponential moment.
- Used the full projected temporal eigenvalue profile rather than only Frobenius and spectral norm summaries.
- Added Experiment AG and public matrix-concentration APIs, claim-level tests, machine-readable results, and a visible figure.
- Added the repository-wide Markdown style test that rejects Unicode en dash and em dash punctuation.

[Proposition 47](proposition_47_weighted_wishart_matrix_chernoff.md) · [Experiment AG data](weighted_wishart_matrix_chernoff.json)

## 0.34.0 - 2026-09-08

**Main result:** Proposition 46 and Experiment AF.

- Added a design-specific continuum envelope over a calibrated AR(1) interval.
- Replaced rank-only nuisance pessimism with bounds using the actual declared nuisance design.
- Added analytic between-grid control so the guarantee covers the complete interval.

[Proposition 46](proposition_46_design_specific_ar1_envelope.md) · [Experiment AF data](design_specific_ar1_envelope.json)

## 0.33.0 - 2026-09-08

**Main result:** Proposition 45 and Experiment AE.

- Combined observable nonnegative AR(1) calibration with a general time-varying nuisance projection.
- Propagated uncertainty in the projected covariance normalization.
- Added an exact regression reduction to Proposition 43 when the nuisance rank is one.

[Proposition 45](proposition_45_estimated_ar1_nuisance_projection.md) · [Experiment AE data](estimated_ar1_nuisance_projection.json)

## 0.32.0 - 2026-09-08

**Main result:** Proposition 44 and Experiment AD.

- Replaced ordinary constant mean-centering by projection away from any fixed declared temporal nuisance subspace.
- Proved exact unbiasedness after normalization by `tr(P_H R)`.
- Added a finite-sample covariance radius based on the projected temporal covariance.

[Proposition 44](proposition_44_nuisance_projection.md) · [Experiment AD data](nuisance_projection_calibration.json)