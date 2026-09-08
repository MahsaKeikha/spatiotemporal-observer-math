"""Finite-sample e-value confidence sets for Gaussian temporal families.

Proposition 51 uses a fixed Gaussian mixture density over a declared temporal
parameter family. For any candidate parameter theta, the density ratio

    e_theta(z) = q(z) / p_theta(z)

has expectation one when theta is the true parameter. Markov's inequality then
gives a continuum confidence set without a union bound over parameter values.

Unknown constant channel means are removed exactly with an orthonormal Helmert
contrast before the Gaussian residual likelihood is evaluated.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike
from scipy.special import logsumexp


@dataclass(frozen=True)
class GaussianAR1WhiteNoiseEValueModel:
    """Observed-data object defining the Proposition 51 continuum confidence set."""

    sample_count: int
    channel_count: int
    contrast_dimension: int
    confidence: float
    log_evalue_threshold: float
    declared_autocorrelation_lower_bound: float
    declared_autocorrelation_upper_bound: float
    declared_white_noise_fraction_lower_bound: float
    declared_white_noise_fraction_upper_bound: float
    mixture_autocorrelation_grid: np.ndarray
    mixture_white_noise_fraction_grid: np.ndarray
    mixture_point_count: int
    contrast_matrix: np.ndarray
    residual_scatter: np.ndarray
    log_mixture_density_kernel: float


@dataclass(frozen=True)
class GaussianAR1WhiteNoiseEValueGrid:
    """Deterministic numerical evaluation of the continuum e-value set.

    The accepted grid is a visualization and numerical diagnostic. Proposition
    51's probability statement concerns the continuum set defined by the
    pointwise e-value, not only these grid points.
    """

    autocorrelation_grid: np.ndarray
    white_noise_fraction_grid: np.ndarray
    log_evalues: np.ndarray
    accepted_mask: np.ndarray
    accepted_point_count: int
    total_point_count: int
    accepted_autocorrelation_lower_bound: float
    accepted_autocorrelation_upper_bound: float
    accepted_white_noise_fraction_lower_bound: float
    accepted_white_noise_fraction_upper_bound: float


def gaussian_helmert_contrast(
    sample_count: int,
    contrast_dimension: int | None = None,
) -> np.ndarray:
    """Return fixed orthonormal contrasts that annihilate the constant vector.

    With the default ``contrast_dimension=None``, the returned matrix has
    ``sample_count - 1`` rows and spans the complete orthogonal complement of
    the constant temporal direction. Smaller fixed dimensions deliberately
    discard some calibration information but retain the exact e-value theorem.
    """
    if isinstance(sample_count, bool) or not isinstance(
        sample_count, (int, np.integer)
    ):
        raise TypeError("sample_count must be an integer")
    if sample_count < 2:
        raise ValueError("sample_count must be at least two")

    if contrast_dimension is None:
        dimension = sample_count - 1
    else:
        if isinstance(contrast_dimension, bool) or not isinstance(
            contrast_dimension, (int, np.integer)
        ):
            raise TypeError("contrast_dimension must be an integer or None")
        dimension = int(contrast_dimension)
        if not 1 <= dimension < sample_count:
            raise ValueError("contrast_dimension must lie in [1, sample_count - 1]")

    contrast = np.zeros((dimension, sample_count), dtype=float)
    for row in range(1, dimension + 1):
        scale = 1.0 / np.sqrt(row * (row + 1.0))
        contrast[row - 1, :row] = scale
        contrast[row - 1, row] = -row * scale
    return contrast


def _validated_parameter_box(
    lower_autocorrelation: float,
    upper_autocorrelation: float,
    lower_white_noise_fraction: float,
    upper_white_noise_fraction: float,
) -> tuple[float, float, float, float]:
    lower_phi = float(lower_autocorrelation)
    upper_phi = float(upper_autocorrelation)
    lower_eta = float(lower_white_noise_fraction)
    upper_eta = float(upper_white_noise_fraction)
    if not 0.0 <= lower_phi <= upper_phi < 1.0:
        raise ValueError(
            "require 0 <= lower_autocorrelation <= upper_autocorrelation < 1"
        )
    if not 0.0 <= lower_eta <= upper_eta < 1.0:
        raise ValueError(
            "require 0 <= lower_white_noise_fraction <= "
            "upper_white_noise_fraction < 1"
        )
    return lower_phi, upper_phi, lower_eta, upper_eta


def _validated_grid_size(value: int, name: str, *, degenerate: bool) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an integer")
    minimum = 1 if degenerate else 2
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return int(value)


def _parameter_grid(lower: float, upper: float, size: int) -> np.ndarray:
    if lower == upper:
        return np.array([lower], dtype=float)
    return np.linspace(lower, upper, size)


def _temporal_covariance(
    sample_count: int,
    autocorrelation: float,
    white_noise_fraction: float,
) -> np.ndarray:
    phi = float(autocorrelation)
    eta = float(white_noise_fraction)
    indices = np.arange(sample_count)
    ar1 = phi ** np.abs(indices[:, None] - indices[None, :])
    return (1.0 - eta) * ar1 + eta * np.eye(sample_count)


def _log_likelihood_kernel(
    channel_count: int,
    residual_scatter: np.ndarray,
    covariance: np.ndarray,
) -> float:
    sign, log_determinant = np.linalg.slogdet(covariance)
    if sign <= 0.0 or not np.isfinite(log_determinant):
        raise ValueError("compressed temporal covariance must be positive definite")
    solved = np.linalg.solve(covariance, residual_scatter)
    quadratic_trace = float(np.trace(solved))
    return float(-0.5 * channel_count * log_determinant - 0.5 * quadratic_trace)


def _compressed_temporal_covariance(
    model_or_contrast: GaussianAR1WhiteNoiseEValueModel | np.ndarray,
    sample_count: int,
    autocorrelation: float,
    white_noise_fraction: float,
) -> np.ndarray:
    contrast = (
        model_or_contrast.contrast_matrix
        if isinstance(model_or_contrast, GaussianAR1WhiteNoiseEValueModel)
        else model_or_contrast
    )
    temporal = _temporal_covariance(
        sample_count,
        autocorrelation,
        white_noise_fraction,
    )
    compressed = contrast @ temporal @ contrast.T
    return 0.5 * (compressed + compressed.T)


def gaussian_ar1_white_noise_evalue_model(
    standardized_observations: ArrayLike,
    *,
    lower_autocorrelation: float,
    upper_autocorrelation: float,
    lower_white_noise_fraction: float = 0.0,
    upper_white_noise_fraction: float = 0.10,
    confidence: float = 0.9875,
    contrast_dimension: int | None = None,
    mixture_autocorrelation_grid_size: int = 9,
    mixture_white_noise_fraction_grid_size: int = 7,
) -> GaussianAR1WhiteNoiseEValueModel:
    """Build the observed-data object for Proposition 51.

    The mixture grid is fixed by the declared parameter box and supplied grid
    sizes. Equal positive weights are used. The finite mixture is only the
    numerator density ``q``. The confidence set itself remains a continuum in
    ``(phi, eta)`` because the denominator ``p_theta`` can be evaluated at any
    admissible parameter value.
    """
    lower_phi, upper_phi, lower_eta, upper_eta = _validated_parameter_box(
        lower_autocorrelation,
        upper_autocorrelation,
        lower_white_noise_fraction,
        upper_white_noise_fraction,
    )
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")

    values = np.asarray(standardized_observations, dtype=float)
    if values.ndim == 1:
        values = values[:, None]
    if values.ndim != 2 or values.shape[0] < 2 or values.shape[1] < 1:
        raise ValueError(
            "standardized_observations must have shape (sample_count, channel_count)"
        )
    if not np.all(np.isfinite(values)):
        raise ValueError("standardized_observations must be finite")

    sample_count, channel_count = values.shape
    contrast = gaussian_helmert_contrast(sample_count, contrast_dimension)
    residuals = contrast @ values
    scatter = residuals @ residuals.T
    scatter = 0.5 * (scatter + scatter.T)

    phi_count = _validated_grid_size(
        mixture_autocorrelation_grid_size,
        "mixture_autocorrelation_grid_size",
        degenerate=lower_phi == upper_phi,
    )
    eta_count = _validated_grid_size(
        mixture_white_noise_fraction_grid_size,
        "mixture_white_noise_fraction_grid_size",
        degenerate=lower_eta == upper_eta,
    )
    phi_grid = _parameter_grid(lower_phi, upper_phi, phi_count)
    eta_grid = _parameter_grid(lower_eta, upper_eta, eta_count)

    component_log_likelihoods = []
    for phi in phi_grid:
        for eta in eta_grid:
            covariance = _compressed_temporal_covariance(
                contrast,
                sample_count,
                float(phi),
                float(eta),
            )
            component_log_likelihoods.append(
                _log_likelihood_kernel(channel_count, scatter, covariance)
            )
    component_array = np.asarray(component_log_likelihoods, dtype=float)
    log_mixture = float(logsumexp(component_array) - np.log(component_array.size))

    return GaussianAR1WhiteNoiseEValueModel(
        sample_count=int(sample_count),
        channel_count=int(channel_count),
        contrast_dimension=int(contrast.shape[0]),
        confidence=float(confidence),
        log_evalue_threshold=float(np.log(1.0 / (1.0 - confidence))),
        declared_autocorrelation_lower_bound=lower_phi,
        declared_autocorrelation_upper_bound=upper_phi,
        declared_white_noise_fraction_lower_bound=lower_eta,
        declared_white_noise_fraction_upper_bound=upper_eta,
        mixture_autocorrelation_grid=phi_grid,
        mixture_white_noise_fraction_grid=eta_grid,
        mixture_point_count=int(phi_grid.size * eta_grid.size),
        contrast_matrix=contrast,
        residual_scatter=scatter,
        log_mixture_density_kernel=log_mixture,
    )


def gaussian_ar1_white_noise_log_evalue(
    model: GaussianAR1WhiteNoiseEValueModel,
    autocorrelation: float,
    white_noise_fraction: float,
) -> float:
    """Evaluate ``log(q / p_theta)`` at one admissible continuum parameter."""
    if not isinstance(model, GaussianAR1WhiteNoiseEValueModel):
        raise TypeError("model has the wrong type")
    phi = float(autocorrelation)
    eta = float(white_noise_fraction)
    if not (
        model.declared_autocorrelation_lower_bound
        <= phi
        <= model.declared_autocorrelation_upper_bound
    ):
        raise ValueError("autocorrelation lies outside the declared model")
    if not (
        model.declared_white_noise_fraction_lower_bound
        <= eta
        <= model.declared_white_noise_fraction_upper_bound
    ):
        raise ValueError("white_noise_fraction lies outside the declared model")

    covariance = _compressed_temporal_covariance(
        model,
        model.sample_count,
        phi,
        eta,
    )
    log_likelihood = _log_likelihood_kernel(
        model.channel_count,
        model.residual_scatter,
        covariance,
    )
    return float(model.log_mixture_density_kernel - log_likelihood)


def gaussian_ar1_white_noise_evalue_grid(
    model: GaussianAR1WhiteNoiseEValueModel,
    *,
    autocorrelation_grid_size: int = 33,
    white_noise_fraction_grid_size: int = 26,
) -> GaussianAR1WhiteNoiseEValueGrid:
    """Evaluate the Proposition 51 continuum e-value on a plotting grid.

    This function does not discretize the theorem. It reports which selected
    points satisfy the exact pointwise confidence-set inequality.
    """
    if not isinstance(model, GaussianAR1WhiteNoiseEValueModel):
        raise TypeError("model has the wrong type")

    phi_count = _validated_grid_size(
        autocorrelation_grid_size,
        "autocorrelation_grid_size",
        degenerate=(
            model.declared_autocorrelation_lower_bound
            == model.declared_autocorrelation_upper_bound
        ),
    )
    eta_count = _validated_grid_size(
        white_noise_fraction_grid_size,
        "white_noise_fraction_grid_size",
        degenerate=(
            model.declared_white_noise_fraction_lower_bound
            == model.declared_white_noise_fraction_upper_bound
        ),
    )
    phi_grid = _parameter_grid(
        model.declared_autocorrelation_lower_bound,
        model.declared_autocorrelation_upper_bound,
        phi_count,
    )
    eta_grid = _parameter_grid(
        model.declared_white_noise_fraction_lower_bound,
        model.declared_white_noise_fraction_upper_bound,
        eta_count,
    )

    log_evalues = np.empty((phi_grid.size, eta_grid.size), dtype=float)
    for phi_index, phi in enumerate(phi_grid):
        for eta_index, eta in enumerate(eta_grid):
            log_evalues[phi_index, eta_index] = gaussian_ar1_white_noise_log_evalue(
                model,
                float(phi),
                float(eta),
            )
    accepted = log_evalues < model.log_evalue_threshold
    accepted_count = int(np.sum(accepted))

    if accepted_count:
        phi_mask = np.any(accepted, axis=1)
        eta_mask = np.any(accepted, axis=0)
        phi_lower = float(phi_grid[phi_mask][0])
        phi_upper = float(phi_grid[phi_mask][-1])
        eta_lower = float(eta_grid[eta_mask][0])
        eta_upper = float(eta_grid[eta_mask][-1])
    else:
        phi_lower = np.nan
        phi_upper = np.nan
        eta_lower = np.nan
        eta_upper = np.nan

    return GaussianAR1WhiteNoiseEValueGrid(
        autocorrelation_grid=phi_grid,
        white_noise_fraction_grid=eta_grid,
        log_evalues=log_evalues,
        accepted_mask=accepted,
        accepted_point_count=accepted_count,
        total_point_count=int(accepted.size),
        accepted_autocorrelation_lower_bound=phi_lower,
        accepted_autocorrelation_upper_bound=phi_upper,
        accepted_white_noise_fraction_lower_bound=eta_lower,
        accepted_white_noise_fraction_upper_bound=eta_upper,
    )
