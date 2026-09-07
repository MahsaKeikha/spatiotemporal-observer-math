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
from observer_math import block_system, correlated_but_uncoupled_system, ring_system
```

These functions construct small deterministic systems for tests and examples.
They are not empirical models.
