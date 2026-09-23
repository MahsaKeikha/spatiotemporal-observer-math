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


def test_targeted_repairs_reset_only_dependent_records():
    x=targeted_repair_trajectory()
    assert x["covariance"]["reset_structural"]
    assert not x["covariance"]["reset_evidence"]
    assert x["predictive"]["reset_evidence"]
    assert not x["predictive"]["reset_structural"]
    assert x["temporal"]["reset_structural"] and x["temporal"]["reset_evidence"]
    assert x["coverage"]["reset_candidates"]
    assert x["coverage"]["reset_structural"] and x["coverage"]["reset_evidence"]

def test_reset_records_cannot_immediately_recertify():
    x=targeted_repair_trajectory()
    for case in x.values():
        if case["reset_structural"] or case["reset_evidence"]:
            assert case["post_repair"]["state"]!="CERTIFY"
