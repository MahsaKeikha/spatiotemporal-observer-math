# Recent releases

This page records the research-software releases added after the older root changelog entries. Each release corresponds to a specific mathematical step rather than a cosmetic version bump.

## 0.35.0 - 2026-09-08

**Main result:** Proposition 47 and Experiment AG.

- Added direct matrix-Laplace concentration for weighted Gaussian Wishart covariance.
- Replaced the previous sphere-net operator-norm reduction by an exact rank-one Gaussian matrix exponential moment.
- Used the full projected temporal eigenvalue profile rather than only Frobenius and spectral norm summaries.
- Added Experiment AG, including the comparison `1.077 -> 0.459` at `N=850`, `phi=0.65`, and `1.630 -> 0.653` at `phi=0.80`.
- Added a 96-trial short-record check at `N=300`, `phi=0.65`.
- Added public matrix-concentration APIs, claim-level tests, machine-readable results, and a visible figure.
- Added a repository-wide Markdown style test that rejects en dash and em dash Unicode punctuation.
- Rewrote the landing page, research overview, and research index around the current theorem chain.

[Proposition 47](proposition_47_weighted_wishart_matrix_chernoff.md) · [Experiment AG data](weighted_wishart_matrix_chernoff.json)

## 0.34.0 - 2026-09-08

**Main result:** Proposition 46 and Experiment AF.

- Added a design-specific continuum envelope over a calibrated AR(1) interval.
- Replaced rank-only nuisance pessimism with bounds that use the actual declared nuisance design.
- Added analytic Lipschitz control between deterministic AR(1) grid points so the guarantee covers the entire interval.
- Added Experiment AF, including a regime where the rank-only lower normalization becomes negative while the design-specific lower normalization remains positive near `99.75`.
- Added claim-level continuum checks against dense intermediate AR(1) values.

[Proposition 46](proposition_46_design_specific_ar1_envelope.md) · [Experiment AF data](design_specific_ar1_envelope.json)

## 0.33.0 - 2026-09-08

**Main result:** Proposition 45 and Experiment AE.

- Combined observable nonnegative AR(1) calibration with a general time-varying nuisance projection.
- Propagated uncertainty in the projected covariance normalization.
- Added an exact regression reduction to Proposition 43 when the nuisance rank is one.
- Added Experiment AE with 192 seeded target records. All recorded AR(1) intervals contained the true coefficient and all recorded covariance errors were below the theorem radius.
- Documented the strong-correlation conservatism that motivated Propositions 46 and 47.

[Proposition 45](proposition_45_estimated_ar1_nuisance_projection.md) · [Experiment AE data](estimated_ar1_nuisance_projection.json)

## 0.32.0 - 2026-09-08

**Main result:** Proposition 44 and Experiment AD.

- Replaced ordinary constant mean-centering by projection away from any fixed declared temporal nuisance subspace.
- Proved exact unbiasedness after normalization by `tr(P_H R)`.
- Added a finite-sample covariance radius based on the projected temporal covariance.
- Added Experiment AD. The projected estimator remained stable under large affine drift while ordinary constant mean-centering became severely biased.
- Added public nuisance-projection APIs, five claim-level tests, machine-readable results, and a visible figure.

[Proposition 44](proposition_44_nuisance_projection.md) · [Experiment AD data](nuisance_projection_calibration.json)
