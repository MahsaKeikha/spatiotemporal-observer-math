"""Transparent baselines for changing-boundary experiments."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike


@dataclass(frozen=True)
class BaselinePath:
    """A baseline path and the local-score sum used to select it."""

    path: tuple[tuple[int, ...], ...]
    candidate_indices: tuple[int, ...]
    local_score_sum: float


def independent_local_path(
    local_scores: ArrayLike,
    candidates: Sequence[Sequence[int]],
) -> BaselinePath:
    """Choose the highest local score independently at every time."""
    local = np.asarray(local_scores, dtype=float)
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    if local.ndim != 2 or local.shape[1] != len(candidate_tuple):
        raise ValueError("local_scores and candidates have incompatible shapes")
    indices = tuple(int(index) for index in np.argmax(local, axis=1))
    score = float(sum(local[time, index] for time, index in enumerate(indices)))
    return BaselinePath(
        path=tuple(candidate_tuple[index] for index in indices),
        candidate_indices=indices,
        local_score_sum=score,
    )


def best_fixed_boundary(
    local_scores: ArrayLike,
    candidates: Sequence[Sequence[int]],
) -> BaselinePath:
    """Use the one candidate with the largest local-score sum at every time."""
    local = np.asarray(local_scores, dtype=float)
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    if local.ndim != 2 or local.shape[1] != len(candidate_tuple):
        raise ValueError("local_scores and candidates have incompatible shapes")
    index = int(np.argmax(np.sum(local, axis=0)))
    indices = (index,) * local.shape[0]
    return BaselinePath(
        path=(candidate_tuple[index],) * local.shape[0],
        candidate_indices=indices,
        local_score_sum=float(np.sum(local[:, index])),
    )
