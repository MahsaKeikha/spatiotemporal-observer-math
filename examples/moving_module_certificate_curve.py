"""Research I moving-module finite-sample certificate curve.

The factors are computed from the analytical moving-module covariance model,
not hard-coded benchmark outcomes. The script identifies the population best
and runner-up world tubes, extracts their factor paths, and propagates the
Research I simultaneous Wishart radius through the canonical perturbation
chain. It writes results only when explicitly executed.
"""
from __future__ import annotations
import json
from itertools import combinations
from pathlib import Path
import numpy as np

from observer_math import moving_module_systems, optimize_worldtube
from observer_math.gaussian import stationary_covariance
from observer_math.metrics import observer_metrics_from_covariances, transport_metrics_from_covariances
from observer_math.finite_sample_certificate import (
    critical_relative_covariance_radius,
    finite_sample_pair_certificate,
    minimum_wishart_sample_count_for_radius,
)
from observer_math.certificate_decomposition import pair_certificate_decomposition
from observer_math.certificate_sensitivity import burden_sensitivity, counterfactual_tightening, primitive_factor_pressure
from observer_math.active_measurement import (
    observer_factor_radii_from_relative_covariance,
    transport_score_radius_from_relative_covariance,
)

TRANSPORT_WEIGHT=.25
CONTINUITY_WEIGHT=.08
CONFIDENCE=.975

def analytical_scores():
    planted,systems=moving_module_systems()
    candidates=tuple(combinations(range(systems[0][0].shape[0]),len(planted[0])))
    cov=[stationary_covariance(*systems[0])]
    # Propagate covariance under each time-varying linear Gaussian system.
    for A,Q in systems:
        cov.append(A@cov[-1]@A.T+Q)
    T=len(systems)
    local=np.zeros((T,len(candidates)))
    local_factors=np.zeros((T,len(candidates),3))
    transport=np.zeros((T-1,len(candidates),len(candidates)))
    transport_factors=np.zeros((T-1,len(candidates),len(candidates),2))
    for t in range(T):
        joint=np.block([[cov[t],cov[t]@systems[t][0].T],
                        [systems[t][0]@cov[t],cov[t+1]]])
        for i,S in enumerate(candidates):
            m=observer_metrics_from_covariances(cov[t],joint,S)
            local[t,i]=m.observer_score
            local_factors[t,i]=[m.integration_strength,m.independence,m.persistence]
        if t<T-1:
            for i,S in enumerate(candidates):
                for j,R in enumerate(candidates):
                    m=transport_metrics_from_covariances(cov[t],joint,S,R)
                    transport[t,i,j]=m.transport_score
                    transport_factors[t,i,j]=[m.independence,m.persistence]
    return planted,candidates,local,local_factors,transport,transport_factors

def path_action(path,candidates,local,transport):
    idx={c:i for i,c in enumerate(candidates)}
    ids=[idx[tuple(x)] for x in path]
    value=sum(local[t,i] for t,i in enumerate(ids))
    for t,(i,j) in enumerate(zip(ids[:-1],ids[1:])):
        a,b=set(candidates[i]),set(candidates[j])
        jaccard=1-len(a&b)/len(a|b)
        value+=TRANSPORT_WEIGHT*transport[t,i,j]-CONTINUITY_WEIGHT*jaccard
    return float(value),ids

def extract(ids,local_factors,transport_factors):
    lf=np.array([local_factors[t,i] for t,i in enumerate(ids)])
    tf=np.array([transport_factors[t,i,j] for t,(i,j) in enumerate(zip(ids[:-1],ids[1:]))])
    return lf,tf

