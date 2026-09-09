from pathlib import Path

path = Path("src/observer_math/__init__.py")
text = path.read_text(encoding="utf-8")
old = '''    "GaussianIrregularRelaxationEValueOuterCover",
    "GaussianIrregularRelaxationTargetBound",
    "GaussianPathRecoveryBound",
    "GaussianProjectedTemporalEnvelope",
    "GaussianIrregularRelaxationSecondOrderOuterCover",
    "GaussianReferenceWhitenedRelaxationTargetBound",
'''
new = '''    "GaussianIrregularRelaxationEValueOuterCover",
    "GaussianIrregularRelaxationSecondOrderOuterCover",
    "GaussianIrregularRelaxationTargetBound",
    "GaussianPathRecoveryBound",
    "GaussianProjectedTemporalEnvelope",
    "GaussianReferenceWhitenedRelaxationTargetBound",
'''
if text.count(old) != 1:
    raise RuntimeError("class export ordering anchor did not match exactly once")
text = text.replace(old, new, 1)
old = '''    "gaussian_relative_cmi_covariance_error_bound",
    "gaussian_relative_null_cmi_covariance_error_bound",
    "gaussian_relative_null_integration_factor_error_bound",
    "gaussian_reference_whitened_irregular_relaxation_target_matrix_chernoff_bound",
    "gaussian_relative_structural_null_near_competitor_screen",
'''
new = '''    "gaussian_reference_whitened_irregular_relaxation_target_matrix_chernoff_bound",
    "gaussian_relative_cmi_covariance_error_bound",
    "gaussian_relative_null_cmi_covariance_error_bound",
    "gaussian_relative_null_integration_factor_error_bound",
    "gaussian_relative_structural_null_near_competitor_screen",
'''
if text.count(old) != 1:
    raise RuntimeError("function export ordering anchor did not match exactly once")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
