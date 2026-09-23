# Proposition 62: Boundary Confidence-Set Propagation

## Question

P61 protects the clean case in which Research I selects one world-tube from pilot data and freezes it before downstream certification. That does not address a scientifically important case: the physical data may support several competing subsystem paths.

P62 keeps that ambiguity visible.

## Setup

Let \(D_B\) denote boundary-identification data and let

\[
\mathfrak W_\delta(D_B)
\]

be a set-valued Research I procedure satisfying

\[
\Pr(W_*\in\mathfrak W_\delta)\ge 1-\delta,
\]

for the declared true world-tube \(W_*\) under the boundary model.

For every \(W\in\mathfrak W_\delta\), construct the corresponding downstream physical descriptor \(Z^W\) and a nonnegative evidence variable \(E_W\) on protected certification data satisfying

\[
\mathbb E_{H_0(W)}[E_W\mid D_B]\le 1.
\]

Define the robust evidence envelope

\[
\boxed{
E_{\rm rob}=\inf_{W\in\mathfrak W_\delta}E_W.
}
\]

## Result 1: conditional union-null validity

For the union null

\[
H_0^{\rm rob}=\bigcup_{W\in\mathfrak W_\delta}H_0(W),
\]

the robust envelope obeys

\[
\boxed{
\mathbb E[E_{\rm rob}\mid D_B]\le 1
}
\]

whenever at least one member \(W_0\in\mathfrak W_\delta\) has a true downstream null.

### Proof

If \(H_0(W_0)\) is true for some \(W_0\) in the set, then pointwise

\[
E_{\rm rob}\le E_{W_0}.
\]

Taking conditional expectations gives

\[
\mathbb E[E_{\rm rob}\mid D_B]
\le
\mathbb E[E_{W_0}\mid D_B]
\le 1.
\]

Therefore Markov's inequality gives the conditional level rule

\[
\Pr(E_{\rm rob}\ge 1/\alpha\mid D_B)\le\alpha.
\]

The construction is conservative by design: strong evidence requires every still-admissible boundary to be incompatible with its corresponding downstream null.

## Result 2: end-to-end error accounting

Suppose the scientific claim of interest requires both:

1. coverage of the true physical world-tube by \(\mathfrak W_\delta\); and
2. rejection of the robust downstream union null at conditional level \(\alpha\).

Then the probability of a false end-to-end conclusion is bounded by

\[
\boxed{\delta+\alpha}
\]

by a union bound: at most \(\delta\) is spent on boundary-set noncoverage and at most \(\alpha\) on downstream rejection conditional on coverage.

This is a transparent engineering budget, not a claim that the sum is optimal.

## Why this matters

A common pipeline selects one physical boundary, computes a descriptor on that boundary, and forgets that competing boundaries existed. P62 instead propagates the set of physically admissible explanations into the downstream test.

This changes the scientific question from

> Is the target incompatible with the descriptor built on the winning boundary?

to

> Is the target incompatible with the declared descriptor family for every physical boundary that the upstream data still allow?

## Engineering requirements

The confidence set must record its coverage target, construction assumptions, candidate universe, and data lineage. The downstream evidence for each path must be computed on certification information protected from the construction of the set, or must use another selection-valid argument.

The robust envelope must be evaluated over the complete retained set. Approximate search may be used only with a certified lower bound on the infimum.

## Negative result

If even one admissible world-tube yields weak downstream evidence, the robust envelope remains weak. This is not a failure of the method. It identifies unresolved physical-boundary ambiguity as the reason a stronger downstream conclusion is not justified.

## Next step

P63 will use Research I path-score uncertainty and action margins to construct safe supersets of the admissible world-tubes and prune paths that provably cannot enter the boundary confidence set. The objective is computational compression without sacrificing the coverage guarantee used by P62.

## Scientific boundary

P62 is a theorem about propagation of subsystem-identification uncertainty into downstream model testing. It does not identify a world-tube, descriptor, latent target, or evidence variable with consciousness.
