# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.47.1-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

**Mahsa Keikha, PhD**

> **If a subsystem moves through the coordinates used to observe a larger physical system, when can its boundary be inferred from the dynamics rather than fixed in advance?**

This repository develops a mathematical and computational framework for **time-dependent subsystem identification**. The object of inference is a moving sequence of candidate boundaries, not a single static partition. The framework asks whether internal integration, environmental insulation, predictive persistence, and transport support one spatiotemporal path more strongly than its alternatives after identifiability and finite-sample uncertainty are taken into account.

The primary conceptual starting point is Max Tegmark's observer-factorization question in ["Consciousness as a State of Matter"](https://doi.org/10.1016/j.chaos.2015.03.014). The development here makes the boundary explicitly time dependent and studies recovery, identifiability, physical-time calibration, and measurement certification.

## Start here

| Reader goal | Entry point |
| --- | --- |
| Understand the project visually | **[Visual Research Guide](docs/visual_research_guide.md)** |
| Follow the physics and units | **[Physics Guide](docs/physics_guide.md)** |
| Trace equations to sources and proofs | **[Physics + Mathematics + Citation Map](docs/physics_mathematics_citation_map.md)** |
| Read the scientific narrative | [Research Overview](docs/research_overview.md) |
| Audit every theorem and experiment | [Research Index](docs/research_index.md) |
| Inspect assumptions and failure conditions | [Assumption Ledger](docs/assumption_ledger.md) |
| Trace the literature | [Bibliography and Citation Map](docs/bibliography.md) |

---

# 1. The problem in one picture

[![Physics to inference pipeline](docs/physics_pipeline.svg)](docs/physics_guide.md)

At time \(t\), let the measured state be

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

The central inference problem is to determine whether the dynamics distinguish one such world-tube from competing paths.

The term **observer** is used operationally for the candidate subsystem defined by this dynamical criterion. The mathematical results concern subsystem identification, persistence, recovery, and measurement certification.

---

# 2. Physics first

The main analytical observation model is

\[
\boxed{
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t),
\qquad
\varepsilon_t\perp X_t.
}
\]

Here \(A_t\) is an effective one-step coupling or propagation operator in the chosen measured coordinates, while \(Q_t\) represents unresolved stochastic forcing in the declared model.

If

\[
\Sigma_t=\operatorname{Cov}(X_t),
\]

then

\[
\boxed{
\Sigma_{t+1}=A_t\Sigma_tA_t^{\mathsf T}+Q_t,
\qquad
\operatorname{Cov}(X_t,X_{t+1})=\Sigma_tA_t^{\mathsf T}.
}
\]

The resulting joint covariance of \((X_t,X_{t+1})\) supplies the fluctuation geometry used by the Gaussian information and canonical-correlation quantities below.

This is an effective statistical model, not a universal microscopic law. A physical application must validate its observables, sampling, temporal structure, nuisance representation, and candidate geometry. The detailed dimensional and physical interpretation is in the [Physics Guide](docs/physics_guide.md).

---

# 3. Mathematical construction

The score separates four dynamical properties rather than compressing them into one undefined notion of coherence.

| Property | Physical question | Mathematical object |
| --- | --- | --- |
| **Integration** | Do internal parts add predictive information about one another? | directed conditional-information cut |
| **Insulation** | Does the measured exterior add limited next-step prediction once the candidate state is known? | conditional environmental leakage |
| **Persistence** | Does collective organization remain predictive through time? | canonical-correlation persistence |
| **Transport** | Can organization persist while its measured coordinates change? | cross-boundary predictive continuity |

For a nontrivial bipartition \(S=U\sqcup V\), the internal directed-information cut is

\[
J_t(U,V)
=
I(X_U^{t+1};X_V^t\mid X_U^t)
+
I(X_V^{t+1};X_U^t\mid X_V^t),
\]

with normalized integration factor

\[
\mathcal J_t(S)
=
\frac{1}{|S|}\min_{U\sqcup V=S}J_t(U,V),
\qquad
G_t(S)=1-2^{-\mathcal J_t(S)}.
\]

Environmental leakage and insulation are

\[
\mathcal L_t(S)
=
\frac{1}{|S|}I(X_S^{t+1};X_{\bar S}^{t}\mid X_S^t),
\qquad
K_t(S)=2^{-\mathcal L_t(S)}.
\]

For two Gaussian vectors \(X,Y\), define

\[
C=\Sigma_X^{-1/2}\operatorname{Cov}(X,Y)\Sigma_Y^{-1/2},
\]

and let \(\rho_i\) be the singular values of \(C\). The persistence functional is

