"""Factorwise diagnosis of finite-sample certificate conservatism."""
from __future__ import annotations
import numpy as np
from .active_measurement import (
    observer_factor_radii_from_relative_covariance,
    transport_score_radius_from_relative_covariance,
)

def path_radius_decomposition(*,covariance_relative_error:float,local_factors,
                              transport_factors,subset_size:int,ambient_size:int,
                              transport_weight:float):
    local=np.asarray(local_factors,float); trans=np.asarray(transport_factors,float)
    local_rows=[observer_factor_radii_from_relative_covariance(
        subset_size=subset_size,ambient_size=ambient_size,
        covariance_relative_error=covariance_relative_error,
        integration_factor=f[0],insulation_factor=f[1],persistence_factor=f[2])
        for f in local]
    transport_rows=[transport_score_radius_from_relative_covariance(
        subset_size=subset_size,ambient_size=ambient_size,
        covariance_relative_error=covariance_relative_error,
        insulation_factor=f[0],persistence_factor=f[1])
        for f in trans]
    local_score=np.array([r["observer_score"] for r in local_rows])
    transport_score=np.array([r["transport_score"] for r in transport_rows])
    return {
        "local_score_radii":local_score,
        "transport_score_radii":transport_score,
        "local_total":float(local_score.sum()),
        "transport_weighted_total":float(abs(transport_weight)*transport_score.sum()),
        "factor_error_sums":{
            "integration":float(sum(r["integration"] for r in local_rows)),
            "local_insulation":float(sum(r["insulation"] for r in local_rows)),
            "local_persistence":float(sum(r["persistence"] for r in local_rows)),
            "transport_insulation":float(sum(r["insulation"] for r in transport_rows)),
            "transport_persistence":float(sum(r["persistence"] for r in transport_rows)),
        },
    }

def pair_certificate_decomposition(*,covariance_relative_error:float,
                                   leader_local_factors,leader_transport_factors,
                                   competitor_local_factors,competitor_transport_factors,
                                   subset_size:int,ambient_size:int,transport_weight:float):
    leader=path_radius_decomposition(
        covariance_relative_error=covariance_relative_error,
        local_factors=leader_local_factors,transport_factors=leader_transport_factors,
        subset_size=subset_size,ambient_size=ambient_size,transport_weight=transport_weight)
    competitor=path_radius_decomposition(
        covariance_relative_error=covariance_relative_error,
        local_factors=competitor_local_factors,transport_factors=competitor_transport_factors,
        subset_size=subset_size,ambient_size=ambient_size,transport_weight=transport_weight)
    local=leader["local_total"]+competitor["local_total"]
    transport=leader["transport_weighted_total"]+competitor["transport_weighted_total"]
    return {"leader":leader,"competitor":competitor,
            "pair_local_burden":float(local),
            "pair_transport_burden":float(transport),
            "pair_total_burden":float(local+transport)}
