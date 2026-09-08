# API guide

The package is small enough that the public surface can be listed directly.
Arrays are NumPy-compatible, node indices are zero based, and information
quantities are returned in bits.

## Stationary Gaussian helpers

```python
from observer_math.gaussian import stationary_covariance, two_time_covariance

sigma = stationary_covariance(transition, noise_covariance)
joint = two_time_covariance(transition, noise_covariance, lag=1)
```

`stationary_covariance` requires spectral radius below one and solves
\(\Sigma=A\Sigma A^\mathsf T+Q\). `two_time_covariance` returns the covariance
of the stacked vector \([X_t,X_{t+\tau}]\).

## Information quantities

```python
from observer_math.gaussian import (
    canonical_correlations,
    gaussian_conditional_mutual_information,
    gaussian_mutual_information,
)

mi = gaussian_mutual_information(covariance, x=(0, 1), y=(2,))
cmi = gaussian_conditional_mutual_information(
    covariance, x=(0,), y=(1,), given=(2,)
)
rhos = canonical_correlations(source_covariance, target_covariance, cross_covariance)
```

Indices refer to positions in the supplied joint covariance. Empty \(X\) or
\(Y\) sets return zero mutual information. Covariances are symmetrized for
numerical evaluation and must be finite square matrices.

## Fixed-boundary metrics

```python
from observer_math import observer_metrics

metrics = observer_metrics(transition, noise_covariance, subset=(0, 1, 2))
print(metrics.observer_score)
print(metrics.weakest_partition)
```

This convenience function assumes stationary dynamics. For a time-varying
system, supply the present and adjacent-time covariances explicitly:

```python
from observer_math import adjacent_joint_covariance, observer_metrics_from_covariances

joint = adjacent_joint_covariance(current_covariance, transition, noise_covariance)
metrics = observer_metrics_from_covariances(
    current_covariance, joint, subset=(0, 1, 2)
)
```

## Nonstationary propagation and transport

```python
from observer_math import (
    full_trajectory_covariance,
    propagate_covariances,
    transport_metrics,
)

covariance_path = propagate_covariances(
    transitions,
    noise_covariances,
    initial_covariance,
)

trajectory_covariance = full_trajectory_covariance(
    transitions,
    noise_covariances,
    initial_covariance,
)

transport = transport_metrics(
    covariance_path[0],
    transitions[0],
    noise_covariances[0],
    source=(0, 1, 2),
    target=(1, 2, 3),
)
print(transport.persistence)
print(transport.environmental_leakage_bits_per_node)
print(transport.transport_score)
```

The covariance path has one more element than the transition sequence. If each
state has dimension `d`, `full_trajectory_covariance` returns the covariance of
the stacked vector `[X_0, ..., X_T]`, with shape `((T + 1) * d, (T + 1) * d)`.
Its off-diagonal blocks preserve the dependence between covariance estimates
formed from the same complete trajectories. Source indices in `transport_metrics`
refer to \(X_t\); target indices refer to \(X_{t+1}\).

## Exhaustive fixed-subsystem ranking

```python
from observer_math import rank_subsystems

ranking = rank_subsystems(
    transition,
    noise_covariance,
    min_size=2,
    max_size=3,
)
for candidate in ranking[:5]:
    print(candidate.rank, candidate.metrics.subset, candidate.metrics.observer_score)
```

This enumerates all requested subsets and all internal bipartitions. It is
intended for small systems.

## World-tube optimization

```python
from observer_math import certify_worldtube, optimize_worldtube

result = optimize_worldtube(
    local_scores,
    candidates,
    transport_scores=transport_scores,
    transport_weight=0.25,
    continuity_weight=0.08,
)

certificate = certify_worldtube(
    local_scores,
    candidates,
    transport_scores=transport_scores,
    transport_weight=0.25,
    continuity_weight=0.08,
)
```

Expected shapes are:

- `local_scores`: `(time_count, candidate_count)`
- `transport_scores`: `(time_count - 1, candidate_count, candidate_count)`
- `candidates`: a sequence of node-index sequences

`WorldTubeResult` contains the selected path and the decomposition of its total
action. `WorldTubeCertificate` adds the exact runner-up, action margin, and
uniform score-perturbation radius. The radius treats continuity distances and
both weights as exact.

## Reference model constructors

```python
from observer_math import (
    block_system,
    correlated_but_uncoupled_system,
    moving_module_systems,
    ring_system,
)
```

These functions construct small deterministic systems for tests and examples.
They are not empirical models.

## Sampling and empirical covariances

