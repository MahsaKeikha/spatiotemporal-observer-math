"""Graph-local covariance perturbation envelopes."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike


@dataclass(frozen=True)
class BlockCovarianceErrorEnvelope:
    """Block comparison recursion for covariance and adjacent-joint errors."""

    time_count: int
    block_count: int
    transition_comparisons: tuple[np.ndarray, ...]
    forcing_comparisons: tuple[np.ndarray, ...]
    perturbation_comparisons: tuple[np.ndarray, ...]
    state_error_comparisons: tuple[np.ndarray, ...]
    cross_error_comparisons: tuple[np.ndarray, ...]
    global_state_error_bounds: tuple[float, ...]


def _comparison_sequence(
    values: ArrayLike,
    *,
    label: str,
    time_count: int | None = None,
    block_count: int | None = None,
) -> np.ndarray:
    """Validate a nonnegative sequence of square comparison matrices."""
    array = np.asarray(values, dtype=float)
    if array.ndim != 3 or array.shape[1] != array.shape[2]:
        raise ValueError(f"{label} must have shape (time_count, block_count, block_count)")
    if time_count is not None and array.shape[0] != time_count:
        raise ValueError(f"{label} must have the same time_count")
    if block_count is not None and array.shape[1] != block_count:
        raise ValueError(f"{label} must have the same block_count")
    if np.any(~np.isfinite(array)) or np.any(array < 0.0):
        raise ValueError(f"{label} must be finite and nonnegative")
    return array


def block_covariance_error_envelope(
    transition_comparisons: ArrayLike,
    forcing_comparisons: ArrayLike,
    perturbation_comparisons: ArrayLike,
    *,
    initial_error_comparison: ArrayLike | None = None,
) -> BlockCovarianceErrorEnvelope:
    """Propagate blockwise covariance error without a global scalar recursion.

    Entry ``[t, a, b]`` in a comparison array bounds the operator norm of the
    corresponding block. ``perturbation_comparisons`` bounds the additive
    transition error and is used in the adjacent cross-covariance envelope.
    """
    transitions = _comparison_sequence(
        transition_comparisons, label="transition_comparisons"
    )
    time_count, block_count, _ = transitions.shape
    forcings = _comparison_sequence(
        forcing_comparisons,
        label="forcing_comparisons",
        time_count=time_count,
        block_count=block_count,
    )
    perturbations = _comparison_sequence(
        perturbation_comparisons,
        label="perturbation_comparisons",
        time_count=time_count,
        block_count=block_count,
    )
    if initial_error_comparison is None:
        initial = np.zeros((block_count, block_count), dtype=float)
    else:
        initial = np.asarray(initial_error_comparison, dtype=float)
        if initial.shape != (block_count, block_count):
            raise ValueError(
                "initial_error_comparison must have shape (block_count, block_count)"
            )
        if np.any(~np.isfinite(initial)) or np.any(initial < 0.0):
            raise ValueError("initial_error_comparison must be finite and nonnegative")
    if not np.allclose(initial, initial.T):
        raise ValueError("initial_error_comparison must be symmetric")

    states = [initial.copy()]
    crosses = []
    for time in range(time_count):
        current = states[-1]
        cross = transitions[time] @ current + perturbations[time]
        next_state = (
            transitions[time] @ current @ transitions[time].T + forcings[time]
        )
        next_state = np.maximum(next_state, next_state.T)
        crosses.append(cross)
        states.append(next_state)

    return BlockCovarianceErrorEnvelope(
        time_count=time_count,
        block_count=block_count,
        transition_comparisons=tuple(matrix.copy() for matrix in transitions),
        forcing_comparisons=tuple(matrix.copy() for matrix in forcings),
        perturbation_comparisons=tuple(matrix.copy() for matrix in perturbations),
        state_error_comparisons=tuple(states),
        cross_error_comparisons=tuple(crosses),
        global_state_error_bounds=tuple(
            float(np.linalg.norm(matrix, ord=2)) for matrix in states
        ),
    )


def block_covariance_error_envelope_from_perturbations(
    base_transition_comparisons: ArrayLike,
    transition_perturbation_comparisons: ArrayLike,
    noise_perturbation_comparisons: ArrayLike,
    *,
    initial_error_comparison: ArrayLike | None = None,
) -> BlockCovarianceErrorEnvelope:
    """Construct the forcing comparison and propagate the covariance error."""
    base = _comparison_sequence(
        base_transition_comparisons, label="base_transition_comparisons"
    )
    time_count, block_count, _ = base.shape
    perturbations = _comparison_sequence(
        transition_perturbation_comparisons,
        label="transition_perturbation_comparisons",
        time_count=time_count,
        block_count=block_count,
    )
    noise = _comparison_sequence(
        noise_perturbation_comparisons,
        label="noise_perturbation_comparisons",
        time_count=time_count,
        block_count=block_count,
    )
    transitions = base + perturbations
    forcings = np.empty_like(base)
    for time in range(time_count):
        forcing = (
            base[time] @ perturbations[time].T
            + perturbations[time] @ base[time].T
            + perturbations[time] @ perturbations[time].T
            + noise[time]
        )
        forcings[time] = np.maximum(forcing, forcing.T)
    return block_covariance_error_envelope(
        transitions,
        forcings,
        perturbations,
        initial_error_comparison=initial_error_comparison,
    )


def block_joint_covariance_error_bound(
    envelope: BlockCovarianceErrorEnvelope,
    time: int,
    present_blocks: tuple[int, ...],
    future_blocks: tuple[int, ...] | None = None,
) -> float:
    """Bound one compressed adjacent-joint covariance perturbation."""
    if isinstance(time, bool) or not isinstance(time, (int, np.integer)):
        raise TypeError("time must be an integer")
    if not 0 <= time < envelope.time_count:
        raise ValueError("time lies outside the envelope horizon")
    if future_blocks is None:
        future_blocks = present_blocks
    present = tuple(dict.fromkeys(present_blocks))
    future = tuple(dict.fromkeys(future_blocks))
    if not present or not future:
        raise ValueError("present_blocks and future_blocks must be nonempty")
    if any(
        isinstance(index, bool)
        or not isinstance(index, (int, np.integer))
        or not 0 <= index < envelope.block_count
        for index in present + future
    ):
        raise ValueError("block indices lie outside the comparison partition")

    current = envelope.state_error_comparisons[time][np.ix_(present, present)]
    next_state = envelope.state_error_comparisons[time + 1][
        np.ix_(future, future)
    ]
    cross = envelope.cross_error_comparisons[time][np.ix_(future, present)]
    joint_comparison = np.block(
        [
            [current, cross.T],
            [cross, next_state],
        ]
    )
    return float(np.linalg.norm(joint_comparison, ord=2))
