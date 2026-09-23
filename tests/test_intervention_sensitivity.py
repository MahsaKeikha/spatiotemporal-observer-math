import numpy as np

from observer_math.intervention_sensitivity import evaluate_single_block_intervention


def test_p78_reports_actual_pipeline_change_not_local_proxy():
    def evaluator(block_id, radius):
        assert block_id == "B7"
        if radius > 0.2:
            return 12, 2.0
        return 3, 8.5

    out = evaluate_single_block_intervention("B7", 0.4, 0.1, evaluator)
    assert out.ambiguity_reduction == 9
    assert np.isclose(out.evidence_gain, 6.5)


def test_p78_does_not_allow_uncertainty_increase_to_masquerade_as_tightening():
    try:
        evaluate_single_block_intervention("B", 0.1, 0.2, lambda _b, _r: (1, 1.0))
    except ValueError as exc:
        assert "must not increase" in str(exc)
    else:
        raise AssertionError("expected ValueError")