```python
import numpy as np

from observer_math import adjacent_sample_covariances, simulate_gaussian_ensemble

states = simulate_gaussian_ensemble(
    transitions,
    noise_covariances,
    initial_covariance,
    sample_count=320,
    rng=np.random.default_rng(7),
)
present, joint = adjacent_sample_covariances(states[0], states[1], ridge=1e-5)
```

The simulator returns independent trajectories rather than one long dependent
time series. `adjacent_sample_covariances` preserves consistency by taking the
present covariance as the leading principal block of the regularized joint
covariance.

Empirical transport is evaluated without supplying \(A_t\) or \(Q_t\):

```python
from observer_math import transport_metrics_from_covariances

metrics = transport_metrics_from_covariances(
    present,
    joint,
    source=(0, 1, 2),
    target=(1, 2, 3),
)
```

## Recovery bounds

```python
from observer_math import (
    canonical_persistence_covariance_error_bound,
    componentwise_recovery_bound,
    finite_sample_recovery_bound,
    gaussian_cmi_covariance_error_bound,
    gaussian_path_recovery_bound,
    linear_gaussian_localized_recovery_bound,
    localized_gaussian_path_recovery_bound,
    minimum_gaussian_sample_size,
    minimum_localized_gaussian_sample_size,
    product_root_error_bound,
    screen_near_competitors,
)

population = componentwise_recovery_bound(
    local_scores,
    candidates,
    planted_indices,
    transport_scores=transport_scores,
    transport_weight=0.25,
    continuity_weight=0.08,
)

sample_bound = finite_sample_recovery_bound(
    population_action_margin=0.126,
    time_count=5,
    local_score_error=0.005,
    transport_score_error=0.005,
    transport_weight=0.25,
)

cmi_error = gaussian_cmi_covariance_error_bound(
    x_dimension=3,
    y_dimension=4,
    given_dimension=3,
    minimum_eigenvalue=0.2,
    covariance_spectral_error=0.01,
)

persistence_error = canonical_persistence_covariance_error_bound(
    minimum_eigenvalue=0.2,
    maximum_eigenvalue=1.4,
    covariance_spectral_error=0.01,
)

end_to_end = gaussian_path_recovery_bound(
    population_action_margin=0.126,
    node_count=7,
    subset_size=3,
    time_count=5,
    sample_count=640,
    minimum_joint_eigenvalue=0.086,
    maximum_joint_eigenvalue=1.125,
    confidence=0.95,
    transport_weight=0.25,
)

minimum_samples = minimum_gaussian_sample_size(
    population_action_margin=0.126,
    node_count=7,
    subset_size=3,
    time_count=5,
    minimum_joint_eigenvalue=0.086,
    maximum_joint_eigenvalue=1.125,
    confidence=0.95,
    transport_weight=0.25,
    maximum_sample_count=10**30,
)

factor_error = product_root_error_bound(
    population_factors=(0.7, 0.9, 0.8),
    factor_error_bounds=(0.01, 0.01, 0.02),
)

localized = localized_gaussian_path_recovery_bound(
    local_factors,
    transport_factors,
    candidates,
    sample_count=640,
    node_count=7,
    subset_size=3,
    minimum_block_eigenvalues=minimum_block_eigenvalues,
    maximum_block_eigenvalues=maximum_block_eigenvalues,
    confidence=0.95,
    transport_weight=0.25,
    continuity_weight=0.08,
)

parameter_level = linear_gaussian_localized_recovery_bound(
    transitions,
    noise_covariances,
    initial_covariance,
    candidates,
    sample_count=640,
    confidence=0.95,
    transport_weight=0.25,
    continuity_weight=0.08,
)

screen = screen_near_competitors(
    local_scores,
    transport_scores,
    candidates,
    local_score_errors,
    transport_score_errors,
    transport_weight=0.25,
    continuity_weight=0.08,
)
print(screen.viable_states, screen.viable_edges)
```

The functions progress from score-level checks to covariance perturbation and
then to end-to-end independent-Gaussian-ensemble guarantees. The localized
version uses candidate-specific covariance spectra, positive factor floors, and
an exact error-inflated competitor search. The parameter-level entry point
constructs these quantities directly from linear dynamics. The sample-count
searches return sufficient counts, which can remain extremely conservative.
None of these functions estimates a confidence level from observed data.

## Closed-form moving-clique theorem

