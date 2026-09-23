"""P61 sample-split boundary-freeze contracts.

The module encodes data-lineage checks for the Research I -> Research II handoff.
It does not implement or validate an experiential target.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class BoundaryBridgeSplit:
    boundary_ids: frozenset[str]
    certification_ids: frozenset[str]
    boundary_frozen_before_certification: bool
    certification_used_for_boundary_selection: bool = False

    @property
    def disjoint(self) -> bool:
        return self.boundary_ids.isdisjoint(self.certification_ids)

    @property
    def protected(self) -> bool:
        return (
            self.disjoint
            and self.boundary_frozen_before_certification
            and not self.certification_used_for_boundary_selection
        )


def require_protected_boundary_bridge_split(split: BoundaryBridgeSplit) -> None:
    """Reject a handoff that violates the declared P61 sample-split contract."""
    if not split.disjoint:
        raise ValueError("boundary and certification observations must be disjoint")
    if not split.boundary_frozen_before_certification:
        raise ValueError("boundary must be frozen before certification outcomes are inspected")
    if split.certification_used_for_boundary_selection:
        raise ValueError("certification outcomes cannot select their own physical boundary")
