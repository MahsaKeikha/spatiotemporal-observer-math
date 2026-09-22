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


def minimum_wishart_sample_count_for_radius(*,target_radius:float,
                                            block_dimension:int,block_count:int,
                                            confidence:float)->int:
    """Invert the repository Wishart radius bound exactly up to integer rounding."""
    if not 0.0 < target_radius:
        raise ValueError("target_radius must be positive")
    if block_dimension<1 or block_count<1 or not 0.0<confidence<1.0:
        raise ValueError("invalid Wishart parameters")
    a=np.sqrt(block_dimension)+np.sqrt(2.0*np.log(2.0*block_count/(1.0-confidence)))
    y=np.sqrt(1.0+target_radius)-1.0
    n=max(2,int(np.ceil(1.0+(a/y)**2)))
    # Floating-point guard: return the first integer satisfying the actual bound.
    while gaussian_wishart_relative_covariance_error_bound(
            block_dimension,block_count,n,confidence=confidence)>target_radius:
        n+=1
    while n>2 and gaussian_wishart_relative_covariance_error_bound(
            block_dimension,block_count,n-1,confidence=confidence)<=target_radius:
        n-=1
    return n

def critical_relative_covariance_radius(*,leader_action:float,competitor_action:float,
                                        leader_local_factors,leader_transport_factors,
                                        competitor_local_factors,competitor_transport_factors,
                                        subset_size:int,ambient_size:int,
                                        transport_weight:float,
                                        lower:float=0.0,upper:float=0.999999,
                                        iterations:int=80)->float:
    """Largest delta (to bisection precision) with strict positive robust separation."""
    if not 0.0<=lower<upper<1.0 or iterations<1:
        raise ValueError("require 0 <= lower < upper < 1 and iterations >= 1")
    def sep(delta):
        ll=np.full(np.asarray(leader_local_factors).shape[0],delta)
        lt=np.full(np.asarray(leader_transport_factors).shape[0],delta)
        cl=np.full(np.asarray(competitor_local_factors).shape[0],delta)
        ct=np.full(np.asarray(competitor_transport_factors).shape[0],delta)
        rl=complete_path_radius_from_relative_covariance(
            ll,lt,leader_local_factors,leader_transport_factors,
            subset_size=subset_size,ambient_size=ambient_size,
            transport_weight=transport_weight)
        rc=complete_path_radius_from_relative_covariance(
            cl,ct,competitor_local_factors,competitor_transport_factors,
            subset_size=subset_size,ambient_size=ambient_size,
            transport_weight=transport_weight)
        return float(leader_action-competitor_action-rl-rc)
    if sep(lower)<=0.0:
        raise ValueError("certificate is not positive even at lower radius")
    if sep(upper)>0.0:
        return upper
    lo,hi=lower,upper
    for _ in range(iterations):
        mid=(lo+hi)/2.0
        if sep(mid)>0.0: lo=mid
        else: hi=mid
    return lo

def first_certifying_sample_count_binary(*,minimum:int,maximum:int,**kwargs):
    """Monotone integer search for the first strict finite-sample certificate."""
    if minimum<2 or maximum<minimum:
        raise ValueError("require 2 <= minimum <= maximum")
    if finite_sample_pair_certificate(sample_count=minimum,**kwargs).certified:
        return finite_sample_pair_certificate(sample_count=minimum,**kwargs)
    if not finite_sample_pair_certificate(sample_count=maximum,**kwargs).certified:
        return None
    lo,hi=minimum,maximum
    while lo+1<hi:
        mid=(lo+hi)//2
        if finite_sample_pair_certificate(sample_count=mid,**kwargs).certified:
            hi=mid
        else:
            lo=mid
    return finite_sample_pair_certificate(sample_count=hi,**kwargs)
