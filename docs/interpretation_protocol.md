# Interpretation protocol: from observer structure to consciousness hypotheses

This repository studies mathematically identifiable, persistent, integrated, and dynamically transported subsystem structure. Those are well-defined mathematical properties. Phenomenal consciousness is a different target.

This page states the rules that any future attempt to connect the two must satisfy.

The purpose is not to weaken the research program. It is to make the hardest question precise enough that progress can be recognized, challenged, reproduced, and falsified.

## The central distinction

Let

\[
\mathcal M
\]

be a class of dynamical models, and let

\[
\mathcal O(M)
\]

denote the probability law of the observations available from model \(M\).

The current repository defines and studies quantities such as world-tube action, integration, insulation, persistence, transport, covariance stability, and recovery margins. Collect them into a mathematical structural descriptor

\[
\mathcal S(M).
\]

A claim about phenomenal consciousness would require another object, for example

\[
\mathcal C(M),
\]

where \(\mathcal C\) is intended to encode some precisely stated consciousness property.

Nothing in the definition of \(\mathcal S\) alone implies a particular \(\mathcal C\). A bridge from structure to consciousness must therefore be stated as an additional hypothesis or axiom. It cannot be hidden inside notation or terminology.

## Identifiability comes first

Suppose two admissible models \(M_0,M_1\) satisfy

\[
\mathcal O(M_0)=\mathcal O(M_1)
\]

but a proposed consciousness assignment gives

\[
\mathcal C(M_0)\ne\mathcal C(M_1).
\]

Then no procedure using only the declared observations can distinguish the two consciousness assignments uniformly over the model class.

This is the same basic obstruction that appears in the repository's two-point identifiability result for subsystem boundaries. It is not specific to consciousness. It is a general fact about inference: observationally indistinguishable models cannot support uniformly distinguishable labels without additional information or assumptions.

A future consciousness interpretation must therefore answer both questions:

1. What mathematical property is being proposed as relevant?
2. Under what observables and assumptions is that property identifiable?

## The bridge must be explicit

A future bridge hypothesis should have a form that can be written down and criticized, for example

\[
B\bigl(\mathcal S(M),\mathcal K(M),\mathcal I(M)\bigr)
\Longrightarrow
\mathcal C(M),
\]

where:

- \(\mathcal S(M)\) contains structural quantities proved or estimated by this project;
- \(\mathcal K(M)\) could contain causal or counterfactual properties not recoverable from passive covariance alone;
- \(\mathcal I(M)\) could contain additional intervention, report, biological, or behavioral evidence;
- \(B\) is the proposed bridge statement.

The bridge must never be smuggled into the definition of an "observer." In this repository, observer remains an operational mathematical term for a candidate persistent subsystem structure.

## Requirements for a serious bridge hypothesis

### 1. Representation invariance

If two descriptions differ only by an admissible change of coordinates or relabeling, the proposed consciousness-relevant quantity should not change merely because the representation changed.

A future bridge must therefore specify a transformation group \(G\) and satisfy an invariance condition such as

\[
\mathcal C(g\cdot M)=\mathcal C(M)
\qquad
\text{for all }g\in G.
\]

The repository already treats symmetry and equivalence classes as central to boundary identifiability. Any consciousness interpretation must meet at least the same standard.

### 2. Nontriviality

The proposed property must distinguish meaningful model classes. A quantity that is almost always maximal, almost always zero, or determined only by system size is not enough.

There should be explicit positive controls, negative controls, and adversarial constructions.

### 3. Causal discriminability

Correlation alone can imitate integration and persistence. A serious bridge should eventually distinguish structures that merely share statistical dependence from structures whose organization survives appropriate interventions or counterfactual perturbations.

This suggests future quantities of the form

\[
\mathcal K_t(S)
=
D\left(
P(X_{S,t+1}\mid do(X_{S,t}=x)),
P(X_{S,t+1}\mid do(X_{S,t}=x'))
\right),
\]

for an appropriate divergence \(D\), or other intervention-sensitive objects.

The exact form remains an open research question. The requirement itself is clear: a proposed consciousness bridge should not be reducible to passive correlation when causal alternatives are observationally confounded.

### 4. Temporal identity

If consciousness is interpreted as belonging to a persisting system rather than a single instantaneous covariance matrix, the theory needs a mathematically explicit identity relation across time.

The world-tube formalism provides one candidate language:

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1}).
\]

But persistence of an optimizer is not automatically persistence of a subject. A bridge hypothesis must say what temporal equivalence means and which discontinuities break it.

### 5. Counterfactual robustness

