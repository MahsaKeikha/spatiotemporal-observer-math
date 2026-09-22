"""Deterministic end-to-end trajectories for the self-certifying observer.

This is a state-machine stress protocol, not a performance result. It drives
the public transition API through controlled certificate degradation,
reacquisition, recovery, non-identifiability, and unrecoverable invalidity.
"""
from __future__ import annotations
import json
from pathlib import Path
from observer_math.assumption_audit import AssumptionAudit
from observer_math.repair_semantics import canonical_repair_actions, execute_repair_plan
from observer_math.reacquisition import ReacquisitionAction
from observer_math.self_certifying_observer import transition

H=4.6

def recovery_action():
    return ReacquisitionAction(
        "recalibrate_and_resense",True,True,True,True,
        expected_kl=.6,structural_gain=.5,cost=.05,
    )

def state(t,sep,llr,kl,valid,actions=(),steps=0,budget=3):
    s=transition(
        robust_separation=sep,log_evidence=llr,evidence_threshold=H,
        available_kl=kl,assumptions_valid=valid,recovery_actions=actions,
        reacquisition_steps=steps,reacquisition_budget=budget,
    )
    return dict(t=t,separation=sep,llr=llr,assumptions_valid=valid,
                state=s.state.value,action=s.action,reason=s.reason)


def repaired_record(t,audit,sep,llr,kl):
    """Apply assumption-specific repair and invalidate stale records."""
    effect=execute_repair_plan(audit)
    repaired_sep=0.0 if effect.reset_structural else sep
    repaired_llr=0.0 if effect.reset_evidence else llr
    return {
        "repair_plan":[a.name for a in canonical_repair_actions()
                       if a in __import__("observer_math.repair_semantics",fromlist=["deterministic_repair_plan"]).deterministic_repair_plan(audit)],
        "reset_structural":effect.reset_structural,
        "reset_evidence":effect.reset_evidence,
        "reset_candidates":effect.reset_candidates,
        "post_repair":state(t,repaired_sep,repaired_llr,kl,effect.audit.certificate_valid),
    }

def targeted_repair_trajectory():
    """Exercise covariance-only, predictive, temporal, and coverage repairs."""
    cases={
        "covariance":AssumptionAudit(True,False,True,True),
        "predictive":AssumptionAudit(True,True,True,False),
        "temporal":AssumptionAudit(True,True,False,True),
        "coverage":AssumptionAudit(False,True,True,True),
    }
    return {name:repaired_record(i,a,.12,5.2,[.7])
            for i,(name,a) in enumerate(cases.items())}

def recoverable_trajectory():
    a=recovery_action()
    return [
        state(0,-.30,.2,[.5],True),
        state(1,-.08,2.0,[.5],True),
        state(2,.05,3.7,[.5],True),
        state(3,.08,4.8,[.5],True),
        # Inject calibration/model failure after an earlier certificate.
        state(4,.10,5.3,[.5],False,[a],0,3),
        state(5,.04,4.0,[.6],False,[a],1,3),
        # Recalibration is declared restored here; evidence is rebuilt.
        state(6,.03,4.2,[.6],True),
        state(7,.07,5.0,[.6],True),
    ]

def unidentifiable_trajectory():
    return [
        state(0,-.10,.0,[.2],True),
        state(1,.03,.0,[0.,0.],True),
    ]

def unrecoverable_trajectory():
    # Available action cannot restore calibration, so fail closed.
    bad=ReacquisitionAction(
        "more_of_same_sensor",True,False,True,True,
        expected_kl=2.,structural_gain=2.,cost=0.,
    )
    return [state(0,.4,8.,[1.],False,[bad],0,3)]

def budget_exhaustion_trajectory():
    a=recovery_action()
    return [
        state(0,-.2,1.,[.5],False,[a],0,2),
        state(1,-.1,2.,[.5],False,[a],1,2),
        state(2,-.05,3.,[.5],False,[a],2,2),
    ]

def main():
    payload={
        "scope":"deterministic state-machine stress protocol; not empirical performance",
        "recoverable":recoverable_trajectory(),
        "unidentifiable":unidentifiable_trajectory(),
        "unrecoverable":unrecoverable_trajectory(),
        "budget_exhaustion":budget_exhaustion_trajectory(),
        "targeted_repairs":targeted_repair_trajectory(),
    }
    out=Path("docs/self_certifying_observer_trajectories.json")
    out.write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps(payload,indent=2))

if __name__=="__main__":
    main()
