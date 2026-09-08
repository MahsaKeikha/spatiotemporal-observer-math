"""Information transport in nonstationary linear Gaussian systems."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .gaussian import (
    as_square,
    canonical_persistence,
    gaussian_conditional_mutual_information,
    symmetrize,
)

FloatMatrix = NDArray[np.float64]


@dataclass(frozen=True)
class TransportMetrics:
    """Representation transport from one boundary to the next."""

    source: tuple[int, ...]
    target: tuple[int, ...]
    persistence: float
    environmental_leakage_bits_per_node: float
    independence: float
    transport_score: float


def adjacent_joint_covariance(
    current_covariance: ArrayLike,
    transition: ArrayLike,
    noise_covariance: ArrayLike,
) -> FloatMatrix:
    """Return Cov([X_t, X_(t+1)]) without a stationarity assumption."""
    current = as_square(current_covariance, name="current_covariance")
    transition = as_square(transition, name="transition")
    noise = as_square(noise_covariance, name="noise_covariance")
    if not (current.shape == transition.shape == noise.shape):
        raise ValueError("all matrices must have equal dimensions")
    future = symmetrize(transition @ current @ transition.T + noise)
    cross = current @ transition.T
    return symmetrize(np.block([[current, cross], [cross.T, future]]))


def propagate_covariances(
    transitions: Sequence[ArrayLike],
    noise_covariances: Sequence[ArrayLike],
    initial_covariance: ArrayLike,
) -> tuple[FloatMatrix, ...]:
    """Propagate Sigma_(t+1) = A_t Sigma_t A_t.T + Q_t exactly."""
    if len(transitions) != len(noise_covariances):
        raise ValueError("transitions and noise_covariances must have equal length")
    current = as_square(initial_covariance, name="initial_covariance")
    result = [symmetrize(current)]
    for transition, noise in zip(transitions, noise_covariances, strict=True):
        transition = as_square(transition, name="transition")
        noise = as_square(noise, name="noise_covariance")
        if transition.shape != current.shape or noise.shape != current.shape:
            raise ValueError("all matrices must have equal dimensions")
        current = symmetrize(transition @ current @ transition.T + noise)
        result.append(current)
    return tuple(result)


def full_trajectory_covariance(
    transitions: Sequence[ArrayLike],
    noise_covariances: Sequence[ArrayLike],
    initial_covariance: ArrayLike,
) -> FloatMatrix:
    """Return the exact covariance of ``[X_0, ..., X_T]``.

    The process follows ``X_(t+1) = A_t X_t + epsilon_t`` with independent
    zero-mean innovations having the supplied covariances. No stationarity
    assumption is made.
    """
    if len(transitions) != len(noise_covariances):
        raise ValueError("transitions and noise_covariances must have equal length")
    initial = as_square(initial_covariance, name="initial_covariance")
    transition_tuple = tuple(as_square(value, name="transition") for value in transitions)
    noise_tuple = tuple(as_square(value, name="noise_covariance") for value in noise_covariances)
    if any(value.shape != initial.shape for value in (*transition_tuple, *noise_tuple)):
        raise ValueError("all matrices must have equal dimensions")

    marginals = propagate_covariances(transition_tuple, noise_tuple, initial)
    node_count = initial.shape[0]
    time_count = len(marginals)
    result = np.zeros((time_count * node_count, time_count * node_count))
    for source_time, marginal in enumerate(marginals):
        source = slice(source_time * node_count, (source_time + 1) * node_count)
        result[source, source] = marginal
        cross = marginal
        for target_time in range(source_time + 1, time_count):
            cross = cross @ transition_tuple[target_time - 1].T
            target = slice(target_time * node_count, (target_time + 1) * node_count)
            result[source, target] = cross
            result[target, source] = cross.T
    return symmetrize(result)


def transport_metrics(
    current_covariance: ArrayLike,
    transition: ArrayLike,
    noise_covariance: ArrayLike,
    source: Sequence[int],
    target: Sequence[int],
) -> TransportMetrics:
    """Score transported prediction and insulation across changing boundaries.

    Persistence is representation-invariant under invertible coordinate changes
    within the source and target blocks. Leakage asks how much the present
    environment predicts the future target after conditioning on the source.
    """
    current = as_square(current_covariance, name="current_covariance")
    joint = adjacent_joint_covariance(current, transition, noise_covariance)
    return transport_metrics_from_covariances(current, joint, source, target)


def transport_metrics_from_covariances(
    current_covariance: ArrayLike,
    joint_covariance: ArrayLike,
    source: Sequence[int],
    target: Sequence[int],
) -> TransportMetrics:
    """Score transport from supplied current and adjacent-time covariances.

    This is the model-free entry point for empirical covariance estimates. The
    joint covariance must order variables as ``[X_t, X_(t+1)]``.
    """
    current = as_square(current_covariance, name="current_covariance")
    joint = as_square(joint_covariance, name="joint_covariance")
    node_count = current.shape[0]
    if joint.shape != (2 * node_count, 2 * node_count):
        raise ValueError("joint_covariance must have twice the current dimension")
    source = tuple(sorted({int(node) for node in source}))
    target = tuple(sorted({int(node) for node in target}))
    if not source or not target:
        raise ValueError("source and target must be nonempty")
    if min(source + target) < 0 or max(source + target) >= node_count:
        raise ValueError("source and target must contain valid node indices")

    future_target = tuple(node_count + node for node in target)
    source_covariance = current[np.ix_(source, source)]
    target_covariance = joint[np.ix_(future_target, future_target)]
    cross_covariance = joint[np.ix_(source, future_target)]
    persistence = canonical_persistence(source_covariance, target_covariance, cross_covariance)

    environment = tuple(node for node in range(node_count) if node not in source)
    leakage = gaussian_conditional_mutual_information(
        joint, future_target, environment, source
    ) / len(target)
    independence = 2.0 ** (-leakage)
    score = float(np.sqrt(persistence * independence))
    return TransportMetrics(
        source=source,
        target=target,
        persistence=persistence,
        environmental_leakage_bits_per_node=float(leakage),
        independence=float(independence),
        transport_score=score,
    )