```python
from observer_math import (
    covariance_preserving_moving_clique_bound,
    covariance_preserving_moving_cliques,
)

planted, systems = covariance_preserving_moving_cliques(
    node_count=5,
    module_size=2,
    step_count=3,
    self_memory=0.2,
    internal_coupling=0.3,
)
symbolic = covariance_preserving_moving_clique_bound(
    self_memory=0.2,
    internal_coupling=0.3,
    module_size=2,
    minimum_consecutive_overlap=1,
    transport_weight=0.02,
    continuity_weight=0.01,
)
print(symbolic.per_mismatch_action_margin)
```

The constructor uses \(Q_t=I-A_tA_t^\mathsf T\), which preserves unit
covariance exactly. The symbolic function evaluates Proposition 16 without
enumerating candidates. A positive `per_mismatch_action_margin` is sufficient,
not necessary, for unique planted-path recovery.

### Robust perturbation certificate

```python
from observer_math import (
    perturbed_covariance_preserving_moving_cliques,
    perturbed_moving_clique_recovery_bound,
)

planted, systems = perturbed_covariance_preserving_moving_cliques(
    node_count=5,
    module_size=2,
    step_count=3,
    self_memory=0.2,
    internal_coupling=0.3,
    external_coupling_norm=1e-5,
    noise_perturbation_norm=1e-6,
)
robust = perturbed_moving_clique_recovery_bound(
    self_memory=0.2,
    internal_coupling=0.3,
    module_size=2,
    node_count=5,
    time_count=3,
    transition_perturbation=1e-5,
    noise_perturbation=1e-6,
    minimum_consecutive_overlap=1,
    transport_weight=0.02,
    continuity_weight=0.01,
)
print(robust.guarantees_unique_planted_path)
print(robust.per_mismatch_action_margin)
```

The two perturbation arguments are upper bounds in spectral norm. Transition
perturbations may connect the planted module to its complement. Noise
perturbations may be anisotropic. The certificate assumes \(\Sigma_0=I\), a
finite horizon, equal candidate size, and the moving-clique base family. A
false value is inconclusive; it does not imply failed recovery. Proposition 18
uses the base model's zero conditional cross-covariance to obtain a quadratic
upper bound for incorrect-candidate integration. Proposition 19 propagates this
bound through the complete path action.

### Support-resolved perturbation certificate

```python
from observer_math import support_resolved_moving_clique_recovery_bound

transitions = tuple(system[0] for system in systems)
noises = tuple(system[1] for system in systems)
support = support_resolved_moving_clique_recovery_bound(
    transitions,
    noises,
    planted,
    self_memory=0.2,
    internal_coupling=0.3,
    transport_weight=0.02,
    continuity_weight=0.01,
)
print(support.maximum_incorrect_score_upper_bound)
print(support.per_mismatch_action_margin)
```

This version propagates the specified system from \(\Sigma_0=I\), restricts
the resulting covariance error to each candidate's score coordinates, and
uses the exact incident planted-edge budget at every time. It enumerates all
size-matched candidates. The fields `candidate_overlaps` and
`incorrect_score_upper_bounds`, together with the recorded covariance errors
and base eigenvalue bounds, are indexed first by time and then by the common
`candidates` tuple. The planted candidate has a zero placeholder in the
incorrect-score array because its lower bound is stored separately. A positive
guarantee is sufficient for the supplied matrices and planted path; it is not
an inference procedure for an unknown planted path.

### A priori support-aware certificate

```python
from observer_math import a_priori_support_moving_clique_recovery_bound

transition_errors = tuple(
    system[0] - base[0]
    for system, base in zip(systems, base_systems, strict=True)
)
noise_errors = tuple(
    system[1] - base[1]
    for system, base in zip(systems, base_systems, strict=True)
)
a_priori = a_priori_support_moving_clique_recovery_bound(
    transition_errors,
    noise_errors,
    planted,
    self_memory=0.2,
    internal_coupling=0.3,
    transport_weight=0.02,
    continuity_weight=0.01,
)
print(a_priori.per_mismatch_action_margin)
```

This function receives additive perturbations relative to the moving-clique
base matrices. It bounds covariance errors using row-local transition norms
and compressed forcing matrices, without propagating the actual covariance.
By default it evaluates all fixed-size subsets. Passing `candidate_family`
restricts the computation and the uniqueness claim to exactly that declared
family. The family must be fixed independently of the data used to evaluate a
statistical claim.

### Overlap-class certificate

