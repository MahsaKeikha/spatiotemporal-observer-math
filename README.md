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
| Read machine-readable references | [`references.bib`](references.bib) |
| Read repository citation metadata | [`CITATION.cff`](CITATION.cff) |

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

The term **observer** is used operationally for the candidate subsystem defined by this dynamical criterion. The mathematical results concern subsystem identification, persistence, recovery, identifiability, and measurement certification.

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

Therefore

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

This joint covariance is the fluctuation geometry from which the Gaussian information and canonical-correlation quantities are computed.

This is an effective statistical model, not a universal microscopic law. A physical application must validate its observables, units, sampling, temporal structure, nuisance representation, covariance geometry, and candidate boundary construction. The detailed dimensional and physical interpretation is in the [Physics Guide](docs/physics_guide.md).

---

# 3. Mathematical construction

The score separates four dynamical properties.

| Property | Physical question | Mathematical object |
| --- | --- | --- |
| **Integration** | Do internal parts add predictive information about one another? | directed conditional-information cut |
| **Insulation** | Does the measured exterior add limited next-step prediction once the candidate state is known? | conditional environmental leakage |
| **Persistence** | Does collective organization remain predictive through time? | canonical-correlation persistence |
| **Transport** | Can organization persist while its measured coordinates change? | cross-boundary predictive continuity |

## 3.1 Gaussian information geometry

For Gaussian subvectors \(X\) and \(Y\),

\[
I(X;Y)
=
\frac{1}{2}\log_2
\frac{\det\Sigma_X\det\Sigma_Y}{\det\Sigma_{XY}}.
\]

For conditioning vector \(Z\),

\[
I(X;Y\mid Z)
=
\frac{1}{2}\log_2
\frac{\det\Sigma_{XZ}\det\Sigma_{YZ}}
{\det\Sigma_Z\det\Sigma_{XYZ}}.
\]

**Lineage:** [Shannon 1948](docs/bibliography.md#shannon-1948) and [Cover and Thomas 2006](docs/bibliography.md#cover-and-thomas-2006).

## 3.2 Integration and insulation

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
\frac{1}{|S|}\min_{U\sqcup V=S}J_t(U,V),
\qquad
G_t(S)=1-2^{-\mathcal J_t(S)}.
}
\]

Let \(\bar S\) denote the measured exterior. Define

\[
\boxed{
\mathcal L_t(S)
=
\frac{1}{|S|}I(X_S^{t+1};X_{\bar S}^{t}\mid X_S^t),
\qquad
K_t(S)=2^{-\mathcal L_t(S)}.
}
\]

