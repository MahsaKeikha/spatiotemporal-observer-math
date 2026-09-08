# Experimental protocol

This document records the construction rules, controls, validation tests, and
limitations needed to interpret the committed experiments. Exact numerical
outputs and commands are maintained in
[Reproducible results](reproducible_results.md); theorem assumptions are indexed
in the [Assumption ledger](assumption_ledger.md).

## 1. Numerical regimes

The fixed-system and moving-boundary population experiments use analytical
covariances. They do not draw finite samples, so repeated runs on the same NumPy
and SciPy numerical stack should agree up to floating-point roundoff. The
finite-sample benchmark draws seeded independent trajectory ensembles as
specified in Section 4.

## 2. Fixed modular system

The first system has six variables split into blocks \((0,1,2)\) and
\((3,4,5)\). Before spectral scaling, the transition matrix has

- diagonal entries `0.42`
- off-diagonal entries `0.25` within a block
- off-diagonal entries `0.005` between blocks

The full matrix is rescaled to spectral radius `0.86`. Process noise is
\(Q=0.16I\). The code solves the discrete Lyapunov equation for the stationary
covariance and ranks all \(\binom{6}{3}=20\) three-variable candidates.

The expected result is not assumed by the optimizer. It is known from the way
the matrix was constructed: the two planted blocks should rank ahead of mixed
three-variable subsets.

### Correlation-only control

The control has four variables with transition matrix \(A=0.65I\). Its process
noise has diagonal entries `0.2` and pairwise correlation `0.55`. This creates
instantaneous correlation without cross-variable dynamics. The directed
integration should therefore vanish even though static mutual information does
not.

## 3. Moving-boundary system

The second system has seven variables and five candidate times. The planted
boundary is

\[
(0,1,2),\ (1,2,3),\ (2,3,4),\ (3,4,5),\ (4,5,6).
\]

At time \(t\), the unscaled transition matrix begins with diagonal `0.32` for
all variables. Each variable in the active boundary receives diagonal `0.46`
and directed coefficient `0.18` from each of the other two active variables.
The matrix is then rescaled to spectral radius `0.84`. Process noise is
\(Q_t=0.18I\).

The initial covariance is the stationary covariance associated with the first
transition matrix. Subsequent covariances follow the actual chronological
recursion

\[
\Sigma_{t+1}=A_t\Sigma_tA_t^\mathsf T+Q_t.
\]

For each time, all \(\binom{7}{3}=35\) three-variable boundaries are scored.
For each adjacent pair of times, all \(35^2=1225\) source-target transitions are
scored from the same \((\Sigma_t,A_t,Q_t)\) edge used by covariance propagation.
This shared indexing matters: local dynamics, transport, and covariance must
describe one generative timeline.

The world-tube search uses:

| Parameter | Value |
| --- | ---: |
| Local-score weight | 1.00 |
| Transport weight \(\chi\) | 0.25 |
| Jaccard continuity weight \(\lambda\) | 0.08 |
| Candidate size | 3 |
| Number of candidates per time | 35 |
| Number of candidate times | 5 |

These weights were chosen for the initial construction and must not be treated
as universal constants. The phase diagram scans \(\chi\in[0,0.6]\) and
\(\lambda\in[0,0.8]\) on a 25 by 25 grid.

## 4. Finite-sample benchmark

`finite_sample_benchmark.py` draws independent trajectory ensembles through all
five transitions, producing six observed states per trajectory. It estimates
the covariance of each stacked pair \([X_t,X_{t+1}]\) with a diagonal ridge equal
to `1e-5` times the larger of one and the mean sample variance.

The committed run uses sample sizes `20, 40, 80, 160, 320, 640`, 32 independently
seeded trials at each size, and root `SeedSequence` value `20260907`. Child seeds
are generated before parallel execution, so changing the worker count does not
change the sampled systems.

Five procedures receive the same estimated local scores:

| Procedure | Temporal information used |
| --- | --- |
| Distributional world-tube | Conditional-information transport and Jaccard continuity |
| Independent local choices | No temporal linking; maximize each time separately |
| Local score plus continuity | Jaccard continuity but no transport reward |
| Coefficient-based transport | Transport energy from a least-squares transition estimate |
| Best fixed boundary | One boundary maximizing summed local score at all times |

These are internal baselines, not implementations of named external methods.
The script reports mean boundary accuracy, its standard error, exact path
recovery, and a Wilson 95% interval for the exact-recovery proportion.

### Analytical certificates

The global certificate controls each complete 14-dimensional adjacent
covariance with one spectral envelope. The localized certificate instead uses
the 10-dimensional principal block containing all seven present variables and
the three future variables of each target candidate. It union-bounds over the
five times and 35 targets, propagates the resulting errors through the actual
population score factors, and uses dynamic programming to find the strongest
error-inflated competing path. Both calculations use confidence `0.95`.

### Gaussian screening calibration

`gaussian_screen_calibration.py` isolates the statistical screening question
from trajectory simulation cost by drawing unbiased covariance estimates
directly from their exact Wishart law. For each time, if the population adjacent
covariance is \(\Sigma_t^{(2)}\), the script draws

\[
\widehat\Sigma_t^{(2)}
\sim \frac{1}{N-1}\mathcal W_{14}(N-1,\Sigma_t^{(2)}).
\]

This is the distribution of the usual unbiased sample covariance from \(N\)
independent Gaussian observations. Draws at different times are independent in
this calibration. Cross-time independence is not required by the union-bound
theorem, but Experiment S alone does not reproduce the dependence induced by
following the same trajectories through every time.

The candidate family is fixed before sampling. It contains the five planted
three-node boundaries and three declared alternatives, for eight candidates at
each of five times. No ridge is applied. Exact population eigenvalue envelopes
are used, so the experiment tests the concentration and perturbation chain; it
does not test how to estimate those envelopes from data.

