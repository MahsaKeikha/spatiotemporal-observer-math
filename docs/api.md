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
from observer_math import propagate_covariances, transport_metrics

covariance_path = propagate_covariances(
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

The covariance path has one more element than the transition sequence. Source
indices refer to \(X_t\); target indices refer to \(X_{t+1}\).

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
