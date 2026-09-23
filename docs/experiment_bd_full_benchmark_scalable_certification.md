# Experiment BD: full moving-module scalable certification

BD applies the P58 -> P70 -> P69 chain to the canonical Research I moving-module population benchmark rather than the smaller controlled graphs used for interface tests.

The benchmark has n=7 physical nodes, subset size s=3, T=5 time layers, and C=35 candidate subsystem boundaries per layer. The corresponding implicit world-tube family contains 35^5 = 52,521,875 paths.

BD computes the population local and transport factors from the existing moving-module system, propagates a sweep of declared simultaneous relative covariance radii through P58, converts the resulting score uncertainty directly into P70 node/edge intervals, and runs P69 graph compression without enumerating the path family.

For every covariance radius it records retained nodes, retained edges, total graph size, P58 unique-recovery status, and P58 recovery slack.

The experiment separates two questions: whether graph ambiguity can be reduced computationally and whether the stronger unique population-path recovery theorem is satisfied. These need not occur at the same uncertainty level.

Scientific boundary: BD is a population benchmark plus declared covariance-radius sweep. It does not convert these radii into raw sensor sample counts. P67/P47 address finite-sample covariance radii under their own stated innovation assumptions.

Generator: `../examples/full_benchmark_scalable_certification.py`. Machine-readable record: `full_benchmark_scalable_certification.json`.