The committed run uses 64 seeded trials at each of five sample counts from
`80,000` through `8,000,000,000,000`, with root `SeedSequence` value `20260908`.
The large upper counts are computationally feasible because a Wishart matrix is
drawn directly rather than materializing trillions of observations. They are
included to locate the point at which the conservative analytical screen begins
to remove competitors, not to describe a practical data-collection plan.

Each trial records five binary events: simultaneous covariance coverage,
primitive-factor coverage, complete-score coverage, retention of the population
maximizer, and validity of every spectral perturbation block. It also records
the maximum realized-to-theoretical covariance-radius ratio, retained state and
edge fractions, and the fractions eligible for positive-factor refinement.
Wilson 95% intervals accompany every binary rate.

### Trajectory-coupled Gaussian screening calibration

`trajectory_coupled_screen_calibration.py` repeats the screening audit with the
correct dependence structure for an ensemble of independent complete
trajectories. The code first constructs the exact covariance of

\[
Z=(X_0^\mathsf T,\ldots,X_5^\mathsf T)^\mathsf T\in\mathbb R^{42}.
\]

For \(i<j\), its cross-time block is

\[
\operatorname{Cov}(X_i,X_j)
=\Sigma_i(A_{j-1}\cdots A_i)^\mathsf T.
\]

Each trial then makes one draw

\[
\widehat\Sigma_Z\sim
\frac{1}{N-1}\mathcal W_{42}(N-1,\Sigma_Z)
\]

and extracts all five adjacent 14-dimensional principal blocks. Thus the
timewise covariance estimates have the same marginal Wishart laws as in
Experiment S but are no longer independent. Proposition 36 shows that the same
simultaneous union-bound guarantee applies because it uses only the marginal
failure probabilities, not independence across time.

The committed run uses 128 trials at each of the same five sample counts, root
`SeedSequence` value `20260910`, and the same fixed candidate family. In
addition to the coverage and graph statistics, it audits temporal dependence
through the sample-variance error of node zero. For Gaussian sample covariance,

\[
\operatorname{Corr}(\widehat\Sigma_{aa}-\Sigma_{aa},
                    \widehat\Sigma_{bb}-\Sigma_{bb})
=\frac{\Sigma_{ab}^2}{\Sigma_{aa}\Sigma_{bb}}.
\]

The plotted matrix places empirical correlations above the diagonal and this
exact finite-sample formula below it. The comparison is diagnostic rather than
a fitted target.

The same audit corrected the structural-null mask used by Experiment T. In the
moving-module construction, 28 non-planted candidate-times have an exactly
vanishing conditional cross-covariance for at least one internal bipartition.
Seven other non-planted states have small but positive integration inherited
from earlier dynamics. Those seven now receive the generic perturbation bound.
The numerical mask is accepted only after a model-specific block-support audit:
the exact-zero group lies below `1e-14` in integration while the smallest
positive memory effect exceeds `1e-9`. This separation is a check of the
controlled construction, not a general procedure for discovering nulls from
data.

### Multi-regime trajectory-coupled calibration

`multi_regime_coupled_calibration.py` holds the seven-node, three-member,
five-time candidate problem fixed while varying three independent model axes:

| Axis | Declared values |
| --- | --- |
| Memory `(outside, active)` | short `(0.12, 0.28)`, baseline `(0.32, 0.46)`, long `(0.52, 0.66)` |
| Internal coupling \(\beta\) | `0.10`, `0.18`, `0.26` |
| Process-noise condition number \(\kappa(Q_t)\) | `1`, `9` |

This Cartesian product gives 18 regimes. Each transition is rescaled to
spectral radius `0.84`, so the memory and coupling settings specify their
relative structure rather than changing the stability ceiling. The diagonal
noise entries form a geometric sequence with geometric mean `0.18`; the
sequence is rotated by one coordinate at each time. The baseline-memory,
coupling-`0.18`, condition-`1` cell exactly reproduces Experiment U's population
model, and a regression test checks every adjacent covariance block.

Every cell uses 64 trials, sample count `80,000,000,000`, screening confidence
`0.975`, and root `SeedSequence` value `20260911`. A trial draws one complete
42-dimensional Wishart covariance and extracts all adjacent blocks. The
candidate family and action weights are unchanged. The script records the
population path and action margin, candidate-local spectral extrema, exact-null
count, simultaneous coverage events, and generic and null-aware retained-graph
fractions. Parameters and seeds are fixed before inspecting the outcomes.

The grid is a controlled sensitivity study, not a held-out benchmark. It does
not vary boundary motion, candidate size, latent drive, missingness,
nonlinearity, or distribution family.

### Covariance-normalized paired calibration

`relative_covariance_calibration.py` uses the identical 18-cell grid and sample
budget. Its root `SeedSequence` is `20260912`; each of the 64 seeds per cell
produces one full-trajectory Wishart draw that is passed to both the absolute
and relative structural-null screens. This pairing removes Monte Carlo variation
from the comparison of the two certificates.

For each of the 40 fixed ten-dimensional candidate blocks, the script computes
the realized population-whitened error

\[
\|\Gamma^{-1/2}(\widehat\Gamma-\Gamma)\Gamma^{-1/2}\|_2
\]

and compares it with the simultaneous Proposition 37 radius. It separately
checks complete local and transport score containment, validity of the relative
perturbation regime, and retention of every state and edge on the population
path. Graph fractions for the paired absolute and relative calculations are
then recorded from the same empirical factors.

The experiment uses exact population covariance only to audit the theorem's
coverage event. The public screening function needs dimensions, sample count,
confidence, empirical factors, candidates, and the predeclared structural-null
mask; it does not accept population eigenvalue bounds. This distinction does
not make the procedure distribution-free: the radius still uses the Gaussian
Wishart law.

### Reusable-pilot adaptive calibration

`cross_fitted_relative_calibration.py` keeps the 18 population regimes fixed.
For each regime it draws one pilot covariance from eight trillion independent
complete trajectories and reuses that reference across 64 independent
screening covariances of 300 million trajectories each. The root
`SeedSequence` is `20260915`. Pilot and screening seeds are distinct and fixed
before the results are inspected.

