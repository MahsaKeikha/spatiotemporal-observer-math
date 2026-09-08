import numpy as np

from observer_math.evalue_outer_cover import (
    gaussian_ar1_white_noise_evalue_outer_cover,
    gaussian_evalue_outer_cover_matrix_chernoff_bound,
    gaussian_log_likelihood_cell_variation_bound,
    separable_gaussian_evalue_outer_cover_projected_covariance,
)
from observer_math.evalue_temporal_family import (
    gaussian_ar1_white_noise_evalue_model,
    gaussian_ar1_white_noise_log_evalue,
)


def _temporal_covariance(sample_count, phi, eta):
    indices = np.arange(sample_count)
    ar1 = phi ** np.abs(indices[:, None] - indices[None, :])
    return (1.0 - eta) * ar1 + eta * np.eye(sample_count)


def _simulate_channels(sample_count, channel_count, phi, eta, rng):
    temporal = _temporal_covariance(sample_count, phi, eta)
    return np.linalg.cholesky(temporal) @ rng.normal(size=(sample_count, channel_count))


def _nearest_index(grid, value):
    return int(np.argmin(np.abs(grid - value)))


def test_likelihood_variation_bound_covers_cell_corners():
    rng = np.random.default_rng(20261110)
    values = _simulate_channels(42, 20, 0.52, 0.025, rng)
    model = gaussian_ar1_white_noise_evalue_model(
        values,
        lower_autocorrelation=0.40,
        upper_autocorrelation=0.64,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.08,
        confidence=0.95,
        contrast_dimension=10,
        mixture_autocorrelation_grid_size=5,
        mixture_white_noise_fraction_grid_size=3,
    )
    cover = gaussian_ar1_white_noise_evalue_outer_cover(
        model,
        autocorrelation_grid_size=17,
        white_noise_fraction_grid_size=9,
    )

    phi_index = 8
    eta_index = 4
    center_phi = float(cover.autocorrelation_grid[phi_index])
    center_eta = float(cover.white_noise_fraction_grid[eta_index])
    center_log_evalue = cover.center_log_evalues[phi_index, eta_index]
    variation = cover.likelihood_variation_bounds[phi_index, eta_index]
    half_phi = 0.5 * cover.maximum_autocorrelation_spacing
    half_eta = 0.5 * cover.maximum_white_noise_fraction_spacing

    assert np.isfinite(variation)
    for phi in (center_phi - half_phi, center_phi + half_phi):
        for eta in (center_eta - half_eta, center_eta + half_eta):
            corner_log_evalue = gaussian_ar1_white_noise_log_evalue(
                model, phi, eta
            )
            assert abs(corner_log_evalue - center_log_evalue) <= variation + 1e-10


def test_every_dense_accepted_point_lies_in_a_retained_cell():
    rng = np.random.default_rng(20261111)
    values = _simulate_channels(45, 48, 0.54, 0.03, rng)
    model = gaussian_ar1_white_noise_evalue_model(
        values,
        lower_autocorrelation=0.40,
        upper_autocorrelation=0.68,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.10,
        confidence=0.95,
        contrast_dimension=10,
        mixture_autocorrelation_grid_size=5,
        mixture_white_noise_fraction_grid_size=3,
    )
    cover = gaussian_ar1_white_noise_evalue_outer_cover(
        model,
        autocorrelation_grid_size=15,
        white_noise_fraction_grid_size=9,
    )

    accepted_count = 0
    for phi in np.linspace(0.40, 0.68, 35):
        for eta in np.linspace(0.0, 0.10, 25):
            log_evalue = gaussian_ar1_white_noise_log_evalue(model, phi, eta)
            if log_evalue < model.log_evalue_threshold:
                accepted_count += 1
                phi_index = _nearest_index(cover.autocorrelation_grid, phi)
                eta_index = _nearest_index(cover.white_noise_fraction_grid, eta)
                assert cover.retained_cell_mask[phi_index, eta_index]

    assert accepted_count > 0
    assert cover.guarantees_continuum_outer_cover


def test_outer_cover_is_invariant_to_arbitrary_constant_channel_offsets():
    rng = np.random.default_rng(20261112)
    values = _simulate_channels(38, 16, 0.50, 0.02, rng)
    offsets = np.linspace(-100.0, 80.0, values.shape[1])
    shifted = values + offsets[None, :]

    kwargs = dict(
        lower_autocorrelation=0.36,
        upper_autocorrelation=0.64,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.08,
        confidence=0.95,
        contrast_dimension=9,
        mixture_autocorrelation_grid_size=5,
        mixture_white_noise_fraction_grid_size=3,
    )
    base_model = gaussian_ar1_white_noise_evalue_model(values, **kwargs)
    shifted_model = gaussian_ar1_white_noise_evalue_model(shifted, **kwargs)
    base_cover = gaussian_ar1_white_noise_evalue_outer_cover(
        base_model,
        autocorrelation_grid_size=13,
        white_noise_fraction_grid_size=7,
    )
    shifted_cover = gaussian_ar1_white_noise_evalue_outer_cover(
        shifted_model,
        autocorrelation_grid_size=13,
        white_noise_fraction_grid_size=7,
    )

    assert np.allclose(base_model.residual_scatter, shifted_model.residual_scatter, atol=1e-9)
    assert np.allclose(base_cover.center_log_evalues, shifted_cover.center_log_evalues, atol=1e-8)
    assert np.allclose(
        base_cover.likelihood_variation_bounds,
        shifted_cover.likelihood_variation_bounds,
        atol=1e-8,
    )
    assert np.array_equal(base_cover.retained_cell_mask, shifted_cover.retained_cell_mask)


