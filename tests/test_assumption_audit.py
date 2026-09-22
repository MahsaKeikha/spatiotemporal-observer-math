from observer_math.assumption_audit import (
    AssumptionAudit, audited_certificate, calibration_stress, motion_regime_valid,
)

def valid_audit():
    return AssumptionAudit(True, True, True, True)

def test_valid_assumptions_allow_certificate_when_both_gates_pass():
    assert audited_certificate(
        robust_separation=.1, log_evidence=5., evidence_threshold=4.6, audit=valid_audit()
    ) == "CERTIFY"

def test_structural_or_evidence_deficit_requests_more_measurement():
    assert audited_certificate(
        robust_separation=-.01, log_evidence=9., evidence_threshold=4.6, audit=valid_audit()
    ) == "MEASURE_MORE"
    assert audited_certificate(
        robust_separation=.2, log_evidence=2., evidence_threshold=4.6, audit=valid_audit()
    ) == "MEASURE_MORE"

def test_any_invalid_certificate_assumption_forces_abstention():
    audits=[
        AssumptionAudit(False,True,True,True),
        AssumptionAudit(True,False,True,True),
        AssumptionAudit(True,True,False,True),
        AssumptionAudit(True,True,True,False),
    ]
    for audit in audits:
        assert audited_certificate(
            robust_separation=1.,log_evidence=100.,evidence_threshold=4.6,audit=audit
        ) == "ABSTAIN_INVALID_ASSUMPTIONS"

def test_under_calibrated_radius_is_detected():
    assert calibration_stress(.2,.2)
    assert not calibration_stress(.21,.2)

def test_abrupt_motion_outside_declared_envelope_is_detected():
    assert motion_regime_valid(.1,.1)
    assert not motion_regime_valid(.11,.1)