```python
from observer_math import overlap_class_moving_clique_recovery_bound

overlap = overlap_class_moving_clique_recovery_bound(
    node_count=5,
    planted_path=planted,
    self_memory=0.2,
    internal_coupling=0.3,
    transition_perturbation_bounds=global_transition,
    noise_perturbation_bounds=global_noise,
    row_transition_perturbation_bounds=row_transition,
    within_transition_perturbation_bounds=within_transition,
    local_noise_perturbation_bounds=local_noise,
    transport_weight=0.02,
    continuity_weight=0.01,
)
print(overlap.candidate_count, overlap.overlap_class_count)
print(overlap.per_mismatch_action_margin)
```

Each local table has shape `(time_count, module_size + 1)`, with column `q`
bounding all candidates whose intersection with the planted boundary has size
`q`. The global arrays have shape `(time_count,)`. The certificate checks
feasible consecutive overlap pairs and does not construct any candidate
subsets. The caller is responsible for proving that the supplied class budgets
cover their stated maxima. `overlap_class_multiplicities` records the number of
candidates represented by each value in `overlap_values`.

### Block-sparse structural certificate

```python
import numpy as np

from observer_math import block_sparse_moving_clique_recovery_bound

entries_e = np.full((time_count, 2, 2), 1e-8)
degrees_e = np.full((time_count, 2, 2), 2, dtype=int)
entries_f = np.full((time_count, 2, 2), 1e-9)
degrees_f = np.full((time_count, 2, 2), 2, dtype=int)

structural = block_sparse_moving_clique_recovery_bound(
    node_count,
    planted,
    self_memory=0.2,
    internal_coupling=0.1,
    transition_entry_bounds=entries_e,
    transition_row_degrees=degrees_e,
    transition_column_degrees=degrees_e,
    noise_entry_bounds=entries_f,
    noise_row_degrees=degrees_f,
    noise_column_degrees=degrees_f,
    transport_weight=0.02,
    continuity_weight=0.01,
)
print(structural.recovery.per_mismatch_action_margin)
```

Every envelope array has shape `(time_count, 2, 2)`. Index zero denotes the
planted type and index one its complement; the final two axes select row and
column type. Entry arrays bound absolute entry magnitude in each block. Degree
arrays bound the number of nonzero entries in each block row or column. The
function converts these declarations into Proposition 22 budgets without
receiving a perturbation matrix. `structural.budgets` exposes the derived
radii, and `structural.recovery` contains the complete overlap-class result.

For symmetric noise perturbations, separate row and column degree arrays are
still accepted so that the structural assumptions remain explicit. A positive
certificate is conditional on the stated entry and degree envelopes being
valid for the intended model.

### Block-local covariance influence

```python
from observer_math import (
    block_covariance_error_envelope_from_perturbations,
    block_joint_covariance_error_bound,
)

envelope = block_covariance_error_envelope_from_perturbations(
    base_transition_comparisons,
    transition_perturbation_comparisons,
    noise_perturbation_comparisons,
)
local_radius = block_joint_covariance_error_bound(
    envelope,
    time=3,
    present_blocks=(0,),
    future_blocks=(0,),
)
```

Every comparison sequence has shape `(time_count, block_count, block_count)`.
An entry bounds the operator norm of the corresponding matrix block. The
recursion retains the location of covariance forcing and exposes both
blockwise state-error matrices and adjacent cross-error matrices. Unlike a
global scalar radius, an unreachable block remains exactly zero.

`block_joint_covariance_error_bound` permits different present and future
block selections. The partition is fixed over the supplied horizon; changing
partitions are handled by the separate rectangular API below. Supplying an
underestimated comparison entry invalidates the guarantee.

### Moving-partition covariance influence

```python
from observer_math import (
    moving_block_covariance_error_envelope,
    moving_block_joint_covariance_error_bound,
)

envelope = moving_block_covariance_error_envelope(
    transition_comparisons,
    forcing_comparisons,
    perturbation_comparisons,
)
local_radius = moving_block_joint_covariance_error_bound(
    envelope,
    time=2,
    present_blocks=(0,),
    future_blocks=(0, 1),
)
```

The transition and perturbation matrix at time \(t\) has shape
`(block_counts[t + 1], block_counts[t])`; its rows use the future partition
and its columns use the present partition. The forcing matrix is square on the
future partition. The number of blocks may change at every time. The returned
`block_counts`, state comparisons, and cross comparisons retain those shapes.

This API does not build a common refinement. It therefore permits explicit
split, merge, and membership-reassignment layers without exponential growth in
membership histories. The caller remains responsible for providing valid
operator-norm bounds for every time-indexed block.

### Moving-partition path recovery

