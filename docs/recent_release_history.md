# Recent release history

This page keeps the newest theorem sequence compact and points to the canonical proof, experiment, and release records. Earlier detailed history remains in the root [`CHANGELOG.md`](../CHANGELOG.md) and [Earlier Recent Releases](recent_releases.md).

## 0.46.0 - 2026-09-08

**Proposition 57, Experiment AR**

- Propagates the finite-sample Proposition 55 physical relaxation-time interval through one fixed working innovation whitener.
- Certifies the complete transformed temporal family `C_tau = W0 R_tau W0^T` with a deterministic operator cover and Proposition 49 matrix concentration.
- Removes Proposition 56's exact-target-tau assumption on the controlled benchmark.
- Reduces the calibrated raw-time target radius from `2.41488` to `0.86771`, a reduction of about `64.1%`, while retaining `epsilon < 1`.
- Uses calibration and target confidence `0.975` each, giving combined confidence lower bound `0.950625` under the declared independent-record design.
- Adds a proof page, public API, machine-readable Experiment AR record, deterministic SVG, renderer, and claim-level artifact checks.
- Updates the research record to 57 propositions, 44 experiments, 32 scientific result figures, and 219 claim-level tests.

[Proposition 57](proposition_57_robust_innovation_whitening.md) | [Experiment AR data](robust_innovation_whitened_target.json) | [Experiment AR figure](robust_innovation_whitened_target.svg) | [Release record](release_0_46.md)

## 0.45.0 - 2026-09-08

**Proposition 56, Experiment AQ**

- Replaces the previous raw-time target estimator by exact physical-time innovation whitening when the target relaxation time is known.
- Applies the Proposition 53 whitener to both measurements and the fixed nuisance design.
- Reduces the 120-sample target problem to exactly 118 residual Gaussian innovation degrees of freedom after rank-2 nuisance removal.
- Reduces the known-tau raw-time oracle radius from `2.16725` to `0.43644`, a `79.86%` reduction, crossing `epsilon < 1` without adding target samples.
- Explicitly records exact target tau as the remaining assumption addressed by Proposition 57.
- Updates the research record to 56 propositions, 43 experiments, 31 scientific result figures, and 211 claim-level tests.

[Proposition 56](proposition_56_innovation_whitened_target.md) | [Experiment AQ data](innovation_whitened_target.json) | [Experiment AQ figure](innovation_whitened_target.svg) | [Release record](release_0_45.md)

## 0.44.0 - 2026-09-08

**Proposition 55, Experiment AP**

- Replaces the first-order calibration enclosure by an exact local log-evalue slope plus a rigorous cell-local curvature certificate.
- At 160 cells, contracts the certified tau width by about `73.0%`.
- Improves the target radius to `2.41488`.
- Adds the decisive known-tau oracle diagnostic `2.16725 > 1`, showing that target covariance concentration, not calibration uncertainty, is then the dominant bottleneck.

[Proposition 55](proposition_55_quadratic_relaxation_calibration.md) | [Experiment AP data](quadratic_relaxation_calibration.json) | [Release record](release_0_44.md)

## 0.43.0 - 2026-09-08

**Proposition 54, Experiment AO**

- Separates fine irregular-time calibration certification from target temporal-cover resolution.
- Reduces the Experiment AN target radius from `3.15549` to `2.57207` while retaining the same combined-confidence construction.
- Records that the radius remains above one and identifies local temporal-envelope tightness as the next issue.

[Proposition 54](proposition_54_two_scale_irregular_tau_cover.md) | [Experiment AO data](two_scale_irregular_tau_cover.json) | [Release record](release_0_43.md)

## 0.42.0 - 2026-09-08

**Proposition 53B, Experiment AN**

- Adds direct finite-sample inference for physical relaxation time on irregular timestamps.
- Uses the exact irregular-grid Gaussian innovation likelihood to construct a continuum e-value confidence set.
- Adds a certified finite outer cover, time-unit invariance, and independent target composition.
- Explicitly exposes the remaining target covariance radius `3.1554895445 > 1` as a tightness frontier.

[Proposition 53B](proposition_53b_irregular_tau_evalue.md) | [Experiment AN data](irregular_relaxation_evalue_calibration.json) | [Release record](release_0_42.md)

## 0.41.1 - 2026-09-08

**Proposition 53 extension, Experiment AM extension**

