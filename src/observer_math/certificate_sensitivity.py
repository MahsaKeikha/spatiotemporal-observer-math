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


def primitive_factor_pressure(*,covariance_relative_error:float,
                              leader_local_factors,leader_transport_factors,
                              competitor_local_factors,competitor_transport_factors,
                              subset_size:int,ambient_size:int):
    """Sum canonical primitive factor-error bounds across both retained paths.

    These are pre-product-root pressures. They diagnose where the canonical
    covariance-to-factor map is loose; they are not additive score radii.
    """
    from .recovery import relative_covariance_factor_error_bounds
    local_count=len(leader_local_factors)+len(competitor_local_factors)
    trans_count=len(leader_transport_factors)+len(competitor_transport_factors)
    le,lv=relative_covariance_factor_error_bounds(
        covariance_relative_error,ambient_size,subset_size,transport=False)
    te,tv=relative_covariance_factor_error_bounds(
        covariance_relative_error,ambient_size,subset_size,transport=True)
    if not (lv and tv):
        return {"valid":False}
    vals={
      "integration":float(local_count*le[0]),
      "local_insulation":float(local_count*le[1]),
      "local_persistence":float(local_count*le[2]),
      "transport_insulation":float(trans_count*te[0]),
      "transport_persistence":float(trans_count*te[1]),
    }
    total=sum(vals.values())
    return {"valid":True,"pressure":vals,
            "fractions":{k:(v/total if total else 0.) for k,v in vals.items()},
            "total_primitive_pressure":float(total)}
