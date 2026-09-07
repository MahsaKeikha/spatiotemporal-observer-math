# Experimental protocol

This document describes the five committed experiments closely enough to rebuild
them without guessing from the figures.

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
| `test_simulated_covariance_converges_to_population_covariance` | Ensemble covariance estimates approach the analytical joint covariance |

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
python -m pytest
python -m ruff check .
```

Each committed figure is regenerated by its corresponding experiment script so
that the plotted result can be traced to the current code.