The script compares two screens on every screening draw. The fixed screen uses
the Proposition 37 radius at 300 million trajectories. The adaptive screen
computes each candidate's exact pilot-normalized discrepancy and composes it
with the simultaneous pilot radius using Proposition 38. Both receive the same
screening covariance, candidate family, 28-state exact-null mask, score weights,
and zero later-certification budget.

Recorded events include the one pilot-coverage event per regime, adaptive
population-relative covariance coverage for every later draw, complete local
and transport score coverage, valid-radius status, and population-path
retention. The figure reports graph fractions. The JSON also records the
adaptive-to-fixed radius ratio and actual-error-to-adaptive-radius ratio.

This is an amortized-reference experiment. The eight-trillion pilot is not
charged as though it were collected separately for each screening draw, and the
comparison is not an equal-total-sample efficiency claim. Reuse is valid only
under the same population covariance.

### Declared-drift calibration

`drift_robust_relative_calibration.py` fixes the baseline memory regime,
isotropic process noise, coupling `0.18`, one eight-trillion-trajectory pilot,
and seven log-scale amplitudes from `0` through `0.00075`. The root
`SeedSequence` is `20260918`. For each amplitude it forms one exact screening
population covariance by the full-trajectory diagonal congruence

\[
D_{t,j}=\exp\{\gamma(-1)^{t+j}\},
\qquad \Gamma^1=D\Gamma^0D.
\]

This transformation is invertible, time-local, and coordinatewise. Gaussian
mutual information, conditional mutual information, canonical correlations,
the population score arrays, and the optimal path are therefore unchanged.
The script recomputes all local and transport factors after each congruence and
requires agreement within `1e-10`; the committed maximum absolute difference
is `1.9984e-15`.
The exact candidate-block drift radii are computed from \(\Gamma^0\) and
\(\Gamma^1\), then supplied as the independently declared input to Proposition
39. Each drift level receives 64 independent full-trajectory Wishart draws at
300 million trajectories.

Every draw records current-population covariance coverage, complete score
coverage, radius validity, path retention, stationary and drift-robust radii,
and both retained graph fractions. The stationary calculation is a diagnostic
in the old population metric, not a claimed guarantee after drift. Because the
exact population envelope is used, this experiment audits propagation given a
correct envelope; it does not test how an application should estimate one.

### Statistically calibrated drift comparison

`calibrated_drift_comparison.py` fixes the Experiment Y baseline at log-scale
amplitude `0.00010`, whose exact maximum candidate-block drift is
`0.000325463`. It draws one old-population reference from eight trillion
complete trajectories. For each of ten current calibration sizes from 300
million through eight trillion, it then draws 64 independent calibration and
screening pairs; every screening covariance uses 300 million trajectories. The
root `SeedSequence` is `20260924`.

The calibrated-drift method divides a requested 2.5% failure budget equally
between the old-reference and current-calibration simultaneous Wishart events.
It estimates the Proposition 40 envelope, passes it through Proposition 39,
and records the complete screen. Two paired controls use the exact population
drift and use the current calibration covariance directly as a refreshed
Proposition 38 reference. The exact drift appears only in the oracle control
and in coverage auditing; neither implementable method receives it.

Recorded events are estimated-drift coverage, current-population covariance
coverage, complete score coverage, valid-radius status, and population-path
retention. The study compares radius and graph size rather than recovery rate,
because all three screens are sufficient screens and retain the population path
on every recorded draw.

### Separably dependent Gaussian calibration

`dependent_gaussian_calibration.py` tests the first concentration result in the
repository that permits dependence across the sample index. Each trial draws a
known-zero-mean Gaussian matrix (Y\in\mathbb R^{N\times d}) with

\[
\operatorname{Cov}(Y_i,Y_j)=R_{ij}I_d,
\qquad R_{ij}=\phi^{|i-j|}.
\]

The construction is an exact stationary AR(1) process. The committed run fixes
(N=50{,}000), (d=10), one candidate block, confidence `0.975`, root
`SeedSequence` value `20260927`, and 128 independent trials at each

\[
\phi\in\{0,0.25,0.50,0.70,0.85,0.93,0.97\}.
\]

The population covariance is exactly (I_d). Each trial records the operator
norm of the uncentered empirical covariance error and compares the i.i.d.
Wishart radius with the Proposition 41 radius based on

\[
N_F=\frac{N^2}{\lVert R\rVert_F^2},
\qquad
N_{\mathrm{op}}=\frac{N}{\lVert R\rVert_2}.
\]

The Frobenius norm is evaluated exactly for the Toeplitz AR(1) matrix; the
spectral norm uses the valid row-sum envelope

\[
\min\left\{N,\frac{1+|\phi|}{1-|\phi|}\right\}.
\]

The i.i.d. curve is a diagnostic comparator and is guaranteed only at
(\phi=0). Exact population covariance is used solely to audit coverage. The
experiment assumes a known zero mean, known common AR(1) coefficient, exact
separability (R\otimes I_d), and one fixed block. It does not validate
same-sample mean centering, estimated temporal correlation, nonseparable
multivariate dependence, adaptive block selection, or arbitrary overlapping
windows from a single dynamical record.

## 5. Exchangeable identifiability counterexample

The fourth experiment uses four independent, identically distributed Gaussian
coordinates with \(A=0.5I\) and \(Q=0.2I\). Every coordinate permutation leaves
the full trajectory law unchanged. All two-node candidates therefore have
symmetry-related scores. With transport weight `0.25` and continuity weight
`0.08`, multiple constant paths tie and the exact labeled-path margin is zero.
This checks the distinction between returning one representative and identifying
a unique physical boundary.

## 6. Symbolic moving-clique experiment

