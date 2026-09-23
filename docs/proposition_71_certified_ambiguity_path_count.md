# Proposition 71: exact ambiguity-path counting on the certified graph

P69 compresses a layered world-tube graph without enumerating complete paths. P71 quantifies the residual ambiguity by counting every complete path that remains in that certified graph.

Let R^V(t,j) indicate that candidate j survives at time t and R^E(t,i,j) indicate that transition i to j survives between adjacent layers. Define forward counts

c_0(j) = R^V(0,j)

and

c_t(j) = R^V(t,j) sum_i c_{t-1}(i) R^E(t-1,i,j).

Then the total number of complete retained world-tubes is

N_R = sum_j c_{T-1}(j).

This recursion is exact for the retained graph and requires O(T C^2) arithmetic. It does not enumerate the N_R paths.

## Interpretation

N_R is the number of complete paths compatible with the graph-level P69 certificate. It is therefore a sharper ambiguity measure than retained-node or retained-edge counts alone.

A graph may retain many nodes yet admit very few complete paths, or retain relatively few edges arranged into many combinations. P71 makes that distinction explicit.

## Verification

The claim-level tests compare the dynamic count against exhaustive enumeration on a small graph and verify that a complete T=5, C=35 graph returns exactly 35^5 = 52,521,875 paths.

## Scientific boundary

P71 counts paths in the retained certificate graph. It does not assign probabilities to those paths and does not claim that every retained path is equally plausible.
