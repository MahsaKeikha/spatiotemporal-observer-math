from observer_math.assumption_audit import AssumptionAudit
from observer_math.repair_semantics import (
    apply_repair,canonical_repair_actions,deterministic_repair_plan,
    execute_repair_plan,required_repairs,
)

def audit(c=True,v=True,t=True,p=True):
    return AssumptionAudit(c,v,t,p)

def test_covariance_repair_resets_only_structural_certificate():
    a=audit(v=False)
    action=[x for x in canonical_repair_actions() if x.name=="RECALIBRATE_COVARIANCE"][0]
    e=apply_repair(a,action)
    assert e.audit.certificate_valid
    assert e.reset_structural and not e.reset_evidence and not e.reset_candidates

def test_predictive_repair_invalidates_stale_likelihood_evidence():
    a=audit(p=False)
    action=[x for x in canonical_repair_actions() if x.name=="RECALIBRATE_PREDICTIVE"][0]
    e=apply_repair(a,action)
    assert e.audit.certificate_valid
    assert e.reset_evidence and not e.reset_structural

def test_candidate_expansion_invalidates_both_certificate_and_evidence():
    a=audit(c=False)
    e=execute_repair_plan(a)
    assert e.audit.certificate_valid
    assert e.reset_candidates and e.reset_structural and e.reset_evidence

def test_temporal_relocalization_invalidates_both_affected_records():
    e=execute_repair_plan(audit(t=False))
    assert e.audit.certificate_valid
    assert e.reset_structural and e.reset_evidence

def test_multiple_failures_get_sequential_repairs():
    a=audit(c=False,v=False,p=False)
    plan=deterministic_repair_plan(a)
    assert {x.name for x in plan}=={
        "EXPAND_CANDIDATES","RECALIBRATE_COVARIANCE","RECALIBRATE_PREDICTIVE"}
    e=execute_repair_plan(a)
    assert e.audit.certificate_valid
    assert e.reset_candidates and e.reset_structural and e.reset_evidence

def test_uncovered_failure_fails_closed():
    a=audit(p=False)
    assert deterministic_repair_plan(a,actions=())==()
    e=execute_repair_plan(a,actions=())
    assert not e.audit.certificate_valid
