# Changelog

## 0.26.0 - 2026-09-08

- Proved an observable pilot-normalized covariance bound by composing the
  Gaussian pilot event with each exact pilot-to-screening Loewner sandwich.
- Added a public end-to-end adaptive screen that computes its factors directly
  from the screening covariances and returns candidate-specific relative radii,
  factor errors, score errors, masks, graph, and validity diagnostics.
- Added a fixed 18-regime study with one reusable eight-trillion-trajectory
  pilot per regime and 64 screening draws of 300 million trajectories each.
- Recorded complete pilot, adaptive covariance, score, valid-radius, and path
  coverage. The maximum adaptive radius averages `0.5097` of the fixed radius,
  and the adaptive graph is smaller in every regime.
- Added the four-panel comparison figure, full numerical table, machine-readable
  record, API guide, protocol, assumption audit, and three theorem-level tests.

## 0.25.0 - 2026-09-08

- Proved a covariance-normalized Gaussian screening theorem that propagates a
  population-whitened relative covariance event through conditional mutual
  information, canonical persistence, exact structural nulls, complete scores,
  and the near-competitor graph.
- Added a simultaneous relative Wishart radius whose formula depends on block
  dimension, block count, confidence, and sample count, without population
  eigenvalue-envelope inputs.
- Implemented the relative structural-null screen and exposed every primitive
  factor, score, radius, mask, and validity diagnostic through the public API.
- Added a paired 1,152-trial comparison on the 18-regime grid. Every recorded
  relative covariance, score, and path event is covered; the normalized screen
  retains exactly five states and four edges in every trial and regime.
- Added a four-panel landing-page figure, complete 18-row result table,
  machine-readable record, protocol, assumption audit, API documentation, and
  three direct theorem tests.

## 0.24.0 - 2026-09-08

- Added a fixed 18-regime trajectory-coupled calibration spanning three memory
  levels, three internal-coupling strengths, and two process-noise condition
  numbers, with 64 complete-trajectory Wishart trials per regime.
- Verified all four declared covariance, score, null-aware score, and
  population-path retention events in all 1,152 trials. The per-regime
  64-of-64 Wilson interval is reported rather than treating this run as precise
  validation of a 97.5% tail probability.
- Recorded a nontrivial sharpness result: anisotropic noise can increase the
  population action margin while making the certified screen substantially less
  selective because the candidate-local eigenvalue floor deteriorates.
- Added a three-panel regime map of population margins, retained states, and
  retained edges, together with the complete machine-readable record.
- Refactored the calibration construction so the baseline grid cell is tested
  against and exactly reproduces the original moving-module problem.
- Updated the landing page, central visual overview, protocol, limitations,
  research program, reader guide, result log, and verification counts.

## 0.23.0 - 2026-09-08

- Added the exact covariance of a complete nonstationary Gaussian trajectory,
  including every cross-time block, and tested its adjacent-block consistency.
- Proved that the marginal Wishart and simultaneous screening guarantees remain
  valid when all time points come from the same ensemble of independent complete
  trajectories; independence between timewise covariance estimates is unnecessary.
- Added a 128-trial, five-scale trajectory-coupled calibration using one exact
  42-dimensional Wishart draw per trial, with analytical and empirical cross-time
  covariance-error correlations shown in the committed figure.
- Corrected the moving-module structural-null mask from 35 non-planted states to
  the 28 states whose conditional cross-covariance vanishes exactly. Seven
  non-planted states retain small positive integration through covariance memory
  and now use the generic bound.
- Regenerated the structural-null result under the corrected premise: at 80
  billion trajectories the null-aware screen retains 15 of 40 states and 27 of
  256 edges, compared with 40 states and 231 edges under the generic screen,
  while retaining the population path.
- Expanded the protocol, API guide, limitations, research overview, result log,
  and landing-page gallery to cover the coupled construction and correction.

## 0.22.2 - 2026-09-08

- Moved the complete visual result record onto the repository landing page so
  figures are visible before a visitor opens the documentation.
- Added linked previews for all seven committed figures, organized by moving-
  boundary inference, finite-sample statistics, and recovery certificates.
- Added a compact landing-page verification table linking the 35 propositions,
  20 experiments, seven figures, 94-test record, and CI matrix.
- Removed repeated standalone figures farther down the README so each result has
  one clear visual entry point.

## 0.22.1 - 2026-09-08

- Reorganized the central overview as a visual research record with every
  proposition and experiment title linked to its exact source section.
- Embedded all seven committed result figures with direct links to their
  generating commands, parameters, tables, and interpretation notes.
- Added a compact diagram separating path computation from robustness and
  confidence certification.
- Added a publication-quality comparison of generic and structural-null score
  radii and retained graph fractions.
- Added a visible verification table covering the 94-test suite, lint, Python
  matrix, experiment count, and committed figures without treating software
  tests as scientific validation.

## 0.22.0 - 2026-09-08

- Added a central research overview connecting all 35 propositions, all 20
  experiments, their code, assumptions, numerical evidence, and limitations.
- Derived a quadratic covariance-to-information bound at a predeclared exact
  structural integration null and propagated it through the complete local
  score.
- Added a structural-null Gaussian screen that keeps the general factor-aware
  radius as a fallback and leaves all transport bounds unchanged.
