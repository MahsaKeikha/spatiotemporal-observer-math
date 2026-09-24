import pytest

from observer_math.budgeted_precision_allocation import exact_budgeted_allocation


def test_p80_finds_interacting_pair_under_declared_budget():
    def evaluator(selected):
        if selected == {"B", "C"}:
            return 2, 0.5
        ambiguity = 20 - sum({"A": 8, "B": 4, "C": 3}[key] for key in selected)
        return ambiguity, float(ambiguity)

    result = exact_budgeted_allocation(
        {"A": 1.0, "B": 1.0, "C": 1.0},
        2.0,
        evaluator,
        max_cardinality=2,
    )
    assert result.intervention_ids == ("B", "C")
    assert result.ambiguity_count == 2
    assert result.feasible_subsets_evaluated == 7


def test_p80_respects_cost_and_deterministic_tie_breaks():
    result = exact_budgeted_allocation(
        {"A": 2.0, "B": 1.0, "C": 1.0},
        1.0,
        lambda selected: (10 if selected else 20, float(len(selected))),
    )
    assert result.intervention_ids == ("B",)
    assert result.total_cost == 1.0


def test_p80_rejects_invalid_costs():
    with pytest.raises(ValueError, match="positive"):
        exact_budgeted_allocation({"A": 0.0}, 1.0, lambda _selected: (1, 0.0))
