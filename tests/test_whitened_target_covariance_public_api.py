import observer_math as om


def test_proposition_56_symbols_are_exported_from_package_root() -> None:
    expected = (
        "GaussianWhitenedProjectedCovarianceBound",
        "GaussianWhitenedScalarChiSquareBound",
        "exponential_relaxation_whitened_projected_covariance",
        "gaussian_whitened_projected_covariance_bound",
        "gaussian_whitened_scalar_chi_square_bound",
        "separable_gaussian_whitened_projected_covariance",
        "whitened_nuisance_projector",
    )
    for name in expected:
        assert hasattr(om, name), name
        assert name in om.__all__