```python
from observer_math import moving_partition_localized_recovery_bound

certificate = moving_partition_localized_recovery_bound(
    envelope,
    future_candidate_blocks,
    local_factors,
    transport_factors,
    candidates,
    node_count,
    subset_size,
    minimum_block_eigenvalues=minimum_eigenvalues,
    maximum_block_eigenvalues=maximum_eigenvalues,
)
print(certificate.recovery_slack)
```

`future_candidate_blocks[t][j]` lists the blocks of partition `t + 1` whose
union is candidate `j`'s future coordinate set. The function selects all
present blocks and only that future union from the moving covariance envelope.
It propagates the resulting candidate-local radius through Gaussian
information, canonical persistence, geometric score stability, and the robust
world-tube dynamic program.

For applications that already have candidate-local covariance radii, call
`covariance_radius_path_recovery_bound` directly. Both functions return the
complete covariance, local-score, and transport-score error arrays, as well as
the population path, adversarial competitor, robust slack, and sufficient
recovery decision. This is a deterministic certificate. It does not assign a
probability to the supplied perturbation envelope.

### Class-compressed path recovery

```python
from observer_math import class_compressed_covariance_path_recovery_bound

certificate = class_compressed_covariance_path_recovery_bound(
    local_factors_by_class,
    transport_factors_by_class_pair,
    class_multiplicities,
    planted_class_indices,
    feasible_class_edges,
    continuity_distance_lower_bounds,
    planted_continuity_distances,
    node_count,
    subset_size,
    covariance_spectral_errors=class_covariance_errors,
    minimum_block_eigenvalues=class_minimum_eigenvalues,
    maximum_block_eigenvalues=class_maximum_eigenvalues,
    transport_covariance_spectral_errors=class_edge_covariance_errors,
    minimum_transport_block_eigenvalues=class_edge_minimum_eigenvalues,
    maximum_transport_block_eigenvalues=class_edge_maximum_eigenvalues,
)
```

This entry point represents every candidate only through an exact equivalence
class. `local_factors_by_class[t, k]` must be constant across class `k`, and
the transport factors must be constant across every declared ordered class
pair. Local covariance arrays must bound every member of a state class, and
transport covariance arrays must separately bound every member of each ordered
class pair. This distinction is required when a candidate changes overlap
class between adjacent planted boundaries. The planted class at each time must
have multiplicity one.

`continuity_distance_lower_bounds[t, k, l]` may contain zero when no sharper
uniform lower bound is known. `feasible_class_edges` excludes impossible class
transitions. The returned adversarial class path is computed with a binary
mismatch state, ensuring that the all-planted class path is not compared
against itself.

Class multiplicities may be arbitrary Python integers. The implementation
therefore records candidate and path counts beyond fixed-width integer ranges.
Its numerical dynamic program costs \(O(TK^2)\), where \(K\) is the class
count, and does not depend on those multiplicities.

### Interval-certified class recovery

```python
from observer_math import interval_class_covariance_path_recovery_bound

certificate = interval_class_covariance_path_recovery_bound(
    local_factor_lower_bounds,
    local_factor_upper_bounds,
    transport_factor_lower_bounds,
    transport_factor_upper_bounds,
    class_multiplicities,
    planted_class_indices,
    feasible_class_edges,
    continuity_distance_lower_bounds,
    planted_continuity_distances,
    node_count,
    subset_size,
    covariance_spectral_errors=class_covariance_errors,
    minimum_block_eigenvalues=class_minimum_eigenvalues,
    maximum_block_eigenvalues=class_maximum_eigenvalues,
    transport_covariance_spectral_errors=class_edge_covariance_errors,
    minimum_transport_block_eigenvalues=class_edge_minimum_eigenvalues,
    maximum_transport_block_eigenvalues=class_edge_maximum_eigenvalues,
)
```

The local factor arrays have shape `(time, classes, 3)` and bound integration,
insulation, and persistence componentwise for every member of each class. The
transport arrays have shape `(time - 1, classes, classes, 2)` and bound the two
transport factors for every member edge of each ordered class pair. Bounds are
inclusive, finite, and lie in `[0, 1]`.

The function expands each factor interval using the supplied covariance and
spectral envelopes, then takes the appropriate geometric-mean endpoints. It
returns all factor-error arrays and score intervals, as well as the planted
lower action, adversarial competitor upper action, robust slack, and sufficient
decision. Negative transport weights are supported and reverse which endpoint
is favorable.

The guarantee is uniform over every population factor assignment inside the
declared intervals and every covariance perturbation inside the declared
envelopes. It does not prove that the intervals themselves cover a particular
model. Class multiplicities and the singleton planted-class requirement have
the same meaning as in the exact class API.