\[
P(X,Y)=\frac{1}{r}\sum_{i=1}^{r}\rho_i^2,
\qquad
r=\min(\dim X,\dim Y).
\]

For source \(S\) and next-time target \(R\), transport combines persistence with conditional leakage:

\[
\Theta_t(S\to R)
=
\sqrt{
P(X_S^t,X_R^{t+1})
2^{-L_t(S\to R)}
}.
\]

The local subsystem score is

\[
\boxed{
\Omega_t(S)
=
\left[
G_t(S)K_t(S)P(X_S^t,X_S^{t+1})
\right]^{1/3}.
}
\]

For a path \(p=(j_0,\ldots,j_{T-1})\), the world-tube objective is

\[
\boxed{
A(p)=
\sum_{t=0}^{T-1}\Omega_t(S^{(j_t)})
+
\chi\sum_{t=0}^{T-2}\Theta_t(S^{(j_t)}\to S^{(j_{t+1})})
-
\lambda\sum_{t=0}^{T-2}d_J(S^{(j_t)},S^{(j_{t+1})}).
}
\]

The continuity term uses Jaccard distance

\[
d_J(S,R)=1-\frac{|S\cap R|}{|S\cup R|}.
\]

For a finite candidate family, the globally optimal path and exact runner-up are obtained by dynamic programming. Their objective difference supplies the recovery margin used in robustness analysis.

**Mathematical lineage.** Gaussian information quantities follow Shannon and Cover-Thomas; canonical correlation follows Hotelling; the continuity geometry follows Jaccard; finite-horizon optimization follows Bellman. Exact source roles and repository-specific definitions are mapped in the [Physics + Mathematics + Citation Map](docs/physics_mathematics_citation_map.md).

---

# 4. Conceptual lineage and extension

The primary conceptual source is:

**Max Tegmark. "Consciousness as a State of Matter." _Chaos, Solitons & Fractals_ 76 (2015): 238-270.**

