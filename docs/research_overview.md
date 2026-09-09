# Research overview

**Spatiotemporal Observer Mathematics** studies a single question:

> **When can a moving subsystem boundary be inferred from the dynamics of a larger measured physical system?**

The project begins from Max Tegmark's observer-factorization question in ["Consciousness as a State of Matter"](https://doi.org/10.1016/j.chaos.2015.03.014) and develops a time-dependent inference framework built around moving subsystem boundaries, recovery, identifiability, finite-sample measurement certification, physical relaxation time, innovation inference, and observer-scale uncertainty propagation.

For a visual first reading, use the [Visual Research Guide](visual_research_guide.md). For physical meaning and units, use the [Physics Guide](physics_guide.md). For equation-level provenance, use the [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md). For theorem-by-theorem navigation, use the [Research Index](research_index.md).

The current **0.47.1** research record contains **58 propositions, 45 reproducible experiments, 33 scientific result figures, and 223 claim-level tests** across Python 3.10, 3.11, and 3.12.

---

# 1. From factorization to a moving boundary

At time \(t\), let the measured state be

\[
X_t=(X_t^{(1)},\ldots,X_t^{(n)}).
\]

A candidate subsystem is

\[
S_t\subseteq\{1,\ldots,n\},
\]

and its time-dependent history is

\[
\boxed{
\mathcal W=(S_0,S_1,\ldots,S_{T-1}).
}
\]

The object of inference is therefore a path through subsystem space rather than a single static partition.

The central conceptual extension is:

```text
observer-factorization question
        -> time-dependent candidate boundary S_t
        -> dynamical coherence and insulation
        -> persistence and transport across time
        -> world-tube optimization
        -> recovery and identifiability
        -> finite-sample measurement certification
```

The explicit relationship to Tegmark's 2015 and 2016 work is documented in [README Section 13](../README.md#13-relationship-to-tegmarks-observer-factorization-question) and the [Bibliography and Citation Map](bibliography.md).

---

# 2. Physical observation model

The principal analytical model is

\[
\boxed{
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t),
\qquad
\varepsilon_t\perp X_t.
}
\]

Here \(A_t\) represents effective one-step propagation in the declared measured coordinates and \(Q_t\) represents unresolved stochastic forcing within the model.

If

\[
\Sigma_t=\operatorname{Cov}(X_t),
\]

then

\[
\Sigma_{t+1}=A_t\Sigma_tA_t^{\mathsf T}+Q_t,
\]

and the adjacent-state covariance is

\[
\boxed{
\operatorname{Cov}
\begin{pmatrix}
X_t\\X_{t+1}
\end{pmatrix}
=
\begin{pmatrix}
\Sigma_t & \Sigma_tA_t^{\mathsf T}\\
A_t\Sigma_t & A_t\Sigma_tA_t^{\mathsf T}+Q_t
\end{pmatrix}.
}
\]

This covariance geometry supplies the Gaussian information quantities used by the observer score.

[![Physics to inference pipeline](physics_pipeline.svg)](physics_guide.md)

---

# 3. Four operational dynamical factors

The framework uses four distinct properties.

## 3.1 Integration

For a nontrivial bipartition \(S=U\sqcup V\),

\[
J_t(U,V)
=
I(X_U^{t+1};X_V^t\mid X_U^t)
+
I(X_V^{t+1};X_U^t\mid X_V^t),
\]

\[
\boxed{
\mathcal J_t(S)
=
\frac{1}{|S|}
\min_{U\sqcup V=S}J_t(U,V).
}
\]

This asks whether parts of the candidate contribute predictive information about one another across the time step.

## 3.2 Environmental insulation

Let \(\bar S\) denote measured coordinates outside the candidate. Define

\[
\boxed{
\mathcal L_t(S)
=
\frac{1}{|S|}
I(X_S^{t+1};X_{\bar S}^t\mid X_S^t).
}
\]

This measures the residual predictive contribution of the measured exterior once the present candidate state is known.

## 3.3 Persistence

For vectors \(X\) and \(Y\), define the whitened cross-covariance