### Residual-derived class recovery

```python
from observer_math import residual_class_covariance_path_recovery_bound

result = residual_class_covariance_path_recovery_bound(
    representative_local_factors,
    representative_transport_factors,
    class_multiplicities,
    planted_class_indices,
    feasible_class_edges,
    continuity_distance_lower_bounds,
    planted_continuity_distances,
    node_count,
    subset_size,
    local_covariance_residual_bounds=local_residuals,
    representative_minimum_block_eigenvalues=local_reference_minimum,
    representative_maximum_block_eigenvalues=local_reference_maximum,
    transport_covariance_residual_bounds=edge_residuals,
    representative_minimum_transport_eigenvalues=edge_reference_minimum,
    representative_maximum_transport_eigenvalues=edge_reference_maximum,
    covariance_spectral_errors=local_observation_errors,
    transport_covariance_spectral_errors=edge_observation_errors,
)
certificate = result.recovery
```

This entry point derives the Proposition 28 factor boxes. Each residual radius
bounds the spectral distance between a representative covariance and every
population covariance represented by its state class or ordered edge class.
The observation-error arrays are separate second-stage radii around those
population members.

The returned `ResidualClassPathRecoveryBound` exposes the derived lower and
upper factor arrays, heterogeneity factor-error radii, Weyl-adjusted member
eigenvalue envelopes, and the complete interval recovery result. Residual
radii must be strictly below their representative eigenvalue floors. A valid
statistical use must establish the residual radii independently or account for
their estimation in its coverage argument.

### Block-structured residual class recovery

```python
from observer_math import structured_residual_class_path_recovery_bound

result = structured_residual_class_path_recovery_bound(
    moving_envelope,
    future_class_blocks,
    representative_local_factors,
    representative_transport_factors,
    class_multiplicities,
    planted_class_indices,
    feasible_class_edges,
    continuity_distance_lower_bounds,
    planted_continuity_distances,
    node_count,
    subset_size,
    representative_minimum_block_eigenvalues=local_reference_minimum,
    representative_maximum_block_eigenvalues=local_reference_maximum,
    representative_minimum_transport_eigenvalues=edge_reference_minimum,
    representative_maximum_transport_eigenvalues=edge_reference_maximum,
    covariance_spectral_errors=local_observation_errors,
    transport_covariance_spectral_errors=edge_observation_errors,
)
certificate = result.recovery.recovery
```

`future_class_blocks[t][k]` lists the blocks of partition `t + 1` whose union
contains the future variables used by class `k`. The function selects every
present block so environmental leakage remains covered, derives local residual
radii from the corresponding joint comparison norm, and repeats the target
class radius across incoming source classes for the transport array.

The returned object exposes both derived covariance-residual arrays and the
complete residual-derived result. The envelope can itself be constructed from
primitive transition and noise perturbation comparisons with
`moving_block_covariance_error_envelope`. The guarantee is invalid if a class
selection omits variables used by its score.

### Screened-environment structural recovery

```python
from observer_math import screened_structural_class_path_recovery_bound

result = screened_structural_class_path_recovery_bound(
    moving_envelope,
    local_present_class_blocks,
    local_future_class_blocks,
    transport_present_class_blocks,
    transport_future_class_blocks,
    screened_representative_local_factors,
    screened_representative_transport_factors,
    local_omitted_leakage_bits_per_node,
    transport_omitted_leakage_bits_per_node,
    class_multiplicities,
    planted_class_indices,
    feasible_class_edges,
    continuity_distance_lower_bounds,
    planted_continuity_distances,
    node_count,
    subset_size,
    representative_minimum_block_eigenvalues=local_reference_minimum,
    representative_maximum_block_eigenvalues=local_reference_maximum,
    representative_minimum_transport_eigenvalues=edge_reference_minimum,
    representative_maximum_transport_eigenvalues=edge_reference_maximum,
)
```

Local block selections have shape `(time, classes, blocks)`. Transport
selections have shape `(time - 1, source classes, target classes, blocks)` and
may differ for every ordered pair. Each present selection must contain every
variable used by its screened integration, leakage, and persistence factors;
each future selection must contain every target variable.

The omitted-leakage arrays are nonnegative upper bounds in bits per node. The
function multiplies the lower insulation endpoint by `2**(-tail)` using the
conditional-information chain rule. A zero tail is a substantive conditional
irrelevance claim, not a default. This API currently certifies population
heterogeneity only and intentionally applies no sampling-error radius.

