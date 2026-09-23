import numpy as np

from observer_math.score_interval_graph import compress_score_interval_graph


def test_bd_graph_compression_handles_full_research_i_graph_shape():
    t_count, c_count = 5, 35
    local = np.zeros((t_count, c_count))
    local[:, 0] = 1.0
    local_errors = np.full_like(local, 0.01)
    transport = np.zeros((t_count - 1, c_count, c_count))
    transport_errors = np.full_like(transport, 0.01)
    continuity = np.zeros((c_count, c_count))
    out = compress_score_interval_graph(
        local, local_errors, transport, transport_errors, continuity,
        transport_weight=0.25, continuity_weight=0.08,
    )
    assert out.retained_nodes.shape == (5, 35)
    assert out.retained_edges.shape == (4, 35, 35)
    assert np.all(out.retained_nodes[:, 0])


def test_bd_smaller_uniform_score_uncertainty_cannot_reduce_graph_retention():
    t_count, c_count = 5, 35
    local = np.zeros((t_count, c_count))
    local[:, 0] = 1.0
    transport = np.zeros((t_count - 1, c_count, c_count))
    continuity = np.zeros((c_count, c_count))
    coarse = compress_score_interval_graph(
        local, np.full_like(local, 0.05), transport,
        np.full_like(transport, 0.05), continuity,
        transport_weight=0.25, continuity_weight=0.08,
    )
    fine = compress_score_interval_graph(
        local, np.full_like(local, 0.01), transport,
        np.full_like(transport, 0.01), continuity,
        transport_weight=0.25, continuity_weight=0.08,
    )
    assert np.sum(fine.retained_nodes) <= np.sum(coarse.retained_nodes)
    assert np.sum(fine.retained_edges) <= np.sum(coarse.retained_edges)