- Keeps the research record at Proposition 53 for consequences of the same exponential physical-time kernel.
- Derives the exact irregular-grid transition law with local coefficients `alpha_i = exp(-(t_{i+1}-t_i)/tau)`.
- Proves that products of local transition coefficients reproduce every long-range exponential covariance entry exactly.
- Constructs an exact lower-bidiagonal temporal whitening matrix.
- Derives the exact tridiagonal temporal precision matrix `R_tau^-1 = W_tau^T W_tau`.
- Derives the exact determinant and log-determinant factorization from local innovation variances.
- Proves exact composition of transitions and innovation variances when intermediate observations are removed.
- Updates the research record to 53 propositions, 39 experiments, 27 scientific result figures, and 188 tests.

[Proposition 53](proposition_53_physical_relaxation_time.md) | [Experiment AM data](physical_relaxation_sampling.json) | [Markov figure](physical_relaxation_markov.svg) | [Release record](release_0_41_1.md)

## 0.41.0 - 2026-09-08

**Proposition 53, Experiment AM**

- Replaces sample-index AR(1) persistence as the primary physical parameter with a relaxation time `tau` for the exponential temporal model.
- Proves exact uniform-sampling equivalence `phi_Delta = exp(-Delta/tau)` and exact coarse-sampling consistency.
- Makes the covariance representation invariant to consistent rescaling of timestamps and tau.
- Extends the model to irregular physical timestamps and derives an analytic operator-Lipschitz cover.
- Updates the research record to 53 propositions, 39 experiments, 26 scientific result figures, and 183 tests.

[Proposition 53](proposition_53_physical_relaxation_time.md) | [Experiment AM data](physical_relaxation_sampling.json) | [Release record](release_0_41_0.md)

## 0.40.0 - 2026-09-08

**Proposition 52, Experiment AL, physics-first documentation**

- Adds a certified finite outer cover of the Proposition 51 continuum e-value confidence set.
- Excludes a parameter cell only when a deterministic likelihood perturbation bound proves that every point in the cell is rejected.
- Composes the retained temporal family with Proposition 49 for an independent target covariance record.
- Adds the Physics Guide, physics pipeline, Figure Reading Guide, and physical-accountability contribution standard.
- Updates the research record to 52 propositions, 38 experiments, 25 scientific result figures, and 177 tests.

[Proposition 52](proposition_52_certified_evalue_outer_cover.md) | [Experiment AL data](certified_evalue_outer_cover.json) | [Release record](release_0_40.md)

## 0.39.0 - 2026-09-08

**Proposition 51, Experiment AK**

- Adds a finite-sample continuum e-value confidence set for the two-parameter temporal family using the complete residual Gaussian likelihood.
- Removes arbitrary constant calibration-channel means exactly with fixed Helmert contrasts.
- Uses a proper mixture density fixed before observing calibration data and obtains coverage without a parameterwise union bound.
- Updates the research record to 51 propositions, 37 experiments, 24 figures, and 171 tests.

[Proposition 51](proposition_51_evalue_temporal_confidence_set.md) | [Experiment AK data](evalue_temporal_confidence_set.json) | [Release record](release_0_39.md)

## 0.38.0 - 2026-09-08

**Proposition 50, Experiment AJ**

- Adds observable two-parameter temporal calibration for `R(phi, eta) = (1 - eta) R_phi + eta I`.
- Maps simultaneous lag-correlation intervals into a conservative `(phi, eta)` rectangle.
- Composes the random calibrated family with Proposition 49 for an independent target record.
- Adds the observer-to-consciousness Interpretation Protocol.
- Updates the research record to 50 propositions, 36 experiments, 23 figures, and 166 tests.

[Proposition 50](proposition_50_calibrated_temporal_family.md) | [Experiment AJ data](calibrated_temporal_family.json) | [Release record](release_0_38.md)

## 0.37.0 - 2026-09-08

**Proposition 49, Experiment AI**

- Generalizes temporal matrix concentration from an AR(1) interval to an arbitrary compact temporal covariance family with a certified deterministic finite cover.
- Uses operator and normalization covering radii together with Weyl control of the projected eigenvalue spectrum.
- Keeps cover geometry deterministic so cover refinement does not consume confidence through a stochastic union penalty.
- Adds the concrete two-parameter AR(1) plus white-noise helper and Experiment AI.
- Updates the research record to 49 propositions, 35 experiments, 22 figures, and 161 tests.

[Proposition 49](proposition_49_compact_temporal_family.md) | [Experiment AI data](compact_temporal_family.json)

## Earlier releases

Release 0.36.0 and earlier are recorded in the root [`CHANGELOG.md`](../CHANGELOG.md). Compact records for releases 0.32.0 through 0.35.0 are also preserved in [Earlier Recent Releases](recent_releases.md).