### Gaussian-safe first-split screen

```python
from observer_math import gaussian_safe_near_competitor_screen

safe_screen = gaussian_safe_near_competitor_screen(
    empirical_local_scores,
    empirical_transport_scores,
    candidates,
    screening_sample_count=10_000_000,
    node_count=24,
    subset_size=2,
    minimum_block_eigenvalues=minimum_eigenvalues,
    maximum_block_eigenvalues=maximum_eigenvalues,
    certification_local_score_errors=local_certification_budget,
    certification_transport_score_errors=transport_certification_budget,
    confidence=0.975,
)
```

The empirical score arrays must be computed from the first-split covariance
estimates. The minimum and maximum eigenvalue arrays are deterministic
population envelopes with shape `(time, candidates)`. The function applies a
simultaneous Gaussian covariance bound, propagates it through the three local
factors and two transport factors, adds the declared second-stage score budget,
and calls the forward-backward screen.

`screening_local_score_errors` and `screening_transport_score_errors` contain
only the first-stage contribution. Their `total_*` counterparts include the
certification budget. `guarantees_safe_screen` is true only if every covariance
radius remains strictly below its eigenvalue floor. In that case the screen is
safe with at least `confidence` probability over the first split for every
later score realization inside the certification budget. This is a screening
statement, not by itself a final path-recovery statement.

`covariance_spectral_errors` contains the radius for every candidate-local
block, rather than only the reported maximum. It is useful for audits that
compare realized block errors with the exact envelope used by the theorem.

Transport-edge radii use the destination candidate's local spectral envelope,
uniformly over source candidates. This matches the localized recovery API and
is conservative when source-target blocks have substantially different
conditioning.

### Positive-factor Gaussian screen

```python
from observer_math import gaussian_factor_aware_near_competitor_screen

factor_aware = gaussian_factor_aware_near_competitor_screen(
    empirical_local_factors,
    empirical_transport_factors,
    candidates,
    screening_sample_count=10_000_000,
    node_count=8,
    subset_size=2,
    minimum_block_eigenvalues=minimum_eigenvalues,
    maximum_block_eigenvalues=maximum_eigenvalues,
    certification_local_score_errors=local_certification_budget,
    certification_transport_score_errors=transport_certification_budget,
    confidence=0.975,
)
```

`empirical_local_factors` has shape `(time, candidates, 3)` and stores
integration, insulation, and persistence. `empirical_transport_factors` has
shape `(time - 1, candidates, candidates, 2)` and stores insulation and
persistence. The function constructs the geometric-mean scores itself, so the
factor arrays and score centers cannot become inconsistent.

For every state and edge, the implementation first calculates the zero-safe
Hölder radius. If every empirical factor minus its perturbation radius is
strictly positive, it also evaluates the local Lipschitz radius and uses the
smaller result. `positive_local_factor_floor_mask` and
`positive_transport_factor_floor_mask` show exactly where that refinement was
available. The primitive radii are returned in
`screening_local_factor_errors` and `screening_transport_factor_errors` for
independent inspection.

No positive-factor assumption is required to call the function. A state or edge
that lacks a certified positive floor automatically uses the zero-safe bound.
The guarantee flag has the same meaning and confidence as in the base Gaussian
screen.

### Structural-null Gaussian screen

```python
from observer_math import gaussian_structural_null_near_competitor_screen

null_aware = gaussian_structural_null_near_competitor_screen(
    empirical_local_factors,
    empirical_transport_factors,
    candidates,
    screening_sample_count,
    node_count,
    subset_size,
    structural_integration_null_mask=predeclared_null_mask,
    minimum_block_eigenvalues=minimum_eigenvalues,
    maximum_block_eigenvalues=maximum_eigenvalues,
    certification_local_score_errors=local_certification_budget,
    certification_transport_score_errors=transport_certification_budget,
    confidence=0.975,
)
```

A true mask entry asserts that a model-level argument, fixed independently of
the screening data, proves an exactly zero population integration factor. The
population local score is then zero regardless of insulation and persistence.
The function combines three valid radii: the general factor-aware radius, the
observed local score itself, and the quadratic null-CMI radius from Proposition
18. Unmasked states and every transport edge use the ordinary factor-aware
calculation.

`structural_integration_null_mask` and `null_local_score_errors` are returned
with the result so a reviewer can see every place where structural information
entered. The function deliberately accepts only a Boolean array; it does not
infer nulls by thresholding empirical factors. A false null declaration can
invalidate the guarantee even when all numerical checks pass.

