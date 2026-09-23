"""Controlled reacquisition after certificate failure.

Reacquisition does not override a failed assumption. It asks whether an
available measurement configuration can restore every required validity gate
and provide positive predictive information. If so, the observer enters a
bounded REACQUIRE state; otherwise it remains abstained.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class ReacquisitionAction:
    name: str
    restores_coverage: bool
    restores_calibration: bool
    restores_temporal_model: bool
    restores_predictive_model: bool
    expected_kl: float
    structural_gain: float
    cost: float = 0.0

    @property
    def restores_validity(self) -> bool:
        return all((self.restores_coverage,self.restores_calibration,
                    self.restores_temporal_model,self.restores_predictive_model))

@dataclass(frozen=True)
class ReacquisitionPlan:
    decision: str
    action: str | None
    utility: float
    reason: str

def select_reacquisition_action(actions, *, evidence_deficit: float,
                                structural_deficit: float,
                                kl_tolerance: float=1e-12) -> ReacquisitionPlan:
    """Select a valid recovery action or remain safely abstained.

    Utility is bottleneck-oriented: an action is useful only if it can restore
    the validity gates and address every currently positive deficit.
    """
    actions=tuple(actions)
    if evidence_deficit < 0 or structural_deficit < 0:
        raise ValueError("deficits must be nonnegative")
    if not actions:
        return ReacquisitionPlan("ABSTAIN_NO_RECOVERY_ACTION",None,0.0,"no actions available")
    feasible=[]
    for a in actions:
        if a.expected_kl < 0 or a.structural_gain < 0 or a.cost < 0:
            raise ValueError("action information, gain, and cost must be nonnegative")
        if not a.restores_validity:
            continue
        if evidence_deficit > 0 and a.expected_kl <= kl_tolerance:
            continue
        if structural_deficit > 0 and a.structural_gain <= 0:
            continue
        e=1.0 if evidence_deficit==0 else min(1.0,a.expected_kl/evidence_deficit)
        s=1.0 if structural_deficit==0 else min(1.0,a.structural_gain/structural_deficit)
        utility=min(e,s)-a.cost
        feasible.append((utility,a.name))
    if not feasible:
        return ReacquisitionPlan(
            "ABSTAIN_UNRECOVERABLE_WITH_AVAILABLE_ACTIONS",None,0.0,
            "no action restores validity while addressing active deficits")
    utility,name=max(feasible,key=lambda item:(item[0],item[1]))
    return ReacquisitionPlan("REACQUIRE",name,float(utility),
                             "validity-restoring action available")

def bounded_reacquisition_status(*, steps_used:int, step_budget:int,
                                 assumptions_restored:bool,
                                 certificate_restored:bool) -> str:
    """Finite recovery-state semantics prevent endless reacquisition loops."""
    if steps_used < 0 or step_budget < 1 or steps_used > step_budget:
        raise ValueError("require 0 <= steps_used <= step_budget")
    if assumptions_restored and certificate_restored:
        return "CERTIFY"
    if steps_used >= step_budget:
        return "ABSTAIN_REACQUISITION_BUDGET_EXHAUSTED"
    return "REACQUIRE"
