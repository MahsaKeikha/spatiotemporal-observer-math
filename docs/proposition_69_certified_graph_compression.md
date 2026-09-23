# Proposition 69: polynomial-time certified graph compression

P63 safely prunes an explicitly enumerated collection of world-tube paths. P69 removes that enumeration requirement.

Consider a layered graph with T time layers and C candidate subsystem boundaries per layer. Let v^- and v^+ be simultaneous lower and upper node-action contributions and e^- and e^+ the corresponding edge contributions.

A max-plus forward dynamic program on lower weights computes

L_* = max_p L_p,

the best certified lower action over all paths.

Forward and backward dynamic programs on upper weights compute, for every node (t,j), the largest path upper bound among all paths constrained to pass through that node. The same construction gives an upper max-marginal for every edge.

For tolerance eta >= 0, prune a node or edge whenever its upper max-marginal is strictly below L_* - eta.

## Safety

If a true path p is eta-near-optimal, then A(p) >= A_* - eta >= L_* - eta. On the simultaneous interval event, U_p >= A(p). Every node and edge used by p therefore has upper max-marginal at least U_p and cannot be pruned.

Thus no eta-near-optimal true path is removed on the declared interval event.

## Complexity

The forward/backward recursions require O(T C^2) arithmetic and O(T C^2) storage when all edge max-marginals are retained. This replaces explicit enumeration of C^T world-tubes.

## Relationship to P63

P69 is not a heuristic approximation to P63. It computes graph-level upper max-marginals over the complete layered path family. The same interval logic is used, but impossible nodes and edges are removed before individual paths need to be listed.

## Scientific boundary

P69 is deterministic conditional on valid simultaneous node and edge intervals. It spends no additional probability budget and does not make the upstream measurement model more general.