The broader conceptual background includes [Tegmark 2015](docs/bibliography.md#tegmark-2015), [Tegmark 2016](docs/bibliography.md#related-tegmark-work-tegmark-2016), and the integrated-information literature. The operational functionals above are the definitions used in this repository.

## 3.3 Persistence and transport

For Gaussian vectors \(X,Y\), define the whitened cross-covariance

\[
C=\Sigma_X^{-1/2}\operatorname{Cov}(X,Y)\Sigma_Y^{-1/2}.
\]

Let \(\rho_i\) be its singular values. The persistence functional is

\[
\boxed{
P(X,Y)=\frac{1}{r}\sum_{i=1}^{r}\rho_i^2,
\qquad
r=\min(\dim X,\dim Y).
}
\]

**Lineage:** canonical correlation from [Hotelling 1936](docs/bibliography.md#hotelling-1936), with matrix-analysis tools from [Bhatia 1997](docs/bibliography.md#bhatia-1997).

For source \(S\) and next-time target \(R\), define

\[
L_t(S\to R)
=
\frac{1}{|R|}I(X_R^{t+1};X_{\bar S}^{t}\mid X_S^t),
\]

\[
\boxed{
\Theta_t(S\to R)
=
\sqrt{
P(X_S^t,X_R^{t+1})
2^{-L_t(S\to R)}
}.
}
\]

## 3.4 Local score and world-tube objective

\[
\boxed{
\Omega_t(S)
=
\left[
G_t(S)K_t(S)P(X_S^t,X_S^{t+1})
\right]^{1/3}.
}
\]

For a path \(p=(j_0,\ldots,j_{T-1})\),

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

**Lineage:** [Jaccard 1901](docs/bibliography.md#jaccard-1901) for set-overlap geometry and [Bellman 1952](docs/bibliography.md#bellman-1952) for dynamic programming. The complete world-tube objective is defined in this repository.

## 3.5 Finite-sample covariance certification

The central relative covariance event is

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

When \(\epsilon<1\), inverse-covariance perturbation calculations remain in a controlled regime.

**Lineage:** [Wishart 1928](docs/bibliography.md#wishart-1928), [Tropp 2012](docs/bibliography.md#tropp-2012), and [Bhatia 1997](docs/bibliography.md#bhatia-1997).

For the equation-by-equation provenance trail, see the **[Physics + Mathematics + Citation Map](docs/physics_mathematics_citation_map.md)**.

---

# 4. Current research record

| Research record | Current state |
| --- | ---: |
| Proposition-level statements | **58** |
| Reproducible studies | **45 experiments, A-Z and AA-AS** |
| Scientific result figures | **33 figures** |
| Claim-level tests | **223 tests** |
| CI matrix | **Python 3.10, 3.11, 3.12** |
| Research-software version | **0.47.1** |

The explanatory physics pipeline is not included in the count of 33 scientific result figures.

---

# 5. Complete visual research atlas

All **33 scientific result figures** are intentionally visible on the main page. Each image links to the theorem page or reproducibility record that explains its construction, assumptions, numerical data, and interpretation. A more detailed figure-by-figure reading guide is available in the [Visual Research Guide](docs/visual_research_guide.md).

## Phase I. Moving-boundary recovery

| Candidate scores and recovered path | Recovery landscape |
| --- | --- |
| [![World-tube baseline](docs/worldtube_baseline.png)](docs/reproducible_results.md) | [![World-tube phase diagram](docs/worldtube_phase_diagram.png)](docs/reproducible_results.md) |

The controlled planted path is

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

The first figure shows the candidate-score geometry and recovered world-tube. The phase diagram shows where recovery persists across objective parameters.

## Phase II. Finite-sample and perturbation recovery

| Finite-sample benchmark | Symbolic recovery region |
| --- | --- |
| [![Finite-sample benchmark](docs/finite_sample_benchmark.png)](docs/reproducible_results.md) | [![Symbolic recovery region](docs/symbolic_recovery_region.png)](docs/reproducible_results.md) |

[![Perturbed recovery region](docs/perturbed_recovery_region.png)](docs/reproducible_results.md)

These figures move from population recovery to finite covariance estimation, theorem-derived recovery regions, and robustness under perturbations of transitions, forcing, and covariance geometry.

## Phase III. Screening and localization

| Gaussian screen calibration | Structural-null screen |
| --- | --- |
| [![Gaussian screen calibration](docs/gaussian_screen_calibration.png)](docs/reproducible_results.md) | [![Structural-null screen](docs/structural_null_screen.png)](docs/reproducible_results.md) |

| Trajectory-coupled screening | Relative covariance calibration |
| --- | --- |
| [![Trajectory-coupled screening](docs/trajectory_coupled_screen_calibration.png)](docs/reproducible_results.md) | [![Relative covariance calibration](docs/relative_covariance_calibration.png)](docs/reproducible_results.md) |

These experiments study candidate screening under finite-sample uncertainty, exact structural nulls, shared trajectories, and population-whitened covariance error.

## Phase IV. Cross-fitting, drift, and changing populations

| Cross-fitted calibration | Drift-robust calibration |
| --- | --- |
| [![Cross-fitted relative calibration](docs/cross_fitted_relative_calibration.png)](docs/reproducible_results.md) | [![Drift-robust relative calibration](docs/drift_robust_relative_calibration.png)](docs/reproducible_results.md) |

| Calibrated drift comparison | Multi-regime coupled calibration |
| --- | --- |
| [![Calibrated drift comparison](docs/calibrated_drift_comparison.png)](docs/reproducible_results.md) | [![Multi-regime coupled calibration](docs/multi_regime_coupled_calibration.png)](docs/reproducible_results.md) |

This phase separates pilot geometry from certification data and makes population change an explicit part of the uncertainty model.

## Phase V. Temporally dependent measurements

| Dependent Gaussian calibration | Unknown-mean dependent calibration |
| --- | --- |
| [![Dependent Gaussian calibration](docs/dependent_gaussian_calibration.png)](docs/reproducible_results.md) | [![Dependent centered Gaussian calibration](docs/dependent_centered_gaussian_calibration.png)](docs/reproducible_results.md) |

[![Estimated AR1 calibration](docs/estimated_ar1_calibration.png)](docs/reproducible_results.md)

These figures show why temporally correlated measurements cannot be treated as independent and how temporal persistence can be estimated rather than supplied as an oracle quantity.

## Phase VI. Time-varying nuisance structure

| Proposition 44 / Experiment AD | Proposition 45 / Experiment AE |
| --- | --- |
| [![Nuisance projection](docs/nuisance_projection_calibration.svg)](docs/proposition_44_nuisance_projection.md) | [![Estimated AR1 nuisance projection](docs/estimated_ar1_nuisance_projection.svg)](docs/proposition_45_estimated_ar1_nuisance_projection.md) |

[![Design-specific AR1 envelope](docs/design_specific_ar1_envelope.svg)](docs/proposition_46_design_specific_ar1_envelope.md)

For nuisance design \(H\), the fixed-subspace projection is

\[
P_H=I-H(H^{\mathsf T}H)^{-1}H^{\mathsf T}.
\]

This phase studies covariance inference after nuisance removal and then combines nuisance uncertainty with temporal-correlation uncertainty.

## Phase VII. Direct matrix concentration

| Proposition 47 / Experiment AG | Proposition 48 / Experiment AH |
| --- | --- |
| [![Weighted Wishart matrix Chernoff](docs/weighted_wishart_matrix_chernoff.svg)](docs/proposition_47_weighted_wishart_matrix_chernoff.md) | [![Uniform matrix Chernoff AR1](docs/uniform_matrix_chernoff_ar1.svg)](docs/proposition_48_uniform_matrix_chernoff_ar1.md) |

[![Compact temporal family](docs/compact_temporal_family.svg)](docs/proposition_49_compact_temporal_family.md)

The concentration analysis moves from direct weighted-Wishart matrix bounds to uncertainty in temporal persistence and then to compact temporal covariance families.

## Phase VIII. Learning temporal physics from calibration data

| Proposition 50 / Experiment AJ | Proposition 51 / Experiment AK |
| --- | --- |
| [![Calibrated temporal family](docs/calibrated_temporal_family.svg)](docs/proposition_50_calibrated_temporal_family.md) | [![E-value temporal confidence set](docs/evalue_temporal_confidence_set.svg)](docs/proposition_51_evalue_temporal_confidence_set.md) |

[![Certified e-value outer cover](docs/certified_evalue_outer_cover.svg)](docs/proposition_52_certified_evalue_outer_cover.md)

This phase learns temporal-family uncertainty from calibration data and propagates a finite-sample confidence set into an independent target covariance theorem.

## Phase IX. Sampling consistency and physical-time calibration

| Sampling-consistent relaxation | Irregular-grid Markov factorization |
| --- | --- |
| [![Physical relaxation sampling](docs/physical_relaxation_sampling.svg)](docs/proposition_53_physical_relaxation_time.md) | [![Irregular-grid Markov factorization](docs/physical_relaxation_markov.svg)](docs/proposition_53_physical_relaxation_time.md) |

The physical-time covariance model is

\[
\boxed{
K_\tau(t_i,t_j)
=
\exp\left(-\frac{|t_i-t_j|}{\tau}\right).
}
\]

For irregular adjacent gaps,

\[
\alpha_i=e^{-(t_{i+1}-t_i)/\tau},
\]

and Proposition 53 gives the local innovation representation

\[
X_{i+1}
=
\alpha_iX_i+
\sqrt{1-\alpha_i^2}\,\varepsilon_i.
\]

[![Experiment AN: irregular-time tau calibration](docs/irregular_relaxation_evalue_calibration.svg)](docs/proposition_53b_irregular_tau_evalue.md)

[![Experiment AO: two-scale relaxation cover](docs/two_scale_irregular_tau_cover.svg)](docs/proposition_54_two_scale_irregular_tau_cover.md)

[![Experiment AP: quadratic relaxation calibration](docs/quadratic_relaxation_calibration.svg)](docs/proposition_55_quadratic_relaxation_calibration.md)

This sequence converts sampling-dependent temporal correlation into a physical relaxation time measured in seconds, calibrates it on irregular timestamps, and studies how sharply that uncertainty can be propagated.

## Phase X. Exact local innovation target inference

[![Experiment AQ: innovation-whitened target covariance](docs/innovation_whitened_target.svg)](docs/proposition_56_innovation_whitened_target.md)

Proposition 56 applies the exact physical-time innovation transform before target covariance concentration. On the controlled scalar benchmark, the known-\(\tau\) target radius changes from approximately `2.16725` to `0.43647`.

## Phase XI. Robust innovation inference under calibrated physical time

[![Experiment AR: robust innovation-whitened target covariance](docs/robust_innovation_whitened_target.svg)](docs/proposition_57_robust_innovation_whitening.md)

Proposition 57 propagates finite-sample physical-time uncertainty through a fixed calibration-derived whitener. The tightened uniform scalar certificate is

\[
\boxed{
\varepsilon_{57}=0.7195879984<1.
}
\]

The trace-specific normalization analysis preserves the operator/eigenvalue cover while avoiding the earlier overly conservative residual-rank-times-operator normalization step.

## Phase XII. Covariance uncertainty back to world-tube recovery

[![Experiment AS: observer-scale covariance-to-world-tube audit](docs/observer_bridge_dimension_audit.svg)](docs/proposition_58_observer_bridge.md)

Proposition 58 returns covariance uncertainty to the original moving-boundary objective. For future candidate \(S\), define the observer covariance block

\[
\boxed{
B_{t,S}=(X_t,X_{t+1}^{S}).
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
C={7\choose3}=35,
\]

so

\[
\boxed{
d_{\mathrm{obs}}=n+s=10,
\qquad
B_{\mathrm{obs}}=TC=175.
}
\]

Even when the true physical relaxation time is supplied exactly, the current observer-scale matrix theorem at 118 residual innovation degrees gives

\[
\boxed{
\varepsilon_{\mathrm{observer}}=1.8573569119>1.
}
\]

This identifies a concrete structural bottleneck: block dimension, simultaneous candidate coverage, and generic factor-by-factor perturbation now dominate the current certificate.

---

# 6. Scientific result architecture

The 58 proposition-level statements provide auditability. The scientific argument is more compact:

| Result group | Question answered | Detailed record |
| --- | --- | --- |
| **Dynamics to covariance** | What fluctuation geometry follows from the declared dynamics? | [Derivations](docs/derivations.md) |
| **Moving-boundary score and optimization** | How is a time-dependent candidate boundary scored and recovered? | [Proofs and conjectures](docs/proofs_and_conjectures.md) |
| **Recovery and identifiability** | When is the preferred path stable, and when is it observationally non-identifiable? | [Research Index](docs/research_index.md) |
| **Finite-sample certification** | How do covariance, nuisance, dependence, and calibration uncertainty affect recovery? | [Research Overview](docs/research_overview.md) |
| **Physical-time measurement bridge** | Can physical temporal uncertainty be calibrated and propagated back to the complete world-tube objective? | [P53-P58 records](docs/research_index.md) |

This organization keeps the central argument visible while preserving proposition-level traceability underneath it.

---

# 7. Recent physical-time sequence

| Result | Question | Controlled result |
| --- | --- | ---: |
| P53 / AM | Can temporal memory be parameterized in physical time? | sampling-consistent \(\tau\) and irregular-grid Markov structure |
| P53B / AN | Can \(\tau\) be calibrated directly on irregular timestamps? | finite-sample e-value confidence set |
| P54 / AO | Can calibration and target-cover resolutions be separated? | target radius `3.15549 -> 2.57207` |
| P55 / AP | Can local likelihood curvature tighten the physical-time set? | retained hull width `0.1646875 s`; raw-time target radius `2.41488` |
| P56 / AQ | Can exact local innovations change the estimator? | exact-\(\tau\) scalar radius `2.16725 -> 0.43647` |
| P57 / AR | Does the gain survive finite-sample \(\tau\) uncertainty? | uniform scalar radius `0.71959 < 1` |
| P58 / AS | Can covariance uncertainty return to the full moving-boundary objective? | deterministic bridge; current observer-scale radius `1.85736 > 1` at 118 residual degrees |

Each step addresses a limitation exposed by the previous result. Negative diagnostics are retained as part of the scientific record.

---

# 8. Identifiability and falsifiability

A high score is not sufficient if distinct boundaries generate observationally equivalent measured dynamics. The framework therefore treats identifiability as a separate mathematical problem rather than assuming that every preferred path represents a uniquely recoverable subsystem.

The repository includes symmetry and observational-equivalence results, controlled counterexamples, and recovery conditions. See the [Research Index](docs/research_index.md) and the [identifiability example](examples/identifiability_counterexample.py).

Relevant model diagnostics include:

- residual temporal structure inconsistent with the declared temporal family;
- multiple or drifting relaxation scales;
- oscillatory or nonmonotone temporal dependence;
- heavy-tailed or non-Gaussian innovations;
- nonseparable space-time covariance;
- calibration-to-target mismatch;
- nuisance modes selected adaptively from the same target noise;
- candidate geometry inconsistent with physically admissible boundaries;
- inferred boundaries that fail under held-out data, changes in sampling, or physically admissible coordinate transformations.

---

# 9. Interpretive scope

The established mathematical results concern:

- time-dependent candidate subsystem scores;
- exact finite-horizon world-tube optimization;
- recovery margins and stability;
- identifiability and observational equivalence;
- finite-sample covariance certification;
- temporally dependent and nuisance-contaminated measurements;
- finite-sample temporal-parameter calibration;
- physical relaxation-time representation;
- exact and robust innovation inference;
- deterministic propagation of covariance uncertainty to the world-tube objective.

The theorem set is conditional on the declared observation and stochastic models. Further interpretation connecting an operationally identified subsystem to consciousness requires additional bridge assumptions and empirical evidence beyond the present mathematics.

The detailed distinction between mathematical result, physical model, and interpretation is maintained in the [Interpretation Protocol](docs/interpretation_protocol.md).

---

# 10. Current frontier

Proposition 58 identifies the immediate mathematical bottleneck: reduce the gap between scalar covariance certification and observer-scale world-tube certification without replacing the uncertainty analysis by a heuristic.

The leading directions are:

1. **Factor-specific covariance blocks:** certify only the covariance geometry required by each information factor.
2. **Screen-first simultaneity reduction:** use safe screening and near-competitor structure so distant candidates do not consume the strongest simultaneous guarantee.
3. **Candidate-local uncertainty radii:** retain heterogeneous uncertainty rather than replacing it by one global worst case.
4. **Direct score-margin concentration:** control score or path-action differences more directly instead of repeatedly passing through generic intermediate bounds.
5. **Richer temporal physics:** extend beyond one stationary exponential timescale after the present structural bottleneck is understood.

The guiding question remains:

> **When does the dynamics itself justify a moving subsystem boundary, and when is the evidence insufficient to identify one?**

---

# 11. Reproducibility and audit trail

A result is documented with the relevant combination of assumptions, theorem or operational definition, derivation, implementation, tests, machine-readable numerical data, and visible figure.

Repository-local Markdown and image targets are checked automatically in the test suite.

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

For a complete audit, use the [Research Index](docs/research_index.md), [Assumption Ledger](docs/assumption_ledger.md), [Reproducible Results](docs/reproducible_results.md), and [Visual Research Guide](docs/visual_research_guide.md).

---

# 12. Citations and bibliography

The repository separates three forms of provenance:

1. **Conceptual lineage**, including Tegmark's observer-factorization question.
2. **Standard mathematical foundations**, including information theory, canonical correlation, dynamic programming, matrix analysis, covariance concentration, and e-value methods.
3. **Repository-specific definitions and theorems**, cited to their derivation and proof records.

| Citation layer | Purpose |
| --- | --- |
| [Bibliography and Citation Map](docs/bibliography.md) | full references and the role each source plays |
| [`references.bib`](references.bib) | machine-readable BibTeX |
| [`CITATION.cff`](CITATION.cff) | citation metadata for this repository |
| [Physics + Mathematics + Citation Map](docs/physics_mathematics_citation_map.md) | equation-by-equation provenance |

Major external foundations include Tegmark 2015 and 2016, Shannon and Cover-Thomas, Hotelling, Jaccard, Bellman, Wishart, Aitken, Bhatia, Tropp, Vovk-Wang, Shafer, Uhlenbeck-Ornstein, and Doob. Exact source roles are maintained in the bibliography rather than treated as a generic reference list.

---

# 13. Relationship to Tegmark's observer-factorization question

## 13.1 Primary conceptual source

**Max Tegmark. "Consciousness as a State of Matter." _Chaos, Solitons & Fractals_ 76 (2015): 238-270.**

- [DOI: 10.1016/j.chaos.2015.03.014](https://doi.org/10.1016/j.chaos.2015.03.014)
- [Technical preprint: arXiv:1401.1219](https://arxiv.org/abs/1401.1219)
- [Repository bibliography entry](docs/bibliography.md#tegmark-2015)

Tegmark asks why an observer should correspond to one factorization of a physical system rather than another and studies information, integration, independence, and dynamics as candidate organizing principles.

The extension studied here is explicitly time dependent:

\[
\boxed{
S_0\to S_1\to\cdots\to S_{T-1}.
}
\]

The central object is therefore not one selected partition but a path through candidate subsystem space.

## 13.2 Conceptual lineage and mathematical development

| Scientific element | Tegmark 2015 lineage | Development in this repository |
| --- | --- | --- |
| observer-factorization question | primary conceptual source | starting problem |
| information and integration | organizing principles | operational score ingredients |
| environmental independence | organizing principle | conditional predictive insulation |
| dynamics and observer structure | conceptual motivation | explicit time-indexed boundary recovery |
| time-dependent boundary \(S_t\) | extension point | central mathematical object |
| world-tube \(\mathcal W\) | beyond a static partition | defined and optimized here |
| transport between changing boundaries | beyond static factorization | operational transport functional |
| exact finite-horizon path recovery | algorithmic development | dynamic-programming recovery and runner-up margin |
| symmetry and observational equivalence | identifiability development | formalized in the theorem sequence |
| finite-sample covariance-to-path certification | statistical development | built across the recovery and concentration results |
| physical-time calibration and innovation inference | measurement development | P53-P57 |
| covariance-to-world-tube certification | end-to-end measurement development | P58 |

The conceptual lineage begins with the factorization question. The subsequent work develops a time-dependent inference and certification framework around that question.

## 13.3 Mathematical extension in one picture

```text
Tegmark observer-factorization question
                |
                v
Which subsystem decomposition is physically distinguished?
                |
                v
Explicit time dependence
                |
                v
S_0 -> S_1 -> ... -> S_(T-1)
                |
                v
integration + insulation + persistence + transport
                |
                v
world-tube optimization
                |
                v
identifiability + finite-sample recovery
                |
                v
physical measurement certification
```

The extension developed here is a mathematical program for **dynamically inferred, time-dependent subsystem boundaries** with explicit recovery, uncertainty, identifiability, and falsification conditions.

## 13.4 Related Tegmark work

**Max Tegmark. "Improved Measures of Integrated Information." _PLOS Computational Biology_ 12(11) (2016): e1005123.**

- [DOI: 10.1371/journal.pcbi.1005123](https://doi.org/10.1371/journal.pcbi.1005123)
- [Preprint: arXiv:1601.02626](https://arxiv.org/abs/1601.02626)
- [Repository bibliography entry](docs/bibliography.md#related-tegmark-work-tegmark-2016)

This work provides relevant context on integrated-information measures and factorization choices. The world-tube construction, transport functional, recovery theorems, and finite-sample measurement program are developed separately in this repository.

## 13.5 Interpretive scope and citation practice

The formal results here concern operational subsystem identification, dynamical persistence, recovery, identifiability, and measurement certification. A physical application must separately validate the observation model and its assumptions. Further interpretation requires additional bridge assumptions and empirical evidence.

For the conceptual origin of the observer-factorization question, cite Tegmark 2015. For integrated-information measure context, cite Tegmark 2016 where relevant. For mathematical or computational results introduced in this repository, cite the repository together with the external mathematical source appropriate to the method being used.

The complete literature map is maintained in the [Bibliography and Citation Map](docs/bibliography.md), with machine-readable entries in [`references.bib`](references.bib) and repository metadata in [`CITATION.cff`](CITATION.cff).
