"""Finite-sample e-value calibration for a two-parameter temporal family.

Proposition 51 uses the complete Gaussian residual likelihood of independent
calibration channels instead of separate lag intervals. Unknown constant
channel means are removed exactly by projection onto the orthogonal complement
of the constant vector.

For each temporal parameter theta, let p_theta denote the exact residual
Gaussian density and let q be a fixed finite mixture of such densities chosen
before seeing the calibration data. Then q / p_theta is an e-value under the
model theta because its expectation is exactly one. A continuum confidence set
is obtained by retaining every parameter cell that cannot be certified as
excluded using a deterministic likelihood perturbation bound.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike
from scipy.special import logsumexp

from .compact_temporal_family import (
    GaussianCompactTemporalFamilyMatrixChernoffBound,
    _ar1_matrix,
    _ar1_spectral_derivative_bound,
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)


@dataclass(frozen=True)
class GaussianTemporalEValueConfidenceSet:
    """Certified continuum confidence set represented by retained grid cells."""

    sample_count: int
    channel_count: int
    residual_dimension: int
    confidence: float
    alpha: float
    declared_autocorrelation_lower_bound: float
    declared_autocorrelation_upper_bound: float
    declared_white_noise_fraction_lower_bound: float
    declared_white_noise_fraction_upper_bound: float
    autocorrelation_grid: np.ndarray
    white_noise_fraction_grid: np.ndarray
    maximum_autocorrelation_spacing: float
    maximum_white_noise_fraction_spacing: float
    autocorrelation_lipschitz_bound: float
    white_noise_fraction_lipschitz_bound: float
    calibration_cell_operator_radius: float
    log_likelihood_grid: np.ndarray
    log_mixture_density: float
    log_e_values: np.ndarray
    likelihood_cell_variation_bounds: np.ndarray
    retained_cell_mask: np.ndarray
    retained_parameter_points: np.ndarray
    retained_cell_count: int
    excluded_cell_count: int
    log_evalue_threshold: float


@dataclass(frozen=True)
class GaussianEValueCalibratedTemporalFamilyMatrixChernoffBound:
    """End-to-end covariance certificate after Proposition 51 calibration."""

    confidence_set: GaussianTemporalEValueConfidenceSet
    covariance_bound: GaussianCompactTemporalFamilyMatrixChernoffBound
    calibration_confidence: float
    covariance_confidence: float
    combined_confidence_lower_bound: float
    target_eigenvalue_covering_radius: float
    target_normalization_covering_radius: float
    requires_independent_target_record: bool


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


def _validated_grid_size(value: int, name: str, degenerate: bool) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an integer")
    minimum = 1 if degenerate else 2
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return int(value)


def _mean_orthogonal_basis(sample_count: int) -> np.ndarray:
    constant = np.ones((sample_count, 1), dtype=float)
    basis, _ = np.linalg.qr(constant, mode="complete")
    return basis[:, 1:]


def _ar1_white_noise_covariance(
    sample_count: int,
    autocorrelation: float,
    white_noise_fraction: float,
) -> np.ndarray:
    temporal = _ar1_matrix(sample_count, float(autocorrelation))
    return (1.0 - float(white_noise_fraction)) * temporal + float(
        white_noise_fraction
    ) * np.eye(sample_count)


def _residual_log_likelihood(
    residuals: np.ndarray,
    temporal_covariance: np.ndarray,
    basis: np.ndarray,
) -> tuple[float, float]:
    compressed = basis.T @ temporal_covariance @ basis
    compressed = 0.5 * (compressed + compressed.T)
    sign, logdet = np.linalg.slogdet(compressed)
    if sign <= 0.0:
        raise ValueError("compressed temporal covariance must be positive definite")
    solved = np.linalg.solve(compressed, residuals)
    quadratic = float(np.sum(residuals * solved))
    residual_dimension, channel_count = residuals.shape
    normalizer = channel_count * (
        residual_dimension * np.log(2.0 * np.pi) + float(logdet)
    )
    return float(-0.5 * (normalizer + quadratic)), float(
        np.linalg.eigvalsh(compressed)[0]
    )


def gaussian_ar1_white_noise_residual_log_likelihood(
    observations: ArrayLike,
    autocorrelation: float,
    white_noise_fraction: float,
) -> float:
    """Return the exact constant-mean-invariant residual Gaussian log likelihood."""
    values = np.asarray(observations, dtype=float)
    if values.ndim == 1:
        values = values[:, None]
    if values.ndim != 2 or values.shape[0] < 3 or values.shape[1] < 1:
        raise ValueError(
            "observations must have shape (sample_count, channel_count) with "
            "sample_count at least three"
        )
    if not np.all(np.isfinite(values)):
        raise ValueError("observations must be finite")
    phi = float(autocorrelation)
    eta = float(white_noise_fraction)
    if not 0.0 <= phi < 1.0:
        raise ValueError("autocorrelation must lie in [0, 1)")
    if not 0.0 <= eta < 1.0:
        raise ValueError("white_noise_fraction must lie in [0, 1)")

    basis = _mean_orthogonal_basis(values.shape[0])
    residuals = basis.T @ values
    temporal = _ar1_white_noise_covariance(values.shape[0], phi, eta)
    log_likelihood, _ = _residual_log_likelihood(residuals, temporal, basis)
    return log_likelihood


def _parameter_grid(
    lower: float,
    upper: float,
    size: int,
) -> tuple[np.ndarray, float]:
    if lower == upper:
        return np.array([lower], dtype=float), 0.0
    grid = np.linspace(lower, upper, size)
    return grid, float((upper - lower) / (size - 1))


def _family_lipschitz_bounds(sample_count: int, upper_phi: float) -> tuple[float, float]:
    phi_lipschitz = _ar1_spectral_derivative_bound(sample_count, upper_phi)
    ar1_spectral_bound = min(
        float(sample_count),
        (1.0 + upper_phi) / (1.0 - upper_phi),
    )
    eta_lipschitz = max(1.0, ar1_spectral_bound - 1.0)
    return float(phi_lipschitz), float(eta_lipschitz)


def _likelihood_cell_variation_bound(
    minimum_eigenvalue: float,
    operator_radius: float,
    residual_energy: float,
    residual_dimension: int,
    channel_count: int,
) -> float:
    if operator_radius == 0.0:
        return 0.0
    if operator_radius >= minimum_eigenvalue:
        return float("inf")
    ratio = operator_radius / minimum_eigenvalue
    logdet_change = (
        0.5
        * channel_count
        * residual_dimension
        * float(-np.log1p(-ratio))
    )
    inverse_change = (
        0.5
        * residual_energy
        * operator_radius
        / (minimum_eigenvalue * (minimum_eigenvalue - operator_radius))
    )
    return float(logdet_change + inverse_change)


def gaussian_ar1_white_noise_evalue_confidence_set(
    standardized_observations: ArrayLike,
    *,
    lower_autocorrelation: float,
    upper_autocorrelation: float,
    lower_white_noise_fraction: float = 0.0,
    upper_white_noise_fraction: float = 0.10,
    confidence: float = 0.9875,
    autocorrelation_grid_size: int = 17,
    white_noise_fraction_grid_size: int = 9,
) -> GaussianTemporalEValueConfidenceSet:
    """Build a finite-sample continuum confidence set from the full likelihood.

    The calibration channels are independent Gaussian channels with known unit
    marginal variance and one common temporal covariance from the declared
    family. Every channel may have an arbitrary constant mean. Projection onto
    the complement of the constant vector removes those means exactly.

    A fixed uniform mixture over the parameter-grid residual densities defines
    ``q``. For every admissible true parameter ``theta``, ``q / p_theta`` has
    expectation one. Therefore the set ``q / p_theta < 1 / alpha`` has coverage
    at least ``1 - alpha``. The implementation returns a certified union of
    grid cells containing that exact continuum set. Cells are removed only when
    a deterministic likelihood perturbation bound proves every parameter in
    the cell has e-value at least ``1 / alpha``.
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
    if values.ndim != 2 or values.shape[0] < 3 or values.shape[1] < 1:
        raise ValueError(
            "standardized_observations must have shape "
            "(sample_count, channel_count) with sample_count at least three"
        )
    if not np.all(np.isfinite(values)):
        raise ValueError("standardized_observations must be finite")

    phi_count = _validated_grid_size(
        autocorrelation_grid_size,
        "autocorrelation_grid_size",
        lower_phi == upper_phi,
    )
    eta_count = _validated_grid_size(
        white_noise_fraction_grid_size,
        "white_noise_fraction_grid_size",
        lower_eta == upper_eta,
    )
    phi_grid, phi_spacing = _parameter_grid(lower_phi, upper_phi, phi_count)
    eta_grid, eta_spacing = _parameter_grid(lower_eta, upper_eta, eta_count)

    sample_count, channel_count = values.shape
    basis = _mean_orthogonal_basis(sample_count)
    residuals = basis.T @ values
    residual_energy = float(np.sum(residuals**2))
    residual_dimension = residuals.shape[0]

    phi_lipschitz, eta_lipschitz = _family_lipschitz_bounds(
        sample_count, upper_phi
    )
    cell_radius = float(
        0.5 * phi_spacing * phi_lipschitz
        + 0.5 * eta_spacing * eta_lipschitz
    )

    log_likelihoods: list[float] = []
    minimum_eigenvalues: list[float] = []
    parameter_points: list[tuple[float, float]] = []
    for phi in phi_grid:
        for eta in eta_grid:
            temporal = _ar1_white_noise_covariance(
                sample_count, float(phi), float(eta)
            )
            log_likelihood, minimum_eigenvalue = _residual_log_likelihood(
                residuals, temporal, basis
            )
            log_likelihoods.append(log_likelihood)
            minimum_eigenvalues.append(minimum_eigenvalue)
            parameter_points.append((float(phi), float(eta)))

    log_likelihood_grid = np.asarray(log_likelihoods, dtype=float)
    log_mixture = float(logsumexp(log_likelihood_grid) - np.log(log_likelihood_grid.size))
    log_e_values = log_mixture - log_likelihood_grid
    variation_bounds = np.asarray(
        [
            _likelihood_cell_variation_bound(
                minimum_eigenvalue,
                cell_radius,
                residual_energy,
                residual_dimension,
                channel_count,
            )
            for minimum_eigenvalue in minimum_eigenvalues
        ],
        dtype=float,
    )
    alpha = float(1.0 - confidence)
    log_threshold = float(np.log(1.0 / alpha))
    certified_excluded = log_e_values - variation_bounds >= log_threshold
    retained = ~certified_excluded
    points = np.asarray(parameter_points, dtype=float)
    retained_points = points[retained]
    if retained_points.shape[0] < 1:
        raise RuntimeError("e-value confidence set unexpectedly retained no parameter cells")

    return GaussianTemporalEValueConfidenceSet(
        sample_count=int(sample_count),
        channel_count=int(channel_count),
        residual_dimension=int(residual_dimension),
        confidence=float(confidence),
        alpha=alpha,
        declared_autocorrelation_lower_bound=lower_phi,
        declared_autocorrelation_upper_bound=upper_phi,
        declared_white_noise_fraction_lower_bound=lower_eta,
        declared_white_noise_fraction_upper_bound=upper_eta,
        autocorrelation_grid=phi_grid,
        white_noise_fraction_grid=eta_grid,
        maximum_autocorrelation_spacing=phi_spacing,
        maximum_white_noise_fraction_spacing=eta_spacing,
        autocorrelation_lipschitz_bound=phi_lipschitz,
        white_noise_fraction_lipschitz_bound=eta_lipschitz,
        calibration_cell_operator_radius=cell_radius,
        log_likelihood_grid=log_likelihood_grid,
        log_mixture_density=log_mixture,
        log_e_values=log_e_values,
        likelihood_cell_variation_bounds=variation_bounds,
        retained_cell_mask=retained,
        retained_parameter_points=retained_points,
        retained_cell_count=int(np.sum(retained)),
        excluded_cell_count=int(np.sum(certified_excluded)),
        log_evalue_threshold=log_threshold,
    )


