"""Certified outer covers for Proposition 51 e-value confidence sets.

Proposition 52 converts the irregular continuum confidence set from Proposition
51 into a finite data-adaptive cover without treating a plotting grid as the
theorem. A parameter cell is discarded only when a deterministic likelihood
perturbation bound proves that every parameter in that cell lies outside the
exact e-value confidence set.

The retained cells therefore contain the complete Proposition 51 continuum
confidence set. For an independent target record, their temporal covariance
centers and deterministic cell radii can be passed to Proposition 49.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .compact_temporal_family import (
    GaussianCompactTemporalFamilyMatrixChernoffBound,
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)
from .evalue_temporal_family import (
    GaussianAR1WhiteNoiseEValueModel,
    gaussian_ar1_white_noise_log_evalue,
)
from .nuisance import temporal_nuisance_projector


@dataclass(frozen=True)
class GaussianEValueTemporalOuterCover:
    """Certified finite outer cover of a Proposition 51 continuum confidence set."""

    model: GaussianAR1WhiteNoiseEValueModel
    autocorrelation_grid: np.ndarray
    white_noise_fraction_grid: np.ndarray
    maximum_autocorrelation_spacing: float
    maximum_white_noise_fraction_spacing: float
    autocorrelation_lipschitz_bound: float
    white_noise_fraction_lipschitz_bound: float
    calibration_operator_cell_radius: float
    calibration_operator_cell_radii: np.ndarray
    center_log_evalues: np.ndarray
    center_minimum_eigenvalues: np.ndarray
    likelihood_variation_bounds: np.ndarray
    certified_excluded_mask: np.ndarray
    retained_cell_mask: np.ndarray
    retained_parameter_centers: np.ndarray
    retained_cell_count: int
    excluded_cell_count: int
    total_cell_count: int
    guarantees_continuum_outer_cover: bool


@dataclass(frozen=True)
class GaussianEValueOuterCoverMatrixChernoffBound:
    """End-to-end target covariance certificate built from Proposition 52."""

    outer_cover: GaussianEValueTemporalOuterCover
    covariance_bound: GaussianCompactTemporalFamilyMatrixChernoffBound
    calibration_confidence: float
    covariance_confidence: float
    combined_confidence_lower_bound: float
    target_eigenvalue_covering_radius: float
    target_normalization_covering_radius: float
    requires_independent_target_record: bool


def _validated_grid_size(value: int, name: str, degenerate: bool) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an integer")
    minimum = 1 if degenerate else 2
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return int(value)


def _grid_with_spacing(lower: float, upper: float, size: int) -> tuple[np.ndarray, float]:
    if lower == upper:
        return np.array([lower], dtype=float), 0.0
    grid = np.linspace(lower, upper, size)
    return grid, float((upper - lower) / (size - 1))


def _ar1_matrix(sample_count: int, autocorrelation: float) -> np.ndarray:
    indices = np.arange(sample_count)
    return float(autocorrelation) ** np.abs(indices[:, None] - indices[None, :])


def _ar1_white_noise_covariance(
    sample_count: int,
    autocorrelation: float,
    white_noise_fraction: float,
) -> np.ndarray:
    ar1 = _ar1_matrix(sample_count, autocorrelation)
    eta = float(white_noise_fraction)
    return (1.0 - eta) * ar1 + eta * np.eye(sample_count)


def _ar1_derivative_matrix(sample_count: int, autocorrelation: float) -> np.ndarray:
    indices = np.arange(sample_count)
    lags = np.abs(indices[:, None] - indices[None, :])
    derivative = np.zeros((sample_count, sample_count), dtype=float)
    mask = lags >= 1
    derivative[mask] = lags[mask] * np.power(
        float(autocorrelation),
        lags[mask] - 1,
    )
    return derivative


def _ar1_second_derivative_row_sum_bound(
    sample_count: int,
    upper_phi: float,
) -> float:
    lags = np.arange(2, sample_count, dtype=float)
    if lags.size == 0:
        return 0.0
    if upper_phi == 0.0:
        powers = np.zeros_like(lags)
        powers[0] = 1.0
    else:
        powers = float(upper_phi) ** (lags - 2.0)
    return float(2.0 * np.sum(lags * (lags - 1.0) * powers))


def _ar1_derivative_operator_bound(sample_count: int, upper_phi: float) -> float:
    lags = np.arange(1, sample_count, dtype=float)
    if upper_phi == 0.0:
        powers = np.zeros_like(lags)
        powers[0] = 1.0
    else:
        powers = float(upper_phi) ** (lags - 1.0)
    return float(2.0 * np.sum(lags * powers))


def _white_noise_direction_operator_bound(sample_count: int, upper_phi: float) -> float:
    ar1_spectral = min(
        float(sample_count),
        (1.0 + float(upper_phi)) / (1.0 - float(upper_phi)),
    )
    return float(max(1.0, ar1_spectral - 1.0))


def _family_lipschitz_bounds(sample_count: int, upper_phi: float) -> tuple[float, float]:
    return (
        _ar1_derivative_operator_bound(sample_count, upper_phi),
        _white_noise_direction_operator_bound(sample_count, upper_phi),
    )


def _symmetric_operator_norm(matrix: np.ndarray) -> float:
    symmetric = 0.5 * (matrix + matrix.T)
    eigenvalues = np.linalg.eigvalsh(symmetric)
    return float(np.max(np.abs(eigenvalues)))


def _compressed_local_cell_operator_radius(
    compression: np.ndarray,
    sample_count: int,
    center_phi: float,
    center_eta: float,
    phi_spacing: float,
    eta_spacing: float,
    lower_eta: float,
    upper_phi: float,
) -> float:
    """Bound compressed covariance motion inside one clipped parameter cell.

    Write ``B`` for a row-orthonormal compression and

    ``C(phi, eta) = B R(phi, eta) B.T``.

    For a cell centered at ``(phi0, eta0)``, use

    ``C(phi, eta) - C(phi0, eta0)``
    ``= (1 - eta) B(R_phi - R_phi0)B.T``
    ``  + (eta - eta0) B(I - R_phi0)B.T``.

    The first derivative at the cell center is evaluated after compression.
    Its between-center variation is bounded by the raw AR(1) second-derivative
    row sum, which remains valid after orthonormal compression. This is sharper
    than applying the raw first-derivative bound everywhere in the box.
    """
    half_phi = 0.5 * float(phi_spacing)
    half_eta = 0.5 * float(eta_spacing)
    local_upper_phi = min(float(upper_phi), float(center_phi) + half_phi)
    local_lower_eta = max(float(lower_eta), float(center_eta) - half_eta)

    derivative_center = _ar1_derivative_matrix(sample_count, center_phi)
    compressed_derivative = compression @ derivative_center @ compression.T
    derivative_change_bound = (
        half_phi
        * _ar1_second_derivative_row_sum_bound(
            sample_count,
            local_upper_phi,
        )
    )
    phi_direction_bound = (
        _symmetric_operator_norm(compressed_derivative)
        + derivative_change_bound
    )

    ar1_center = _ar1_matrix(sample_count, center_phi)
    eta_direction = compression @ (np.eye(sample_count) - ar1_center) @ compression.T
    eta_direction_bound = _symmetric_operator_norm(eta_direction)

    return float(
        half_phi * (1.0 - local_lower_eta) * phi_direction_bound
        + half_eta * eta_direction_bound
    )


def _raw_local_cell_operator_radius(
    sample_count: int,
    center_phi: float,
    center_eta: float,
    phi_spacing: float,
    eta_spacing: float,
    lower_eta: float,
    upper_phi: float,
) -> float:
    """Bound raw temporal covariance motion inside one clipped parameter cell."""
    half_phi = 0.5 * float(phi_spacing)
    half_eta = 0.5 * float(eta_spacing)
    local_upper_phi = min(float(upper_phi), float(center_phi) + half_phi)
    local_lower_eta = max(float(lower_eta), float(center_eta) - half_eta)
    phi_direction_bound = (
        (1.0 - local_lower_eta)
        * _ar1_derivative_operator_bound(sample_count, local_upper_phi)
    )
    eta_direction_bound = _white_noise_direction_operator_bound(
        sample_count,
        local_upper_phi,
    )
    return float(
        half_phi * phi_direction_bound
        + half_eta * eta_direction_bound
    )


def _compressed_covariance(
    model: GaussianAR1WhiteNoiseEValueModel,
    phi: float,
    eta: float,
) -> np.ndarray:
    temporal = _ar1_white_noise_covariance(model.sample_count, phi, eta)
    compressed = model.contrast_matrix @ temporal @ model.contrast_matrix.T
    return 0.5 * (compressed + compressed.T)


def gaussian_log_likelihood_cell_variation_bound(
    minimum_eigenvalue: float,
    operator_radius: float,
    residual_scatter_trace: float,
    residual_dimension: int,
    channel_count: int,
) -> float:
    """Bound log-likelihood variation over one covariance perturbation ball.

    Let ``C0`` be the center covariance with minimum eigenvalue ``m`` and let
    every covariance ``C`` in the cell satisfy ``||C - C0||_2 <= delta < m``.
    For the Gaussian residual log likelihood used by Proposition 51,

    ``|ell(C) - ell(C0)|``

    is at most the returned quantity.
    """
    m = float(minimum_eigenvalue)
    delta = float(operator_radius)
    scatter_trace = float(residual_scatter_trace)
    if not np.isfinite(m) or m <= 0.0:
        raise ValueError("minimum_eigenvalue must be finite and positive")
    if not np.isfinite(delta) or delta < 0.0:
        raise ValueError("operator_radius must be finite and nonnegative")
    if not np.isfinite(scatter_trace) or scatter_trace < 0.0:
        raise ValueError("residual_scatter_trace must be finite and nonnegative")
    for value, name in (
        (residual_dimension, "residual_dimension"),
        (channel_count, "channel_count"),
    ):
        if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
            raise TypeError(f"{name} must be an integer")
        if value < 1:
            raise ValueError(f"{name} must be positive")
    if delta == 0.0:
        return 0.0
    if delta >= m:
        return float("inf")

    ratio = delta / m
    determinant_term = (
        0.5
        * int(channel_count)
        * int(residual_dimension)
        * float(-np.log1p(-ratio))
    )
    inverse_term = 0.5 * scatter_trace * delta / (m * (m - delta))
    return float(determinant_term + inverse_term)


def gaussian_ar1_white_noise_evalue_outer_cover(
    model: GaussianAR1WhiteNoiseEValueModel,
    *,
    autocorrelation_grid_size: int = 33,
    white_noise_fraction_grid_size: int = 21,
) -> GaussianEValueTemporalOuterCover:
    """Return a certified finite outer cover of the Proposition 51 set.

    The parameter grid is fixed by the declared model box and requested sizes.
    It defines Voronoi-style cells with half-grid-spacing radii along each
    parameter coordinate. The data enter only through Proposition 51's
    observed likelihood and determine which cells can be certified as wholly
    outside the exact continuum confidence set.

    Every cell receives its own deterministic compressed covariance radius.
    The radius uses the actual contrast geometry at the cell center plus a
    certified second-derivative remainder across the cell.

    A cell is excluded only when

    ``log_e(center) - likelihood_variation >= log(1 / alpha)``.

    Therefore every point in the exact Proposition 51 confidence set lies in a
    retained cell.
    """
    if not isinstance(model, GaussianAR1WhiteNoiseEValueModel):
        raise TypeError("model has the wrong type")

    lower_phi = model.declared_autocorrelation_lower_bound
    upper_phi = model.declared_autocorrelation_upper_bound
    lower_eta = model.declared_white_noise_fraction_lower_bound
    upper_eta = model.declared_white_noise_fraction_upper_bound

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
    phi_grid, phi_spacing = _grid_with_spacing(lower_phi, upper_phi, phi_count)
    eta_grid, eta_spacing = _grid_with_spacing(lower_eta, upper_eta, eta_count)

    phi_lipschitz, eta_lipschitz = _family_lipschitz_bounds(
        model.sample_count,
        upper_phi,
    )
    scatter_trace = float(np.trace(model.residual_scatter))

    log_evalues = np.empty((phi_grid.size, eta_grid.size), dtype=float)
    minimum_eigenvalues = np.empty_like(log_evalues)
    operator_radii = np.empty_like(log_evalues)
    variations = np.empty_like(log_evalues)

    for phi_index, phi in enumerate(phi_grid):
        for eta_index, eta in enumerate(eta_grid):
            operator_radius = _compressed_local_cell_operator_radius(
                model.contrast_matrix,
                model.sample_count,
                float(phi),
                float(eta),
                phi_spacing,
                eta_spacing,
                lower_eta,
                upper_phi,
            )
            operator_radii[phi_index, eta_index] = operator_radius
            covariance = _compressed_covariance(model, float(phi), float(eta))
            minimum_eigenvalue = float(np.linalg.eigvalsh(covariance)[0])
            minimum_eigenvalues[phi_index, eta_index] = minimum_eigenvalue
            log_evalues[phi_index, eta_index] = gaussian_ar1_white_noise_log_evalue(
                model,
                float(phi),
                float(eta),
            )
            variations[phi_index, eta_index] = (
                gaussian_log_likelihood_cell_variation_bound(
                    minimum_eigenvalue,
                    operator_radius,
                    scatter_trace,
                    model.contrast_dimension,
                    model.channel_count,
                )
            )

    excluded = log_evalues - variations >= model.log_evalue_threshold
    retained = ~excluded
    centers = np.array(
        [
            (float(phi), float(eta))
            for phi_index, phi in enumerate(phi_grid)
            for eta_index, eta in enumerate(eta_grid)
            if retained[phi_index, eta_index]
        ],
        dtype=float,
    )
    if centers.size == 0:
        centers = np.empty((0, 2), dtype=float)

    return GaussianEValueTemporalOuterCover(
        model=model,
        autocorrelation_grid=phi_grid,
        white_noise_fraction_grid=eta_grid,
        maximum_autocorrelation_spacing=phi_spacing,
        maximum_white_noise_fraction_spacing=eta_spacing,
        autocorrelation_lipschitz_bound=phi_lipschitz,
        white_noise_fraction_lipschitz_bound=eta_lipschitz,
        calibration_operator_cell_radius=float(np.max(operator_radii)),
        calibration_operator_cell_radii=operator_radii,
        center_log_evalues=log_evalues,
        center_minimum_eigenvalues=minimum_eigenvalues,
        likelihood_variation_bounds=variations,
        certified_excluded_mask=excluded,
        retained_cell_mask=retained,
        retained_parameter_centers=centers,
        retained_cell_count=int(np.sum(retained)),
        excluded_cell_count=int(np.sum(excluded)),
        total_cell_count=int(retained.size),
        guarantees_continuum_outer_cover=True,
    )


def _validated_nuisance_design(nuisance_design: ArrayLike) -> np.ndarray:
    design = np.asarray(nuisance_design, dtype=float)
    if design.ndim == 1:
        design = design[:, None]
    if design.ndim != 2 or design.shape[0] < 2 or design.shape[1] < 1:
        raise ValueError("nuisance_design must be a nonempty two-dimensional design")
    if not np.all(np.isfinite(design)):
        raise ValueError("nuisance_design must be finite")
    rank = int(np.linalg.matrix_rank(design))
    if rank != design.shape[1] or rank >= design.shape[0]:
        raise ValueError("nuisance_design must have full column rank below sample_count")
    return design


def _nuisance_complement(design: np.ndarray) -> np.ndarray:
    basis, _ = np.linalg.qr(design, mode="complete")
    return basis[:, design.shape[1] :]


def gaussian_evalue_outer_cover_matrix_chernoff_bound(
    model: GaussianAR1WhiteNoiseEValueModel,
    block_dimension: int,
    block_count: int,
    nuisance_design: ArrayLike,
    *,
    outer_autocorrelation_grid_size: int = 33,
    outer_white_noise_fraction_grid_size: int = 21,
    covariance_confidence: float = 0.9875,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianEValueOuterCoverMatrixChernoffBound:
    """Compose the Proposition 52 outer cover with Proposition 49.

    The target record must be independent of the calibration record used to
    construct ``model`` and must share the same true temporal parameters. On
    the Proposition 51 calibration event, the true temporal covariance lies in
    one retained Proposition 52 cell. Conditional on the calibration record,
    those cells are fixed and Proposition 49 applies to the independent target.

    The eigenvalue cover uses compressed cell radii for the target nuisance
    complement. The normalization cover is separate: all family members have
    trace equal to ``sample_count``, so for ``P = I - Q`` with nuisance rank
    ``q``, ``tr(P Delta R) = -tr(Q Delta R)`` and its absolute value is at most
    ``q ||Delta R||_2``. The normalization radius therefore uses the retained
    raw temporal cell radii, not the compressed eigenvalue radius.
    """
    if not 0.0 < covariance_confidence < 1.0:
        raise ValueError("covariance_confidence must lie in (0, 1)")

    outer_cover = gaussian_ar1_white_noise_evalue_outer_cover(
        model,
        autocorrelation_grid_size=outer_autocorrelation_grid_size,
        white_noise_fraction_grid_size=outer_white_noise_fraction_grid_size,
    )
    if outer_cover.retained_cell_count < 1:
        raise ValueError(
            "the observed certified outer cover is empty; no target certificate is issued"
        )

    design = _validated_nuisance_design(nuisance_design)
    target_sample_count = design.shape[0]
    nuisance_rank = design.shape[1]
    lower_eta = model.declared_white_noise_fraction_lower_bound
    upper_phi = model.declared_autocorrelation_upper_bound
    target_compression = _nuisance_complement(design).T

    retained_target_eigenvalue_radii = np.asarray(
        [
            _compressed_local_cell_operator_radius(
                target_compression,
                target_sample_count,
                float(phi),
                float(eta),
                outer_cover.maximum_autocorrelation_spacing,
                outer_cover.maximum_white_noise_fraction_spacing,
                lower_eta,
                upper_phi,
            )
            for phi, eta in outer_cover.retained_parameter_centers
        ],
        dtype=float,
    )
    retained_target_raw_radii = np.asarray(
        [
            _raw_local_cell_operator_radius(
                target_sample_count,
                float(phi),
                float(eta),
                outer_cover.maximum_autocorrelation_spacing,
                outer_cover.maximum_white_noise_fraction_spacing,
                lower_eta,
                upper_phi,
            )
            for phi, eta in outer_cover.retained_parameter_centers
        ],
        dtype=float,
    )
    target_eigenvalue_radius = float(np.max(retained_target_eigenvalue_radii))
    target_normalization_radius = float(
        nuisance_rank * np.max(retained_target_raw_radii)
    )

    temporal_grid = np.asarray(
        [
            _ar1_white_noise_covariance(target_sample_count, phi, eta)
            for phi, eta in outer_cover.retained_parameter_centers
        ],
        dtype=float,
    )
    covariance_bound = gaussian_compact_temporal_family_matrix_chernoff_bound(
        block_dimension,
        block_count,
        temporal_grid,
        design,
        eigenvalue_covering_radius=target_eigenvalue_radius,
        normalization_covering_radius=target_normalization_radius,
        confidence=covariance_confidence,
        upper_theta_grid_size=upper_theta_grid_size,
        lower_theta_grid_size=lower_theta_grid_size,
    )

    return GaussianEValueOuterCoverMatrixChernoffBound(
        outer_cover=outer_cover,
        covariance_bound=covariance_bound,
        calibration_confidence=float(model.confidence),
        covariance_confidence=float(covariance_confidence),
        combined_confidence_lower_bound=float(
            model.confidence * covariance_confidence
        ),
        target_eigenvalue_covering_radius=target_eigenvalue_radius,
        target_normalization_covering_radius=target_normalization_radius,
        requires_independent_target_record=True,
    )


def separable_gaussian_evalue_outer_cover_projected_covariance(
    target_observations: ArrayLike,
    nuisance_design: ArrayLike,
    bound: GaussianEValueOuterCoverMatrixChernoffBound,
) -> np.ndarray:
    """Estimate spatial covariance using Proposition 52's reference normalization."""
    if not isinstance(bound, GaussianEValueOuterCoverMatrixChernoffBound):
        raise TypeError("bound has the wrong type")
    values = np.asarray(target_observations, dtype=float)
    if values.ndim == 1:
        values = values[:, None]
    if values.ndim != 2 or not np.all(np.isfinite(values)):
        raise ValueError("target_observations must be a finite matrix")
    projector = temporal_nuisance_projector(nuisance_design)
    if projector.shape[0] != values.shape[0]:
        raise ValueError("nuisance_design and target_observations must share sample_count")
    degrees = bound.covariance_bound.reference_projected_degrees_of_freedom
    return (values.T @ projector @ values) / degrees
