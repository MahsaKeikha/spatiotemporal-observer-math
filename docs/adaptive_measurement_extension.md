# Adaptive Measurement Extension

Research I asks whether a time-dependent subsystem boundary can be inferred from the stochastic dynamics of a measured system. The next engineering extension closes the loop around that inference: the measurement system can use the inferred boundary and its certified uncertainty to decide **how to measure next**.

This is not a replacement for the consciousness research question. It is an operational extension of it.

## From passive observation to adaptive measurement

The original inference pipeline is

\[
X_{0:T}
\longrightarrow
\widehat{\mathcal W}
=
(\widehat S_0,\ldots,\widehat S_{T-1}),
\]

where \(\widehat S_t\) is the selected subsystem boundary at time \(t\).

For an adaptive measurement device, introduce a sensing configuration \(a_t\). It may encode which channels are sampled, sampling cadence, measurement resolution, gain/range, or another physically defined acquisition setting. The observation law becomes

\[
Y_t = H(a_t)X_t + v_t.
\]

The device therefore has two coupled dynamical objects:

\[
\text{physical dynamics}
\qquad\text{and}\qquad
\text{measurement dynamics}.
\]

The proposed extension is to make the second respond to uncertainty in the first.

## Certified observer state

Define the device observer state

\[
Z_t=
\bigl(
\widehat X_t,
\widehat S_t,
\mathcal C_t,
\Delta_t
\bigr),
\]

where

- \(\widehat X_t\) is the estimated measured-system state;
- \(\widehat S_t\) is the selected moving boundary;
- \(\mathcal C_t\) is the retained candidate/certification set;
- \(\Delta_t\) is the current winning-versus-competing path margin.

The key design principle is that **a boundary estimate and confidence in that estimate are different state variables**.

## Certification-gated sensing law

Let \(\mathcal A\) be the admissible set of sensing configurations. A general adaptive acquisition law is

\[
a_{t+1}
=
\pi_{\mathrm{meas}}
\left(
\widehat X_t,
\widehat S_t,
\mathcal C_t,
\Delta_t
\right),
\qquad
a_{t+1}\in\mathcal A.
\]

This creates the loop

\[
\boxed{
\text{measure}
\to
\text{infer boundary}
\to
\text{quantify uncertainty}
\to
\text{adapt measurement}
\to
\text{measure again}
}
\]

rather than treating sensing as a fixed front end.

## Three operational regimes

A certification-aware device naturally separates three regimes.

### Track

When one boundary path is well separated from its competitors, preserve the sensing configuration required to track the supported structure.

### Resolve

When competing boundaries remain plausible, allocate measurement effort toward channels or times expected to distinguish those competitors.

### Abstain

When the observation model does not support a unique structural interpretation, do not silently convert the optimizer into a physical claim. Preserve the ambiguity and use a conservative acquisition mode.

The abstention state follows directly from the existing distinction between optimization recovery and observational identifiability.

## Active-resolution objective

For candidate sensing action \(a\), define a future ambiguity functional

\[
\mathcal U_t(a)
=
\mathbb E
\left[
\Phi\!\left(
\mathcal C_{t+1},
\Delta_{t+1}
\right)
\mid
\mathcal F_t,a
\right],
\]

where \(\Phi\) is a declared uncertainty functional and \(\mathcal F_t\) is the information available at time \(t\).

A measurement action can then be selected by

\[
a_{t+1}
\in
\arg\min_{a\in\mathcal A}
\left\{
\mathcal U_t(a)
+
\lambda_E C_E(a)
+
\lambda_S C_S(a,a_t)
\right\}.
\]

Here \(C_E\) penalizes measurement expenditure and \(C_S\) penalizes excessive sensing reconfiguration.

This equation defines an engineering direction, not yet a proved optimal policy. Its value is that it connects the existing Research I uncertainty objects directly to the next measurement decision.

## Boundary-margin targeting

The path margin supplies a particularly natural control target. Instead of maximizing an abstract observer score, the adaptive device can seek measurements expected to increase separation between the current winner and its strongest plausible competitor.

If \(p^{(1)}\) and \(p^{(2)}\) denote the leading paths, define

\[
\Delta_t
=
A_t\!\left(p^{(1)}\right)
-
A_t\!\left(p^{(2)}\right).
\]

A candidate measurement action is valuable when it is expected to increase discriminative evidence for the coordinates and transitions on which those paths disagree.

This makes the near-competitor structure computationally useful: measurement effort can be concentrated on the unresolved part of the structural decision instead of uniformly increasing all sensing.

## Consciousness-measurement interpretation

The extension preserves a strict interpretation boundary. The device measures physical signals and computes operational dynamical quantities. The inferred moving boundary is a candidate structural correlate under the declared model.

Accordingly, the adaptive loop is designed to **improve the resolution and certification of the operational measurement problem**. It does not assume that increasing a score increases consciousness, and it does not equate a selected boundary with phenomenal experience.

## Why the extension belongs to Research I

The adaptive measurement loop uses objects already developed by the Research I program:

\[
\text{world-tube path}
+
\text{runner-up structure}
+
\text{recovery margin}
+
\text{candidate localization}
+
\text{finite-sample uncertainty}
+
\text{identifiability boundary}.
\]

The new engineering question is therefore not an unrelated feedback problem. It is:

> **Can a measurement system use the uncertainty structure of a moving-boundary inference problem to decide where, when, and how to acquire the next evidence?**

That question provides a direct bridge from the mathematical consciousness-measurement program to a physical adaptive measurement device.

## Evidence boundary

This page defines the adaptive-measurement architecture and the mathematical objects that connect it to Research I. Performance, stability, information gain, and device-level advantages become established results only when the corresponding derivations and reproducible experiments are added to the research record.


## Next mathematical layer

The first concrete policy derived from this architecture is the [Competitor-Directed Active Measurement](competitor_directed_active_measurement.md) construction. It converts the disagreement geometry of retained world-tube hypotheses into a budgeted sensing objective, proves the exact optimizer for the basic cardinality-constrained case, and separates set-disagreement coverage from true statistical discriminability.
