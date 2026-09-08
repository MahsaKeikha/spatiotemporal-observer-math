# Recent release history

This page continues the older root changelog for the newest theorem releases. It keeps the recent sequence compact and points directly to proof and experiment records rather than duplicating every derivation.

## 0.41.0 - 2026-09-08

**Proposition 53, Experiment AM**

- Replaced the sample-index AR(1) coefficient as the primary physical parameter with a relaxation time \(\tau\) for the exponential temporal model.
- Proved exact uniform-sampling equivalence \(\phi_{\Delta t}=\exp(-\Delta t/\tau)\).
- Proved exact coarse-sampling consistency \(\phi_{k\Delta t}=\phi_{\Delta t}^k\).
- Made the covariance invariant to a change of time units when timestamps and \(\tau\) are rescaled together.
- Extended the temporal covariance model to irregular physical timestamps.
- Derived an analytic operator-Lipschitz bound over a declared relaxation-time interval and composed the resulting deterministic cover with Proposition 49.
- Added Experiment AM, machine-readable data, deterministic SVG rendering, and six claim-level tests.
- Updated the research record to 53 propositions, 39 experiments, 26 scientific result figures, and 183 tests.

[Proposition 53](proposition_53_physical_relaxation_time.md) · [Experiment AM data](physical_relaxation_sampling.json) · [Release record](release_0_41_0.md)

## 0.40.0 - 2026-09-08

**Proposition 52, Experiment AL, and physics-first documentation**

- Added a certified finite outer cover of the Proposition 51 continuum e-value confidence set.
- Excluded a parameter cell only when a deterministic likelihood perturbation bound proves that every point in the cell is rejected by Proposition 51.
- Composed the retained temporal family with Proposition 49 for an independent target covariance record.
- Kept the nuisance-compressed eigenvalue radius separate from the raw temporal normalization radius required by the projected trace proof.
- Added Experiment AL, machine-readable results, deterministic SVG rendering, and six claim-level tests.
- Added the Physics Guide, physics pipeline, Figure Reading Guide, and a physical-accountability contribution standard.
- Updated the research record to 52 propositions, 38 experiments, 25 scientific result figures, and 177 tests.

[Proposition 52](proposition_52_certified_evalue_outer_cover.md) · [Experiment AL data](certified_evalue_outer_cover.json) · [Release record](release_0_40.md)

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
