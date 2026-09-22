import numpy as np
from observer_math.assumption_audit import AssumptionAudit
from observer_math.repair_semantics import canonical_repair_actions
from observer_math.reacquisition_ledger import (
    MeasurementLedger,acquire_certification_samples,acquire_predictive_evidence,
    apply_targeted_repair,evaluate_ledger,
)
LOCAL=np.array([[.7,.8,.75],[.72,.78,.77],[.74,.8,.76]])
TRANS=np.array([[.8,.75],[.79,.76]])
KW=dict(block_dimension=10,block_count=20,confidence=.95,
        leader_action=2.,competitor_action=1.,
        leader_local_factors=LOCAL,leader_transport_factors=TRANS,
        competitor_local_factors=LOCAL,competitor_transport_factors=TRANS,
        subset_size=3,ambient_size=7,transport_weight=.35)
def action(name):
    return next(a for a in canonical_repair_actions() if a.name==name)
def valid():
    return AssumptionAudit(True,True,True,True)

def test_covariance_repair_preserves_evidence_but_requires_new_structural_samples():
    x=MeasurementLedger(20000,7.,AssumptionAudit(True,False,True,True))
    x=apply_targeted_repair(x,action("RECALIBRATE_COVARIANCE"))
    assert x.log_evidence==7. and x.structural_stale and not x.evidence_stale
    assert evaluate_ledger(x,evidence_threshold=4.,available_kl=[1.],certificate_kwargs=KW).decision=="ABSTAIN_INVALID_ASSUMPTIONS"
    x=acquire_certification_samples(x,100)
    assert not x.structural_stale

def test_predictive_repair_preserves_samples_but_requires_new_evidence():
    x=MeasurementLedger(20000,7.,AssumptionAudit(True,True,True,False))
    x=apply_targeted_repair(x,action("RECALIBRATE_PREDICTIVE"))
    assert x.certification_samples==20000 and x.log_evidence==0.
    assert x.evidence_stale and not x.structural_stale
    x=acquire_predictive_evidence(x,5.)
    assert x.log_evidence==5. and not x.evidence_stale

def test_coverage_change_requires_both_records_to_be_rebuilt():
    x=MeasurementLedger(20000,7.,AssumptionAudit(False,True,True,True))
    x=apply_targeted_repair(x,action("EXPAND_CANDIDATES"))
    assert x.structural_stale and x.evidence_stale and x.log_evidence==0.
    x=acquire_certification_samples(x,100)
    assert x.evidence_stale
    x=acquire_predictive_evidence(x,5.)
    assert not x.structural_stale and not x.evidence_stale