- Improved the certified boundary rate from the generic `N^-1/6` local-score
  rate to `N^-1/3` under the exact-null assumption.
- Initially reported a reduction at 80 billion observations from 40 states and
  231 edges to 6 states and 5 edges. Version 0.23.0 supersedes that result after
  correcting an over-broad structural-null mask; the corrected graph retains 15
  states and 27 edges.
- Added randomized containment and rate tests together with a false-null
  counterexample documenting why the mask cannot be inferred from a small
  empirical score.

## 0.21.0 - 2026-09-08

- Added a seeded calibration of the complete Gaussian screening chain using
  direct draws from the exact unbiased sample-covariance Wishart law.
- Measured simultaneous covariance, primitive-factor, complete-score, and
  population-path coverage at five sample scales spanning eight orders.
- Exposed every candidate-local covariance radius for realized-error audits.
- Recorded realized-to-theoretical radius ratios, positive-factor eligibility,
  and retained state and edge fractions in a machine-readable result file.
- Added Wilson intervals and stated why 64 successful trials cannot precisely
  validate a nominal 97.5% tail probability.
- Documented the distinction between marginal Wishart calibration and a shared
  dependent trajectory ensemble.
- Added a reproducible two-panel calibration figure and three regression tests.

## 0.20.0 - 2026-09-08

- Added a positive-factor refinement for Gaussian first-split screening.
- Constructed score centers directly from empirical primitive factors so the
  factor and score representations cannot disagree.
- Applied local Lipschitz bounds only where every perturbed factor has a
  strictly positive empirical lower endpoint.
- Preserved the zero-safe Hölder fallback independently at every state and edge.
- Exposed primitive factor radii and positive-floor masks for auditability.
- Added randomized containment, refinement monotonicity, zero-factor fallback,
  and range-validation tests.
- Added a controlled comparison in which the refined screen retains 4 of 16
  states and 3 of 48 edges while the zero-safe screen remains complete.

## 0.19.0 - 2026-09-08

- Derived the first-stage screening safety probability from simultaneous
  Gaussian covariance concentration over fixed candidate-local blocks.
- Propagated covariance radii through integration, insulation, canonical
  persistence, and the complete local and transport scores.
- Added first- and second-stage score budgets through an explicit triangle
  inequality before forward-backward graph screening.
- Reported invalid spectral regimes without issuing a false safety guarantee.
- Added randomized containment, monotonicity, invalid-regime, and input-shape
  tests for the new screen.
- Recorded the large sample requirement of the zero-safe worst-case bound as a
  limitation and moved practical factor-aware sharpness to the research frontier.

## 0.18.0 - 2026-09-07

- Added independent sample-split confidence accounting for random screening and
  fixed conditional certification.
- Exposed screening, certification, and combined confidence levels separately.
- Derived the retained-block Gaussian covariance radius and compared it with a
  deterministic admissible recovery radius.
- Refused to issue a guarantee when screening and certification reuse data.
- Added a minimal certification-sample search and checked integer minimality.
- Reframed the remaining conjecture as deriving the first-stage screening
  safety probability rather than composing it with certification.

## 0.17.0 - 2026-09-07

- Replaced the full-present structural compression by explicit class-specific
  present and future block selections.
- Derived a multiplicative insulation correction from a certified upper bound
  on conditional information omitted outside the screened environment.
- Added genuinely ordered source-target transport residuals rather than
  repeating one destination radius across all source classes.
- Kept the new result population-level so data-dependent screening is not
  mistaken for a valid finite-sample guarantee.
- Added a reader guide and assumption ledger for independent expert review.
- Added three regression tests and a screened-environment experiment.

## 0.16.0 - 2026-09-07

- Derived local class and ordered transport-class covariance residuals from a
  moving block comparison envelope.
- Composed block transition, forcing, and cross-error structure with the
  residual-to-factor and factor-to-path recovery theorems.
- Preserved full-present environmental coverage while allowing class-specific
  future block selections.
- Added a structured residual recovery API and explicit intermediate radii.
- Verified the derived radii against direct block compressions and the composed
  result against the residual-level API.
- Added a complete structural example representing more than eight trillion
  candidates per time.

## 0.15.0 - 2026-09-07

- Derived classwise factor intervals from representative covariance models and
  certified spectral-norm residual radii.
- Separated population heterogeneity from subsequent observation covariance
  error as two auditable perturbation stages.
- Used Weyl eigenvalue bounds to construct the spectral envelopes required for
  the second stage automatically.
- Added a public residual-derived class recovery API and result record.
- Verified equivalence with the direct interval API, monotonic degradation with
  residual radius, and rejection at the representative eigenvalue floor.
- Added a 1,000-node example with automatically derived factor intervals and a
  positive complete-path recovery slack.

## 0.14.0 - 2026-09-07

- Replaced exact within-class factor symmetry by certified componentwise factor
  intervals for state classes and ordered transport-class pairs.
- Propagated separate local and edge covariance envelopes into lower and upper
  score intervals.
- Treated positive and negative transport weights with the correct reversal of
  interval endpoints.
- Reused the mismatch-state dynamic program to obtain an \(O(TK^2)\) uniform
  recovery certificate over all admitted within-class heterogeneity.
- Added randomized containment, interval monotonicity, signed-weight, and
  invalid-bound tests.
- Added a 1,000-node heterogeneous-class example with a positive robust slack.

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