The fifth experiment sets \(\Sigma_0=I\), \(\alpha=0.2\), \(\beta=0.3\), and
\(Q_t=I-A_tA_t^\mathsf T\) on a five-node system with a moving two-node clique.
It ranks all ten two-node candidates at three times. Transport and continuity
weights are `0.02` and `0.01`, chosen so the symbolic sufficient condition is
satisfied. Consecutive planted boundaries overlap in one node, which enters the
bound through their exact Jaccard distance. The experiment compares the
theorem's closed-form score and margin lower bound against the general covariance
implementation and exact dynamic program; it does not fit any parameter.
The generated recovery-region figure scans 81 self-memory values and 91 internal
couplings. Gray cells violate the transition stability condition, and the black
zero contour separates positive from nonpositive theorem margins. The negative
side is not interpreted as a necessary failure region.

## 7. Perturbed symbolic recovery experiment

The sixth experiment keeps the five-node, two-node, three-time construction and
adds two deterministic perturbations at every time:

- a cross-boundary transition matrix scaled to spectral norm `1e-5`
- an anisotropic diagonal noise perturbation scaled to spectral norm `1e-6`

The transition direction is fixed by node and time indices, so the result is
fully reproducible and uses no fitted parameter. The process covariance is
checked for positive definiteness. Actual state covariances are propagated from
the identity, and all local and transport scores are recomputed from the
resulting adjacent covariances.

The theorem check has two parts. First, the exact dynamic program must recover
the planted path with a margin no smaller than the symbolic lower bound. Second,
at least one incorrect candidate must acquire positive integration, while all
incorrect scores remain below the theorem's uniform upper bound. The associated
figure scans 110 logarithmically spaced transition radii and 110 noise radii.
The zero contour separates positive and nonpositive sufficient margins, not
empirical success and failure.

A second certificate uses the same realized matrices but compresses each
adjacent-covariance error to the coordinates required by a particular score.
It enumerates every two-node candidate and records its overlap with the planted
pair. The test verifies every planted lower bound and every incorrect upper
bound against the directly computed scores. This comparison is fixed before
inspection of the numerical margin; no parameter is tuned to improve the
localized result.

The third certificate is given only the transition and noise perturbation
matrices relative to the base family. It does not receive or propagate the
actual state covariance. Its global scalar recursion, row-local transition
norms, and compressed forcing matrices must upper bound every realized
candidate block. A separate deterministic random test repeats this containment
and the resulting score inequalities for eight dense perturbation sequences.

The fourth certificate receives only global radii and three tables indexed by
candidate-planted overlap: row-transition, within-candidate transition, and
local-noise budgets. For this finite audit, the tables are formed by exhaustive
maximization so that their relation to every matrix-level candidate can be
tested directly. The certificate itself neither receives perturbation matrices
nor constructs candidates. A separate occupancy test compares every feasible
consecutive overlap pair with exhaustive enumeration on a seven-node,
three-member system.

The fifth certificate starts from entry-magnitude and row/column-degree
envelopes for the four planted-inside/outside perturbation blocks. A
two-by-two comparison matrix converts them to all required global and local
operator-norm budgets. Random sparse matrices are used only for containment
tests. The large deterministic example supplies the structural envelopes
directly and evaluates six classes representing more than eight trillion
candidates without constructing a perturbation matrix or candidate subset.

The sixth certificate uses a fixed eight-block line graph. A single forcing
term is placed at block seven and the reported local joint bound is evaluated
at block zero. The global covariance bound responds at time one. The local
bound remains exactly zero through time six and becomes positive at time seven,
matching the graph distance. A separate random-matrix test verifies every
state block and a mixed present/future joint compression against direct matrix
propagation.

## 8. What the figures show

`worldtube_baseline.png` displays local fixed-boundary scores for the twelve
candidates with the largest maximum score across time. Cyan outlines mark the
candidate selected by the full path objective. Because the heat map shows local
scores while the outline comes from the full action, it should not be read as a
plot of the action itself.

`worldtube_phase_diagram.png` records the fraction of the five planted
boundaries recovered at each pair of regularization weights. The abrupt loss of
recovery at large continuity weight is expected: sufficiently strong Jaccard
penalization favors retaining physical members even when the active module has
moved.

`finite_sample_benchmark.png` shows recovery from estimated covariances and
includes Wilson intervals for exact-path recovery. Overlapping bands should not
be interpreted as pairwise significance tests.

`perturbed_recovery_region.png` shows the Proposition 19 lower bound as a
function of two operator-norm radii. Its logarithmic axes resolve the small
certified neighborhood created by the zero-factor cube-root term.

`gaussian_screen_calibration.png` places empirical coverage beside retained
state and edge fractions. The first panel must be interpreted with the reported
Wilson intervals; the second shows screen usefulness, not coverage.

`structural_null_screen.png` compares the generic and structural-null local
score radii on a logarithmic scale, then reports retained state and edge
fractions on a common percentage scale. Its footer records the model-derived
null-mask premise and population-path retention.

`trajectory_coupled_screen_calibration.png` shows simultaneous coverage under
the shared-trajectory construction, the generic and null-aware graph fractions,
and the cross-time variance-error correlation audit. In the correlation panel,
the empirical upper triangle and theoretical lower triangle are intentionally
kept separate so agreement and Monte Carlo noise remain visible.

`multi_regime_coupled_calibration.png` aligns three heat maps on the same
18-cell parameter grid: exact population action margin, null-aware state
fraction, and null-aware edge fraction. The shared axes make it possible to see
that a larger population margin need not imply a sharper finite-sample screen
when conditioning simultaneously worsens.

`relative_covariance_calibration.png` places absolute and relative state and
edge retention on four heat maps with a common zero-to-100-percent scale. All
four panels use paired draws and the same regime ordering. The constant right
panels are a recorded result of this grid, not a plotting normalization.

`cross_fitted_relative_calibration.png` compares fixed and pilot-adaptive
relative screens at the lower 300-million screening size. All four heat maps
share a zero-to-100-percent scale. The footer states the separate pilot and
screening sample counts, the mean radius ratio, and the minimum recorded
coverage so the gain cannot be mistaken for an equal-budget comparison.

