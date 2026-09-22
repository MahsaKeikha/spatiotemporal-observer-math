"""Adversarial controls for the self-certifying observer benchmark.

These scenarios test failure behavior rather than optimize headline accuracy.
A trustworthy observer should delay or refuse certification when identifiability,
coverage, or uncertainty assumptions are deliberately weakened.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

SEED=20260921
TRIALS=300
BUDGET=60
ALPHA=.01
H=float(np.log(1/ALPHA))
TRUE_MARGIN=.62

SCENARIOS={
 "nominal": dict(mean_gap=.55, radius_scale=1., coverage=True, dropout=0., noise_scale=1.),
 "near_equivalence": dict(mean_gap=.07, radius_scale=1., coverage=True, dropout=0., noise_scale=1.),
 "exact_equivalence": dict(mean_gap=0., radius_scale=1., coverage=True, dropout=0., noise_scale=1.),
 "inflated_uncertainty": dict(mean_gap=.55, radius_scale=2.4, coverage=True, dropout=0., noise_scale=1.),
 "channel_dropout": dict(mean_gap=.55, radius_scale=1.25, coverage=True, dropout=.45, noise_scale=1.),
 "heterogeneous_noise": dict(mean_gap=.55, radius_scale=1.15, coverage=True, dropout=0., noise_scale=2.2),
 "candidate_misspecification": dict(mean_gap=.55, radius_scale=1., coverage=False, dropout=0., noise_scale=1.),
}

BASE_PRESSURE=np.array([.31,.27,.09,.06,.18,.05])
CONTRACTION=np.array([.12,.10,.04,.03,.08,.02])
VAR=np.array([.24,.18,.20,.18,.22,.20])
GAP_PROFILE=np.array([1.,0.,.72,0.,.18,0.])


def radius(counts, scale):
    return float(scale*np.sum(BASE_PRESSURE/(1+CONTRACTION*counts)))


def run_trial(name, seed):
    cfg=SCENARIOS[name]
    rng=np.random.default_rng(seed)
    counts=np.zeros(6)
    llr=0.
    certified_at=None
    for step in range(1,BUDGET+1):
        # Joint acquisition: maximize the weakest normalized structural/evidence gain.
        structural=(cfg["radius_scale"]*BASE_PRESSURE/(1+CONTRACTION*counts)
                    -cfg["radius_scale"]*BASE_PRESSURE/(1+CONTRACTION*(counts+1)))
        variance=VAR*cfg["noise_scale"]
        kl=.5*(cfg["mean_gap"]*GAP_PROFILE)**2/variance
        s=structural/max(structural.max(),np.finfo(float).eps)
        k=kl/max(kl.max(),np.finfo(float).eps) if kl.max()>0 else np.zeros_like(kl)
        utility=np.minimum(s,k)
        channel=int(np.argmax(utility)) if utility.max()>0 else int(np.argmax(structural))
        if rng.random()<cfg["dropout"]:
            continue
        gap=cfg["mean_gap"]*GAP_PROFILE[channel]
        y=rng.normal(gap,np.sqrt(variance[channel]))
        # log f_gap(y)/f_0(y)
        llr += (gap*y-.5*gap*gap)/variance[channel]
        counts[channel]+=1
        structural_ok=TRUE_MARGIN>radius(counts,cfg["radius_scale"])
        evidence_ok=llr>=H
        coverage_ok=bool(cfg["coverage"])
        if structural_ok and evidence_ok and coverage_ok and certified_at is None:
            certified_at=step
    return dict(certified=certified_at is not None,certified_at=certified_at,
                final_radius=radius(counts,cfg["radius_scale"]),final_llr=float(llr),
                coverage=bool(cfg["coverage"]))


def summarize(name):
    rows=[run_trial(name,SEED+i) for i in range(TRIALS)]
    times=[r["certified_at"] for r in rows if r["certified_at"] is not None]
    return dict(scenario=name,trials=TRIALS,budget=BUDGET,
                certification_rate=float(np.mean([r["certified"] for r in rows])),
                median_time_to_certificate=None if not times else float(np.median(times)),
                mean_final_radius=float(np.mean([r["final_radius"] for r in rows])),
                mean_final_llr=float(np.mean([r["final_llr"] for r in rows])))


def main():
    result={"scope":"synthetic falsification suite; not a biological model",
            "results":[summarize(name) for name in SCENARIOS]}
    out=Path("docs/self_certifying_observer_falsification.json")
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
