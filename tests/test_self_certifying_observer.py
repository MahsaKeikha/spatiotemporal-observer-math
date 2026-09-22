from observer_math.reacquisition import ReacquisitionAction
from observer_math.self_certifying_observer import ObserverState,recovery_transition,transition

def recovery(name="recalibrate"):
    return ReacquisitionAction(name,True,True,True,True,.5,.5,0.)

def test_valid_but_incomplete_state_measures_more():
    s=transition(robust_separation=-.1,log_evidence=1.,evidence_threshold=4.6,
                 available_kl=[.2],assumptions_valid=True)
    assert s.state==ObserverState.MEASURE_MORE

def test_equivalence_is_terminal_abstention_not_reacquisition():
    s=transition(robust_separation=.2,log_evidence=0.,evidence_threshold=4.6,
                 available_kl=[0.,0.],assumptions_valid=True,recovery_actions=[recovery()])
    assert s.state==ObserverState.ABSTAIN_UNIDENTIFIABLE

def test_invalid_assumptions_enter_reacquisition_only_with_valid_recovery_action():
    s=transition(robust_separation=-.1,log_evidence=1.,evidence_threshold=4.6,
                 available_kl=[.2],assumptions_valid=False,recovery_actions=[recovery()])
    assert s.state==ObserverState.REACQUIRE
    assert s.action=="recalibrate"

def test_invalid_assumptions_without_recovery_fail_closed():
    s=transition(robust_separation=10.,log_evidence=100.,evidence_threshold=4.6,
                 available_kl=[1.],assumptions_valid=False,recovery_actions=[])
    assert s.state==ObserverState.ABSTAIN_UNRECOVERABLE

def test_budget_exhaustion_blocks_recovery_loop():
    s=transition(robust_separation=-.1,log_evidence=1.,evidence_threshold=4.6,
                 available_kl=[.2],assumptions_valid=False,recovery_actions=[recovery()],
                 reacquisition_steps=3,reacquisition_budget=3)
    assert s.state==ObserverState.ABSTAIN_UNRECOVERABLE

def test_recovery_can_return_to_certificate():
    assert recovery_transition(steps_used=2,step_budget=3,
        assumptions_restored=True,certificate_restored=True)==ObserverState.CERTIFY