[DOI](https://doi.org/10.1016/j.chaos.2015.03.014) | [arXiv](https://arxiv.org/abs/1401.1219) | [Bibliography entry](docs/bibliography.md#tegmark-2015)

Tegmark studies why an observer should correspond to one factorization of a physical system rather than another and considers information, integration, independence, and dynamics as organizing principles.

The extension studied here is explicit time dependence:

\[
\text{static factorization question}
\quad\longrightarrow\quad
S_0\to S_1\to\cdots\to S_{T-1}.
\]

This changes the mathematical problem from selecting one subsystem to recovering a **path through subsystem space**. It introduces transport between changing boundaries, finite-horizon path recovery, observational-equivalence limits, finite-sample covariance certification, physical-time calibration, and an end-to-end bridge from measurement uncertainty back to world-tube uncertainty.

Related integrated-information context, including Tegmark 2016 and the IIT literature, is recorded in the [Bibliography](docs/bibliography.md).

---

# 5. Decisive numerical evidence

The complete project contains 33 scientific result figures. The landing page shows only the results that define the scientific arc. The full visual record is in the **[Visual Research Guide](docs/visual_research_guide.md)**.

## 5.1 Moving subsystem recovery

| Recovered moving path | Recovery landscape |
| --- | --- |
| [![World-tube baseline](docs/worldtube_baseline.png)](docs/reproducible_results.md) | [![World-tube phase diagram](docs/worldtube_phase_diagram.png)](docs/reproducible_results.md) |

In the controlled planted example, the recovered population path is

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

The phase diagram shows where that recovery survives changes in the objective parameters rather than relying on a single tuned point.

## 5.2 Finite measurement uncertainty

| Robust physical-time innovation inference | Observer-scale certification audit |
| --- | --- |
| [![Robust innovation-whitened target covariance](docs/robust_innovation_whitened_target.svg)](docs/proposition_57_robust_innovation_whitening.md) | [![Observer-scale covariance-to-world-tube audit](docs/observer_bridge_dimension_audit.svg)](docs/proposition_58_observer_bridge.md) |

The recent finite-sample sequence produces two complementary results.

For Proposition 57, calibrated physical-time uncertainty can be propagated through innovation whitening while retaining a scalar relative covariance certificate inside the perturbative regime:

\[
\boxed{
\varepsilon_{57}=0.7195879984<1.
}
\]

For Proposition 58, returning that measurement uncertainty to the full observer-scale covariance geometry exposes the present limitation:

\[
\boxed{
\varepsilon_{\mathrm{observer}}=1.8573569119>1
}
\]

at 118 residual innovation degrees of freedom in the controlled benchmark.

This is scientifically useful: the current bottleneck is no longer physical-time calibration alone. It is the combination of observer-block dimension, simultaneous candidate coverage, and conservative propagation through the full score.

---

# 6. Result architecture

The detailed repository contains 58 proposition-level statements for auditability. The scientific structure is more compact:

| Result group | Question answered | Detailed record |
| --- | --- | --- |
| **Dynamics to covariance** | What fluctuation geometry follows from the declared dynamics? | [Derivations](docs/derivations.md) |
| **Moving-boundary score and optimization** | How is a time-dependent candidate boundary scored and recovered? | [Proofs and conjectures](docs/proofs_and_conjectures.md) |
| **Recovery and identifiability** | When is the preferred path stable, and when is it observationally non-identifiable? | [Research Index](docs/research_index.md) |
| **Finite-sample certification** | How does covariance, nuisance, dependence, and calibration uncertainty affect recovery? | [Research Overview](docs/research_overview.md) |
| **Physical-time measurement bridge** | Can physical temporal uncertainty be calibrated and propagated back to the complete world-tube objective? | [P53-P58 records](docs/research_index.md) |

This organization is intended to keep the scientific argument visible while preserving proposition-level traceability underneath it.

---

# 7. Identifiability and falsifiability

A high score is not sufficient if different boundaries generate observationally equivalent measured dynamics. The framework therefore treats identifiability as a separate mathematical issue rather than assuming that every preferred path represents a uniquely recoverable subsystem.

The repository includes symmetry and observational-equivalence results, controlled counterexamples, and recovery conditions. See the [Research Index](docs/research_index.md) and the [identifiability example](examples/identifiability_counterexample.py).

A physical application should be treated as unsupported when the declared model fails materially. Relevant diagnostics include residual temporal structure outside the temporal family, multiple or drifting relaxation scales, heavy-tailed innovations, nonseparable space-time covariance, calibration-to-target mismatch, nuisance selection from target noise, or inferred boundaries that fail under held-out data, sampling changes, or physically admissible coordinate changes.

---

# 8. Interpretive scope

The established mathematical results concern:

- time-dependent candidate subsystem scores;
- exact finite-horizon path optimization;
- recovery margins and stability;
- identifiability and observational equivalence;
- finite-sample covariance certification;
- temporally dependent and nuisance-contaminated measurements;
- physical relaxation-time calibration;
- exact and robust innovation inference;
- deterministic propagation of covariance uncertainty to the world-tube objective.

The theorem set is conditional on the declared observation and stochastic models. Further interpretation connecting an operationally identified subsystem to consciousness requires additional bridge assumptions and empirical evidence beyond the present mathematics.

The detailed distinction between mathematical result, physical model, and interpretation is maintained in the [Interpretation Protocol](docs/interpretation_protocol.md).

---

# 9. Current frontier

Proposition 58 identifies a concrete next problem: reduce the gap between scalar covariance certification and observer-scale world-tube certification without hiding the uncertainty in a looser heuristic.

The leading directions are factor-specific covariance blocks, safe reduction of the simultaneous candidate family, candidate-local uncertainty radii, and more direct concentration of score or path-margin differences. Richer temporal physics is a subsequent direction once the present structural bottleneck is understood.

The guiding question remains:

> **When does the dynamics itself justify a moving subsystem boundary, and when is the evidence insufficient to identify one?**

---

# 10. Reproducibility and audit trail

Current repository state:

| Item | Status |
| --- | ---: |
| Research-software version | **0.47.1** |
| Proposition-level statements | **58** |
| Reproducible studies | **45** |
| Scientific result figures | **33** |
| Claim-level tests | **223** |
| CI matrix | **Python 3.10, 3.11, 3.12** |

A result is documented with the relevant combination of assumptions, theorem or definition, derivation, implementation, tests, machine-readable result data, and figure. Repository-local Markdown and image targets are checked automatically in the test suite.

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

For a complete audit, use the [Research Index](docs/research_index.md), [Assumption Ledger](docs/assumption_ledger.md), [Reproducible Results](docs/reproducible_results.md), and [Visual Research Guide](docs/visual_research_guide.md).

---

# 11. Citation

The repository separates three forms of provenance:

1. **Conceptual lineage**, including Tegmark's observer-factorization question.
2. **Standard mathematical foundations**, including information theory, canonical correlation, dynamic programming, matrix analysis, covariance concentration, and e-value methods.
3. **Repository-specific definitions and theorems**, cited to their derivation and proof records.

Full references are maintained in the [Bibliography and Citation Map](docs/bibliography.md), machine-readable BibTeX in [`references.bib`](references.bib), and repository citation metadata in [`CITATION.cff`](CITATION.cff).
