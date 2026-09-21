"""Closed-loop bridge from Research I world-tube inference to sensing.

This module deliberately reuses the repository's existing covariance scoring and
world-tube optimizer. It does not replace the Research I inference machinery.

The bridge extracts the best and runner-up paths from the same local,
transport, and continuity objective, converts their structural disagreement
into a sensing target, and selects a physical channel using predictive
discrimination.
"""

from __future__ import annotations

from itertools import combinations
from typing import Sequence

import numpy as np

from observer_math import (
    adjacent_sample_covariances,
    observer_metrics_from_covariances,
    transport_metrics_from_covariances,
)


def jaccard_distance(a: Sequence[int], b: Sequence[int]) -> float:
    aa, bb = set(a), set(b)
    return 1.0 - len(aa & bb) / len(aa | bb)


def score_worldtube_arrays(states, candidates, *, ridge=1e-5):
    """Compute Research I local and distributional transport score arrays."""
    time_count = len(states) - 1
    candidate_count = len(candidates)
    local = np.zeros((time_count, candidate_count))
    transport = np.zeros((time_count - 1, candidate_count, candidate_count))

    for t in range(time_count):
        present, joint = adjacent_sample_covariances(states[t], states[t + 1], ridge=ridge)
        for i, candidate in enumerate(candidates):
            local[t, i] = observer_metrics_from_covariances(
                present, joint, candidate
            ).observer_score
        if t < time_count - 1:
            for i, source in enumerate(candidates):
                for j, target in enumerate(candidates):
                    transport[t, i, j] = transport_metrics_from_covariances(
                        present, joint, source, target
                    ).transport_score
    return local, transport


def ranked_worldtubes(
    local: np.ndarray,
    candidates,
    transport: np.ndarray,
    *,
    transport_weight=0.25,
    continuity_weight=0.08,
):
    """Return best and runner-up paths under the Research I path objective.

    This is a transparent exhaustive reference implementation intended for the
    small n=7 benchmark. Production inference should keep using the repository's
    dynamic-programming optimizer.
    """
    t_count, c_count = local.shape
    scores = [([j], float(local[0, j])) for j in range(c_count)]

    for t in range(1, t_count):
        expanded = []
        for path, score in scores:
            i = path[-1]
            for j in range(c_count):
                step = (
                    local[t, j]
                    + transport_weight * transport[t - 1, i, j]
                    - continuity_weight * jaccard_distance(candidates[i], candidates[j])
                )
                expanded.append((path + [j], score + float(step)))
        # Keeping two prefixes per terminal state is sufficient for exact global
        # best and runner-up extraction in this additive first-order objective.
        next_scores = []
        for j in range(c_count):
            terminal = [item for item in expanded if item[0][-1] == j]
            terminal.sort(key=lambda x: x[1], reverse=True)
            next_scores.extend(terminal[:2])
        scores = next_scores

    scores.sort(key=lambda x: x[1], reverse=True)
    if len(scores) < 2:
        raise ValueError("At least two world-tube paths are required.")
    return (
        tuple(candidates[i] for i in scores[0][0]),
        float(scores[0][1]),
        tuple(candidates[i] for i in scores[1][0]),
        float(scores[1][1]),
    )


def disagreement_weights(best_path, runner_up_path) -> np.ndarray:
    n = max(max(max(s) for s in best_path), max(max(s) for s in runner_up_path)) + 1
    weights = np.zeros(n)
    for a, b in zip(best_path, runner_up_path):
        for j in set(a).symmetric_difference(b):
            weights[j] += 1.0
    return weights / len(best_path)


def select_predictive_channel(
    best_path,
    runner_up_path,
    predictive_mean_best: np.ndarray,
    predictive_mean_runner_up: np.ndarray,
    predictive_variance: np.ndarray,
):
    """Select a channel that is both structurally disputed and predictive."""
    q = disagreement_weights(best_path, runner_up_path)
    if len(q) < len(predictive_mean_best):
        q = np.pad(q, (0, len(predictive_mean_best) - len(q)))
    kl = 0.5 * (predictive_mean_best - predictive_mean_runner_up) ** 2 / predictive_variance
    utility = q * kl
    if np.allclose(utility, 0.0):
        return None, utility
    return int(np.argmax(utility)), utility


def infer_competitors_and_target(
    states,
    *,
    subset_size,
    predictive_mean_best,
    predictive_mean_runner_up,
    predictive_variance,
    ridge=1e-5,
):
    """Full bridge: sampled states -> world tubes -> disagreement -> sensor."""
    dimension = states[0].shape[1]
    candidates = tuple(combinations(range(dimension), subset_size))
    local, transport = score_worldtube_arrays(states, candidates, ridge=ridge)
    best, best_score, second, second_score = ranked_worldtubes(
        local, candidates, transport
    )
    sensor, utility = select_predictive_channel(
        best,
        second,
        predictive_mean_best,
        predictive_mean_runner_up,
        predictive_variance,
    )
    return {
        "best_path": best,
        "runner_up_path": second,
        "path_margin": best_score - second_score,
        "disagreement_weights": disagreement_weights(best, second),
        "selected_channel": sensor,
        "channel_utility": utility,
    }
