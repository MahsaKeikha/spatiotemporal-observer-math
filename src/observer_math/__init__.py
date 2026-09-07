"""Mathematical tools for detecting spatiotemporal observer-like subsystems."""

from .baselines import BaselinePath, best_fixed_boundary, independent_local_path
from .metrics import ObserverMetrics, observer_metrics, observer_metrics_from_covariances
from .models import (
    block_system,
    correlated_but_uncoupled_system,
    moving_module_systems,
    ring_system,
)
from .nonstationary import (
    TransportMetrics,
    adjacent_joint_covariance,
    propagate_covariances,
    transport_metrics,
    transport_metrics_from_covariances,
)
from .recovery import (
    ComponentwiseRecoveryBound,
    FiniteSampleRecoveryBound,
    componentwise_recovery_bound,
    finite_sample_recovery_bound,
    gaussian_cmi_covariance_error_bound,
)
from .sampling import (
    adjacent_sample_covariances,
    regularized_sample_covariance,
    simulate_gaussian_ensemble,
)
from .search import Candidate, rank_subsystems
from .worldtube import (
    WorldTubeCertificate,
    WorldTubeResult,
    certify_worldtube,
    optimize_worldtube,
    structural_transport,
)

__all__ = [
    "BaselinePath",
    "Candidate",
    "ComponentwiseRecoveryBound",
    "FiniteSampleRecoveryBound",
    "ObserverMetrics",
    "TransportMetrics",
    "WorldTubeCertificate",
    "WorldTubeResult",
    "adjacent_joint_covariance",
    "adjacent_sample_covariances",
    "best_fixed_boundary",
    "block_system",
    "certify_worldtube",
    "componentwise_recovery_bound",
    "correlated_but_uncoupled_system",
    "finite_sample_recovery_bound",
    "gaussian_cmi_covariance_error_bound",
    "independent_local_path",
    "moving_module_systems",
    "observer_metrics",
    "observer_metrics_from_covariances",
    "optimize_worldtube",
    "propagate_covariances",
    "rank_subsystems",
    "regularized_sample_covariance",
    "ring_system",
    "simulate_gaussian_ensemble",
    "structural_transport",
    "transport_metrics",
    "transport_metrics_from_covariances",
]