`drift_robust_relative_calibration.png` plots the maximum stationary and
drift-robust radii, the retained state and edge fractions, all three recorded
event frequencies, and the additive certificate radius charged for drift. The
horizontal axis is the maximum candidate-block \(100\rho\), not the input
log-scale amplitude, so it reports the covariance quantity used by the theorem.

`calibrated_drift_comparison.png` uses a logarithmic calibration-sample axis.
Its panels show convergence of the estimated drift envelope, maximum final
radius, retained states, and retained edges for the oracle, calibrated-drift,
and refreshed-reference screens. All graph panels use identical candidates,
scores, screening draws, structural-null masks, and action weights.

`dependent_gaussian_calibration.png` shows how increasing AR(1) dependence
reduces both effective sample sizes, increases the empirical covariance error,
and invalidates use of the i.i.d. radius. The final panel compares analytical
radii with the empirical 95th percentile so coverage and conservatism remain
visible together.

## 9. Tests tied to scientific claims

| Test | Property checked |
| --- | --- |
| `test_covariance_propagation_matches_recursion` | The implemented nonstationary covariance follows the analytical recursion |
| `test_canonical_correlations_are_block_coordinate_invariant` | Transport persistence survives invertible basis changes within source and target |
| `test_environmental_drive_reduces_transport_independence` | Added external drive increases leakage and lowers insulation |
| `test_static_correlation_is_not_mistaken_for_directed_integration` | Common correlated noise does not create directed integration |
| `test_certificate_finds_exact_runner_up_and_positive_radius` | The two-best dynamic program agrees with hand-enumerated path scores |
| `test_perturbation_below_certificate_radius_preserves_path` | A bounded perturbation inside the certificate leaves the optimum unchanged |
| `test_positive_componentwise_margins_imply_planted_optimum` | Positive component margins imply the planted global optimum |
| `test_componentwise_condition_can_fail_when_path_is_still_optimal` | The sufficient recovery condition is not presented as necessary |
| `test_finite_sample_bound_has_correct_threshold` | The path-level sampling error budget has the derived coefficient |
| `test_cmi_covariance_error_bound_covers_direct_perturbation` | The analytical Gaussian CMI bound covers a direct covariance perturbation |
| `test_canonical_persistence_bound_covers_direct_perturbation` | The canonical-persistence bound covers a direct joint-covariance perturbation |
| `test_relative_information_and_persistence_bounds_cover_direct_perturbation` | Relative-event CMI and canonical-persistence bounds cover a direct covariance perturbation |
| `test_relative_null_bound_covers_conditional_independence_perturbation` | The Schur-complement null bound covers a perturbed exact conditional-independence model |
| `test_relative_wishart_radius_and_screen_are_condition_number_free` | The relative radius contracts with sample size and the screen requires no population spectral envelope |
| `test_pilot_sandwich_composition_covers_screening_covariance` | Two relative Loewner sandwiches compose to the stated observable pilot radius |
| `test_cross_fitted_screen_covers_scores_and_retains_population_path` | The public pilot-normalized entry point covers candidate blocks and retains the population path on fixed draws |
| `test_cross_fitted_screen_rejects_mismatched_covariance_sequences` | Pilot and screening covariance sequences cannot be silently misaligned |
| `test_three_sandwich_composition_covers_drifted_screening_covariance` | Pilot, observed, and population-drift Loewner sandwiches compose into the current-population radius |
| `test_drift_robust_screen_covers_scores_and_retains_population_path` | The public drift-aware entry point covers a fixed drifted draw and retains the population path |
| `test_drift_robust_screen_rejects_invalid_drift_envelope` | A drift radius at the singular boundary cannot be passed as a valid guarantee |
| `test_calibrated_drift_composition_is_sharp_in_one_dimension` | The two-cohort drift formula is attained by a scalar Loewner construction |
| `test_calibrated_population_drift_bound_covers_known_change` | The public calibrated envelope covers a fixed known population change |
| `test_calibrated_drift_screen_covers_scores_and_retains_path` | The end-to-end confidence-budgeted screen covers the current population and retains its path |
| `test_calibrated_drift_rejects_invalid_confidence` | An impossible confidence request is rejected at the public entry point |
| `test_ar1_temporal_norm_envelope_matches_explicit_matrix` | The closed-form AR(1) Frobenius norm equals the explicit Toeplitz calculation and its spectral envelope is valid |
| `test_dependent_relative_radius_covers_seeded_ar1_covariance` | The dependence-aware radius contains a seeded AR(1) Gaussian covariance error |
| `test_dependent_screen_covers_scores_and_retains_population_path` | The public dependent-sample screen propagates covariance control through complete scores and retains the reference path |
| `test_temporal_dependence_reduces_effective_sample_size_and_inflates_radius` | Stronger declared correlation lowers effective sample sizes and widens the analytical radius |
| `test_end_to_end_gaussian_bound_improves_with_sample_size` | The complete Gaussian guarantee contracts with sample size and its integer threshold is minimal |
| `test_positive_factor_bound_improves_on_zero_safe_holder_bound` | Positive factor floors produce a valid bound sharper than zero-safe Hölder continuity |
| `test_localized_gaussian_certificate_has_minimal_threshold` | The localized certificate changes from failure to success at the returned integer threshold |
| `test_linear_gaussian_parameters_produce_recovery_certificate` | Linear transition and noise parameters generate the planted-path certificate directly |
| `test_path_equivalence_is_computed_over_permutation_orbits` | Relabeled paths are compared as symmetry orbits rather than raw labels |
| `test_identical_observation_laws_limit_two_point_recovery_to_one_half` | Incompatible boundaries under identical laws have maximin success at most one half |
| `test_exchangeable_dynamics_do_not_select_a_unique_boundary` | Fully exchangeable dynamics produce zero labeled-path margin |
| `test_closed_form_moving_clique_score_matches_covariance_calculation` | Closed-form integration, persistence, and score equal the general covariance calculation |
| `test_symbolic_margin_guarantees_moving_clique_path` | The planted path is recovered and its exact margin exceeds the symbolic lower bound |
| `test_near_competitor_screen_removes_paths_below_robust_lower_action` | Forward-backward screening removes every state and edge below the robust winner lower action |
| `test_perturbed_generator_has_requested_norms_and_nonzero_external_entries` | The construction has the requested spectral radii, cross-boundary support, and positive process covariance |
| `test_perturbed_symbolic_margin_guarantees_numerical_path` | Positive incorrect scores remain bounded and the exact perturbed path margin exceeds the theorem's lower bound |
| `test_perturbed_bound_rejects_nonfinite_radius_and_extends_certified_radius` | Invalid radii are rejected, the quadratic bound certifies `1e-4`, and a larger unresolved radius remains inconclusive |
| `test_perturbed_factor_bounds_cover_random_dense_directions` | Covariance and local-score bounds cover twelve reproducible dense perturbation sequences |
| `test_support_resolved_bound_covers_scores_and_improves_global_margin` | Every candidate-local bound covers its computed score and the resolved action margin improves on the global bound |
| `test_support_resolved_bound_rejects_indefinite_noise` | The parameter-level certificate rejects an invalid process covariance |
| `test_a_priori_support_bound_is_nested_and_nonvacuous` | A priori block radii contain realized radii, retain a positive margin, and support a declared reduced family |
| `test_a_priori_support_bounds_cover_random_dense_perturbations` | State, joint-covariance, and score bounds cover eight reproducible dense perturbation sequences |
| `test_a_priori_support_bound_rejects_invalid_model_or_family` | The certificate rejects missing planted boundaries and nonpositive process noise |
| `test_overlap_class_occupancy_matches_exhaustive_candidates` | The integer occupancy criterion gives exactly the consecutive overlap pairs found by enumeration |
| `test_overlap_class_bound_dominates_every_candidate_certificate` | Every matrix-level candidate radius and incorrect-score bound lies below its overlap-class counterpart |
| `test_overlap_class_bound_rejects_inconsistent_local_budgets` | Local class budgets inconsistent with their global radii are rejected |
| `test_overlap_class_bound_scales_without_candidate_construction` | An 8,250,291,250,200-candidate family is represented by six overlap classes without constructing its subsets |
| `test_block_sparse_budgets_cover_every_matrix_compression` | Derived structural budgets contain every global, row-local, and candidate-local norm of random sparse perturbations |
| `test_block_sparse_structural_certificate_is_direct_and_nonvacuous` | Entry and degree envelopes alone produce a positive complete-family recovery certificate |
| `test_block_sparse_budget_validation_rejects_fractional_degrees` | Structural support degrees must be nonnegative integers |
| `test_block_covariance_envelope_covers_exact_matrix_recursion` | Every blockwise state and mixed adjacent-joint bound contains direct matrix propagation |
| `test_block_covariance_envelope_has_finite_graph_influence_speed` | Remote forcing cannot enter a local joint bound before a time-respecting graph path reaches it |
| `test_block_covariance_envelope_rejects_invalid_comparisons` | Negative comparison entries are rejected |
| `test_moving_partition_envelope_covers_exact_matrix_recursion` | Rectangular block comparisons cover exact propagation across changing partitions and block counts |
| `test_moving_partition_envelope_has_layered_influence_speed` | A forcing block remains excluded until its layered path reaches the observed block |
| `test_moving_partition_envelope_rejects_misaligned_layers` | Consecutive rectangular comparison layers must have conformable block counts |
| `test_covariance_radius_certificate_recovers_separated_path` | Candidate-local covariance radii propagate through every score factor to a positive robust path slack |
| `test_moving_envelope_propagates_through_scores_and_path_certificate` | Moving-envelope joint radii exactly equal those consumed by the path certificate |
| `test_covariance_radius_certificate_marks_invalid_spectral_regime` | A covariance radius at the eigenvalue floor cannot produce a valid recovery guarantee |
| `test_class_dynamic_program_matches_exhaustive_class_paths` | The mismatch-state class dynamic program equals exhaustive class-path maximization |
| `test_overlap_multiplicities_scale_without_candidate_construction` | Six overlap classes represent all five-node candidates and their implicit paths on 1,000 nodes |
| `test_class_certificate_requires_singleton_planted_classes` | A non-singleton planted class cannot certify a unique candidate path |
| `test_class_certificate_checks_transport_spectral_regime_separately` | Invalid edge covariance radii cannot be hidden by valid local-state radii |
| `test_interval_class_certificate_contains_random_heterogeneous_members` | Random member factors and perturbations inside every declared box remain between the certified planted and competitor actions |
| `test_wider_factor_intervals_cannot_improve_recovery_slack` | Enlarging admissible heterogeneity cannot strengthen the sufficient margin |
| `test_negative_transport_weight_reverses_interval_endpoints` | A negative transport weight uses the upper endpoint in the planted lower action |
| `test_interval_class_certificate_rejects_reversed_bounds` | A componentwise lower factor bound cannot exceed its upper bound |
| `test_residual_wrapper_matches_direct_interval_certificate` | Residual-derived factor boxes reproduce the corresponding direct interval certificate |
| `test_larger_covariance_residuals_cannot_improve_recovery_slack` | Increasing certified class heterogeneity cannot strengthen the sufficient margin |
| `test_residual_wrapper_rejects_radius_at_representative_eigenvalue_floor` | A residual that destroys the representative spectral floor is rejected |
| `test_structured_residuals_equal_direct_block_compressions` | Class residual arrays equal direct spectral norms of the selected moving-block comparisons |
| `test_structured_wrapper_matches_explicit_residual_composition` | The structural wrapper exactly composes with the independently tested residual-level API |
| `test_structured_wrapper_rejects_invalid_class_block_selection` | Future class selections cannot reference blocks outside their time layer |
| `test_screened_residuals_equal_source_specific_joint_compressions` | Local and ordered edge residuals equal their declared source-specific block compressions |
| `test_omitted_leakage_tail_has_exact_insulation_multiplier` | The conditional-information tail produces the exact exponential lower correction to insulation |
| `test_screened_certificate_rejects_negative_omitted_leakage` | Omitted conditional information cannot have a negative upper bound |
| `test_sample_split_bound_reports_stagewise_and_combined_confidence` | Wishart radius and product confidence agree with the stated independent-stage calculation |
| `test_same_data_refuses_sample_split_guarantee` | Reusing observations across selection and certification cannot produce a sample-split guarantee |
| `test_screening_reduction_and_more_samples_tighten_certification_radius` | Fewer retained blocks and more certification observations reduce the covariance radius |
| `test_minimum_sample_split_size_is_first_certified_integer` | The returned certification threshold is the first integer satisfying the strict radius condition |
| `test_safe_screen_contains_every_sampled_second_split_winner` | Every randomized later winner inside the two-stage error box remains in the first-split graph |
| `test_more_screening_samples_tighten_errors_and_cannot_expand_screen` | Increasing the first-split sample count tightens every radius and cannot enlarge the retained graph |
| `test_invalid_perturbation_regime_is_reported_without_false_guarantee` | Crossing an eigenvalue floor produces unit zero-safe score errors and no screening guarantee |
| `test_safe_screen_rejects_malformed_certification_budget` | Stage-two error arrays must match the state and edge score shapes exactly |
| `test_positive_factor_refinement_is_no_wider_than_zero_safe_bound` | Every positive-factor score radius and retained graph is no larger than its zero-safe counterpart |
| `test_factor_aware_screen_contains_randomized_later_winners` | Random factor perturbations and later score errors preserve winner containment in the refined graph |
| `test_zero_factor_uses_zero_safe_fallback` | A vanishing factor disables the local Lipschitz refinement at that entry without disabling safety |
| `test_factor_aware_screen_rejects_factors_outside_unit_interval` | Empirical primitive factors must remain inside their mathematical range |
| `test_calibration_problem_has_declared_population_path` | The calibration model, candidate family, spectra, and exact maximizing path match the documented construction |
| `test_calibration_trial_is_reproducible_and_in_range` | A fixed Wishart seed reproduces all trial statistics and maintains valid fractions |
| `test_calibration_aggregation_preserves_events_and_means` | Event rates, Wilson intervals, means, and standard errors are aggregated without changing their meanings |
| `test_structural_null_mask_separates_exact_zeros_from_memory_effects` | The model-specific mask separates exact conditional-cross-covariance zeros from weak positive covariance-memory effects |
| `test_quadratic_null_cmi_bound_contains_random_covariance_perturbations` | The structural-null CMI radius contains randomized admissible covariance perturbations |
| `test_null_cmi_bound_is_quadratic_near_zero` | Halving a sufficiently small covariance radius reduces the boundary CMI bound by the expected factor of four |
| `test_structural_null_screen_reduces_graph_and_retains_population_path` | The null-aware screen tightens the committed graph without removing the population optimizer |
| `test_false_structural_null_can_understate_score_error` | A false null declaration can produce an invalidly small score radius even when the empirical integration factor is zero |
| `test_simulated_covariance_converges_to_population_covariance` | Ensemble covariance estimates approach the analytical joint covariance |
| `test_full_trajectory_covariance_contains_every_adjacent_joint` | Every adjacent principal block of the complete trajectory covariance equals the direct two-time construction |
| `test_full_trajectory_covariance_rejects_incompatible_dimensions` | A malformed nonstationary sequence cannot silently produce a trajectory covariance |
| `test_complete_trajectory_covariance_reproduces_population_adjacent_blocks` | The calibration's 42-dimensional covariance contains all five declared population marginals |
| `test_coupled_trial_is_reproducible_and_covers_both_screens` | A fixed coupled Wishart seed reproduces the audit and satisfies the declared coverage events |
| `test_gaussian_sample_variance_error_correlation_formula` | Monte Carlo covariance errors agree with the exact Gaussian cross-time correlation formula |
| `test_baseline_parameterized_system_reproduces_original_problem` | The baseline cell of the new grid reproduces every adjacent covariance in the original calibration model |
| `test_declared_regime_grid_has_three_independent_axes` | The fixed grid contains exactly three memory, three coupling, and two conditioning levels |
| `test_small_regime_run_is_reproducible_and_well_formed` | A seeded multi-regime cell is reproducible and reports valid coverage and graph statistics |

