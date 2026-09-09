from pathlib import Path

path = Path("src/observer_math/__init__.py")
text = path.read_text(encoding="utf-8")

import_anchor = "from .worldtube import (\n"
import_block = '''from .whitened_target_covariance import (
    GaussianWhitenedProjectedCovarianceBound,
    GaussianWhitenedScalarChiSquareBound,
    exponential_relaxation_whitened_projected_covariance,
    gaussian_whitened_projected_covariance_bound,
    gaussian_whitened_scalar_chi_square_bound,
    separable_gaussian_whitened_projected_covariance,
    whitened_nuisance_projector,
)
'''
if text.count(import_anchor) != 1:
    raise RuntimeError("expected exactly one worldtube import anchor")
if "from .whitened_target_covariance import (" in text:
    raise RuntimeError("Proposition 56 import block already present")
text = text.replace(import_anchor, import_block + import_anchor, 1)

class_anchor = '    "GaussianWeightedWishartMatrixBound",\n'
class_insert = (
    '    "GaussianWeightedWishartMatrixBound",\n'
    '    "GaussianWhitenedProjectedCovarianceBound",\n'
    '    "GaussianWhitenedScalarChiSquareBound",\n'
)
if text.count(class_anchor) != 1:
    raise RuntimeError("expected exactly one class export anchor")
text = text.replace(class_anchor, class_insert, 1)

function_anchor = '    "finite_sample_recovery_bound",\n'
function_insert = (
    '    "exponential_relaxation_whitened_projected_covariance",\n'
    '    "finite_sample_recovery_bound",\n'
)
if text.count(function_anchor) != 1:
    raise RuntimeError("expected exactly one exponential export anchor")
text = text.replace(function_anchor, function_insert, 1)

wishart_anchor = '    "gaussian_wishart_relative_covariance_error_bound",\n'
wishart_insert = (
    '    "gaussian_whitened_projected_covariance_bound",\n'
    '    "gaussian_whitened_scalar_chi_square_bound",\n'
    '    "gaussian_wishart_relative_covariance_error_bound",\n'
)
if text.count(wishart_anchor) != 1:
    raise RuntimeError("expected exactly one Gaussian export anchor")
text = text.replace(wishart_anchor, wishart_insert, 1)

separable_anchor = '    "separable_gaussian_projected_covariance",\n'
separable_insert = (
    '    "separable_gaussian_projected_covariance",\n'
    '    "separable_gaussian_whitened_projected_covariance",\n'
)
if text.count(separable_anchor) != 1:
    raise RuntimeError("expected exactly one separable export anchor")
text = text.replace(separable_anchor, separable_insert, 1)

transport_anchor = '    "transport_metrics_from_covariances",\n'
transport_insert = (
    '    "transport_metrics_from_covariances",\n'
    '    "whitened_nuisance_projector",\n'
)
if text.count(transport_anchor) != 1:
    raise RuntimeError("expected exactly one final export anchor")
text = text.replace(transport_anchor, transport_insert, 1)

path.write_text(text, encoding="utf-8")