def test_certified_excluded_cells_reject_sampled_interior_points():
    rng = np.random.default_rng(20261113)
    values = _simulate_channels(36, 192, 0.51, 0.02, rng)
    model = gaussian_ar1_white_noise_evalue_model(
        values,
        lower_autocorrelation=0.40,
        upper_autocorrelation=0.62,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.06,
        confidence=0.95,
        contrast_dimension=7,
        mixture_autocorrelation_grid_size=5,
        mixture_white_noise_fraction_grid_size=3,
    )
    cover = gaussian_ar1_white_noise_evalue_outer_cover(
        model,
        autocorrelation_grid_size=33,
        white_noise_fraction_grid_size=17,
    )

    excluded_indices = np.argwhere(cover.certified_excluded_mask)
    assert excluded_indices.shape[0] > 0
    half_phi = 0.5 * cover.maximum_autocorrelation_spacing
    half_eta = 0.5 * cover.maximum_white_noise_fraction_spacing

    for phi_index, eta_index in excluded_indices[:12]:
        center_phi = float(cover.autocorrelation_grid[phi_index])
        center_eta = float(cover.white_noise_fraction_grid[eta_index])
        for u, v in ((0.0, 0.0), (-0.4, 0.3), (0.35, -0.25)):
            phi = float(
                np.clip(
                    center_phi + 2.0 * u * half_phi,
                    model.declared_autocorrelation_lower_bound,
                    model.declared_autocorrelation_upper_bound,
                )
            )
            eta = float(
                np.clip(
                    center_eta + 2.0 * v * half_eta,
                    model.declared_white_noise_fraction_lower_bound,
                    model.declared_white_noise_fraction_upper_bound,
                )
            )
            assert (
                gaussian_ar1_white_noise_log_evalue(model, phi, eta)
                >= model.log_evalue_threshold - 1e-10
            )


def test_outer_cover_composes_with_proposition_49_and_preserves_nuisance_invariance():
    rng = np.random.default_rng(20261114)
    calibration = _simulate_channels(40, 48, 0.47, 0.02, rng)
    model = gaussian_ar1_white_noise_evalue_model(
        calibration,
        lower_autocorrelation=0.36,
        upper_autocorrelation=0.58,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.06,
        confidence=0.95,
        contrast_dimension=8,
        mixture_autocorrelation_grid_size=5,
        mixture_white_noise_fraction_grid_size=3,
    )

    target_count = 48
    time = np.linspace(-1.0, 1.0, target_count)
    design = np.column_stack((np.ones_like(time), time))
    bound = gaussian_evalue_outer_cover_matrix_chernoff_bound(
        model,
        block_dimension=3,
        block_count=1,
        nuisance_design=design,
        outer_autocorrelation_grid_size=9,
        outer_white_noise_fraction_grid_size=5,
        covariance_confidence=0.95,
        upper_theta_grid_size=128,
        lower_theta_grid_size=128,
    )

    assert bound.outer_cover.retained_cell_count >= 1
    assert bound.covariance_bound.cover_point_count == bound.outer_cover.retained_cell_count
    assert np.isclose(bound.combined_confidence_lower_bound, 0.95**2)
    assert bound.target_eigenvalue_covering_radius > 0.0
    assert bound.target_normalization_covering_radius > 0.0
    assert bound.requires_independent_target_record

    target = rng.normal(size=(target_count, 3))
    nuisance_coefficients = np.array([[100.0, -30.0, 12.0], [80.0, 20.0, -50.0]])
    base = separable_gaussian_evalue_outer_cover_projected_covariance(
        target, design, bound
    )
    shifted = separable_gaussian_evalue_outer_cover_projected_covariance(
        target + design @ nuisance_coefficients,
        design,
        bound,
    )
    assert np.allclose(base, shifted, atol=1e-11)


def test_zero_radius_likelihood_bound_is_exact():
    value = gaussian_log_likelihood_cell_variation_bound(
        minimum_eigenvalue=0.4,
        operator_radius=0.0,
        residual_scatter_trace=20.0,
        residual_dimension=5,
        channel_count=8,
    )
    assert value == 0.0
