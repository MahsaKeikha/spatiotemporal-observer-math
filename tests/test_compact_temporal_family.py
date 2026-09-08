import numpy as np

from observer_math.compact_temporal_family import (
    gaussian_ar1_white_noise_temporal_cover,
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)
from observer_math.matrix_chernoff import (
    gaussian_projected_weighted_wishart_matrix_bound,
)
from observer_math.nuisance import temporal_nuisance_projector


def _ar1_matrix(sample_count, phi):
    indices = np.arange(sample_count)
    return phi ** np.abs(indices[:, None] - indices[None, :])


def _temporal_member(sample_count, phi, eta):
    return (1.0 - eta) * _ar1_matrix(sample_count, phi) + eta * np.eye(sample_count)


def _affine_design(sample_count):
    time = np.linspace(-1.0, 1.0, sample_count)
    return np.column_stack((np.ones_like(time), time))


def _sphere_net_family_radius(
    block_dimension,
    block_count,
    temporal_grid,
    design,
    eigenvalue_covering_radius,
    normalization_covering_radius,
    confidence,
):
    basis, _ = np.linalg.qr(design, mode="complete")
    complement = basis[:, design.shape[1] :]
    frobenius = []
    spectral = []
    degrees = []
    for temporal in temporal_grid:
        compressed = complement.T @ temporal @ complement
        eigenvalues = np.maximum(np.linalg.eigvalsh(compressed), 0.0)
        frobenius.append(float(np.linalg.norm(eigenvalues)))
        spectral.append(float(eigenvalues[-1]))
        degrees.append(float(np.sum(eigenvalues)))

    projected_rank = complement.shape[1]
    f_plus = max(frobenius) + np.sqrt(projected_rank) * eigenvalue_covering_radius
    s_plus = max(spectral) + eigenvalue_covering_radius
    d_lower = min(degrees) - normalization_covering_radius
    d_upper = max(degrees) + normalization_covering_radius
    tail = np.log(
        2.0 * block_count * 9.0**block_dimension / (1.0 - confidence)
    )
    oracle = 4.0 * (f_plus * np.sqrt(tail) + s_plus * tail) / d_lower
    reference = 0.5 * (d_lower + d_upper)
    a = d_lower / reference
    b = d_upper / reference
    return float(
        max(
            abs(a - 1.0) + a * oracle,
            abs(b - 1.0) + b * oracle,
        )
    )


def test_zero_radius_single_cover_point_recovers_proposition_47():
    sample_count = 55
    design = _affine_design(sample_count)
    temporal = _temporal_member(sample_count, 0.48, 0.03)

    exact = gaussian_projected_weighted_wishart_matrix_bound(
        3,
        1,
        temporal,
        design,
        confidence=0.95,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )
    generic = gaussian_compact_temporal_family_matrix_chernoff_bound(
        3,
        1,
        temporal[None, :, :],
        design,
        eigenvalue_covering_radius=0.0,
        normalization_covering_radius=0.0,
        confidence=0.95,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )

    assert np.isclose(
        generic.oracle_upper_deviation,
        exact.upper_deviation,
        rtol=1e-10,
        atol=1e-10,
    )
    assert np.isclose(
        generic.oracle_lower_deviation,
        exact.lower_deviation,
        rtol=1e-10,
        atol=1e-10,
    )
    assert np.isclose(
        generic.covariance_relative_error,
        exact.relative_covariance_error,
        rtol=1e-9,
        atol=1e-9,
    )


