# Experiment BC: certified graph compression without path enumeration

BC demonstrates P69 on a controlled layered graph with 8 time layers and 12 candidates per layer.

The explicit world-tube family contains 12^8 paths. P69 never enumerates those paths. It computes the best certified lower action plus node and edge upper max-marginals by dynamic programming, then removes graph elements that cannot lie on any near-optimal true path under the declared simultaneous interval event.

The experiment reports total and retained nodes and edges, compression fractions, the implicit path-family size, and the algorithmic complexity statement O(T C^2).

BC is an algorithmic certificate audit rather than a wall-clock benchmark. Runtime claims depend on implementation and hardware and are not inferred from this controlled example.

Generator: `../examples/certified_graph_compression_audit.py`. Machine-readable record: `certified_graph_compression_audit.json`.
