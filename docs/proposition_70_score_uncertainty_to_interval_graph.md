# Proposition 70: direct score-uncertainty to certified interval graph

P70 connects the P58 score-level uncertainty output directly to the P69 layered graph, avoiding construction or enumeration of individual world-tube path intervals.

For local nominal score l(t,j) with error e_l(t,j), define node interval endpoints l-e_l and l+e_l.

For transport nominal score theta(t,i,j), transport error e_theta(t,i,j), transport weight chi, continuity weight lambda, and exact continuity cost d(i,j), define the edge nominal contribution

chi theta - lambda d

with radius

|chi| e_theta.

These node and edge intervals reproduce exactly the P64 lower and upper action interval for every individual path. Therefore P69 may operate directly on them while preserving P64's interval semantics.

## Equivalence contract

The claim-level test exhaustively enumerates a small graph and verifies that summing P70 node/edge endpoints along every path equals the corresponding P64 explicit path interval, up to floating-point tolerance.

## Consequence

P58 score radii can now flow directly into P69 graph compression in O(T C^2) graph operations rather than requiring a C^T path list.

## Scope

P70 is deterministic. Its validity is conditional on the validity and simultaneity of the upstream P58 score intervals. It introduces no additional confidence expenditure and does not broaden the upstream measurement assumptions.
