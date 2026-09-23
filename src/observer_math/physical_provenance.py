"""P77: trace decision-limiting graph elements to declared physical uncertainty blocks."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PhysicalUncertaintyBlock:
    block_id: str
    time: int
    channels: tuple[int, ...]
    role: str


@dataclass(frozen=True)
class GraphElementProvenance:
    kind: str
    time: int
    source: int
    target: int | None
    blocks: tuple[PhysicalUncertaintyBlock, ...]


def trace_bottleneck_provenance(
    *,
    kind: str,
    time: int,
    source: int,
    target: int | None,
    node_blocks: dict[tuple[int, int], tuple[PhysicalUncertaintyBlock, ...]],
    edge_blocks: dict[tuple[int, int, int], tuple[PhysicalUncertaintyBlock, ...]],
) -> GraphElementProvenance:
    """Return declared physical uncertainty blocks used by a graph element."""
    if kind == "node":
        key = (time, source)
        blocks = node_blocks.get(key, ())
        resolved_target = None
    elif kind == "edge":
        if target is None:
            raise ValueError("edge provenance requires a target")
        key = (time, source, target)
        blocks = edge_blocks.get(key, ())
        resolved_target = target
    else:
        raise ValueError("kind must be node or edge")
    return GraphElementProvenance(kind, time, source, resolved_target, tuple(blocks))


def unique_channels(provenance: GraphElementProvenance) -> tuple[int, ...]:
    """Return sorted physical channels appearing in the declared provenance."""
    return tuple(sorted({channel for block in provenance.blocks for channel in block.channels}))