\[
C=\Sigma_X^{-1/2}\operatorname{Cov}(X,Y)\Sigma_Y^{-1/2}.
\]

If \(\rho_i\) are its singular values,

\[
\boxed{
P(X,Y)=\frac{1}{r}\sum_{i=1}^{r}\rho_i^2,
\qquad
r=\min(\dim X,\dim Y).
}
\]

This is built from canonical-correlation geometry in the lineage of [Hotelling 1936](bibliography.md#hotelling-1936).

## 3.4 Transport

For source candidate \(S\) at time \(t\) and target candidate \(R\) at time \(t+1\), the transport functional combines cross-boundary persistence with conditional insulation:

\[
\boxed{
\Theta_t(S\to R)
=
\sqrt{P_t(S\to R)2^{-L_t(S\to R)}}.
}
\]

This is the mathematical mechanism that allows the inferred organization to move through the measured coordinate system.

---

# 4. World-tube optimization

The local candidate score is

\[
\boxed{
\Omega_t(S)
=
\left[
G_t(S)K_t(S)P(X_S^t,X_S^{t+1})
\right]^{1/3}.
}
\]

For path \(p=(j_0,\ldots,j_{T-1})\), the world-tube objective is

\[
\boxed{
A(p)=
\sum_t\Omega_t(S^{(j_t)})
+
\chi\sum_t\Theta_t(S^{(j_t)}\to S^{(j_{t+1})})
-
\lambda\sum_t d_J(S^{(j_t)},S^{(j_{t+1})}).
}
\]

The Jaccard term controls abrupt changes in boundary membership, while the transport term rewards predictive continuity across changing coordinates.

Exact finite-horizon optimization is carried out by dynamic programming, with algorithmic lineage to [Bellman 1952](bibliography.md#bellman-1952).

The runner-up path defines an optimization margin. That margin is central to subsequent robustness and recovery results.

---

# 5. Recovery and identifiability

The early theorem sequence separates two questions that are often conflated:

1. **Recovery:** if a population world-tube is separated from alternatives by a positive objective margin, how much perturbation can be tolerated before the optimizer changes?
2. **Identifiability:** does the observational model distinguish the boundary labels at all?

Propositions 4-12 develop perturbation and finite-sample recovery. Propositions 13-14 formalize symmetry-aware equivalence and observational impossibility.

This distinction is important because numerical optimization can return a unique path even when the physical observation model does not support unique labeled identification.

---

# 6. Finite-sample measurement certification

The central covariance event is

\[
\boxed{
\left\|
\Sigma^{-1/2}
(\widehat\Sigma-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le\epsilon.
}
\]

The later theorem program asks how this uncertainty propagates through information factors, persistence, transport, and ultimately the complete path objective.

The statistical development proceeds through:

- Gaussian covariance concentration;
- candidate-local and structural screening;
- sample splitting and calibration;
- temporally dependent observations;
- nuisance-subspace projection;
- direct matrix concentration;
- calibrated temporal covariance families.

The relevant external foundations include [Wishart 1928](bibliography.md#wishart-1928), [Bhatia 1997](bibliography.md#bhatia-1997), and [Tropp 2012](bibliography.md#tropp-2012).

---

# 7. Physical time rather than sampling-index time

The recent theorem sequence introduces a physical relaxation time \(\tau\) through

\[
\boxed{
K_\tau(t_i,t_j)
=
\exp\left(-\frac{|t_i-t_j|}{\tau}\right).
}
\]

For adjacent irregular gaps,

\[
\alpha_i=e^{-(t_{i+1}-t_i)/\tau},
\]

and Proposition 53 gives the exact local innovation representation

\[
\boxed{
X_{i+1}
=
\alpha_iX_i+
\sqrt{1-\alpha_i^2}\,\varepsilon_i.
}
\]

The corresponding temporal whitener satisfies

\[
\boxed{
W_\tau R_\tau W_\tau^{\mathsf T}=I.
}
\]

The physical lineage includes [Uhlenbeck and Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930) and Gaussian Markov-process context from [Doob 1942](bibliography.md#doob-1942).

---

# 8. P53-P58 as one scientific sequence

| Result | Question answered | Main controlled result |
| --- | --- | ---: |
| P53A / AM | Can temporal memory be parameterized in physical time? | one \(\tau\) remains meaningful across sampling intervals |
| P53B / AN | Can \(\tau\) be calibrated from irregular finite data? | continuum e-value confidence set |
| P54 / AO | Can calibration and target resolutions be separated? | target radius `3.15549 -> 2.57207` |
| P55 / AP | Can likelihood curvature sharpen the physical-time set? | hull width `0.1646875 s`; target radius `2.41488` |
| P56 / AQ | Can exact innovations remove the raw-time temporal penalty? | exact-\(\tau\) scalar radius `2.16725 -> 0.43647` |
| P57 / AR | Does the gain survive finite-sample \(\tau\) uncertainty? | corrected uniform radius `0.71959 < 1` |
| P58 / AS | Does scalar covariance success imply observer-scale certification? | observer-scale exact-\(\tau\) radius `1.85736 > 1` at current N |

The progression is methodological: each theorem responds to a limitation made visible by the previous one.

---

# 9. Proposition 57 correction in 0.47.1

Proposition 57 uses a working whitener \(W_0\) and the transformed family

\[
C_\tau=W_0R_\tau W_0^{\mathsf T}.
\]

The operator/eigenvalue cover remains unchanged. The 0.47.1 correction improves only the projected normalization enclosure.

Define

\[
d(\tau)=\operatorname{tr}(P_GC_\tau).
\]

For exponential covariance

\[
R_\tau(i,j)=e^{-D_{ij}/\tau},
\]

\[
\frac{\partial R_\tau(i,j)}{\partial\tau}
=
\frac{D_{ij}}{\tau^2}e^{-D_{ij}/\tau}.
\]

This gives a direct trace-specific Lipschitz certificate for \(d(\tau)\). The corrected Experiment AR result is

\[
\boxed{
\varepsilon_{57}=0.7195879984<1,
}
\]

at combined calibration-target confidence lower bound `0.950625`.

See [Proposition 57](proposition_57_robust_innovation_whitening.md) and the [0.47.1 research correction record](release_0_47_1.md).

---

# 10. Returning covariance uncertainty to the moving-boundary problem

Proposition 58 defines the observer covariance block

\[
\boxed{
B_{t,S}=(X_t,X_{t+1}^{S}).
}
\]

For ambient dimension \(n\) and candidate size \(s\),

\[
\boxed{
d_{\mathrm{obs}}=n+s.
}
\]

On the controlled benchmark,

\[
n=7,
\qquad
s=3,
\qquad
T=5,
\qquad
C=35,
\]

so

\[
\boxed{
d_{\mathrm{obs}}=10,
\qquad
B_{\mathrm{obs}}=175.
}
\]

The planted and recovered population path is

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

with population optimization margin `0.1264216185`.

At 118 residual innovation degrees, the current exact-\(\tau\) matrix theorem gives

\[
\boxed{
\varepsilon_{\mathrm{observer}}=1.8573569119>1.
}
\]

This identifies the present frontier as observer-scale dimension and structural propagation of uncertainty.

---

# 11. Current research frontier

The immediate directions are:

1. factor-specific covariance blocks;
2. safe screen-first reduction of simultaneous candidates;
3. candidate-local uncertainty radii;
4. direct score-margin or action-margin concentration;
5. richer temporal physics after the structural bottleneck is better understood.

The central scientific question remains:

> **When does the dynamics itself justify a moving subsystem boundary, and when does the available evidence remain insufficient to identify one?**

---

# 12. Reading and verification map

| Purpose | Page |
| --- | --- |
| physical meaning and units | [Physics Guide](physics_guide.md) |
| equation-level source provenance | [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md) |
| all figures with explanations | [Visual Research Guide](visual_research_guide.md) |
| proposition and experiment audit | [Research Index](research_index.md) |
| assumptions and failure conditions | [Assumption Ledger](assumption_ledger.md) |
| literature and source roles | [Bibliography and Citation Map](bibliography.md) |
| machine-readable references | [`references.bib`](../references.bib) |
| interpretation protocol | [Interpretation Protocol](interpretation_protocol.md) |
