# Engineering value gate for the Research I to Research II program

This document is a design constraint on the next research stage. A new proposition or experiment should not be added merely because it is mathematically possible. It should close a concrete engineering gap in the chain from uncertain subsystem identification to a downstream decision.

## System problem

A deployed inference system observes noisy multivariate dynamics, identifies a moving subsystem boundary, constructs a downstream descriptor from that boundary, and asks whether the descriptor is sufficient for a separately defined target. Boundary estimation is uncertain. Treating the selected boundary as known can make the downstream conclusion overconfident.

The engineering objective is therefore:

> produce a computationally tractable decision interface that carries physical boundary uncertainty into downstream evidence, identifies the unresolved boundary alternatives that limit a decision, and exposes what additional measurement precision would actually change that decision.

## Required value test

A proposed addition belongs in the core paper only if it materially improves at least one of these capabilities while preserving the others:

1. **Certifiability:** turns an informal uncertainty statement into a finite-sample or deterministic certificate.
2. **Scalability:** replaces exponential path enumeration with polynomial-time computation.
3. **Decision relevance:** changes or explains a downstream decision rather than only changing an internal score.
4. **Diagnostic value:** identifies which node, transition, sensor block, or boundary alternative is limiting certification.
5. **Design actionability:** maps the limiting object to a measurable engineering intervention such as precision, sensing, calibration, or protected-data allocation.
6. **Reproducibility:** produces source, tests, machine-readable results, and regenerated figures from one computation.

## Current contribution chain

P47/P58: finite-data covariance uncertainty to score uncertainty.

P70/P69: score uncertainty to a certified retained layered graph without enumerating all world-tubes.

P71: exact residual ambiguity count on that graph.

P72/P66: ambiguity cardinality is separated from robust downstream evidence.

P73/BG: precision, ambiguity, evidence, and workload are treated as separate engineering coordinates; the canonical benchmark reveals a sharp ambiguity-collapse regime.

P74: under affine uncertainty comparisons, certificate topology changes only at algebraic breakpoints, replacing arbitrary dense uncertainty sweeps with regime analysis.

P75: when an already-valid positive path evidence factorization is available, worst-case retained-path evidence and its limiting path are computed exactly in O(T C^2).

## Missing engineering capability

The next central gap is **actionable sensitivity**. P75 can identify the limiting world-tube, but it does not yet answer:

- Which local node or transition on that path is responsible for weak robust evidence?
- Which physical uncertainty block keeps that alternative in the retained graph?
- How much tightening of a declared uncertainty radius is required before that limiting alternative is certified away?
- Would that tightening actually change the downstream robust conclusion?

This gap should drive the next propositions and experiments. A generic new score, visualization, or mathematical extension that does not answer one of these questions should remain outside the core research path.

## Intended engineering deliverable

The target is a boundary-uncertainty-aware decision support layer with this interface:

physical measurements -> certified uncertainty -> retained boundary graph -> limiting robust-evidence path -> bottleneck localization -> required precision change -> recomputed downstream decision.

This is an engineering architecture. It does not identify consciousness, assign probabilities to retained paths, or claim that every application has the same utility or sensing cost.
