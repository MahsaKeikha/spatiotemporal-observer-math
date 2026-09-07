"""Finite-sample utilities for nonstationary Gaussian experiments."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.random import Generator
from numpy.typing import ArrayLike, NDArray

from .gaussian import as_square, symmetrize

FloatArray = NDArray[np.float64]
FloatMatrix = NDArray[np.float64]


def regularized_sample_covariance(
    samples: ArrayLike,
    *,
    ridge: float = 1e-6,
) -> FloatMatrix:
    """Estimate covariance and add a scale-relative diagonal ridge."""
    values = np.asarray(samples, dtype=float)
    if values.ndim != 2 or values.shape[0] < 2:
        raise ValueError("samples must have shape (sample_count, dimension) with sample_count >= 2")
    if not np.all(np.isfinite(values)):
        raise ValueError("samples must contain only finite values")
    if ridge < 0:
        raise ValueError("ridge must be nonnegative")
    covariance = np.atleast_2d(np.cov(values, rowvar=False, ddof=1)).astype(float)
    dimension = covariance.shape[0]
    scale = max(1.0, float(np.trace(covariance) / dimension))
    return symmetrize(covariance) + ridge * scale * np.eye(dimension)


def adjacent_sample_covariances(
    present_samples: ArrayLike,
    future_samples: ArrayLike,
    *,
    ridge: float = 1e-6,
) -> tuple[FloatMatrix, FloatMatrix]:
    """Estimate present and stacked adjacent-time covariances from paired data."""
    present = np.asarray(present_samples, dtype=float)
    future = np.asarray(future_samples, dtype=float)
    if present.ndim != 2 or future.ndim != 2 or present.shape != future.shape:
        raise ValueError("present_samples and future_samples must have equal 2D shapes")
    joint = np.concatenate([present, future], axis=1)
    joint_covariance = regularized_sample_covariance(joint, ridge=ridge)
    dimension = present.shape[1]
    return joint_covariance[:dimension, :dimension], joint_covariance


def simulate_gaussian_ensemble(
    transitions: Sequence[ArrayLike],
    noise_covariances: Sequence[ArrayLike],
    initial_covariance: ArrayLike,
    sample_count: int,
    *,
    rng: Generator,
) -> tuple[FloatArray, ...]:
    """Draw independent trajectories through a time-varying linear system.

    Each returned array has shape ``(sample_count, dimension)``. The tuple has
    one more state than the number of transition matrices.
    """
    if len(transitions) != len(noise_covariances):
        raise ValueError("transitions and noise_covariances must have equal length")
    if sample_count < 2:
        raise ValueError("sample_count must be at least two")
    initial = as_square(initial_covariance, name="initial_covariance")
    dimension = initial.shape[0]
    current = rng.multivariate_normal(np.zeros(dimension), symmetrize(initial), sample_count)
    states = [current]
    for transition, noise in zip(transitions, noise_covariances, strict=True):
        transition = as_square(transition, name="transition")
        noise = as_square(noise, name="noise_covariance")
        if transition.shape != initial.shape or noise.shape != initial.shape:
            raise ValueError("all matrices must have equal dimensions")
        innovations = rng.multivariate_normal(
            np.zeros(dimension), symmetrize(noise), sample_count
        )
        current = current @ transition.T + innovations
        states.append(current)
    return tuple(states)
