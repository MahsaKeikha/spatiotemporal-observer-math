# Competitor-Directed Active Measurement

The moving-boundary framework does more than return one selected path. It also exposes **where the structural decision remains unresolved**. This extension turns that geometry into a measurement policy.

## 1. Disagreement support

Let \(p^{(1)}=(S_0^{(1)},\ldots,S_T^{(1)})\) be the current winning path and \(p^{(2)}\) its strongest retained competitor. Define the time-indexed disagreement support

\[
D_t=S_t^{(1)}\triangle S_t^{(2)},
\]

where \(\triangle\) denotes symmetric difference.

For a retained competitor family \(\mathcal C_t\), define a weighted disagreement profile

\[
q_{t,j}
=
\sum_{p\in\mathcal C_t\setminus\{p^{(1)}\}}
w_t(p)\,
\mathbf 1\!\left\{
j\in S_t^{(1)}\triangle S_t^{(p)}
\right\},
\]

with nonnegative weights \(w_t(p)\) summing to one.

Thus \(q_{t,j}\) is not a generic sensor-importance score. It measures how strongly coordinate \(j\) participates in the **remaining structural ambiguity**.

## 2. Measurement action

Let \(a\in\mathcal A\) denote an admissible sensor configuration and let \(H(a)\) be its observation operator. Define a coordinate visibility vector \(h(a)\), where \(h_j(a)\in[0,1]\) represents how strongly configuration \(a\) observes coordinate \(j\).

A first disagreement-coverage functional is

\[
G_t(a)
=
\sum_{j=1}^{n}
q_{t,j}h_j(a).
\]

A cost-aware active measurement rule is

\[
a_{t+1}
\in
\arg\max_{a\in\mathcal A}
\left[
G_t(a)
-\lambda_E C_E(a)
-\lambda_S C_S(a,a_t)
\right].
\]

This is a transparent baseline for the adaptive device: measure where the surviving structural hypotheses disagree, subject to acquisition and switching costs.

## 3. Transition disagreement

World-tube ambiguity can occur in the transition itself even when two candidates overlap strongly. For competing edges \((S_t,R_{t+1})\) and \((S'_t,R'_{t+1})\), define

\[
D^{\rightarrow}_t
=
(S_t\triangle S'_t)
\cup
(R_{t+1}\triangle R'_{t+1}).
\]

A transition-aware acquisition policy can weight coordinates by disagreement in both source and destination sets. This connects active measurement to the transport component rather than only to static subset membership.

## 4. A basic deterministic result

**Proposition AM1 (optimal disagreement coverage under a cardinality budget).**

Assume an ideal channel-selection device in which an action is a subset \(A\subseteq\{1,\ldots,n\}\) with \(|A|\le b\), visibility is binary,

\[
h_j(A)=\mathbf 1\{j\in A\},
\]

and acquisition/switching costs are absent. Then every action containing the \(b\) largest values of \(q_{t,j}\) maximizes \(G_t(A)\).

**Proof.**
For binary visibility,

\[
G_t(A)=\sum_{j\in A}q_{t,j}.
\]

If an admissible \(A\) contains \(i\) while excluding \(j\) with \(q_{t,j}>q_{t,i}\), replacing \(i\) by \(j\) increases the objective by \(q_{t,j}-q_{t,i}>0\). Repeating the exchange until no such pair remains yields a set of the \(b\) largest weights. No other admissible set has larger total weight. \(\square\)

AM1 is intentionally elementary. Its role is to establish the exact optimizer for the first device-level acquisition objective before introducing probabilistic information-gain claims.

## 5. Why coverage alone is insufficient

High disagreement coverage does **not** imply that a measurement will statistically distinguish the competing paths. Two hypotheses may disagree in labels while inducing identical observable laws.

Therefore define, for two retained hypotheses \(p,r\), the action-dependent predictive laws

\[
P_{t+1}^{p,a},
\qquad
P_{t+1}^{r,a}.
\]

A statistically meaningful active policy must eventually depend on a divergence or certified separation between these predictive laws, not only on set disagreement.

This preserves the Research I distinction between optimization and observational identifiability.

## 6. Pairwise discriminability target

For an action \(a\), define a generic pairwise predictive separation

\[
\mathcal D_t(p,r;a)
=
D\!\left(
P_{t+1}^{p,a}
\,\|\,
P_{t+1}^{r,a}
\right),
\]

where the divergence \(D\) must be specified by the measurement model.

A robust max-min design is

\[
a_{t+1}
\in
\arg\max_{a\in\mathcal A}
\min_{r\in\mathcal C_t\setminus\{p^{(1)}\}}
\mathcal D_t(p^{(1)},r;a)
-
\lambda_E C_E(a)
-
\lambda_S C_S(a,a_t).
\]

This equation defines the next theoretical target: select the measurement that best separates the winner from its hardest surviving competitor.

No claim of optimal statistical discrimination is made until \(D\), the predictive family, and its finite-sample behavior are derived for the declared device model.

## 7. Candidate-local sensing

Research I already motivates localization of uncertainty to candidates and near competitors. Active measurement gives that localization a physical interpretation:

\[
\text{global candidate family}
\rightarrow
\text{near competitors}
\rightarrow
\text{disagreement coordinates}
\rightarrow
\text{targeted acquisition}.
\]

This can reduce unnecessary sensing if the unresolved structural decision depends on only a small part of the measured system.

## 8. Falsifiable experimental question

The first adaptive-measurement benchmark should compare:

- uniform/full sensing;
- fixed reduced sensing;
- random budget-matched sensing;
- disagreement-coverage sensing from \(G_t\);
- predictive-discrimination sensing once its model is implemented.

All policies must receive the same acquisition budget. Outcomes should include exact boundary-path recovery, candidate-set contraction, winning margin, time to certification, measurement cost, and failure/abstention frequency.

A useful adaptive policy must improve structural resolution **at equal or lower measurement budget**. Otherwise the added control layer is not justified.

## 9. Consciousness research boundary

This extension changes **how physical evidence is acquired** for the operational moving-boundary problem. It does not define a consciousness intervention and does not assume that a higher observer score corresponds to more subjective experience.

The scientific question remains whether measured dynamics support a coherent, persistent, insulated, and transporting subsystem boundary. The new contribution is to let unresolved structure guide the next physical measurement.
