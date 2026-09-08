"""Uniform matrix concentration over a calibrated AR(1) interval.

Proposition 48 combines the observable AR(1) calibration of Proposition 43,
the design-specific continuum geometry of Proposition 46, and the direct
weighted-Wishart matrix concentration of Proposition 47.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .design_interval import (
    GaussianAR1DesignUniformEnvelope,
    gaussian_ar1_design_uniform_envelope,
)
from .nuisance import separable_gaussian_projected_covariance, temporal_nuisance_projector
from .recovery import (
    GaussianAR1AutocorrelationInterval,
    gaussian_ar1_increment_autocorrelation_interval,
)


@dataclass(frozen=True)
class GaussianAR1UniformMatrixChernoffBound:
    """Observable covariance certificate uniform over an AR(1) interval."""

    block_dimension: int
    block_count: int
    covariance_confidence: float
    design_envelope: GaussianAR1DesignUniformEnvelope
    eigenvalue_covering_radius: float
    reference_projected_degrees_of_freedom: float
    oracle_upper_deviation: float
    oracle_lower_deviation: float
    oracle_relative_error: float
    normalization_lower_ratio: float
    normalization_upper_ratio: float
    final_upper_deviation: float
    final_lower_deviation: float
    covariance_relative_error: float
    upper_dimensionless_theta: float
    lower_dimensionless_theta: float
    upper_theta_grid_size: int
    lower_theta_grid_size: int


@dataclass(frozen=True)
class GaussianCalibratedAR1UniformMatrixChernoffBound:
    """Proposition 48 bound including the observable AR(1) calibration event."""

    autocorrelation_interval: GaussianAR1AutocorrelationInterval
    matrix_bound: GaussianAR1UniformMatrixChernoffBound
    calibration_confidence: float
    covariance_confidence: float
    combined_confidence: float

    @property
    def covariance_relative_error(self) -> float:
        return self.matrix_bound.covariance_relative_error

    @property
    def reference_projected_degrees_of_freedom(self) -> float:
        return self.matrix_bound.reference_projected_degrees_of_freedom


def _validated_design(nuisance_design: ArrayLike) -> np.ndarray:
    design = np.asarray(nuisance_design, dtype=float)
    if design.ndim == 1:
        design = design[:, None]
    if design.ndim != 2 or design.shape[0] < 2 or design.shape[1] < 1:
        raise ValueError("nuisance_design must have shape (sample_count >= 2, rank >= 1)")
    if not np.all(np.isfinite(design)):
        raise ValueError("nuisance_design must be finite")
    rank = int(np.linalg.matrix_rank(design))
    if rank != design.shape[1]:
        raise ValueError("nuisance_design columns must be linearly independent")
    if rank >= design.shape[0]:
        raise ValueError("nuisance rank must be smaller than sample_count")
    return design


def _ar1_matrix(sample_count: int, autocorrelation: float) -> np.ndarray:
    indices = np.arange(sample_count)
    return autocorrelation ** np.abs(indices[:, None] - indices[None, :])


def _validated_grid_size(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an integer")
    if value < 64:
        raise ValueError(f"{name} must be at least 64")
    return int(value)


def _log_matrix_mgf_factor(
    dimension: int,
    scaled_weights: np.ndarray,
    *,
    upper_tail: bool,
) -> np.ndarray:
    """Return log c_m for the exact Gaussian rank-one matrix mgf."""
    x = np.asarray(scaled_weights, dtype=float)
    if upper_tail:
        if np.any(x < 0.0) or np.any(x >= 0.5):
            raise ValueError("upper-tail theta*lambda values must lie in [0, 1/2)")
        log_chi = -0.5 * dimension * np.log1p(-2.0 * x)
        sign_term = -x
    else:
        if np.any(x < 0.0):
            raise ValueError("lower-tail theta*lambda values must be nonnegative")
        log_chi = -0.5 * dimension * np.log1p(2.0 * x)
        sign_term = x

    if dimension == 1:
        log_bracket = log_chi
    else:
        log_bracket = (
            np.logaddexp(np.log(float(dimension - 1)), log_chi)
            - np.log(float(dimension))
        )
    return sign_term + log_bracket


def _projected_grid_spectra(
    design: np.ndarray,
    lower: float,
    upper: float,
    grid_size: int,
) -> tuple[np.ndarray, list[np.ndarray]]:
    if lower == upper:
        grid = np.array([lower], dtype=float)
    else:
        grid = np.linspace(lower, upper, grid_size)
    projector = temporal_nuisance_projector(design)
    spectra: list[np.ndarray] = []
    for phi in grid:
        temporal = _ar1_matrix(design.shape[0], float(phi))
        projected = projector @ temporal @ projector
        projected = 0.5 * (projected + projected.T)
        eigenvalues = np.linalg.eigvalsh(projected)
        scale = max(1.0, float(np.max(np.abs(eigenvalues))))
        tolerance = 1e-11 * scale
        if eigenvalues[0] < -tolerance:
            raise RuntimeError("projected AR(1) covariance lost positive semidefiniteness")
        spectra.append(np.maximum(eigenvalues, 0.0))
    return grid, spectra


def gaussian_ar1_uniform_matrix_chernoff_bound(
    block_dimension: int,
    block_count: int,
    nuisance_design: ArrayLike,
    lower_autocorrelation: float,
    upper_autocorrelation: float,
    *,
    confidence: float = 0.975,
    phi_grid_size: int = 33,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianAR1UniformMatrixChernoffBound:
    """Certify covariance uniformly over a nonnegative AR(1) interval.

    Let ``A(phi)=P_H R_phi P_H``. Proposition 46 gives

    ``||A(phi)-A(psi)||_2 <= L_2 |phi-psi|``.

    Every coefficient in the interval is within half a grid spacing of a
    deterministic grid point. Weyl's inequality therefore puts every ordered
    eigenvalue of ``A(phi)`` within ``delta`` of the corresponding grid
    eigenvalue. The exact Proposition 47 log-mgf factors are nondecreasing in
    each nonnegative temporal eigenvalue. Inflating every grid eigenvalue by
    ``delta`` consequently dominates the complete between-grid matrix mgf.

    The finite theta grids affect tightness only. Every theta candidate used by
    the function is itself a valid uniform Chernoff bound over the full AR(1)
    interval.
    """
    if isinstance(block_dimension, bool) or not isinstance(block_dimension, (int, np.integer)):
        raise TypeError("block_dimension must be an integer")
    if isinstance(block_count, bool) or not isinstance(block_count, (int, np.integer)):
        raise TypeError("block_count must be an integer")
    if block_dimension < 1 or block_count < 1:
        raise ValueError("block_dimension and block_count must be positive")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    upper_theta_count = _validated_grid_size(upper_theta_grid_size, "upper_theta_grid_size")
    lower_theta_count = _validated_grid_size(lower_theta_grid_size, "lower_theta_grid_size")

    design = _validated_design(nuisance_design)
    envelope = gaussian_ar1_design_uniform_envelope(
        design,
        lower_autocorrelation,
        upper_autocorrelation,
        grid_size=phi_grid_size,
    )
    _, spectra = _projected_grid_spectra(
        design,
        envelope.lower_autocorrelation,
        envelope.upper_autocorrelation,
        envelope.grid_size,
    )

    covering_radius = 0.5 * envelope.maximum_grid_spacing
    eigenvalue_delta = envelope.spectral_lipschitz_bound * covering_radius
    spectral_bound = envelope.projected_spectral_norm_bound
    degrees_lower = envelope.projected_degrees_of_freedom_lower_bound
    degrees_upper = envelope.projected_degrees_of_freedom_upper_bound
    if spectral_bound <= 0.0 or degrees_lower <= 0.0:
        raise ValueError("the design envelope leaves no positive covariance information")

    inflated_spectra = [
        np.minimum(spectral_bound, spectrum + eigenvalue_delta)
        for spectrum in spectra
    ]
    log_prefactor = float(
        np.log(2.0 * block_count * block_dimension / (1.0 - confidence))
    )

    upper_x = np.geomspace(1e-8, 0.499999, upper_theta_count)
    upper_values = np.empty_like(upper_x)
    for index, x in enumerate(upper_x):
        theta = x / spectral_bound
        worst_log_mgf = max(
            float(
                np.sum(
                    _log_matrix_mgf_factor(
                        block_dimension,
                        theta * spectrum,
                        upper_tail=True,
                    )
                )
            )
            for spectrum in inflated_spectra
        )
        upper_values[index] = (log_prefactor + worst_log_mgf) / theta / degrees_lower
    upper_index = int(np.argmin(upper_values))
    oracle_upper = float(upper_values[upper_index])

    lower_x = np.geomspace(1e-8, 1e3, lower_theta_count)
    lower_values = np.empty_like(lower_x)
    for index, x in enumerate(lower_x):
        theta = x / spectral_bound
        worst_log_mgf = max(
            float(
                np.sum(
                    _log_matrix_mgf_factor(
                        block_dimension,
                        theta * spectrum,
                        upper_tail=False,
                    )
                )
            )
            for spectrum in inflated_spectra
        )
        lower_values[index] = (log_prefactor + worst_log_mgf) / theta / degrees_lower
    lower_index = int(np.argmin(lower_values))
    oracle_lower = float(min(1.0, lower_values[lower_index]))
    oracle_relative = float(max(oracle_upper, oracle_lower))

    reference_degrees = 0.5 * (degrees_lower + degrees_upper)
    ratio_lower = degrees_lower / reference_degrees
    ratio_upper = degrees_upper / reference_degrees

    final_upper = float(ratio_upper * (1.0 + oracle_upper) - 1.0)
    final_lower = float(max(0.0, 1.0 - ratio_lower * (1.0 - oracle_lower)))
    final_relative = float(max(final_upper, final_lower))

    return GaussianAR1UniformMatrixChernoffBound(
        block_dimension=int(block_dimension),
        block_count=int(block_count),
        covariance_confidence=float(confidence),
        design_envelope=envelope,
        eigenvalue_covering_radius=float(eigenvalue_delta),
        reference_projected_degrees_of_freedom=float(reference_degrees),
        oracle_upper_deviation=oracle_upper,
        oracle_lower_deviation=oracle_lower,
        oracle_relative_error=oracle_relative,
        normalization_lower_ratio=float(ratio_lower),
        normalization_upper_ratio=float(ratio_upper),
        final_upper_deviation=final_upper,
        final_lower_deviation=final_lower,
        covariance_relative_error=final_relative,
        upper_dimensionless_theta=float(upper_x[upper_index]),
        lower_dimensionless_theta=float(lower_x[lower_index]),
        upper_theta_grid_size=upper_theta_count,
        lower_theta_grid_size=lower_theta_count,
    )


def gaussian_calibrated_ar1_uniform_matrix_chernoff_bound(
    block_dimension: int,
    block_count: int,
    nuisance_design: ArrayLike,
    standardized_calibration_observations: ArrayLike,
    *,
    declared_upper_bound: float,
    calibration_confidence: float = 0.9875,
    covariance_confidence: float = 0.9875,
    phi_grid_size: int = 33,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianCalibratedAR1UniformMatrixChernoffBound:
    """Build the complete Proposition 48 bound from observable calibration data."""
    interval = gaussian_ar1_increment_autocorrelation_interval(
        standardized_calibration_observations,
        declared_upper_bound=declared_upper_bound,
        confidence=calibration_confidence,
    )
    matrix_bound = gaussian_ar1_uniform_matrix_chernoff_bound(
        block_dimension,
        block_count,
        nuisance_design,
        interval.lower_bound,
        interval.upper_bound,
        confidence=covariance_confidence,
        phi_grid_size=phi_grid_size,
        upper_theta_grid_size=upper_theta_grid_size,
        lower_theta_grid_size=lower_theta_grid_size,
    )
    combined_confidence = (
        float(calibration_confidence) + float(covariance_confidence) - 1.0
    )
    if combined_confidence <= 0.0:
        raise ValueError("the union-bound combined confidence must be positive")
    return GaussianCalibratedAR1UniformMatrixChernoffBound(
        autocorrelation_interval=interval,
        matrix_bound=matrix_bound,
        calibration_confidence=float(calibration_confidence),
        covariance_confidence=float(covariance_confidence),
        combined_confidence=float(combined_confidence),
    )


def separable_gaussian_calibrated_ar1_uniform_matrix_covariance(
    observations: ArrayLike,
    nuisance_design: ArrayLike,
    bound: GaussianCalibratedAR1UniformMatrixChernoffBound,
) -> np.ndarray:
    """Return the observable covariance estimator certified by Proposition 48."""
    if not isinstance(bound, GaussianCalibratedAR1UniformMatrixChernoffBound):
        raise TypeError("bound has the wrong type")
    return separable_gaussian_projected_covariance(
        observations,
        nuisance_design,
        bound.reference_projected_degrees_of_freedom,
    )