def test_ar1_white_noise_cover_contains_dense_two_parameter_family():
    sample_count = 42
    design = _affine_design(sample_count)
    cover = gaussian_ar1_white_noise_temporal_cover(
        design,
        0.30,
        0.58,
        0.0,
        0.06,
        autocorrelation_grid_size=8,
        white_noise_fraction_grid_size=5,
    )
    projector = temporal_nuisance_projector(design)

    for phi in np.linspace(0.30, 0.58, 15):
        phi_index = int(np.argmin(np.abs(cover.autocorrelation_grid - phi)))
        for eta in np.linspace(0.0, 0.06, 11):
            eta_index = int(
                np.argmin(np.abs(cover.white_noise_fraction_grid - eta))
            )
            grid_index = (
                phi_index * cover.white_noise_fraction_grid.size + eta_index
            )
            temporal = _temporal_member(sample_count, float(phi), float(eta))
            grid_temporal = cover.temporal_covariance_grid[grid_index]
            raw_distance = float(np.linalg.norm(temporal - grid_temporal, ord=2))
            projected_distance = float(
                np.linalg.norm(
                    projector @ (temporal - grid_temporal) @ projector,
                    ord=2,
                )
            )
            normalization_distance = abs(
                float(np.trace(projector @ (temporal - grid_temporal)))
            )

            assert raw_distance <= cover.raw_operator_covering_radius + 1e-10
            assert (
                projected_distance
                <= cover.projected_eigenvalue_covering_radius + 1e-10
            )
            assert (
                normalization_distance
                <= cover.projected_normalization_covering_radius + 1e-10
            )


def test_compact_family_oracle_dominates_dense_known_parameter_bounds():
    sample_count = 48
    design = _affine_design(sample_count)
    cover = gaussian_ar1_white_noise_temporal_cover(
        design,
        0.35,
        0.55,
        0.0,
        0.04,
        autocorrelation_grid_size=7,
        white_noise_fraction_grid_size=5,
    )
    generic = gaussian_compact_temporal_family_matrix_chernoff_bound(
        3,
        1,
        cover.temporal_covariance_grid,
        design,
        eigenvalue_covering_radius=cover.projected_eigenvalue_covering_radius,
        normalization_covering_radius=(
            cover.projected_normalization_covering_radius
        ),
        confidence=0.95,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )

    for phi in np.linspace(0.35, 0.55, 5):
        for eta in np.linspace(0.0, 0.04, 3):
            exact = gaussian_projected_weighted_wishart_matrix_bound(
                3,
                1,
                _temporal_member(sample_count, float(phi), float(eta)),
                design,
                confidence=0.95,
                upper_theta_grid_size=256,
                lower_theta_grid_size=256,
            )
            assert exact.relative_covariance_error <= generic.oracle_relative_error + 1e-9


def test_compact_family_matrix_bound_beats_sphere_net_family_bound():
    sample_count = 70
    design = _affine_design(sample_count)
    cover = gaussian_ar1_white_noise_temporal_cover(
        design,
        0.45,
        0.65,
        0.0,
        0.05,
        autocorrelation_grid_size=9,
        white_noise_fraction_grid_size=5,
    )
    matrix = gaussian_compact_temporal_family_matrix_chernoff_bound(
        3,
        1,
        cover.temporal_covariance_grid,
        design,
        eigenvalue_covering_radius=cover.projected_eigenvalue_covering_radius,
        normalization_covering_radius=(
            cover.projected_normalization_covering_radius
        ),
        confidence=0.95,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )
    sphere = _sphere_net_family_radius(
        3,
        1,
        cover.temporal_covariance_grid,
        design,
        cover.projected_eigenvalue_covering_radius,
        cover.projected_normalization_covering_radius,
        0.95,
    )

    assert matrix.covariance_relative_error < sphere


def test_larger_covering_radii_do_not_improve_certificate():
    sample_count = 55
    design = _affine_design(sample_count)
    cover = gaussian_ar1_white_noise_temporal_cover(
        design,
        0.40,
        0.55,
        0.0,
        0.03,
        autocorrelation_grid_size=7,
        white_noise_fraction_grid_size=4,
    )

    tight = gaussian_compact_temporal_family_matrix_chernoff_bound(
        3,
        1,
        cover.temporal_covariance_grid,
        design,
        eigenvalue_covering_radius=cover.projected_eigenvalue_covering_radius,
        normalization_covering_radius=(
            cover.projected_normalization_covering_radius
        ),
        confidence=0.95,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )
    loose = gaussian_compact_temporal_family_matrix_chernoff_bound(
        3,
        1,
        cover.temporal_covariance_grid,
        design,
        eigenvalue_covering_radius=1.5 * cover.projected_eigenvalue_covering_radius,
        normalization_covering_radius=(
            1.5 * cover.projected_normalization_covering_radius
        ),
        confidence=0.95,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )

    assert loose.covariance_relative_error >= tight.covariance_relative_error
