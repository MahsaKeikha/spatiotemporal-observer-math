# Proposition 74: critical uncertainty breakpoints for affine certificate comparisons

The BG experiment shows that the retained world-tube graph can remain essentially unchanged over a broad uncertainty range and then contract sharply. P74 identifies the algebraic mechanism behind such transitions when the relevant certified bounds are affine in a common uncertainty scale.

Let two competing certified quantities be

f(r) = a_0 + r a_1

and

g(r) = b_0 + r b_1.

Their ordering can change only at a positive solution of

a_0 + r a_1 = b_0 + r b_1,

namely

r* = (b_0 - a_0) / (a_1 - b_1),

when the denominator is nonzero and r* is positive and finite.

Therefore, for a finite family of affine comparisons, the certificate topology is piecewise constant between consecutive positive crossing radii. A graph-pruning decision can change only when at least one comparison reaches a breakpoint.

## Engineering meaning

Instead of choosing an arbitrary dense uncertainty grid, an implementation can enumerate the finite candidate crossing set, evaluate one representative radius in each open interval, and recover every distinct certificate regime induced by the affine model.

## Scope

P74 is an algebraic breakpoint result. It applies only where the relevant interval endpoints and comparison quantities are affine in the common uncertainty scale. It does not claim that raw sample size, sensor noise, or every upstream covariance theorem has an affine relationship to that scale.