def main():
    planted,candidates,local,lf,transport,tf=analytical_scores()
    best=optimize_worldtube(local,candidates,transport_scores=transport,
                            transport_weight=TRANSPORT_WEIGHT,continuity_weight=CONTINUITY_WEIGHT)
    # Exact runner-up by excluding the best path via exhaustive DP helper.
    from examples.worldtube_active_measurement_bridge import top_two_worldtubes_dp
    leader,leader_dp_action,runner,runner_dp_action=top_two_worldtubes_dp(
        local,candidates,transport,transport_weight=TRANSPORT_WEIGHT,
        continuity_weight=CONTINUITY_WEIGHT)
    A1,i1=path_action(leader,candidates,local,transport)
    A2,i2=path_action(runner,candidates,local,transport)
    l1,t1=extract(i1,lf,tf); l2,t2=extract(i2,lf,tf)
    ambient=max(max(candidate) for candidate in candidates)+1
    subset=len(candidates[0])
    block_dimension=ambient+subset
    block_count=len(local)*len(candidates)
    delta_crit=critical_relative_covariance_radius(
        leader_action=A1,competitor_action=A2,
        leader_local_factors=l1,leader_transport_factors=t1,
        competitor_local_factors=l2,competitor_transport_factors=t2,
        subset_size=subset,ambient_size=ambient,
        transport_weight=TRANSPORT_WEIGHT)
    burden=pair_certificate_decomposition(
        covariance_relative_error=delta_crit,
        leader_local_factors=l1,leader_transport_factors=t1,
        competitor_local_factors=l2,competitor_transport_factors=t2,
        subset_size=subset,ambient_size=ambient,transport_weight=TRANSPORT_WEIGHT)
    sensitivity=burden_sensitivity(
        covariance_relative_error=delta_crit,
        leader_local_factors=l1,leader_transport_factors=t1,
        competitor_local_factors=l2,competitor_transport_factors=t2,
        subset_size=subset,ambient_size=ambient,transport_weight=TRANSPORT_WEIGHT)
    tightening=counterfactual_tightening(
        empirical_margin=A1-A2,tightening_fraction=.25,
        covariance_relative_error=delta_crit,
        leader_local_factors=l1,leader_transport_factors=t1,
        competitor_local_factors=l2,competitor_transport_factors=t2,
        subset_size=subset,ambient_size=ambient,transport_weight=TRANSPORT_WEIGHT)
    primitive=primitive_factor_pressure(
        covariance_relative_error=delta_crit,
        leader_local_factors=l1,leader_transport_factors=t1,
        competitor_local_factors=l2,competitor_transport_factors=t2,
        subset_size=subset,ambient_size=ambient)
    n_crit=minimum_wishart_sample_count_for_radius(
        target_radius=delta_crit,block_dimension=block_dimension,
        block_count=block_count,confidence=CONFIDENCE)
    sample_grid=sorted(set([100,200,500,1000,2000,5000,10000,20000,50000,100000,
                            max(2,n_crit-1),n_crit,n_crit+1]))
    rows=[]
    for n in sample_grid:
        x=finite_sample_pair_certificate(
            sample_count=n,block_dimension=block_dimension,block_count=block_count,
            confidence=CONFIDENCE,leader_action=A1,competitor_action=A2,
            leader_local_factors=l1,leader_transport_factors=t1,
            competitor_local_factors=l2,competitor_transport_factors=t2,
            subset_size=subset,ambient_size=ambient,transport_weight=TRANSPORT_WEIGHT)
        rows.append(x.__dict__)
    payload={"scope":"analytical moving-module finite-sample certificate curve",
             "planted":[list(x) for x in planted],"leader":[list(x) for x in leader],
             "runner_up":[list(x) for x in runner],"leader_action":A1,
             "runner_up_action":A2,"population_margin":A1-A2,
             "dp_leader_action":leader_dp_action,"dp_runner_up_action":runner_dp_action,
             "block_dimension":block_dimension,"block_count":block_count,
             "confidence":CONFIDENCE,"critical_covariance_radius":delta_crit,
             "minimum_effective_certification_count":n_crit,
             "critical_radius_burden_decomposition":{
                 "pair_local_burden":burden["pair_local_burden"],
                 "pair_transport_burden":burden["pair_transport_burden"],
                 "pair_total_burden":burden["pair_total_burden"],
                 "leader_factor_error_sums":burden["leader"]["factor_error_sums"],
                 "runner_up_factor_error_sums":burden["competitor"]["factor_error_sums"]},
             "critical_radius_sensitivity":{
                 "local_fraction":sensitivity.local_fraction,
                 "transport_fraction":sensitivity.transport_fraction,
                 "quarter_tightening":tightening,
                 "primitive_factor_pressure":primitive},
             "rows":rows}
    out=Path("docs/moving_module_certificate_curve.json")
    out.write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps(payload,indent=2))

if __name__=="__main__":
    main()