## 10. Known weaknesses of the current experiment

The moving example is a proof of implementation, not a demanding benchmark.
Its limitations are concrete:

1. Ground truth is encoded directly in the transition matrices.
2. The population figure uses exact covariances; the sampled benchmark covers
   only one estimator and one ridge value.
3. Candidate size is fixed and supplied in advance.
4. The active module moves smoothly with two of three members retained.
5. There are no latent confounders, missing observations, or nonlinearities.
6. Hyperparameters are scanned against the same construction used for display.
7. The comparisons are internal baselines rather than complete external methods.
8. The full transport objective is less sample-efficient than local-only
   selection on the current easy construction.
9. The localized analytical threshold remains roughly ten orders of magnitude
   above the empirical recovery scale.
10. The support-resolved theorem uses candidate overlap and perturbation
    location, but requires the realized matrices and exhaustive fixed-size
    candidate enumeration.
11. The a priori matrix-level theorem still uses the full perturbation
    matrices and a global scalar error for influence arriving through
    unselected coordinates.
12. The overlap-class theorem removes matrices and candidate enumeration from
    certificate evaluation, but obtaining rigorous class budgets from a
    general unstructured model can itself require exhaustive work.
13. The block-sparse theorem obtains those budgets analytically, but discards
    signs, cancellation, exact support geometry, and dependencies among blocks.
