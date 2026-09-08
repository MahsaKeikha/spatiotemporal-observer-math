"""Matrix concentration over compact temporal covariance families.

Proposition 49 abstracts the continuum argument from Proposition 48. Instead
of requiring a one-parameter AR(1) interval, it starts from a finite cover of a
compact temporal covariance family together with certified operator and
normalization covering radii.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .uniform_matrix_chernoff import (
    _log_matrix_mgf_factor,
    _validated_design,
    _validated_grid_size,
)


@dataclass(frozen=True)
class GaussianCompactTemporalFamilyMatrixChernoffBound:
    """Uniform covariance certificate over a covered temporal covariance family."""

    block_dimension: int
    block_count: int
    covariance_confidence: float
    sample_count: int
    nuisance_rank: int
    projected_temporal_rank: int
    cover_point_count: int
    eigenvalue_covering_radius: float
    normalization_covering_radius: float
    projected_degrees_of_freedom_lower_bound: float
    projected_degrees_of_freedom_upper_bound: float
    projected_spectral_norm_bound: float
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
class GaussianAR1WhiteNoiseTemporalCover:
    """Finite product-grid cover for an AR(1) plus white-noise temporal family."""

    temporal_covariance_grid: np.ndarray
    autocorrelation_grid: np.ndarray
    white_noise_fraction_grid: np.ndarray
    autocorrelation_lower_bound: float
    autocorrelation_upper_bound: float
    white_noise_fraction_lower_bound: float
    white_noise_fraction_upper_bound: float
    maximum_autocorrelation_spacing: float
    maximum_white_noise_fraction_spacing: float
    autocorrelation_lipschitz_bound: float
    white_noise_fraction_lipschitz_bound: float
    raw_operator_covering_radius: float
    projected_eigenvalue_covering_radius: float
    projected_normalization_covering_radius: float


def _validated_nonnegative_radius(value: float, name: str) -> float:
    radius = float(value)
    if not np.isfinite(radius) or radius < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return radius


def _validated_temporal_grid(
    temporal_covariance_grid: ArrayLike,
    sample_count: int,
) -> np.ndarray:
    grid = np.asarray(temporal_covariance_grid, dtype=float)
    if grid.ndim == 2:
        grid = grid[None, :, :]
    if grid.ndim != 3 or grid.shape[1:] != (sample_count, sample_count):
        raise ValueError(
            "temporal_covariance_grid must have shape "
            "(cover_points, sample_count, sample_count)"
        )
    if grid.shape[0] < 1 or not np.all(np.isfinite(grid)):
        raise ValueError("temporal_covariance_grid must contain finite cover points")

    checked = np.empty_like(grid)
    for index, temporal in enumerate(grid):
        scale = max(1.0, float(np.linalg.norm(temporal, ord=2)))
        tolerance = 1e-10 * scale
        if float(np.linalg.norm(temporal - temporal.T, ord=2)) > tolerance:
            raise ValueError("every temporal cover matrix must be symmetric")
        symmetric = 0.5 * (temporal + temporal.T)
        eigenvalues = np.linalg.eigvalsh(symmetric)
        if eigenvalues[0] < -tolerance:
            raise ValueError("every temporal cover matrix must be positive semidefinite")
        checked[index] = symmetric
    return checked


def _nuisance_complement(design: np.ndarray) -> np.ndarray:
    basis, _ = np.linalg.qr(design, mode="complete")
    return basis[:, design.shape[1] :]


def gaussian_compact_temporal_family_matrix_chernoff_bound(
    block_dimension: int,
    block_count: int,
    temporal_covariance_grid: ArrayLike,
    nuisance_design: ArrayLike,
    *,
    eigenvalue_covering_radius: float,
    normalization_covering_radius: float,
    confidence: float = 0.975,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianCompactTemporalFamilyMatrixChernoffBound:
    """Certify covariance over any temporal family with a valid finite cover.

    Let ``U`` span the orthogonal complement of the nuisance design and let
    ``C(R)=U.T @ R @ U``. The caller must certify two deterministic facts for
    the intended temporal family:

    1. every admissible ``C(R)`` lies within ``eigenvalue_covering_radius`` in
       operator norm of at least one supplied cover matrix after compression;
    2. its projected normalization ``tr(P R)`` lies within
       ``normalization_covering_radius`` of the corresponding cover-point
       normalization.

    Weyl's inequality then inflates every ordered compressed temporal
    eigenvalue by the first radius. Proposition 47's exact Gaussian matrix-mgf
    factors are monotone in every nonnegative temporal eigenvalue, so the
    inflated cover spectra dominate the entire family.

    The finite theta grids affect numerical tightness only. Every individual
    theta candidate already yields a valid bound under the declared cover.
    """
    if isinstance(block_dimension, bool) or not isinstance(
        block_dimension, (int, np.integer)
    ):
        raise TypeError("block_dimension must be an integer")
    if isinstance(block_count, bool) or not isinstance(block_count, (int, np.integer)):
        raise TypeError("block_count must be an integer")
    if block_dimension < 1 or block_count < 1:
        raise ValueError("block_dimension and block_count must be positive")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")

    upper_theta_count = _validated_grid_size(
        upper_theta_grid_size, "upper_theta_grid_size"
    )
    lower_theta_count = _validated_grid_size(
        lower_theta_grid_size, "lower_theta_grid_size"
    )
    eigenvalue_delta = _validated_nonnegative_radius(
        eigenvalue_covering_radius, "eigenvalue_covering_radius"
    )
    normalization_delta = _validated_nonnegative_radius(
        normalization_covering_radius, "normalization_covering_radius"
    )

    design = _validated_design(nuisance_design)
    sample_count, nuisance_rank = design.shape
    complement = _nuisance_complement(design)
    projected_rank = complement.shape[1]
    grid = _validated_temporal_grid(temporal_covariance_grid, sample_count)

    spectra: list[np.ndarray] = []
    degrees: list[float] = []
    for temporal in grid:
        compressed = complement.T @ temporal @ complement
        compressed = 0.5 * (compressed + compressed.T)
        eigenvalues = np.linalg.eigvalsh(compressed)
        scale = max(1.0, float(np.max(np.abs(eigenvalues))))
        tolerance = 1e-11 * scale
        if eigenvalues[0] < -tolerance:
            raise RuntimeError("projected temporal covariance lost positive semidefiniteness")
        spectrum = np.maximum(eigenvalues, 0.0)
        spectra.append(spectrum)
        degrees.append(float(np.sum(spectrum)))

    degrees_lower = min(degrees) - normalization_delta
    degrees_upper = max(degrees) + normalization_delta
    if degrees_lower <= 0.0 or degrees_upper < degrees_lower:
        raise ValueError("the temporal family cover leaves no positive normalization")

    inflated_spectra = [spectrum + eigenvalue_delta for spectrum in spectra]
    spectral_bound = max(float(np.max(spectrum)) for spectrum in inflated_spectra)
    if spectral_bound <= 0.0:
        raise ValueError("the temporal family cover leaves no positive covariance information")

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
        upper_values[index] = (
            log_prefactor + worst_log_mgf
        ) / theta / degrees_lower
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
        lower_values[index] = (
            log_prefactor + worst_log_mgf
        ) / theta / degrees_lower
    lower_index = int(np.argmin(lower_values))
    oracle_lower = float(min(1.0, lower_values[lower_index]))
    oracle_relative = float(max(oracle_upper, oracle_lower))

    reference_degrees = 0.5 * (degrees_lower + degrees_upper)
    ratio_lower = degrees_lower / reference_degrees
    ratio_upper = degrees_upper / reference_degrees
    final_upper = float(ratio_upper * (1.0 + oracle_upper) - 1.0)
    final_lower = float(max(0.0, 1.0 - ratio_lower * (1.0 - oracle_lower)))
    final_relative = float(max(final_upper, final_lower))

    return GaussianCompactTemporalFamilyMatrixChernoffBound(
        block_dimension=int(block_dimension),
        block_count=int(block_count),
        covariance_confidence=float(confidence),
        sample_count=int(sample_count),
        nuisance_rank=int(nuisance_rank),
        projected_temporal_rank=int(projected_rank),
        cover_point_count=int(grid.shape[0]),
        eigenvalue_covering_radius=float(eigenvalue_delta),
        normalization_covering_radius=float(normalization_delta),
        projected_degrees_of_freedom_lower_bound=float(degrees_lower),
        projected_degrees_of_freedom_upper_bound=float(degrees_upper),
        projected_spectral_norm_bound=float(spectral_bound),
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


def _ar1_matrix(sample_count: int, autocorrelation: float) -> np.ndarray:
    indices = np.arange(sample_count)
    return autocorrelation ** np.abs(indices[:, None] - indices[None, :])


def _ar1_spectral_derivative_bound(sample_count: int, upper: float) -> float:
    lags = np.arange(1, sample_count, dtype=float)
    if upper == 0.0:
        powers = np.zeros_like(lags)
        powers[0] = 1.0
    else:
        powers = upper ** (lags - 1.0)
    return float(2.0 * np.sum(lags * powers))


def gaussian_ar1_white_noise_temporal_cover(
    nuisance_design: ArrayLike,
    lower_autocorrelation: float,
    upper_autocorrelation: float,
    lower_white_noise_fraction: float,
    upper_white_noise_fraction: float,
    *,
    autocorrelation_grid_size: int = 17,
    white_noise_fraction_grid_size: int = 9,
) -> GaussianAR1WhiteNoiseTemporalCover:
    """Build a rigorous product-grid cover for a two-parameter temporal family.

    The family is

    ``R(phi, eta) = (1 - eta) R_phi + eta I``

    with ``phi`` and ``eta`` in the supplied intervals. Every matrix is a
    correlation matrix because both terms are positive semidefinite with unit
    diagonal.

    The operator cover uses coordinatewise derivative bounds. Since every
    family member has trace ``N``, the projected normalization can change by at
    most ``q`` times the same raw operator radius, where ``q`` is the nuisance
    rank.
    """
    design = _validated_design(nuisance_design)
    sample_count, nuisance_rank = design.shape

    lower_phi = float(lower_autocorrelation)
    upper_phi = float(upper_autocorrelation)
    lower_eta = float(lower_white_noise_fraction)
    upper_eta = float(upper_white_noise_fraction)
    if not 0.0 <= lower_phi <= upper_phi < 1.0:
        raise ValueError("require 0 <= lower_autocorrelation <= upper_autocorrelation < 1")
    if not 0.0 <= lower_eta <= upper_eta <= 1.0:
        raise ValueError(
            "require 0 <= lower_white_noise_fraction <= upper_white_noise_fraction <= 1"
        )
    for value, name, degenerate in (
        (autocorrelation_grid_size, "autocorrelation_grid_size", lower_phi == upper_phi),
        (
            white_noise_fraction_grid_size,
            "white_noise_fraction_grid_size",
            lower_eta == upper_eta,
        ),
    ):
        if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
            raise TypeError(f"{name} must be an integer")
        minimum = 1 if degenerate else 2
        if value < minimum:
            raise ValueError(f"{name} must be at least {minimum}")

    if lower_phi == upper_phi:
        phi_grid = np.array([lower_phi], dtype=float)
        phi_spacing = 0.0
    else:
        phi_grid = np.linspace(lower_phi, upper_phi, int(autocorrelation_grid_size))
        phi_spacing = float((upper_phi - lower_phi) / (phi_grid.size - 1))

    if lower_eta == upper_eta:
        eta_grid = np.array([lower_eta], dtype=float)
        eta_spacing = 0.0
    else:
        eta_grid = np.linspace(lower_eta, upper_eta, int(white_noise_fraction_grid_size))
        eta_spacing = float((upper_eta - lower_eta) / (eta_grid.size - 1))

    identity = np.eye(sample_count)
    covariances = []
    ar1_by_phi = {float(phi): _ar1_matrix(sample_count, float(phi)) for phi in phi_grid}
    for phi in phi_grid:
        temporal_ar1 = ar1_by_phi[float(phi)]
        for eta in eta_grid:
            covariances.append((1.0 - eta) * temporal_ar1 + eta * identity)

    phi_lipschitz = _ar1_spectral_derivative_bound(sample_count, upper_phi)
    ar1_spectral_bound = min(
        float(sample_count),
        (1.0 + upper_phi) / (1.0 - upper_phi),
    )
    eta_lipschitz = max(1.0, ar1_spectral_bound - 1.0)
    raw_radius = (
        phi_lipschitz * 0.5 * phi_spacing
        + eta_lipschitz * 0.5 * eta_spacing
    )

    return GaussianAR1WhiteNoiseTemporalCover(
        temporal_covariance_grid=np.asarray(covariances),
        autocorrelation_grid=phi_grid,
        white_noise_fraction_grid=eta_grid,
        autocorrelation_lower_bound=lower_phi,
        autocorrelation_upper_bound=upper_phi,
        white_noise_fraction_lower_bound=lower_eta,
        white_noise_fraction_upper_bound=upper_eta,
        maximum_autocorrelation_spacing=phi_spacing,
        maximum_white_noise_fraction_spacing=eta_spacing,
        autocorrelation_lipschitz_bound=phi_lipschitz,
        white_noise_fraction_lipschitz_bound=float(eta_lipschitz),
        raw_operator_covering_radius=float(raw_radius),
        projected_eigenvalue_covering_radius=float(raw_radius),
        projected_normalization_covering_radius=float(nuisance_rank * raw_radius),
    )
