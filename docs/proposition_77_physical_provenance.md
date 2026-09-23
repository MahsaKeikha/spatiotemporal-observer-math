# Proposition 77: physical provenance for a decision-limiting graph element

P76 localizes the node or transition factor that suppresses evidence along the current P75 limiting world-tube. P77 adds the next engineering interface: every such graph element may carry an explicit provenance record listing the physical covariance or measurement blocks used to certify it.

The provenance map is declarative. For a node (t,j), it returns the registered uncertainty blocks used by that local candidate. For an edge (t,i,j), it returns the registered blocks used by the transition certificate. Each block records an identifier, time index, physical channels, and its role in the calculation.

This creates the auditable chain

decision-limiting world-tube -> weak node/transition -> uncertainty blocks -> physical channels.

## Why this matters

A numerical sensitivity result is not actionable if the system cannot say which measured quantities generated the uncertainty. P77 makes that dependency explicit and machine-readable. It also prevents a downstream algorithm from silently inventing sensor attribution from a mathematical score.

## Scope

P77 is a provenance theorem/interface, not a causal claim. A channel appearing in a covariance block does not prove that improving that sensor alone will remove the competing world-tube. The next stage must perturb or tighten declared block uncertainties and rerun the graph certificate to measure actual decision sensitivity.
