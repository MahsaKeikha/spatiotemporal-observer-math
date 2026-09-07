# Changelog

## 0.13.0 - 2026-09-07

- Added robust path recovery over exact candidate equivalence classes.
- Kept separate covariance and eigenvalue envelopes for local classes and
  ordered transport-class pairs.
- Introduced a binary mismatch state that excludes the planted class path
  without enumerating candidate paths.
- Supported arbitrary-size Python integer multiplicities for combinatorial
  candidate families.
- Proved an \(O(TK^2)\) class-compressed certificate conditional on exact
  within-class factors and uniform covariance envelopes.
- Verified the class dynamic program against exhaustive class paths.
- Added a 1,000-node overlap-class example representing more than eight
  trillion candidates per time with six numerical states.

## 0.12.0 - 2026-09-07

- Propagated deterministic candidate-local covariance radii through directed
  integration, environmental insulation, and canonical persistence.
- Added candidate-specific local-score and transport-score error arrays.
- Connected moving-partition block selections to an adversarial world-tube
  recovery dynamic program.
- Proved a robust path certificate for every covariance sequence inside the
  declared layered envelope.
- Refactored the finite-sample localized certificate to use the same
  deterministic covariance-radius core.
- Added three regression tests and a split/merge recovery example.

## 0.11.0 - 2026-09-07

- Generalized the block covariance recursion to arbitrary time-indexed
  partitions using rectangular transition comparisons.
- Proved that finite-horizon influence cones survive block splits, merges, and
  membership reassignment without a common refinement.
- Added a moving-partition joint covariance-error API with time-specific block
  validation.
- Verified the bound against exact random matrix propagation through block
  counts `3 -> 2 -> 4 -> 3`.
- Added a layered influence example with block counts `4 -> 3 -> 4 -> 2 -> 3`.

## 0.10.0 - 2026-09-07

- Derived a block comparison recursion for covariance and adjacent-joint
  perturbation errors.
- Proved an exact finite-horizon influence-cone statement on sparse comparison
  graphs.
- Added local joint-error bounds with different present and future block
  selections.
- Verified every blockwise bound against direct random matrix propagation.
- Added an eight-block line-graph example in which remote forcing is excluded
  from the local certificate until its graph path reaches the observed block.

## 0.9.0 - 2026-09-07

- Derived a two-type block comparison theorem from entry-magnitude and row and
  column support-degree assumptions.
- Added direct construction of every global, row-local, within-candidate, and
  local-noise budget required by the overlap-class certificate.
- Verified the structural budgets against all candidate compressions of random
  sparse transition and symmetric noise perturbations.
- Added a matrix-free 1,000-node example that represents more than eight
  trillion candidates with six overlap classes and a positive sufficient
  recovery margin.
- Preserved the explicit limitation that coarse structural envelopes discard
  cancellation and detailed support geometry.

## 0.8.0 - 2026-09-07

- Derived an exact integer occupancy criterion for consecutive
  candidate-planted overlap pairs.
- Added a matrix-free recovery certificate driven by global radii and
  overlap-indexed row, within-candidate, and local-noise budgets.
- Reduced complete-family certificate evaluation from \(\binom ns\) candidate
  subsets to \(O(Ts^2)\) overlap-pair checks once valid budgets are supplied.
- Verified the occupancy criterion by exhaustive enumeration and checked that
  every overlap-class radius dominates every corresponding matrix-level bound
  on the reference system and eight dense perturbation sequences.
- Recorded the limitation that constructing valid class budgets is a separate
  task and can remain combinatorial without additional structural assumptions.

## 0.7.0 - 2026-09-07

- Derived a row-local covariance recursion from structured transition and noise
  perturbations without propagating the realized state covariance.
- Added an a priori support-aware recovery theorem for either the complete
  fixed-size candidate family or a declared reduced family.
- Verified that every a priori block radius contains its realized counterpart
  on the reference system and across eight reproducible dense perturbation
  sequences.
