# Research overview

This page explains **Spatiotemporal Observer Mathematics** as one scientific argument rather than as a repository file list.

For a visual first reading, use the [Visual Research Guide](visual_research_guide.md). For physical meaning and units, use the [Physics Guide](physics_guide.md). For equation-level provenance, use the [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md). For proposition-by-proposition navigation, use the [Research Index](research_index.md).

The current 0.47.0 record contains **58 propositions, 45 reproducible experiments, 33 scientific result figures, and 223 claim-level tests** across Python 3.10, 3.11, and 3.12.

---

# 1. Conceptual starting point

The primary conceptual starting point is Max Tegmark's ["Consciousness as a State of Matter"](https://doi.org/10.1016/j.chaos.2015.03.014), with technical preprint [arXiv:1401.1219](https://arxiv.org/abs/1401.1219).

Tegmark asks why an observer should correspond to one factorization of the physical world rather than another and considers information, integration, independence, and dynamics as organizing principles.

This repository takes that factorization problem in a separate mathematical direction:

> **Can a subsystem boundary be inferred from dynamical organization when the relevant physical structure is allowed to move through the measured coordinates?**

The repository does not reproduce Tegmark's derivations and does not imply his endorsement. The word `observer` is operational here. It denotes a mathematically defined persistent moving subsystem. No theorem in the repository establishes consciousness or subjective experience.

See [README Section 13](../README.md#13-relationship-to-tegmarks-observer-factorization-question) for the explicit lineage and attribution boundary.

---

# 2. Moving subsystem as the object of inference

Let the measured state be

\[
X_t=(X_t^{(1)},\ldots,X_t^{(n)}).
\]

A candidate subsystem is

\[
S_t\subseteq\{1,\ldots,n\},
\]

and its moving history is

\[
\boxed{
\mathcal W=(S_0,S_1,\ldots,S_{T-1}).
}
\]

The main analytical model is

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t).
\]

The operational score uses four ideas:

1. **Integration:** internal parts add predictive information about one another.
2. **Insulation:** external measured variables add comparatively limited next-step information after the candidate's own present is known.
3. **Persistence:** collective organization predicts its own future.
4. **Transport:** predictive organization can move into different measured coordinates.

The world-tube objective combines local subsystem quality, transport continuity, and a weak continuity penalty between successive candidate memberships.

[![World-tube baseline](worldtube_baseline.png)](reproducible_results.md)

---

# 3. Recovery, ambiguity, and identifiability

A dynamic program finds the globally maximizing path in the declared finite candidate family. A two-best extension identifies the exact runner-up path.

The objective difference between the best and second-best paths is an **optimization margin**. It is used for robustness analysis and should not be confused with physical action.

The early theorem chain establishes that recovery depends on more than optimization. Identifiability must be stated relative to the observables, candidate family, model assumptions, and admissible symmetries.

Propositions 13 and 14 formalize recovery modulo symmetry and observational-equivalence limits. If two physical hypotheses induce indistinguishable observations but incompatible labels, passive data alone cannot support uniformly reliable discrimination.

The standing rule is:

> **Optimization does not create identifiability.**

---

# 4. Why finite-sample covariance became central

Under the Gaussian model, integration, insulation, persistence, and transport are functions of covariance blocks.

The core statistical event is

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

If covariance is estimated poorly, the subsystem factors and recovered path can be wrong. This creates a measurement problem underneath the boundary problem:

> **How much confidence can be placed in the covariance geometry feeding the moving-boundary objective when the data are finite, temporally correlated, irregularly sampled, drifting, and contaminated by deterministic nuisance structure?**

That question drives the later theorem sequence.

---

# 5. The theorem program in layers

| Layer | Propositions | Scientific role |
| --- | ---: | --- |
| Foundations | 1-14 | covariance identities, factor definitions, transport, optimization, recovery, identifiability |
| Structural compression | 15-31 | near competitors, overlap classes, localized recovery, sparse influence structure |
| Screening and drift | 32-40 | sample splitting, safe screening, adaptive calibration, population drift |
| Dependent measurements | 41-52 | temporal dependence, nuisance projection, matrix concentration, temporal-family calibration |
| Physical time | 53A-55 | sampling-consistent relaxation time and finite-sample irregular-time calibration |
| Innovation inference | 56-57 | exact and robust target covariance inference in local innovation coordinates |
| Observer bridge | 58 | deterministic propagation from covariance uncertainty to the full moving-boundary objective |

