import numpy as np

from observer_math.matrix_chernoff import (
    gaussian_projected_weighted_wishart_matrix_bound,
    gaussian_weighted_wishart_matrix_bound,
    projected_temporal_eigenvalues,
)
from observer_math.nuisance import (
    gaussian_ar1_projected_temporal_envelope,
    gaussian_projected_relative_covariance_error_bound,
)


def _ar1_matrix(sample_count, phi):
    index = np.arange(sample_count)
    return phi ** np.abs(index[:, None] - index[None, :])


def _affine_design(sample_count):
    t = np.linspace(-1.0, 1.0, sample_count)
    return np.column_stack((np.ones_like(t), t))


def test_weighted_matrix_bound_is_invariant_to_common_weight_scale():
    weights = np.array([0.25, 0.5, 1.0, 1.5, 2.0])
    base = gaussian_weighted_wishart_matrix_bound(
        4, 2, weights, confidence=0.975, upper_theta_grid_size=1024, lower_theta_grid_size=1024
    )
    scaled = gaussian_weighted_wishart_matrix_bound(
        4,
        2,
        37.0 * weights,
        confidence=0.975,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    assert np.isclose(base.relative_covariance_error, scaled.relative_covariance_error, rtol=1e-12)
    assert np.isclose(base.upper_deviation, scaled.upper_deviation, rtol=1e-12)
    assert np.isclose(base.lower_deviation, scaled.lower_deviation, rtol=1e-12)


def test_matrix_chernoff_improves_previous_sphere_net_bound():
    sample_count = 300
    phi = 0.65
    design = _affine_design(sample_count)
    temporal = _ar1_matrix(sample_count, phi)
    weights = projected_temporal_eigenvalues(temporal, design)
    matrix_bound = gaussian_weighted_wishart_matrix_bound(
        4, 1, weights, confidence=0.975, upper_theta_grid_size=2048, lower_theta_grid_size=2048
    )
    envelope = gaussian_ar1_projected_temporal_envelope(sample_count, phi, design)
    sphere_net = gaussian_projected_relative_covariance_error_bound(
        4, 1, envelope, confidence=0.975
    )

    assert matrix_bound.relative_covariance_error < sphere_net
    assert matrix_bound.relative_covariance_error < 1.0
    assert sphere_net > 1.0


def test_direct_projected_helper_matches_explicit_eigenvalue_call():
    sample_count = 80
    phi = 0.4
    design = _affine_design(sample_count)
    temporal = _ar1_matrix(sample_count, phi)
    weights = projected_temporal_eigenvalues(temporal, design)
    direct = gaussian_projected_weighted_wishart_matrix_bound(
        3,
        2,
        temporal,
        design,
        confidence=0.95,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )
    explicit = gaussian_weighted_wishart_matrix_bound(
        3,
        2,
        weights,
        confidence=0.95,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    assert np.isclose(direct.relative_covariance_error, explicit.relative_covariance_error)
    assert np.isclose(direct.temporal_trace, explicit.temporal_trace)
    assert np.isclose(direct.temporal_frobenius_norm, explicit.temporal_frobenius_norm)
    assert np.isclose(direct.temporal_spectral_norm, explicit.temporal_spectral_norm)


def test_seeded_weighted_wishart_trials_lie_inside_matrix_bound():
    rng = np.random.default_rng(20261022)
    sample_count = 300
    dimension = 4
    phi = 0.65
    design = _affine_design(sample_count)
    temporal = _ar1_matrix(sample_count, phi)
    weights = projected_temporal_eigenvalues(temporal, design)
    bound = gaussian_weighted_wishart_matrix_bound(
        dimension,
        1,
        weights,
        confidence=0.975,
        upper_theta_grid_size=2048,
        lower_theta_grid_size=2048,
    )
    degrees = np.sum(weights)
    errors = []
    for _ in range(96):
        gaussian = rng.normal(size=(weights.size, dimension))
        covariance = gaussian.T @ (weights[:, None] * gaussian) / degrees
        errors.append(float(np.linalg.norm(covariance - np.eye(dimension), ord=2)))

    assert max(errors) < bound.relative_covariance_error


def test_full_eigenvalue_profile_changes_bound_even_at_similar_trace():
    diffuse = np.ones(120)
    concentrated = np.concatenate((np.full(20, 4.0), np.full(40, 1.0)))
    concentrated *= np.sum(diffuse) / np.sum(concentrated)

    diffuse_bound = gaussian_weighted_wishart_matrix_bound(
        4, 1, diffuse, confidence=0.975, upper_theta_grid_size=1024, lower_theta_grid_size=1024
    )
    concentrated_bound = gaussian_weighted_wishart_matrix_bound(
        4,
        1,
        concentrated,
        confidence=0.975,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    assert np.isclose(diffuse_bound.temporal_trace, concentrated_bound.temporal_trace)
    assert concentrated_bound.relative_covariance_error > diffuse_bound.relative_covariance_error