def gaussian_evalue_calibrated_ar1_white_noise_matrix_chernoff_bound(
    standardized_calibration_observations: ArrayLike,
    block_dimension: int,
    block_count: int,
    nuisance_design: ArrayLike,
    *,
    lower_autocorrelation: float,
    upper_autocorrelation: float,
    lower_white_noise_fraction: float = 0.0,
    upper_white_noise_fraction: float = 0.10,
    calibration_confidence: float = 0.9875,
    covariance_confidence: float = 0.9875,
    autocorrelation_grid_size: int = 17,
    white_noise_fraction_grid_size: int = 9,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianEValueCalibratedTemporalFamilyMatrixChernoffBound:
    """Compose Proposition 51 with Proposition 49 for an independent target."""
    confidence_set = gaussian_ar1_white_noise_evalue_confidence_set(
        standardized_calibration_observations,
        lower_autocorrelation=lower_autocorrelation,
        upper_autocorrelation=upper_autocorrelation,
        lower_white_noise_fraction=lower_white_noise_fraction,
        upper_white_noise_fraction=upper_white_noise_fraction,
        confidence=calibration_confidence,
        autocorrelation_grid_size=autocorrelation_grid_size,
        white_noise_fraction_grid_size=white_noise_fraction_grid_size,
    )
    if not 0.0 < covariance_confidence < 1.0:
        raise ValueError("covariance_confidence must lie in (0, 1)")

    design = np.asarray(nuisance_design, dtype=float)
    if design.ndim == 1:
        design = design[:, None]
    if design.ndim != 2 or design.shape[0] < 2 or design.shape[1] < 1:
        raise ValueError("nuisance_design must be a nonempty two-dimensional design")
    if not np.all(np.isfinite(design)):
        raise ValueError("nuisance_design must be finite")
    target_sample_count = design.shape[0]
    nuisance_rank = int(np.linalg.matrix_rank(design))
    if nuisance_rank != design.shape[1] or nuisance_rank >= target_sample_count:
        raise ValueError("nuisance_design must have full column rank below sample_count")

    retained_points = confidence_set.retained_parameter_points
    temporal_grid = np.asarray(
        [
            _ar1_white_noise_covariance(target_sample_count, phi, eta)
            for phi, eta in retained_points
        ]
    )
    phi_lipschitz, eta_lipschitz = _family_lipschitz_bounds(
        target_sample_count,
        confidence_set.declared_autocorrelation_upper_bound,
    )
    raw_radius = float(
        0.5
        * confidence_set.maximum_autocorrelation_spacing
        * phi_lipschitz
        + 0.5
        * confidence_set.maximum_white_noise_fraction_spacing
        * eta_lipschitz
    )
    normalization_radius = float(nuisance_rank * raw_radius)

    covariance = gaussian_compact_temporal_family_matrix_chernoff_bound(
        block_dimension,
        block_count,
        temporal_grid,
        design,
        eigenvalue_covering_radius=raw_radius,
        normalization_covering_radius=normalization_radius,
        confidence=covariance_confidence,
        upper_theta_grid_size=upper_theta_grid_size,
        lower_theta_grid_size=lower_theta_grid_size,
    )
    return GaussianEValueCalibratedTemporalFamilyMatrixChernoffBound(
        confidence_set=confidence_set,
        covariance_bound=covariance,
        calibration_confidence=float(calibration_confidence),
        covariance_confidence=float(covariance_confidence),
        combined_confidence_lower_bound=float(
            calibration_confidence * covariance_confidence
        ),
        target_eigenvalue_covering_radius=raw_radius,
        target_normalization_covering_radius=normalization_radius,
        requires_independent_target_record=True,
    )