- Added an executable comparison among global, realized support-resolved, and
  a priori support-aware recovery margins.

## 0.6.0 - 2026-09-07

- Derived a finite-horizon covariance recursion for transition and process-noise
  perturbations around the covariance-preserving moving-clique family.
- Propagated the resulting adjacent-covariance radius through directed
  integration, environmental insulation, canonical persistence, and the local
  geometric score.
- Added a zero-conditional-cross-covariance theorem that gives quadratic rather
  than first-order control of incorrect-candidate integration near the base
  model.
- Added a sufficient planted-path theorem that permits nonzero external
  coupling, anisotropic noise, and positive scores for incorrect candidates.
- Added a support-resolved theorem that uses candidate-local covariance blocks,
  overlap-sensitive base spectra, and exact incident planted-edge penalties.
- Added a deterministic perturbed-system generator, an end-to-end numerical
  theorem check, a perturbation-region figure, and five regression tests.

## 0.5.0 - 2026-09-07

- Added a forward-backward near-competitor screen that provably retains every
  path capable of winning under supplied score-error radii.
- Added a covariance-preserving moving-clique family with exact unit covariance.
- Derived closed-form conditional-information, persistence, observer-score, and
  action-margin expressions in self-memory, internal coupling, module size,
  boundary overlap, and action weights.
- Added a symbolic sufficient recovery condition and a matching numerical
  experiment whose exact action margin exceeds the theorem's lower bound.

## 0.4.0 - 2026-09-07

- Added positive-factor Lipschitz bounds for geometric observer and transport
  scores.
- Added a candidate-local covariance certificate with exact adversarial-path
  optimization, reducing the example's sufficient sample threshold by roughly
  four million times.
- Added a parameter-level entry point from \(A_t,Q_t,\Sigma_0\) to the localized
  finite-sample recovery certificate.
- Added path equivalence classes under admissible node-permutation groups.
- Added a total-variation two-model impossibility theorem and an exchangeable
  dynamics test showing when no unique labeled boundary is identifiable.
- Added a reproducible exchangeable-system counterexample with zero action
  margin and a one-half observational maximin ceiling.

## 0.3.0 - 2026-09-07

- Added exact second-best world-tube inference and an optimality margin.
- Added a theorem-backed uniform score-perturbation certificate.
- Added adversarial perturbation tests for certified path stability.
- Aligned local scoring, transport, and covariance propagation to a single
  chronological transition index in the moving-boundary experiment.
- Added full derivations, an experimental protocol, an API guide, and a precise
  account of the proposed space-time-observer connection.
- Added a componentwise planted-path recovery theorem and executable margin
  check.
- Added a finite-sample recovery theorem conditional on uniform score bounds.
- Added an explicit spectral covariance-to-Gaussian-CMI error bound.
- Added a canonical-persistence perturbation theorem and numerical bound.
- Added an end-to-end Gaussian sample-complexity guarantee linking Wishart
  concentration, all score factors, the path margin, and recovery probability.
- Added empirical covariance estimation, Gaussian trajectory simulation, and
  model-free transport scoring from paired observations.
- Added a 192-trial finite-sample benchmark with four internal baselines,
  Wilson intervals, raw JSON results, and a recorded negative comparison.

## 0.2.0 - 2026-09-07

- Added exact covariance propagation for nonstationary Gaussian dynamics.
- Added conditional-information transport across changing subsystem boundaries.
- Added coordinate-invariant canonical transport and a proof ledger.
- Replaced the stationary local approximation in the moving-module experiment.
- Added invariance, environmental-drive, and stationary-equivalence tests.
- Added a regularization phase diagram and a living novelty audit.

## 0.1.0 - 2026-09-06

- Added exact Gaussian information calculations.
- Added fixed-boundary observer-like metrics.
- Added a static-correlation null control.
- Added exhaustive subsystem ranking.
- Added the discrete observer world-tube optimizer.
- Added a planted moving-module experiment and figure.
- Added the initial mathematical framework and ongoing research documentation.
