# Recent release history

This page continues the older root changelog for the newest theorem releases. It keeps the recent release sequence compact and points directly to the proof and experiment records rather than duplicating every derivation.

## 0.39.0 - 2026-09-08

**Proposition 51, Experiment AK**

- Added a finite-sample continuum e-value confidence set for the two-parameter temporal family using the complete residual Gaussian likelihood.
- Removed arbitrary constant calibration-channel means exactly with fixed Helmert contrasts.
- Used a proper mixture density `q` fixed before observing the calibration data and the identity `E_theta[q(Z)/p_theta(Z)] = 1` to obtain confidence coverage by Markov's inequality.
- Kept the theorem continuum valued. No parameterwise union bound is used, and the true parameter does not need to lie on the mixture support grid.
- Added Experiment AK, machine-readable results, a deterministic SVG renderer, a visible figure, and five claim-level tests.
- Documented explicitly that the Experiment AK evaluation grid is a visualization, not a certified outer cover of the continuum confidence set.
- Updated the research record to 51 propositions, 37 experiments, 24 figures, and 171 tests.

[Proposition 51](proposition_51_evalue_temporal_confidence_set.md) · [Experiment AK data](evalue_temporal_confidence_set.json) · [Release record](release_0_39.md)

## 0.38.0 - 2026-09-08

**Proposition 50, Experiment AJ**

- Added observable two-parameter temporal calibration for `R(phi, eta) = (1 - eta) R_phi + eta I`.
- Derived finite-sample lag-1 and lag-2 increment-energy bounds that use the filtered temporal spectrum rather than a generic raw-process spectral bound.
- Mapped simultaneous lag-correlation intervals into a conservative `(phi, eta)` rectangle.
- Composed the random calibrated family with Proposition 49 for an independent target record.
- Added Experiment AJ and the observer-to-consciousness interpretation protocol.
- Updated the research record to 50 propositions, 36 experiments, 23 figures, and 166 tests.

[Proposition 50](proposition_50_calibrated_temporal_family.md) · [Experiment AJ data](calibrated_temporal_family.json) · [Release record](release_0_38.md)

## 0.37.0 - 2026-09-08

**Proposition 49, Experiment AI**

- Generalized the temporal concentration theorem from an AR(1) interval to an arbitrary compact temporal covariance family with a certified deterministic finite cover.
- Used operator and normalization covering radii together with Weyl control of the projected eigenvalue spectrum.
- Kept cover geometry deterministic, so cover refinement does not consume confidence through a stochastic union penalty.
- Added the concrete two-parameter AR(1) plus white-noise family helper and Experiment AI.
- Updated the research record to 49 propositions, 35 experiments, 22 figures, and 161 tests.

[Proposition 49](proposition_49_compact_temporal_family.md) · [Experiment AI data](compact_temporal_family.json)

## Earlier releases

The root [`CHANGELOG.md`](../CHANGELOG.md) records releases through 0.36.0 in detail. This recent-history page continues that sequence for the newer temporal-family theorem releases.