14. The moving-partition covariance theorem avoids common refinement, but it
    still assumes valid block-norm comparisons are supplied at every layer.
15. The moving-partition recovery example uses deliberately separated
    population factors and does not measure sharpness near the robust boundary.
16. The interval-class theorem removes exact within-class factor symmetry, but
    the validity of every supplied factor interval must be established outside
    the path optimizer. Coarse intervals can make the result vacuous.
17. The residual-derived theorem constructs those intervals from covariance
    balls, but the residual radii are still assumptions that require a
    structural derivation or an independently valid statistical estimate.
18. The structural class theorem derives residuals from block comparisons but
    uses all present blocks to cover leakage. This can be conservative, and the
    representative factors and spectra remain model inputs.
19. The screened-environment theorem reduces that conservatism only when a
    valid omitted conditional-leakage bound is supplied. It is not yet a
    statistically valid procedure for selecting neighborhoods from the same
    observations used to certify them.
20. The Gaussian first-split theorem derives the advertised safety probability,
    but its simultaneous zero-safe score radii can be highly conservative.
    Experiments S through X broaden calibration but do not establish sharpness
    outside their declared models.
21. The absolute first-split spectral floors and ceilings are deterministic population
    assumptions. Estimating them from the same data without an additional
    confidence argument would invalidate the stated guarantee.
