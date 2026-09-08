import numpy as np

from observer_math.temporal_evalue import (
    gaussian_ar1_white_noise_evalue_confidence_set,
    gaussian_ar1_white_noise_residual_log_likelihood,
    gaussian_evalue_calibrated_ar1_white_noise_matrix_chernoff_bound,
)


def _temporal_covariance(sample_count, phi, eta):
    indices = np.arange(sample_count)
    ar1 = phi ** np.abs(indices[:, None] - indices[None, :])
    return (1.0 - eta) * ar1 + eta * np.eye(sample_count)


def _simulate_channels(sample_count, channel_count, phi, eta, rng):
    temporal = _temporal_covariance(sample_count, phi, eta)
    return np.linalg.cholesky(temporal) @ rng.normal(size=(sample_count, channel_count))


def _nearest_grid_index(result, phi, eta):
    phi_index = int(np.argmin(np.abs(result.autocorrelation_grid - phi)))
    eta_index = int(np.argmin(np.abs(result.white_noise_fraction_grid - eta)))
    return phi_index * result.white_noise_fraction_grid.size + eta_index


def test_residual_likelihood_and_evalue_set_are_invariant_to_channel_offsets():
    rng = np.random.default_rng(20261030)
    values = _simulate_channels(36, 8, 0.52, 0.03, rng)
    offsets = np.linspace(-20.0, 35.0, values.shape[1])
    shifted = values + offsets[None, :]

    base_log_likelihood = gaussian_ar1_white_noise_residual_log_likelihood(
        values, 0.52, 0.03
    )
    shifted_log_likelihood = gaussian_ar1_white_noise_residual_log_likelihood(
        shifted, 0.52, 0.03
    )
    base = gaussian_ar1_white_noise_evalue_confidence_set(
        values,
        lower_autocorrelation=0.35,
        upper_autocorrelation=0.70,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.08,
        confidence=0.95,
        autocorrelation_grid_size=7,
        white_noise_fraction_grid_size=5,
    )
    translated = gaussian_ar1_white_noise_evalue_confidence_set(
        shifted,
        lower_autocorrelation=0.35,
        upper_autocorrelation=0.70,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.08,
        confidence=0.95,
        autocorrelation_grid_size=7,
        white_noise_fraction_grid_size=5,
    )

    assert np.isclose(base_log_likelihood, shifted_log_likelihood, atol=1e-10)
    assert np.allclose(base.log_likelihood_grid, translated.log_likelihood_grid, atol=1e-9)
    assert np.allclose(base.log_e_values, translated.log_e_values, atol=1e-9)
    assert np.array_equal(base.retained_cell_mask, translated.retained_cell_mask)


def test_cellwise_likelihood_variation_bound_covers_parameter_cell_corners():
    rng = np.random.default_rng(20261031)
    values = _simulate_channels(28, 6, 0.50, 0.025, rng)
    result = gaussian_ar1_white_noise_evalue_confidence_set(
        values,
        lower_autocorrelation=0.40,
        upper_autocorrelation=0.60,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.05,
        confidence=0.95,
        autocorrelation_grid_size=5,
        white_noise_fraction_grid_size=3,
    )

    phi_index = 2
    eta_index = 1
    flat_index = phi_index * result.white_noise_fraction_grid.size + eta_index
    center_phi = result.autocorrelation_grid[phi_index]
    center_eta = result.white_noise_fraction_grid[eta_index]
    center_log_likelihood = result.log_likelihood_grid[flat_index]
    bound = result.likelihood_cell_variation_bounds[flat_index]
    half_phi = 0.5 * result.maximum_autocorrelation_spacing
    half_eta = 0.5 * result.maximum_white_noise_fraction_spacing

    for phi in (center_phi - half_phi, center_phi + half_phi):
        for eta in (center_eta - half_eta, center_eta + half_eta):
            corner = gaussian_ar1_white_noise_residual_log_likelihood(values, phi, eta)
            assert abs(corner - center_log_likelihood) <= bound + 1e-10


def test_between_grid_exact_evalue_confidence_point_cannot_be_certified_away():
    rng = np.random.default_rng(20261101)
    true_phi = 0.535
    true_eta = 0.027
    values = _simulate_channels(40, 12, true_phi, true_eta, rng)
    result = gaussian_ar1_white_noise_evalue_confidence_set(
        values,
        lower_autocorrelation=0.40,
        upper_autocorrelation=0.65,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.06,
        confidence=0.95,
        autocorrelation_grid_size=6,
        white_noise_fraction_grid_size=4,
    )

    true_log_likelihood = gaussian_ar1_white_noise_residual_log_likelihood(
        values, true_phi, true_eta
    )
    true_log_evalue = result.log_mixture_density - true_log_likelihood
    nearest = _nearest_grid_index(result, true_phi, true_eta)

    assert true_log_evalue < result.log_evalue_threshold
    assert result.retained_cell_mask[nearest]


def test_maximum_likelihood_grid_point_is_always_retained():
    rng = np.random.default_rng(20261102)
    values = _simulate_channels(32, 5, 0.48, 0.02, rng)
    result = gaussian_ar1_white_noise_evalue_confidence_set(
        values,
        lower_autocorrelation=0.30,
        upper_autocorrelation=0.70,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.10,
        confidence=0.975,
        autocorrelation_grid_size=9,
        white_noise_fraction_grid_size=5,
    )

    maximum_likelihood_index = int(np.argmax(result.log_likelihood_grid))
    assert result.log_e_values[maximum_likelihood_index] <= 1e-12
    assert result.retained_cell_mask[maximum_likelihood_index]
    assert result.retained_cell_count + result.excluded_cell_count == 45


def test_evalue_calibration_composes_with_compact_family_matrix_bound():
    rng = np.random.default_rng(20261103)
    calibration = _simulate_channels(60, 24, 0.47, 0.02, rng)
    target_count = 80
    t = np.linspace(-1.0, 1.0, target_count)
    nuisance_design = np.column_stack((np.ones_like(t), t))

    result = gaussian_evalue_calibrated_ar1_white_noise_matrix_chernoff_bound(
        calibration,
        block_dimension=3,
        block_count=1,
        nuisance_design=nuisance_design,
        lower_autocorrelation=0.35,
        upper_autocorrelation=0.60,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.06,
        calibration_confidence=0.95,
        covariance_confidence=0.95,
        autocorrelation_grid_size=9,
        white_noise_fraction_grid_size=5,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )

    assert result.confidence_set.retained_cell_count >= 1
    assert (
        result.covariance_bound.cover_point_count
        == result.confidence_set.retained_cell_count
    )
    assert np.isclose(result.combined_confidence_lower_bound, 0.95**2)
    assert result.target_eigenvalue_covering_radius > 0.0
    assert result.target_normalization_covering_radius > 0.0
    assert result.requires_independent_target_record
