"""Spatiotemporal measures that extend instantaneous integration."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from numpy.typing import ArrayLike

from .gaussian import (
    as_square,
    gaussian_conditional_mutual_information,
    gaussian_mutual_information,
    predictive_persistence,
    stationary_covariance,
    two_time_covariance,
)


@dataclass(frozen=True)
class ObserverMetrics:
    """Metrics for one candidate subsystem at one temporal lag."""

    subset: tuple[int, ...]
    lag: int
    static_integration_bits_per_node: float
    directed_integration_bits_per_node: float
    environmental_leakage_bits_per_node: float
    integration_strength: float
    independence: float
    persistence: float
    observer_score: float
    weakest_partition: tuple[tuple[int, ...], tuple[int, ...]] | None


def unique_bipartitions(subset: tuple[int, ...]):
    """Yield each nontrivial bipartition once."""
    if len(subset) < 2:
        return
    anchor = subset[0]
    remainder = subset[1:]
    for size in range(len(remainder)):
        for selection in combinations(remainder, size):
            left = (anchor,) + selection
            right = tuple(node for node in subset if node not in left)
            if right:
                yield left, right


def observer_metrics(
    transition: ArrayLike,
    noise_covariance: ArrayLike,
    subset: tuple[int, ...] | list[int],
    *,
    lag: int = 1,
) -> ObserverMetrics:
    """Evaluate integration, independence, and temporal persistence.

    The directed integration term is the weakest bidirectional cross-prediction
    over internal bipartitions. Conditioning on each part's own present prevents
    static correlation alone from being counted as continuing integration.
    """
    if lag < 1:
        raise ValueError("lag must be positive")

    present_covariance = stationary_covariance(transition, noise_covariance)
    joint_covariance = two_time_covariance(transition, noise_covariance, lag=lag)
    return observer_metrics_from_covariances(
        present_covariance, joint_covariance, subset, lag=lag
    )


def observer_metrics_from_covariances(
    present_covariance: ArrayLike,
    joint_covariance: ArrayLike,
    subset: tuple[int, ...] | list[int],
    *,
    lag: int = 1,
) -> ObserverMetrics:
    """Evaluate a candidate from supplied present and two-time covariances.

    Unlike :func:`observer_metrics`, this function makes no stationarity
    assumption and can be used at every step of a time-varying process.
    """
    present_covariance = as_square(present_covariance, name="present_covariance")
    joint_covariance = as_square(joint_covariance, name="joint_covariance")
    node_count = present_covariance.shape[0]
    if joint_covariance.shape != (2 * node_count, 2 * node_count):
        raise ValueError("joint_covariance must have twice the present dimension")
    subset = tuple(sorted({int(node) for node in subset}))
    if not subset or subset[0] < 0 or subset[-1] >= node_count:
        raise ValueError("subset must contain valid node indices")
    if lag < 1:
        raise ValueError("lag must be positive")

    def future(nodes: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(node_count + node for node in nodes)

    static_values: list[float] = []
    directed_values: list[tuple[float, tuple[int, ...], tuple[int, ...]]] = []
    for left, right in unique_bipartitions(subset):
        static_values.append(gaussian_mutual_information(present_covariance, left, right))
        left_from_right = gaussian_conditional_mutual_information(
            joint_covariance, future(left), right, left
        )
        right_from_left = gaussian_conditional_mutual_information(
            joint_covariance, future(right), left, right
        )
        directed_values.append((left_from_right + right_from_left, left, right))

    if directed_values:
        directed_bits, weakest_left, weakest_right = min(directed_values, key=lambda item: item[0])
        static_bits = min(static_values)
        weakest_partition = (weakest_left, weakest_right)
    else:
        directed_bits = 0.0
        static_bits = 0.0
        weakest_partition = None

    environment = tuple(node for node in range(node_count) if node not in subset)
    leakage_bits = gaussian_conditional_mutual_information(
        joint_covariance, future(subset), environment, subset
    )

    size = len(subset)
    static_rate = static_bits / size
    directed_rate = directed_bits / size
    leakage_rate = leakage_bits / size
    integration_strength = 1.0 - 2.0 ** (-directed_rate)
    independence = 2.0 ** (-leakage_rate)
    persistence = predictive_persistence(joint_covariance, subset)

    # A geometric mean makes all three criteria necessary and keeps the score bounded.
    score = float((integration_strength * independence * persistence) ** (1.0 / 3.0))
    return ObserverMetrics(
        subset=subset,
        lag=lag,
        static_integration_bits_per_node=float(static_rate),
        directed_integration_bits_per_node=float(directed_rate),
        environmental_leakage_bits_per_node=float(leakage_rate),
        integration_strength=float(integration_strength),
        independence=float(independence),
        persistence=float(persistence),
        observer_score=score,
        weakest_partition=weakest_partition,
    )
