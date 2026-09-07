"""Mathematical tools for detecting spatiotemporal observer-like subsystems."""

from .metrics import ObserverMetrics, observer_metrics, observer_metrics_from_covariances
from .models import block_system, correlated_but_uncoupled_system, ring_system
from .nonstationary import (
    TransportMetrics,
    adjacent_joint_covariance,
    propagate_covariances,
    transport_metrics,
)
from .search import Candidate, rank_subsystems
from .worldtube import WorldTubeResult, optimize_worldtube, structural_transport

__all__ = [
    "Candidate",
    "ObserverMetrics",
    "TransportMetrics",
    "WorldTubeResult",
    "adjacent_joint_covariance",
    "block_system",
    "correlated_but_uncoupled_system",
    "observer_metrics",
    "observer_metrics_from_covariances",
    "optimize_worldtube",
    "propagate_covariances",
    "rank_subsystems",
    "ring_system",
    "structural_transport",
    "transport_metrics",
]
