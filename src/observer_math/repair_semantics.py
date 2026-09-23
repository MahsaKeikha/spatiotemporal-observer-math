"""Assumption-specific repair semantics for certificate reacquisition.

A repair action need only restore assumptions that are currently invalid.
Repair can invalidate stale structural or likelihood evidence. The reset flags
make that loss of evidential validity explicit instead of silently reusing it.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from .assumption_audit import AssumptionAudit

@dataclass(frozen=True)
class RepairAction:
    name: str
    repairs_coverage: bool=False
    repairs_covariance_calibration: bool=False
    repairs_temporal_model: bool=False
    repairs_predictive_model: bool=False
    reset_structural: bool=False
    reset_evidence: bool=False
    reset_candidates: bool=False
    cost: float=0.0

@dataclass(frozen=True)
class RepairEffect:
    audit: AssumptionAudit
    reset_structural: bool
    reset_evidence: bool
    reset_candidates: bool

def required_repairs(audit: AssumptionAudit) -> frozenset[str]:
    missing=set()
    if not audit.coverage_valid: missing.add("coverage")
    if not audit.covariance_calibration_valid: missing.add("covariance_calibration")
    if not audit.temporal_model_valid: missing.add("temporal_model")
    if not audit.predictive_model_valid: missing.add("predictive_model")
    return frozenset(missing)

def apply_repair(audit: AssumptionAudit, action: RepairAction) -> RepairEffect:
    if action.cost < 0:
        raise ValueError("repair cost must be nonnegative")
    updated=replace(
        audit,
        coverage_valid=audit.coverage_valid or action.repairs_coverage,
        covariance_calibration_valid=(
            audit.covariance_calibration_valid or action.repairs_covariance_calibration),
        temporal_model_valid=audit.temporal_model_valid or action.repairs_temporal_model,
        predictive_model_valid=(
            audit.predictive_model_valid or action.repairs_predictive_model),
    )
    return RepairEffect(updated,action.reset_structural,action.reset_evidence,
                        action.reset_candidates)

def canonical_repair_actions() -> tuple[RepairAction,...]:
    """Fail-closed defaults for the four public assumption gates."""
    return (
        RepairAction("EXPAND_CANDIDATES",repairs_coverage=True,
                     reset_structural=True,reset_evidence=True,reset_candidates=True),
        RepairAction("RECALIBRATE_COVARIANCE",repairs_covariance_calibration=True,
                     reset_structural=True),
        RepairAction("RELOCALIZE_TEMPORAL",repairs_temporal_model=True,
                     reset_structural=True,reset_evidence=True),
        RepairAction("RECALIBRATE_PREDICTIVE",repairs_predictive_model=True,
                     reset_evidence=True),
    )

def deterministic_repair_plan(audit: AssumptionAudit,
                              actions=None) -> tuple[RepairAction,...]:
    """Return the smallest canonical sequence covering all current failures."""
    actions=canonical_repair_actions() if actions is None else tuple(actions)
    missing=required_repairs(audit)
    plan=[]
    covered=set()
    for a in actions:
        repairs=set()
        if a.repairs_coverage: repairs.add("coverage")
        if a.repairs_covariance_calibration: repairs.add("covariance_calibration")
        if a.repairs_temporal_model: repairs.add("temporal_model")
        if a.repairs_predictive_model: repairs.add("predictive_model")
        if (repairs & missing) - covered:
            plan.append(a); covered |= repairs & missing
    if covered != set(missing):
        return ()
    return tuple(plan)

def execute_repair_plan(audit: AssumptionAudit, actions=None) -> RepairEffect:
    plan=deterministic_repair_plan(audit,actions)
    if required_repairs(audit) and not plan:
        return RepairEffect(audit,False,False,False)
    effect=RepairEffect(audit,False,False,False)
    for action in plan:
        step=apply_repair(effect.audit,action)
        effect=RepairEffect(step.audit,
            effect.reset_structural or step.reset_structural,
            effect.reset_evidence or step.reset_evidence,
            effect.reset_candidates or step.reset_candidates)
    return effect
