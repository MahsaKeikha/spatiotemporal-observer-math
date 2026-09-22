"""Finite-sample certificate chain using Research I Wishart radii.

This module removes the surrogate contraction law from certificate-radius
calculations. Sample count is mapped to the simultaneous relative covariance
radius already used by Research I, then through the canonical local/transport
factor perturbation maps and finally to a complete path-action radius.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .active_measurement import complete_path_radius_from_relative_covariance
from .recovery import gaussian_wishart_relative_covariance_error_bound

@dataclass(frozen=True)
class FiniteSamplePathCertificate:
    sample_count: int
    covariance_radius: float
    leader_radius: float
    competitor_radius: float
    empirical_margin: float
    robust_separation: float
    certified: bool

def wishart_path_radius(*,sample_count:int,block_dimension:int,block_count:int,
                        confidence:float,local_factors,transport_factors,
                        subset_size:int,ambient_size:int,transport_weight:float) -> tuple[float,float]:
    delta=gaussian_wishart_relative_covariance_error_bound(
        block_dimension,block_count,sample_count,confidence=confidence)
    local=np.asarray(local_factors,float)
    transport=np.asarray(transport_factors,float)
    local_errors=np.full(local.shape[0],delta)
    transport_errors=np.full(transport.shape[0],delta)
    radius=complete_path_radius_from_relative_covariance(
        local_errors,transport_errors,local,transport,
        subset_size=subset_size,ambient_size=ambient_size,
        transport_weight=transport_weight)
    return float(delta),float(radius)

def finite_sample_pair_certificate(*,sample_count:int,block_dimension:int,block_count:int,
                                   confidence:float,leader_action:float,competitor_action:float,
                                   leader_local_factors,leader_transport_factors,
                                   competitor_local_factors,competitor_transport_factors,
                                   subset_size:int,ambient_size:int,
                                   transport_weight:float) -> FiniteSamplePathCertificate:
    dl,rl=wishart_path_radius(
        sample_count=sample_count,block_dimension=block_dimension,block_count=block_count,
        confidence=confidence,local_factors=leader_local_factors,
        transport_factors=leader_transport_factors,subset_size=subset_size,
        ambient_size=ambient_size,transport_weight=transport_weight)
    dc,rc=wishart_path_radius(
        sample_count=sample_count,block_dimension=block_dimension,block_count=block_count,
        confidence=confidence,local_factors=competitor_local_factors,
        transport_factors=competitor_transport_factors,subset_size=subset_size,
        ambient_size=ambient_size,transport_weight=transport_weight)
    margin=float(leader_action-competitor_action)
    separation=margin-rl-rc
    return FiniteSamplePathCertificate(
        sample_count,float(max(dl,dc)),rl,rc,margin,float(separation),separation>0)

def first_certifying_sample_count(*,minimum:int,maximum:int,**kwargs):
    """Return first integer N in [minimum, maximum] that certifies, else None."""
    if minimum<2 or maximum<minimum:
        raise ValueError("require 2 <= minimum <= maximum")
    for n in range(minimum,maximum+1):
        result=finite_sample_pair_certificate(sample_count=n,**kwargs)
        if result.certified:
            return result
    return None
