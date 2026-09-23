import numpy as np
import pytest
from observer_math.assumption_audit import AssumptionAudit
from observer_math.data_split import DataSplitLedger,add_certification_samples,lock_design
from observer_math.repair_semantics import canonical_repair_actions
from observer_math.reacquisition_ledger import (
    MeasurementLedger,acquire_certification_samples,acquire_predictive_evidence,
    apply_targeted_repair,evaluate_ledger,evaluate_independent_split,mark_structural_rebuilt,
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
    assert evaluate_ledger(x,evidence_threshold=4.,available_kl=[1.],certificate_kwargs=KW).decision=="MEASURE_MORE"
    x=acquire_certification_samples(x,100)
    assert x.structural_stale
    x=mark_structural_rebuilt(x)
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


def test_independent_split_drives_certificate_sample_count():
    ledger=MeasurementLedger(999999,7.,valid())
    split=add_certification_samples(lock_design(DataSplitLedger(design_samples=20)),
                                    200,independent_of_design=True)
    out=evaluate_independent_split(ledger,split,evidence_threshold=4.,
                                   available_kl=[1.],certificate_kwargs=KW)
    assert out.sample_count==199

def test_nonindependent_split_cannot_enter_certificate_evaluator():
    ledger=MeasurementLedger(20000,7.,valid())
    split=add_certification_samples(lock_design(DataSplitLedger(design_samples=20)),
                                    200,independent_of_design=False)
    with pytest.raises(ValueError):
        evaluate_independent_split(ledger,split,evidence_threshold=4.,
                                   available_kl=[1.],certificate_kwargs=KW)


def test_repairs_or_compose_staleness_and_signed_evidence_is_valid():
    x=MeasurementLedger(20000,7.,AssumptionAudit(True,False,True,False))
    x=apply_targeted_repair(x,action("RECALIBRATE_COVARIANCE"))
    x=apply_targeted_repair(x,action("RECALIBRATE_PREDICTIVE"))
    assert x.structural_stale and x.evidence_stale
    x=acquire_predictive_evidence(x,-0.5)
    assert x.log_evidence==-0.5 and not x.evidence_stale
