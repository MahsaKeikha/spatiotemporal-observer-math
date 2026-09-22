from observer_math.reacquisition import (
    ReacquisitionAction,bounded_reacquisition_status,select_reacquisition_action,
)

def action(name,**kw):
    base=dict(restores_coverage=True,restores_calibration=True,restores_temporal_model=True,
              restores_predictive_model=True,expected_kl=.5,structural_gain=.4,cost=0.)
    base.update(kw)
    return ReacquisitionAction(name=name,**base)

def test_reacquisition_requires_restoring_all_validity_gates():
    bad=action("bad",restores_calibration=False,expected_kl=10.,structural_gain=10.)
    plan=select_reacquisition_action([bad],evidence_deficit=1.,structural_deficit=.2)
    assert plan.decision=="ABSTAIN_UNRECOVERABLE_WITH_AVAILABLE_ACTIONS"

def test_reacquisition_rejects_information_free_action_when_evidence_needed():
    zero=action("zero",expected_kl=0.)
    plan=select_reacquisition_action([zero],evidence_deficit=1.,structural_deficit=.2)
    assert plan.action is None

def test_bottleneck_policy_prefers_balanced_recovery():
    structural=action("structural",expected_kl=.05,structural_gain=1.)
    balanced=action("balanced",expected_kl=.5,structural_gain=.5)
    plan=select_reacquisition_action([structural,balanced],evidence_deficit=.5,structural_deficit=.5)
    assert plan.decision=="REACQUIRE"
    assert plan.action=="balanced"

def test_reacquisition_budget_prevents_infinite_loop():
    assert bounded_reacquisition_status(steps_used=3,step_budget=3,
        assumptions_restored=False,certificate_restored=False
    )=="ABSTAIN_REACQUISITION_BUDGET_EXHAUSTED"

def test_recovered_validity_and_certificate_can_certify():
    assert bounded_reacquisition_status(steps_used=2,step_budget=3,
        assumptions_restored=True,certificate_restored=True)=="CERTIFY"
