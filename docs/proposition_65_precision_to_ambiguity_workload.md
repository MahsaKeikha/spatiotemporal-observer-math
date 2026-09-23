# Proposition 65: Precision-to-ambiguity workload monotonicity

## Engineering question

Once P64 has converted measurement uncertainty into path-action intervals and P63 has defined a safe retained set, what does improved measurement precision buy the downstream system?

P65 isolates one auditable answer under a declared common radius scaling.

Let each path p have nominal action a_p and certified base radius r_p >= 0. At uncertainty scale c >= 0, define

I_p(c) = [a_p - c r_p, a_p + c r_p].

With zero near-optimality tolerance, P63 retains p when

a_p + c r_p >= max_q(a_q - c r_q).

## Result

If 0 <= c1 <= c2, then every path retained at c1 is also retained at c2. Equivalently, decreasing the common uncertainty scale cannot increase the number of paths requiring downstream evaluation.

### Proof

For every p, the upper endpoint a_p+c r_p is nondecreasing in c. The best certified lower bound max_q(a_q-c r_q) is nonincreasing in c. Therefore, if the retention inequality holds at c1, it also holds at every c2 >= c1. Hence R(c1) is a subset of R(c2).

## Meaning

This turns measurement precision into a directly interpretable engineering resource. Under the common-scale model, tighter valid uncertainty can only preserve or reduce the boundary ambiguity passed to Research II.

The theorem does not say that collecting more samples always produces a common multiplicative radius reduction. That link belongs to the upstream measurement theorem. P65 begins only after a valid family of scaled action intervals has been declared.

## Experiment AX

Experiment AX uses the population best and runner-up action values from the controlled moving-module record as two of six nominal path actions, then applies controlled action-radius scales. It records how many paths remain after P63 at each uncertainty scale.

The experiment is deliberately an engineering diagnostic, not a sensor sample-complexity claim. Its purpose is to expose the map

uncertainty width -> retained physical ambiguity -> downstream evaluation workload.

The next experiment will connect the scale to actual P58 covariance-derived score radii on a tractable controlled benchmark.

## Scientific boundary

A smaller retained set means that the declared uncertainty intervals separate more candidate physical trajectories. It does not imply that the retained path is conscious or that downstream experiential claims have been established.
