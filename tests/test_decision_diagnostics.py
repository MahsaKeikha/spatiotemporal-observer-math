import math
from observer_math.decision_diagnostics import diagnose_certificate_state, evidence_measurement_lower_bound

def test_reducible_uncertainty_requests_more_measurement():
    d=diagnose_certificate_state(robust_separation=-.2,log_evidence=1.,evidence_threshold=4.6,
                                 available_kl=[.1,.3],assumptions_valid=True)
    assert d.decision=="MEASURE_MORE"
    assert d.structural_deficit==.2
    assert d.evidence_deficit>0

def test_exact_nonidentifiability_abstains_instead_of_requesting_data_forever():
    d=diagnose_certificate_state(robust_separation=.1,log_evidence=0.,evidence_threshold=4.6,
                                 available_kl=[0.,0.],assumptions_valid=True)
    assert d.decision=="ABSTAIN_UNIDENTIFIABLE"
    assert math.isinf(evidence_measurement_lower_bound(d.evidence_deficit,d.best_available_kl))

def test_invalid_assumptions_dominate_apparent_certainty():
    d=diagnose_certificate_state(robust_separation=10.,log_evidence=100.,evidence_threshold=4.6,
                                 available_kl=[1.],assumptions_valid=False)
    assert d.decision=="ABSTAIN_INVALID_ASSUMPTIONS"

def test_complete_valid_gates_certify():
    d=diagnose_certificate_state(robust_separation=.01,log_evidence=4.6,evidence_threshold=4.6,
                                 available_kl=[.2],assumptions_valid=True)
    assert d.decision=="CERTIFY"

def test_expected_evidence_budget_lower_bound():
    assert evidence_measurement_lower_bound(4.6,.5)==10


def test_zero_structural_separation_does_not_certify():
    x=diagnose_certificate_state(
        robust_separation=0.0,log_evidence=10.0,evidence_threshold=4.0,
        available_kl=[1.0],assumptions_valid=True)
    assert x.decision=="MEASURE_MORE"
    assert x.structural_deficit==0.0

def test_positive_structural_separation_can_certify():
    x=diagnose_certificate_state(
        robust_separation=1e-12,log_evidence=4.0,evidence_threshold=4.0,
        available_kl=[1.0],assumptions_valid=True)
    assert x.decision=="CERTIFY"
