import pytest
from observer_math.boundary_confidence_set import BoundaryEvidenceEnvelope


def test_p62_robust_evidence_is_weakest_admissible_boundary():
    e = BoundaryEvidenceEnvelope({"W1": 30.0, "W2": 8.0, "W3": 25.0}, delta=0.05, alpha=0.05)
    assert e.robust_evidence == 8.0
    assert e.weakest_worldtubes == ("W2",)
    assert not e.robust_reject


def test_p62_rejects_only_when_every_admissible_boundary_crosses():
    e = BoundaryEvidenceEnvelope({"W1": 30.0, "W2": 20.0, "W3": 25.0}, delta=0.05, alpha=0.05)
    assert e.robust_evidence == 20.0
    assert e.robust_reject
    assert e.end_to_end_error_budget == pytest.approx(0.10)


def test_p62_ambiguous_boundary_blocks_overstatement():
    e = BoundaryEvidenceEnvelope({"winner": 100.0, "plausible_competitor": 1.2}, delta=0.01, alpha=0.05)
    assert not e.robust_reject
    assert e.weakest_worldtubes == ("plausible_competitor",)


@pytest.mark.parametrize("values", [{}, {"W": -0.1}])
def test_p62_rejects_invalid_evidence_sets(values):
    with pytest.raises(ValueError):
        BoundaryEvidenceEnvelope(values, delta=0.05, alpha=0.05)
