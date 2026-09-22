from examples.self_certifying_observer_trajectories import (
    budget_exhaustion_trajectory,recoverable_trajectory,
    unidentifiable_trajectory,unrecoverable_trajectory,
)

def states(rows):
    return [r["state"] for r in rows]

def test_recoverable_trajectory_contains_certificate_failure_and_recovery():
    s=states(recoverable_trajectory())
    assert "CERTIFY" in s[:4]
    assert "REACQUIRE" in s[4:6]
    assert s[-1]=="CERTIFY"

def test_exact_equivalence_terminates_as_unidentifiable():
    assert states(unidentifiable_trajectory())[-1]=="ABSTAIN_UNIDENTIFIABLE"

def test_nonrestoring_action_is_unrecoverable():
    assert states(unrecoverable_trajectory())==["ABSTAIN_UNRECOVERABLE"]

def test_reacquisition_budget_terminates_loop():
    assert states(budget_exhaustion_trajectory())[-1]=="ABSTAIN_UNRECOVERABLE"
