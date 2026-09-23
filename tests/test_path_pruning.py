import pytest

from observer_math.path_pruning import ActionInterval, prune_inadmissible_paths


def test_p63_prunes_only_paths_below_best_certified_lower_bound():
    intervals = {"A": ActionInterval(9.0, 11.0), "B": ActionInterval(7.0, 8.5), "C": ActionInterval(8.8, 10.2)}
    out = prune_inadmissible_paths(intervals)
    assert out.best_certified_lower_bound == 9.0
    assert out.retained == ("A", "C")
    assert out.pruned == ("B",)


def test_p63_tolerance_preserves_near_optimal_paths():
    intervals = {"A": ActionInterval(9.0, 11.0), "B": ActionInterval(8.2, 8.7), "C": ActionInterval(5.0, 6.0)}
    out = prune_inadmissible_paths(intervals, tolerance=0.5)
    assert out.retained == ("A", "B")
    assert out.pruned == ("C",)


def test_p63_does_not_prune_ambiguous_overlap():
    intervals = {"winner": ActionInterval(10.0, 10.5), "competitor": ActionInterval(9.9, 10.1)}
    out = prune_inadmissible_paths(intervals)
    assert out.retained == ("winner", "competitor")
    assert out.pruned == ()


def test_invalid_interval_is_rejected():
    with pytest.raises(ValueError):
        ActionInterval(2.0, 1.0)
