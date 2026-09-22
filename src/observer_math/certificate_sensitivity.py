"""Sensitivity diagnostics for Research I finite-sample certificate burden.

Counterfactual calculations are diagnostic only: they identify which bound
family would most improve robust separation if tightened by a declared factor.
"""
from __future__ import annotations
from dataclasses import dataclass
from .certificate_decomposition import pair_certificate_decomposition

@dataclass(frozen=True)
class BurdenSensitivity:
    baseline_burden: float
    local_burden: float
    transport_burden: float
    local_fraction: float
    transport_fraction: float

def burden_sensitivity(**kwargs)->BurdenSensitivity:
    x=pair_certificate_decomposition(**kwargs)
    total=x["pair_total_burden"]
    if total<0: raise ValueError("burden must be nonnegative")
    if total==0:
        lf=tf=0.0
    else:
        lf=x["pair_local_burden"]/total
        tf=x["pair_transport_burden"]/total
    return BurdenSensitivity(float(total),float(x["pair_local_burden"]),
        float(x["pair_transport_burden"]),float(lf),float(tf))

def counterfactual_tightening(*,empirical_margin:float,tightening_fraction:float,**kwargs):
    """Compare equal fractional tightening of local vs transport path radii."""
    if not 0.0<=tightening_fraction<=1.0:
        raise ValueError("tightening_fraction must lie in [0,1]")
    s=burden_sensitivity(**kwargs)
    base=empirical_margin-s.baseline_burden
    local=empirical_margin-((1-tightening_fraction)*s.local_burden+s.transport_burden)
    transport=empirical_margin-(s.local_burden+(1-tightening_fraction)*s.transport_burden)
    return {"baseline_separation":float(base),
            "local_tightened_separation":float(local),
            "transport_tightened_separation":float(transport),
            "local_gain":float(local-base),"transport_gain":float(transport-base)}
