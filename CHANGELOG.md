# Changelog

This file records the current research-software release sequence in chronological order. The original detailed changelog is preserved verbatim in [`docs/CHANGELOG_LEGACY_FULL.md`](docs/CHANGELOG_LEGACY_FULL.md).

## 0.47.1 - 2026-09-08

- Tightened Proposition 57 without introducing a new proposition. The projected normalization cover now uses a trace-specific deterministic derivative bound for the transformed exponential temporal family rather than multiplying the operator-cover radius by the full residual rank.
- The Proposition 57 / Experiment AR transformed eigenvalue cover is unchanged, while the projected-normalization covering radius contracts from approximately `7.53776` to `0.01419745`.
- The uniform Experiment AR relative covariance certificate improves from the earlier `0.8677117535` record to `0.7195879984`, still at combined calibration-target confidence lower bound `0.950625`.
- The reduction relative to the Proposition 55 calibrated raw-time radius is now approximately `70.2%`.
- Updated the Proposition 57 proof, implementation, machine-readable JSON, deterministic SVG renderer, visible figure, and claim-level artifact checkpoints so the theorem, data, visual, and tests agree.
- Reorganized the README, Physics Guide, Research Overview, Visual Research Guide, bibliography navigation, and equation-provenance documentation around a physics-first and mathematics-first reading path.
- Added an explicit Physics + Mathematics + Citation Map separating external foundations, repository definitions, repository theorems, experiments, and interpretation boundaries.
- No new proposition or experiment is introduced by this patch. The research record remains 58 propositions, 45 reproducible experiments, 33 scientific result figures, and 223 claim-level tests.

## 0.47.0 - 2026-09-08

- Added Proposition 58, which deterministically propagates simultaneous candidate-local relative covariance uncertainty through integration, environmental insulation, persistence, transport, local observer scores, and the complete world-tube objective.
- Added Experiment AS, the observer-scale covariance-to-world-tube certification audit.
- Identified the observer covariance block `B_(t,S) = (X_t, X_(t+1)^S)` with dimension `n+s` and showed that target-indexed covariance blocks are reused across incoming candidate edges.
- Recorded the controlled benchmark with `n=7`, candidate size `s=3`, horizon `T=5`, 35 candidates per time, 175 target-indexed observer blocks, and population action margin `0.1264216185`.
- Recorded the negative observer-scale concentration diagnostic: at 118 residual innovation degrees the current exact-tau matrix theorem gives relative radius `1.8573569119 > 1` for dimension 10 and 175 simultaneous blocks.
- Added proof documentation, Experiment AS JSON, deterministic figure, renderer, implementation, and claim-level tests.

## 0.46.0 - 2026-09-08

- Added Proposition 57, robust innovation whitening over a finite-sample calibrated physical relaxation-time interval.
- Added Experiment AR, which propagates the Proposition 55 relaxation-time hull through one fixed working innovation whitener.
- Established a uniform finite-sample target covariance certificate under the declared separable Gaussian one-timescale exponential model and calibration-target separation.
- The original 0.46.0 numerical record used a deliberately coarse projected-trace envelope and reported radius `0.8677117535`; release 0.47.1 supersedes that numerical certificate with the tighter trace-specific bound `0.7195879984` while leaving the Proposition 57 construction intact.

## 0.45.0 - 2026-09-08

- Added Proposition 56, exact innovation-whitened target covariance concentration when the physical relaxation time is known.
- Added Experiment AQ.
- On the 120-sample target schedule with nuisance rank two, exact local innovation coordinates reduce the scalar known-tau target covariance radius from approximately `2.16725` to approximately `0.43647`.
- Added the exact Gaussian residual-Wishart reduction, covariance-aware nuisance removal, implementation, proof, machine-readable result, deterministic figure, and claim-level tests.

## 0.44.0 - 2026-09-08

- Added Proposition 55, a quadratic finite-sample outer cover for irregular-time physical relaxation calibration using exact local log-evalue slope and a rigorous cell-local curvature bound.
- Added Experiment AP and a deterministic SVG comparing first-order and quadratic calibration, the target-radius ladder, and the known-tau oracle floor.
- Recorded the known-tau diagnostic `2.1672468952 > 1`, showing that calibration refinement alone could not close the target covariance benchmark.
- The research record at this stage was 55 propositions, 42 experiments, 30 scientific result figures, and 206 claim-level tests.

## 0.43.0 - 2026-09-08

- Added Proposition 54, a two-scale certified physical relaxation-time cover separating calibration-cell resolution from target temporal-cover resolution.
- Added Experiment AO.
- Reduced the Experiment AN target covariance radius from `3.15549` to `2.57207` while retaining combined confidence `0.950625`, with the radius explicitly remaining above one.

## 0.42.0 - 2026-09-08

- Added Proposition 53B, exact irregular-time innovation likelihood and finite-sample continuum e-value inference for physical relaxation time.
- Added Experiment AN, cell-local certified outer covers, target composition through the compact temporal-family theorem, machine-readable results, proof documentation, and deterministic figure.
- Recorded the target covariance radius `3.1554895445 > 1` as the next finite-sample tightness frontier.

## Earlier history

The detailed release history before this condensed sequence, including releases 0.1.0 through 0.41.x and intermediate corrections, is preserved in [`docs/CHANGELOG_LEGACY_FULL.md`](docs/CHANGELOG_LEGACY_FULL.md). Release-specific proof pages, experiment records, figures, and assumptions remain linked from the [Research Index](docs/research_index.md).
