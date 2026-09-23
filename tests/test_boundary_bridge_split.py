import pytest

from observer_math.boundary_bridge_split import (
    BoundaryBridgeSplit,
    require_protected_boundary_bridge_split,
)


def test_p61_accepts_disjoint_frozen_handoff():
    split = BoundaryBridgeSplit(
        boundary_ids=frozenset({"b1", "b2"}),
        certification_ids=frozenset({"c1", "c2"}),
        boundary_frozen_before_certification=True,
    )
    assert split.protected
    require_protected_boundary_bridge_split(split)


def test_p61_rejects_observation_reuse():
    split = BoundaryBridgeSplit(
        boundary_ids=frozenset({"x", "b2"}),
        certification_ids=frozenset({"x", "c2"}),
        boundary_frozen_before_certification=True,
    )
    assert not split.protected
    with pytest.raises(ValueError, match="disjoint"):
        require_protected_boundary_bridge_split(split)


def test_p61_rejects_target_aware_boundary_revision():
    split = BoundaryBridgeSplit(
        boundary_ids=frozenset({"b1"}),
        certification_ids=frozenset({"c1"}),
        boundary_frozen_before_certification=True,
        certification_used_for_boundary_selection=True,
    )
    assert not split.protected
    with pytest.raises(ValueError, match="cannot select"):
        require_protected_boundary_bridge_split(split)


def test_p61_rejects_unfrozen_boundary():
    split = BoundaryBridgeSplit(
        boundary_ids=frozenset({"b1"}),
        certification_ids=frozenset({"c1"}),
        boundary_frozen_before_certification=False,
    )
    with pytest.raises(ValueError, match="frozen"):
        require_protected_boundary_bridge_split(split)
