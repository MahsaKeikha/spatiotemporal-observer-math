# Research I to Research II engineering handoff

## Purpose

This note defines the interface between subsystem identification and bridge-sufficiency testing. It does not assert that the inferred subsystem is consciousness and it does not assume that a Research II target is experiential ground truth.

The engineering problem is narrower:

> How can uncertainty about a moving physical boundary be carried into a downstream sufficiency test without silently treating an estimated boundary as known?

## Upstream object

Research I returns a world-tube estimate

\[
\widehat{\mathcal W}=(\widehat S_0,\ldots,\widehat S_{T-1})
\]

together with a candidate family, path scores, runner-up information, and, when available, a recovery or finite-sample certificate.

The downstream physical descriptor must therefore be treated as an estimated object,

\[
\widehat Z_t = F(X_t,\widehat S_t),
\]

rather than as a fixed oracle descriptor.

## Downstream question

Research II asks whether an independently declared target \(Y\) is adequately represented by a declared physical descriptor. The interface proposed here makes the descriptor depend explicitly on the inferred world-tube:

\[
Z_t^{\mathcal W}=F(X_t,S_t).
\]

The central cross-program question becomes

\[
\boxed{
\text{Does the sufficiency conclusion remain valid over every world-tube still compatible with the Research I uncertainty set?}
}
\]

## Boundary-robust sufficiency principle

Let \(\mathfrak W_\delta\) be a confidence set of admissible world-tubes produced without using the downstream target outcomes that will certify sufficiency.

For each \(W\in\mathfrak W_\delta\), let \(H_0(W)\) denote the declared Research II sufficiency/model null built from descriptor \(Z^W\).

A boundary-robust rejection must reject the union null

\[
H_0^{\mathrm{rob}}
=
\bigcup_{W\in\mathfrak W_\delta} H_0(W).
\]

Consequently, evidence against one selected world-tube is not enough. The downstream test must either:

1. certify the boundary first on independent data and then test the frozen descriptor on fresh target data; or
2. construct simultaneous evidence valid for every \(W\in\mathfrak W_\delta\).

This is the key engineering connection between the programs.

## Why this is a new research direction

Research I currently certifies or diagnoses uncertainty in *which physical subsystem is being followed*. Research II currently protects uncertainty, selection, cross-fitting, and sequential evidence *after a physical description has been declared*.

The missing interface is boundary uncertainty itself.

Treating that interface explicitly creates a joint problem in:

- stochastic subsystem identification;
- uncertainty sets over combinatorial world-tubes;
- descriptor construction on moving supports;
- selection-valid inference;
- robust model-family testing;
- sequential evidence accumulation.

## Proposed theorem sequence

**P61: sample-split boundary freeze.** Use a boundary-identification sample to construct and freeze \(\widehat{\mathcal W}\); use independent certification data for the downstream test. Prove that conditional downstream type-I control is preserved when the Research I selection is measurable with respect to the pilot sigma-field.

**P62: boundary confidence-set propagation.** Replace one selected path by \(\mathfrak W_\delta\). Derive a union-null test or lower evidence envelope that is valid simultaneously over the admissible paths.

**P63: path-margin compression.** Use Research I action margins to eliminate paths that cannot enter \(\mathfrak W_\delta\), reducing downstream multiplicity while retaining coverage.

**P64: cross-fitted world-tube descriptors.** Rotate boundary identification and downstream certification across independent folds so every observation can contribute without certifying a descriptor selected from itself.

**P65: sequential boundary-and-bridge e-process.** Combine fresh cross-fitted rounds with predictable stakes, extending the Research II sequential architecture to the case where the physical subsystem itself is re-estimated between rounds.

## Engineering acceptance criteria

A cross-program result is not considered complete unless it records:

- exactly which data identify the boundary;
- exactly which data define or measure the downstream target;
- whether those data overlap;
- the world-tube uncertainty object passed downstream;
- the physical descriptor induced by each admissible path;
- the null family being tested;
- selection and multiplicity accounting;
- finite-sample assumptions;
- a synthetic benchmark with known ground truth;
- negative controls where boundary ambiguity prevents a strong conclusion.

## Scientific boundary

Even a successful boundary-robust sufficiency test would establish a statement about a declared physical descriptor and an independently declared target under explicit assumptions. It would not by itself identify the target with consciousness or complete the physical-to-experiential bridge.