The primitive public functions
`gaussian_null_cmi_covariance_error_bound` and
`gaussian_null_integration_factor_error_bound` expose the intermediate
quadratic calculation for direct inspection.

### Covariance-normalized Gaussian screen

```python
from observer_math import gaussian_relative_structural_null_near_competitor_screen

relative = gaussian_relative_structural_null_near_competitor_screen(
    empirical_local_factors,
    empirical_transport_factors,
    candidates,
    screening_sample_count,
    node_count,
    subset_size,
    structural_integration_null_mask=predeclared_null_mask,
    certification_local_score_errors=local_certification_budget,
    certification_transport_score_errors=transport_certification_budget,
    confidence=0.975,
)
```

This Proposition 37 entry point has the same factor shapes, structural-null
premise, score construction, certification budgets, and near-competitor output
as the absolute structural-null screen. It does not accept population minimum
or maximum eigenvalue arrays. Instead it constructs a simultaneous Wishart
radius for
`||Sigma^(-1/2) (Sigma_hat - Sigma) Sigma^(-1/2)||_2` from the block dimension,
block count, sample count, and confidence.

`covariance_relative_errors` reports the candidate-local relative radii and
`maximum_covariance_relative_error` reports their maximum. Primitive factor and
complete-score radii remain available through the corresponding `screening_*`
arrays. `all_blocks_valid` requires the relative radius to be below one.

The supporting scalar functions are:

- `gaussian_wishart_relative_covariance_error_bound`
- `gaussian_relative_cmi_covariance_error_bound`
- `canonical_persistence_relative_covariance_error_bound`
- `gaussian_relative_null_cmi_covariance_error_bound`
- `gaussian_relative_null_integration_factor_error_bound`

Population whitening defines the concentration event and its proof; callers do
not estimate or supply a whitening matrix. The guarantee still assumes fixed
positive-definite Gaussian candidate blocks and independent trajectories across
the sample index. Any data-adaptive candidate or null selection needs separate
protection.

### Independent sample-split certification

```python
from observer_math import (
    minimum_sample_split_certification_size,
    sample_split_screened_recovery_bound,
)

bound = sample_split_screened_recovery_bound(
    screening_sample_count=2_000,
    certification_sample_count=100_000,
    retained_block_count=25,
    block_dimension=20,
    maximum_block_eigenvalue=2.0,
    maximum_admissible_covariance_error=0.12,
    screening_confidence=0.975,
    certification_confidence=0.975,
    independent_splits=True,
)

minimum = minimum_sample_split_certification_size(
    screening_sample_count=2_000,
    retained_block_count=25,
    block_dimension=20,
    maximum_block_eigenvalue=2.0,
    maximum_admissible_covariance_error=0.12,
)
```

`screening_confidence` is the probability that the first split retains every
path capable of challenging the population winner under the downstream budget.
It may be supplied by `gaussian_safe_near_competitor_screen` under Proposition
33, or by another independently justified screening theorem.
`certification_confidence` controls simultaneous Gaussian
covariance concentration over at most `retained_block_count` blocks in the
independent second split. The reported overall confidence is their product.

`maximum_admissible_covariance_error` is the strict deterministic radius below
which the downstream recovery certificate succeeds. This function accounts for
confidence composition; it does not infer the admissible radius. Set
`independent_splits=False` whenever the
same observations influence both stages. In that case the function reports no
recovery guarantee even if the numerical covariance radius is small enough.

## Identifiability and symmetry

```python
from observer_math import (
    canonical_path_orbit,
    paths_equivalent_under_permutations,
    two_point_identifiability_bound,
)

permutation_group = ((0, 1, 2), (2, 1, 0))
representative = canonical_path_orbit(path, permutation_group)
equivalent = paths_equivalent_under_permutations(
    path, relabeled_path, permutation_group
)
impossibility = two_point_identifiability_bound(
    total_variation_distance=0.0
)
print(impossibility.maximin_success_probability)  # 0.5
```

The permutation collection must be the full finite group of relabelings that
the application regards as scientifically equivalent. The two-point bound
applies when two models assign correct paths to disjoint such orbits. It is an
upper bound for every estimator using only the stated observations, not just
the world-tube optimizer.

## Internal baselines

```python
from observer_math import best_fixed_boundary, independent_local_path

local_path = independent_local_path(local_scores, candidates)
fixed_path = best_fixed_boundary(local_scores, candidates)
```

These functions answer deliberately simple comparison questions. They are not
surrogates for external published methods.
