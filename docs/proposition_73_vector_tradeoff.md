# Proposition 73: vector-valued precision, ambiguity, evidence, and workload tradeoff

The preceding results expose several scientifically distinct quantities: measurement uncertainty, certified physical ambiguity, robust downstream evidence, and computational workload. P73 formalizes that these should remain separate coordinates rather than being collapsed into an arbitrary scalar score.

Represent an operating point as

q = (delta, N_R, E_rob, W),

where delta is a declared uncertainty radius, N_R is the P71 retained path count, E_rob is P62/P66 robust evidence, and W is a declared graph workload such as retained edge count.

Point q1 dominates q2 only when it is no worse in every declared direction: smaller or equal delta, smaller or equal N_R, greater or equal E_rob, and smaller or equal W, with at least one strict improvement.

The nondominated set is the Pareto frontier.

## Why this matters

A smaller ambiguity count does not automatically compensate for weaker evidence, and stronger evidence does not automatically compensate for higher physical uncertainty. P73 therefore avoids inventing weights that would turn incomparable scientific quantities into a single opaque objective.

## Scope

The dominance relation is descriptive. It does not prescribe which operating point a scientist or engineer should prefer. Any application-specific utility or cost function must be declared separately.
