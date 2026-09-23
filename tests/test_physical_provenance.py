from observer_math.physical_provenance import (
    PhysicalUncertaintyBlock,
    trace_bottleneck_provenance,
    unique_channels,
)


def test_p77_traces_edge_to_declared_measurement_blocks():
    a = PhysicalUncertaintyBlock("target_t1", 1, (1, 2, 3), "target covariance")
    b = PhysicalUncertaintyBlock("source_t0", 0, (0, 1, 2), "source covariance")
    p = trace_bottleneck_provenance(
        kind="edge", time=0, source=4, target=7,
        node_blocks={},
        edge_blocks={(0, 4, 7): (a, b)},
    )
    assert p.blocks == (a, b)
    assert unique_channels(p) == (0, 1, 2, 3)


def test_p77_missing_mapping_is_explicitly_empty():
    p = trace_bottleneck_provenance(
        kind="node", time=2, source=5, target=None,
        node_blocks={}, edge_blocks={},
    )
    assert p.blocks == ()