22. The positive-factor refinement is sharp only relative to the current
    componentwise factor radii. It does not use covariance direction, factor
    dependence, or cancellation between score components.
23. The screening calibration has 64 trials per sample count. Zero observed
    failures therefore gives a Wilson 95% lower endpoint of only `0.943376`,
    which is below the nominal `0.975` confidence. It is compatible with the
    theorem but cannot empirically validate a 2.5% tail probability precisely.
24. Experiment S uses independent timewise Wishart draws and therefore omits
    cross-time dependence. Experiment U restores the exact dependence for an
    ensemble of independent complete Gaussian trajectories, and Experiment V
    varies three population axes. None covers overlapping windows cut from one
    long dependent record.
25. Structural-null screening is valid only when each declared integration null
    is exact and its mask is fixed independently of the screening observations.
    A small empirical score is not sufficient evidence for that declaration.
    The corrected mask is specific to the controlled moving-module model.
26. Experiment V changes memory, coupling, and diagonal-noise conditioning but
    retains the same smooth boundary motion, fixed candidate family, spectral
    radius, action weights, Gaussian law, and exact population spectra. Its
    64 trials per cell have limited power to measure rare failure probabilities.
27. Proposition 37 and Experiment W remove the absolute certificate's global
    eigenvalue-floor penalty, but retain Gaussianity, a fixed candidate family,
    independent complete trajectories, and the independently justified null
    mask. Population whitening defines the proof event; it is not an estimated
    preprocessing step licensed for reuse on the same observations.
28. Proposition 38 and Experiment X use a much larger reusable pilot than each
    screening cohort. The smaller graph is an adaptive-radius result, not an
    equal-total-sample comparison.
29. Proposition 39 assumes that every declared candidate-block drift radius is
    valid. Experiment Y computes that envelope from exact population
    covariances and therefore does not solve drift estimation. Its congruence
    construction deliberately preserves the score and path; it does not test
    structural change, coordinate mismatch, non-Gaussian shift, or dependent
    pilot and screening windows. The complete graph at larger displayed drift
    is a recorded loss of selectivity, not evidence of failed recovery.
30. Proposition 40 supplies a statistical drift envelope only under the same
    fixed-block Gaussian sampling model. Experiment Z uses independent
    calibration and screening trajectories and does not address overlapping
    windows. Its refreshed-reference advantage is empirical for one controlled
    drift family, not a universal theorem. The oracle curve is not an
    implementable competitor because it receives exact population drift.
31. Proposition 41 assumes a known zero mean and exact separable Gaussian
    covariance (R\otimes\Gamma), with valid deterministic bounds on
    \(\lVert R\rVert_F\) and \(\lVert R\rVert_2\). Experiment AA tests only one
    fixed identity-covariance block under a known stationary AR(1) law. Its 128
    trials per correlation level have limited tail resolution and do not cover
    estimated means, estimated dependence, nonseparable space-time covariance,
    or general sliding-window constructions.

A stronger benchmark should vary coupling, noise, overlap, speed, candidate
size, observation length, latent drive, and model misspecification. It should
choose weights on separate training systems and evaluate them on held-out
generative families.

## 11. Reproduction commands

From the repository root:

```bash
python -m pip install -e ".[dev,viz]"
python examples/baseline_experiment.py
python examples/worldtube_experiment.py
python examples/finite_sample_benchmark.py --trials 32 --jobs 6
python examples/identifiability_counterexample.py
python examples/symbolic_recovery_experiment.py
python examples/perturbed_symbolic_recovery_experiment.py
python examples/block_sparse_recovery_experiment.py
python examples/localized_influence_cone_experiment.py
python examples/moving_partition_influence_experiment.py
python examples/moving_partition_recovery_experiment.py
python examples/class_compressed_recovery_experiment.py
python examples/heterogeneous_class_recovery_experiment.py
python examples/residual_derived_class_recovery_experiment.py
python examples/structured_residual_class_recovery_experiment.py
python examples/screened_environment_recovery_experiment.py
python examples/sample_split_screening_experiment.py
python examples/gaussian_safe_screen_experiment.py
python examples/factor_aware_screen_experiment.py
python examples/gaussian_screen_calibration.py --trials 64 --jobs 6
python examples/structural_null_screen_experiment.py
python examples/trajectory_coupled_screen_calibration.py --trials 128 --jobs 6
python examples/multi_regime_coupled_calibration.py --trials 64 --jobs 6
python examples/relative_covariance_calibration.py --trials 64 --jobs 6
python examples/cross_fitted_relative_calibration.py --trials 64 --jobs 6
python examples/drift_robust_relative_calibration.py --trials 64 --jobs 6
python examples/calibrated_drift_comparison.py --trials 64 --jobs 6
python examples/dependent_gaussian_calibration.py --trials 128 --jobs 6
python -m pytest
python -m ruff check .
```

Each committed figure is regenerated by its corresponding experiment script so
that the plotted result can be traced to the current code.
