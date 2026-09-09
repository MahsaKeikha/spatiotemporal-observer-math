import observer_math as om


def test_irregular_relaxation_calibration_symbols_are_exported_from_package_root():
    expected = (
        "GaussianIrregularRelaxationEValueGrid",
        "GaussianIrregularRelaxationEValueModel",
        "GaussianIrregularRelaxationEValueOuterCover",
        "GaussianIrregularRelaxationTargetBound",
        "gaussian_irregular_relaxation_evalue_grid",
        "gaussian_irregular_relaxation_evalue_model",
        "gaussian_irregular_relaxation_evalue_outer_cover",
        "gaussian_irregular_relaxation_log_evalue",
        "gaussian_irregular_relaxation_log_likelihood_kernel",
        "gaussian_irregular_relaxation_log_likelihood_lipschitz_bound",
        "gaussian_irregular_relaxation_target_matrix_chernoff_bound",
    )

    for name in expected:
        assert name in om.__all__
        assert getattr(om, name) is not None