The later measurement results should not be read as unrelated statistical exercises. They are the finite-data accountability layer required by the original observer-boundary question.

---

# 6. Physical time and exact local innovations

A discrete AR(1) coefficient depends on sampling interval, so Proposition 53 parameterizes the temporal model by a physical relaxation time \(\tau\):

\[
\boxed{
K_\tau(t,s)=\exp\left(-\frac{|t-s|}{\tau}\right).
}
\]

For irregular adjacent gaps,

\[
\alpha_i=e^{-(t_{i+1}-t_i)/\tau},
\]

and the model has the exact local transition form

\[
\boxed{
X_{i+1}
=
\alpha_iX_i+
\sqrt{1-\alpha_i^2}\,\varepsilon_i.
}
\]

Proposition 53 also constructs an exact lower-bidiagonal whitener

\[
\boxed{
W_\tau R_\tau W_\tau^{\mathsf T}=I,
\qquad
R_\tau^{-1}=W_\tau^{\mathsf T}W_\tau.
}
\]

This changes the statistical representation from correlated raw measurements to local innovations implied by the declared physical-time model.

The physical stochastic-process lineage is mapped to [Uhlenbeck and Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930) and [Doob 1942](bibliography.md#doob-1942). The exact irregular-grid identities used here are proved within Proposition 53.

---

# 7. P53B through P55: finite-sample physical-time calibration

Proposition 53B uses an irregular-time likelihood-ratio e-value to construct a finite-sample continuum confidence set for \(\tau\).

[![Experiment AN](irregular_relaxation_evalue_calibration.svg)](proposition_53b_irregular_tau_evalue.md)

Proposition 54 separates calibration resolution from target-cover resolution.

[![Experiment AO](two_scale_irregular_tau_cover.svg)](proposition_54_two_scale_irregular_tau_cover.md)

Proposition 55 uses the exact observed-data log-evalue slope plus a rigorous local second-derivative bound to tighten the finite-sample outer cover.

[![Experiment AP](quadratic_relaxation_calibration.svg)](proposition_55_quadratic_relaxation_calibration.md)

On Experiment AP, the retained hull becomes

\[
\boxed{
\tau\in[0.686875,0.8515625]\ \mathrm{s}.
}
\]

But even an unrealistic exact-\(\tau\) oracle under the old raw-time target estimator still gives

\[
2.1672468952>1.
\]

That negative diagnostic shows that physical-time calibration uncertainty is no longer the dominant bottleneck on this benchmark.

---

# 8. P56: change the target representation

Proposition 56 uses the exact physical-time whitener before nuisance fitting and covariance concentration.

For

\[
Y=HB+E,
\qquad
\operatorname{vec}(E)\sim\mathcal N(0,R_\tau\otimes\Gamma),
\]

define

\[
Z=W_\tau Y,
\qquad
G=W_\tau H.
\]

After nuisance removal in innovation coordinates,

\[
\boxed{
(N-q)\widehat\Gamma_{\mathrm{IW}}
\sim
\operatorname{Wishart}_d(\Gamma,N-q).
}
\]

For the controlled target,

\[
N=120,
\qquad
q=2,
\qquad
N-q=118.
\]

The scalar radius changes from the raw-time known-\(\tau\) value

\[
2.1672468952
\]

to

\[
\boxed{
0.4364662463<1.
}
\]

[![Experiment AQ](innovation_whitened_target.svg)](proposition_56_innovation_whitened_target.md)

The improvement comes from changing the estimator and representation, not from another calibration-grid refinement.

---

# 9. P57: robust innovation inference under finite-sample tau uncertainty

Proposition 57 removes the exact-target-\(\tau\) assumption.

Choose one calibration-derived working relaxation time

\[
\tau_0=0.76921875\ \mathrm{s}
\]

with fixed whitener \(W_0\). For every admissible true \(\tau\),

\[
\boxed{
C_\tau=W_0R_\tau W_0^{\mathsf T}.
}
\]

The theorem uses two deterministic covers:

- an operator cover for projected temporal eigenvalues;
- a trace-specific cover for the projected normalization
  \[
  d(\tau)=\operatorname{tr}(P_GC_\tau).
  \]

For the exponential covariance kernel,

\[
\frac{\partial R_\tau(i,j)}{\partial\tau}
=
\frac{D_{ij}}{\tau^2}e^{-D_{ij}/\tau},
\qquad
D_{ij}=|t_i-t_j|.
\]

This gives a direct deterministic Lipschitz certificate for the normalization rather than the much looser residual-rank-times-operator bound.

The current Experiment AR result is

\[
\boxed{
\varepsilon_{57}=0.7195879984<1.
}
\]

at target confidence `0.975`. Combined with independent calibration confidence `0.975`,

\[
\boxed{0.950625}
\]

is the joint lower confidence bound.

Relative to the P55 calibrated raw-time theorem, the radius reduction is approximately

\[
\boxed{70.2\%}.
\]

[![Experiment AR](robust_innovation_whitened_target.svg)](proposition_57_robust_innovation_whitening.md)

---

# 10. P58: return measurement uncertainty to the observer objective

Proposition 58 returns the covariance theorem to the original moving-boundary problem.

For future candidate \(S\), define

\[
\boxed{
B_{t,S}=(X_t,X_{t+1}^{S}).
}
\]

Its dimension is

\[
\boxed{
d_{\mathrm{obs}}=n+s.
}
\]

For Experiment AS,

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

The crucial observer-scale diagnostic is negative. At 118 residual innovation degrees, even the exact-\(\tau\) current matrix theorem gives

\[
\boxed{
\varepsilon_{\mathrm{observer}}=1.8573569119>1.
}
\]

This means scalar covariance success does not automatically imply observer-scale certification.

[![Experiment AS](observer_bridge_dimension_audit.svg)](proposition_58_observer_bridge.md)

The current bottleneck is dimensional and structural, not another temporal-calibration step.

---

# 11. What the project establishes

Under stated assumptions, the repository now provides a conditional pipeline from measured stochastic dynamics to:

- time-dependent candidate boundaries;
- integration, insulation, persistence, and transport scores;
- exact finite-horizon world-tube optimization;
- runner-up margins and finite-sample recovery analysis;
- identifiability and observational-equivalence limits;
- dependent-measurement covariance certification;
- nuisance projection;
- finite-sample temporal-family calibration;
- sampling-consistent physical relaxation time;
- exact irregular-grid innovation inference;
- robust uncertain-\(\tau\) target covariance certification;
- deterministic covariance-to-world-tube uncertainty propagation.

These are mathematical statements conditional on declared models. They do not by themselves validate those models for a real physical system.

---

# 12. What the project does not establish

The repository does not establish that:

- every physical system has a unique observer boundary;
- Gaussianity is universal;
- one stationary exponential timescale is universal;
- covariance eigenvalues are automatically physical energies;
- \(\epsilon<1\) alone guarantees path recovery;
- the world-tube score measures consciousness;
- a recovered operational observer is conscious.

The mathematics, the physical-model validation, and any consciousness interpretation remain three separate scientific layers.

---

# 13. Current frontier

P58 identifies the dominant limitation as observer-scale dimension and structural worst-case propagation.

The next rigorous directions are:

1. factor-specific covariance blocks;
2. screen-first simultaneity reduction;
3. candidate-local uncertainty radii;
4. direct score-margin concentration;
5. richer temporal physics after the structural bottleneck is understood.

The guiding question remains:

> **When does the dynamics itself justify a moving subsystem boundary, and when does the available evidence remain insufficient to identify one?**

---

# 14. Reading and citation map

| Need | Resource |
| --- | --- |
| physics and units | [Physics Guide](physics_guide.md) |
| equation-level source roles | [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md) |
| every result figure | [Visual Research Guide](visual_research_guide.md) |
| assumptions | [Assumption Ledger](assumption_ledger.md) |
| proposition navigation | [Research Index](research_index.md) |
| full references | [Bibliography and Citation Map](bibliography.md) |
| machine-readable citations | [`references.bib`](../references.bib) |
| interpretation limits | [Interpretation Protocol](interpretation_protocol.md) |

The attribution rule is:

> **Conceptual lineage is cited explicitly; repository definitions are identified as definitions; repository theorems are identified as repository results; external literature is cited for the method or idea it actually supplies; no citation is used to imply endorsement.**