A structurally meaningful boundary should not exist only at one exact parameter value. The repository's robustness and finite-sample theorems already quantify stability under perturbations.

A future bridge should require some analogue of

\[
\inf_{M'\in\mathcal N(M)}
\operatorname{margin}(M')>0
\]

for a declared neighborhood \(\mathcal N(M)\), or another explicit robustness criterion.

### 6. Empirical anchoring

Mathematics can prove consequences of assumptions. It cannot, by itself, determine that a chosen bridge axiom describes phenomenal experience in nature.

Any empirical bridge must therefore specify external anchors, such as controlled report, behavior, neural intervention, perturbational response, developmental dissociation, anesthesia transitions, sleep states, or other independently motivated measurements.

Which anchors are appropriate is an empirical question. The mathematical requirement is that they be declared before the bridge is evaluated.

### 7. Falsifiability

A bridge hypothesis should generate conditions under which it would be rejected.

A useful formal structure is:

\[
B\Longrightarrow P_1,P_2,\ldots,P_k,
\]

where at least some \(P_i\) are observations or intervention outcomes not used to fit \(B\).

If no conceivable result can count against a bridge, it is not being used as a scientific hypothesis.

### 8. No circular labels

A consciousness-relevant metric cannot be validated by defining "conscious" systems as systems with high values of the same metric.

Training labels, calibration criteria, and validation outcomes must be logically independent of the metric being tested.

### 9. Competing explanations

A future result should compare the proposed structural quantities with alternative explanations, including system size, signal-to-noise ratio, autocorrelation, connectivity density, common input, model complexity, and optimization bias.

The relevant question is not whether a proposed metric varies. It is whether it explains something that simpler confounds do not.

### 10. Out-of-family prediction

A strong theory should survive systems outside the family in which it was developed.

This repository currently has its sharpest finite-sample results in Gaussian separable models. A consciousness interpretation would require a much broader mathematical and empirical domain, including non-Gaussian, nonlinear, nonstationary, intervention-rich, and potentially nonbiological systems.

## A layered research architecture

To keep the project rigorous as it grows, the intended architecture is:

```text
Layer 1: exact dynamical and information-theoretic definitions
Layer 2: optimization and identifiability of moving subsystem structure
Layer 3: deterministic robustness and finite-sample statistical certification
Layer 4: causal and interventional observer structure
Layer 5: representation-invariant equivalence and temporal identity
Layer 6: explicitly stated consciousness bridge hypotheses
Layer 7: empirical tests capable of supporting or falsifying those hypotheses
```

The current repository is strongest in Layers 1 through 3 and is beginning to create the mathematical language needed for Layers 4 and 5.

Layers 6 and 7 are not implied by the existing propositions.

## What would count as a stronger future result?

Progress toward a mathematically serious theory of consciousness would include results such as:

- an observer property proved invariant under a broad class of physically irrelevant reparameterizations;
- an intervention-based boundary theorem that separates causal organization from passive common input;
- a temporal identity theorem that handles split, merge, replacement, and gradual substrate change;
- an impossibility theorem specifying exactly which consciousness distinctions cannot be identified from a declared observational interface;
- a bridge hypothesis that yields new, preregistered predictions across biological and artificial systems;
- a finite-sample theorem showing when those predictions are statistically distinguishable;
- a counterexample that rules out an attractive but incorrect bridge principle.

Negative results count as progress. An impossibility theorem can be more informative than a broad positive claim because it tells us what additional information is mathematically necessary.

## Language policy for this repository

The following distinctions are intentional:

- **proved:** a mathematical consequence derived from explicit assumptions;
- **certified:** a finite-sample or deterministic guarantee within a stated model class;
- **observed in an experiment:** a reproducible numerical result;
- **hypothesized:** a proposed relationship not yet proved or empirically established;
- **interpreted:** a conceptual reading that requires assumptions beyond the theorem itself.

The repository should not use "proof of consciousness," "consciousness detected," "universal consciousness equation," or equivalent language unless a future result actually supplies a defensible definition, bridge assumptions, identifiability argument, and evidence appropriate to that statement.

This restraint is part of the research method. It leaves room for ambitious mathematics while keeping every public claim auditable.

## Immediate mathematical frontier

The next work should continue in parallel along two tracks.

The statistical track should sharpen data-calibrated temporal confidence regions beyond rectangular lag bounds, then move toward broader spectral-density uncertainty sets.

The structural track should develop intervention-sensitive, representation-invariant observer quantities and prove what they can and cannot identify.

Only after those layers are sufficiently mature should a specific consciousness bridge hypothesis be treated as a formal object of study.
