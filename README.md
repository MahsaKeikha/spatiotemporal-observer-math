# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.47.1-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

**Mahsa Keikha, PhD**

> **If a subsystem moves through the coordinates used to observe a larger physical system, when can its boundary be inferred from the dynamics rather than fixed in advance?**

This repository develops a mathematical and computational framework for **time-dependent subsystem identification**. The object of inference is a moving sequence of candidate boundaries, not a single static partition. The framework asks whether internal integration, environmental insulation, predictive persistence, and transport support one spatiotemporal path more strongly than its alternatives after identifiability and finite-sample uncertainty are taken into account.

The primary conceptual starting point is Max Tegmark's observer-factorization question in ["Consciousness as a State of Matter"](https://doi.org/10.1016/j.chaos.2015.03.014). The development here makes the boundary explicitly time dependent and studies recovery, identifiability, physical-time calibration, and measurement certification.

## Abstract

Many physical and statistical analyses begin by selecting a subsystem boundary first and studying its dynamics second. This project asks whether part of that order can be reversed. Given multivariate measurements of a larger dynamical system, can a candidate subsystem be identified from the way predictive organization persists, remains comparatively insulated from its measured exterior, and transports across changing coordinates through time?

The framework begins with an effective stochastic dynamical model, derives the joint fluctuation geometry of adjacent states, defines operational integration, insulation, persistence, and transport functionals, and combines them into a finite-horizon world-tube objective. Recovery is treated as a global path problem, not a sequence of independent local classifications. The mathematical program then adds identifiability limits, finite-sample covariance perturbation, screening, temporal dependence, nuisance structure, matrix concentration, physical relaxation-time calibration on irregular timestamps, local innovation whitening, and finally a deterministic bridge from covariance uncertainty back to the complete world-tube objective.

The current research record contains **58 proposition-level statements, 45 reproducible experiments, 33 scientific result figures, and 223 claim-level tests**. The most recent results show that physical-time innovation whitening can move a scalar target covariance certificate into the controlled perturbative regime, while the full observer-scale problem remains limited by multivariate block dimension, simultaneous candidate coverage, and conservative uncertainty propagation. This negative diagnostic is retained as part of the scientific result rather than hidden.

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

The physical-to-mathematical flow is

```text
measured physical observables
            |
            v
effective stochastic dynamics
            |
            v
adjacent-state covariance geometry
            |
            v
candidate boundary S_t
            |
            v
integration + insulation + persistence + transport
            |
            v
world-tube objective A(p)
            |
            v
population recovery + identifiability
            |
            v
finite-sample covariance certification
            |
            v
physical-time calibration + innovation inference
            |
            v
covariance uncertainty -> score uncertainty -> path uncertainty
```

---

# 2. Physics first

## 2.1 Effective observation dynamics

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

## 2.2 Physical quantities and units

| Quantity | Meaning | Units or dimensional status |
| --- | --- | --- |
| \(X_t^{(i)}\) | measured physical or derived coordinate | inherited from the sensor or feature definition |
| \(A_t\) | effective one-step propagation/coupling operator | determined by input/output coordinate units |
| \(Q_t\) | covariance of unresolved stochastic forcing | coordinate-product units |
| \(\Sigma_t\) | state covariance | coordinate-product units |
| \(\tau\) | physical relaxation time | time, reported in seconds in the current experiments |
| \(I(X;Y)\), \(I(X;Y\mid Z)\) | mutual and conditional mutual information | bits because logarithms use base 2 |
| \(G_t,K_t,P,\Theta_t\) | normalized score factors | dimensionless |
| \(d_J\) | Jaccard continuity distance | dimensionless |
| \(A(p)\) | world-tube optimization objective | dimensionless under dimensionless weights \(\chi,\lambda\) |

The quantity called an `action` or `action margin` in this repository is an optimization objective and optimization margin. It is not mechanical action measured in joule-seconds.

## 2.3 What covariance means physically

For a multivariate fluctuating system,

\[
\Sigma=\mathbb E[(X-\mu)(X-\mu)^{\mathsf T}]
\]

encodes fluctuation geometry. Diagonal entries are coordinate variances, off-diagonal entries describe co-fluctuation, eigenvectors describe collective fluctuation directions, and eigenvalues describe variance along those directions.

These covariance eigenvalues are not automatically physical energies. An energetic interpretation requires a separate derivation that connects the measured coordinates and covariance to a Hamiltonian, temperature, power spectrum, or another physically defined energetic quantity.

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

## 3.5 Exact finite-horizon optimization

For a finite candidate family, the world-tube problem is a layered finite-horizon path optimization. Dynamic programming computes the globally optimal path without enumerating every path explicitly. The same structure is used to compute the exact runner-up and therefore the population action margin

\[
\boxed{
\Delta_A=A(p_*)-A(p_{(2)}).
}
\]

This margin is central to the later perturbation and recovery theory because a finite-sample path can only be certified when uncertainty remains smaller than the separation between the preferred path and its strongest competitor.

## 3.6 Finite-sample covariance certification

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

Proposition 56 applies the exact physical-time innovation transform before target covariance concentration. On the controlled scalar benchmark, the known-\(\tau\) raw-time radius changes from

\[
2.1672468952
\]

to

\[
\boxed{
\varepsilon_{56}=0.4364443814<1.
}
\]

The reduction is approximately 79.86 percent on the same 120-row target schedule.

## Phase XI. Robust innovation inference under calibrated physical time

[![Experiment AR: robust innovation-whitened target covariance](docs/robust_innovation_whitened_target.svg)](docs/proposition_57_robust_innovation_whitening.md)

Proposition 57 propagates finite-sample physical-time uncertainty through a fixed calibration-derived whitener. The tightened uniform scalar certificate is

\[
\boxed{
\varepsilon_{57}=0.7195879984<1.
}
\]

The independent calibration and target confidence levels are both 0.975, giving the combined lower bound

\[
\boxed{0.950625}.
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

## 6.1 Complete theorem roadmap

| Layer | Propositions | Scientific role |
| --- | ---: | --- |
| A | 1-14 | foundations, transport, exact recovery, perturbation, symmetry, identifiability |
| B | 15-31 | structural compression, moving partitions, overlap structure, localization |
| C | 32-40 | sample splitting, screening, adaptive calibration, population drift |
| D | 41-52 | dependent measurements, nuisance projection, matrix concentration, temporal-family calibration |
| E | 53A-53B | sampling-consistent physical relaxation and irregular-time finite-sample calibration |
| F | 54 | two-scale physical-time uncertainty propagation |
| G | 55 | local likelihood slope and curvature for sharper physical-time calibration |
| H | 56 | exact innovation-whitened target covariance concentration |
| I | 57 | robust innovation whitening over calibrated physical-time uncertainty |
| J | 58 | simultaneous covariance uncertainty propagated to world-tube recovery |

Detailed proof navigation:

- [Propositions 1-43 proof record](docs/proofs_and_conjectures.md)
- [Proposition 44](docs/proposition_44_nuisance_projection.md)
- [Proposition 45](docs/proposition_45_estimated_ar1_nuisance_projection.md)
- [Proposition 46](docs/proposition_46_design_specific_ar1_envelope.md)
- [Proposition 47](docs/proposition_47_weighted_wishart_matrix_chernoff.md)
- [Proposition 48](docs/proposition_48_uniform_matrix_chernoff_ar1.md)
- [Proposition 49](docs/proposition_49_compact_temporal_family.md)
- [Proposition 50](docs/proposition_50_calibrated_temporal_family.md)
- [Proposition 51](docs/proposition_51_evalue_temporal_confidence_set.md)
- [Proposition 52](docs/proposition_52_certified_evalue_outer_cover.md)
- [Proposition 53A](docs/proposition_53_physical_relaxation_time.md)
- [Proposition 53B](docs/proposition_53b_irregular_tau_evalue.md)
- [Proposition 54](docs/proposition_54_two_scale_irregular_tau_cover.md)
- [Proposition 55](docs/proposition_55_quadratic_relaxation_calibration.md)
- [Proposition 56](docs/proposition_56_innovation_whitened_target.md)
- [Proposition 57](docs/proposition_57_robust_innovation_whitening.md)
- [Proposition 58](docs/proposition_58_observer_bridge.md)

---

# 7. Recent physical-time sequence

| Result | Question | Controlled result |
| --- | --- | ---: |
| P53 / AM | Can temporal memory be parameterized in physical time? | sampling-consistent \(\tau\) and irregular-grid Markov structure |
| P53B / AN | Can \(\tau\) be calibrated directly on irregular timestamps? | finite-sample e-value confidence set |
| P54 / AO | Can calibration and target-cover resolutions be separated? | target radius `3.15549 -> 2.57207` |
| P55 / AP | Can local likelihood curvature tighten the physical-time set? | retained hull width `0.1646875 s`; raw-time target radius `2.41488` |
| P56 / AQ | Can exact local innovations change the estimator? | exact-\(\tau\) scalar radius `2.16725 -> 0.43644` |
| P57 / AR | Does the gain survive finite-sample \(\tau\) uncertainty? | uniform scalar radius `0.71959 < 1` |
| P58 / AS | Can covariance uncertainty return to the full moving-boundary objective? | deterministic bridge; current observer-scale radius `1.85736 > 1` at 118 residual degrees |

Each step addresses a limitation exposed by the previous result. Negative diagnostics are retained as part of the scientific record.

## 7.1 Proposition 53: physical time instead of sampling-dependent correlation

The sampling-consistent temporal kernel is

\[
\boxed{
K_\tau(t_i,t_j)=e^{-|t_i-t_j|/\tau}.
}
\]

If the acquisition interval is \(\Delta t\), the corresponding one-step correlation is

\[
\boxed{
\phi_{\Delta t}=e^{-\Delta t/\tau}.
}
\]

Thus \(\tau\) remains a physical timescale while the discrete correlation changes when the sampling interval changes.

**Physical lineage:** [Uhlenbeck and Ornstein 1930](docs/bibliography.md#uhlenbeck-and-ornstein-1930) and Gaussian Markov context from [Doob 1942](docs/bibliography.md#doob-1942).

## 7.2 Proposition 56: exact innovation coordinates

Let \(Y\in\mathbb R^{N\times d}\) satisfy the declared separable Gaussian target model

\[
Y=HB+E,
\qquad
\operatorname{vec}(E)\sim\mathcal N(0,R_\tau\otimes\Gamma).
\]

Proposition 53 gives a lower-bidiagonal whitener \(W_\tau\) satisfying

\[
\boxed{W_\tau R_\tau W_\tau^{\mathsf T}=I.}
\]

With

\[
Z=W_\tau Y,
\qquad
G=W_\tau H,
\]

and

\[
P_G=I-G(G^{\mathsf T}G)^{-1}G^{\mathsf T},
\]

the innovation-whitened covariance estimator is

\[
\boxed{
\widehat\Gamma_{\mathrm{IW}}
=
\frac{1}{N-q}Z^{\mathsf T}P_GZ.
}
\]

Under exact \(\tau\),

\[
\boxed{
(N-q)\widehat\Gamma_{\mathrm{IW}}
\sim\operatorname{Wishart}_d(\Gamma,N-q).
}
\]

This converts predictable temporal dependence into independent innovation coordinates before covariance concentration.

## 7.3 Proposition 57: calibrated uncertainty through one working whitener

Let the calibration record give

\[
\boxed{
\tau_*\in[0.686875,0.8515625]\ \mathrm{s}
}
\]

with confidence 0.975. Experiment AR uses the calibration-only midpoint

\[
\boxed{
\tau_0=0.76921875\ \mathrm{s}.
}
\]

The fixed working whitener \(W_0\) induces the transformed temporal family

\[
\boxed{
C_\tau=W_0R_\tau W_0^{\mathsf T}.
}
\]

The operator family is covered deterministically, while the projected normalization

\[
d(\tau)=\operatorname{tr}(P_GC_\tau)
\]

uses a trace-specific Lipschitz certificate. The resulting target theorem remains uniform over the complete calibrated physical-time interval and gives

\[
\boxed{
\varepsilon_{57}=0.7195879984<1.
}
\]

## 7.4 Proposition 58: measurement uncertainty back to the observer objective

For future candidate \(S\), define

\[
B_{t,S}=(X_t,X_{t+1}^S).
\]

This one block contains the covariance submatrices required for directed integration, environmental leakage, persistence, and every incoming transport edge into future target \(S\). Therefore, with \(T\) times and \(C\) candidates,

\[
\boxed{B_{\mathrm{obs}}=TC}
\]

rather than the full number of candidate-to-candidate edges.

For the controlled benchmark,

\[
\boxed{d_{\mathrm{obs}}=10,\qquad B_{\mathrm{obs}}=175.}
\]

The population world-tube actions are

\[
A_*=1.2543238015,
\qquad
A_{(2)}=1.1279021830,
\]

with margin

\[
\boxed{
\Delta_A=0.1264216185.
}
\]

At the actual observer covariance scale, the exact-\(\tau\) innovation oracle gives

\[
\boxed{
\varepsilon_{10,175}=1.8573569119>1.
}
\]

The current matrix theorem first enters the relative perturbation regime at 346 residual innovation degrees, where

\[
\varepsilon_{346}=0.9991303523,
\]

while at 345 residual degrees

\[
\varepsilon_{345}=1.0007464318.
\]

Crossing one is only entry into the present inverse-covariance perturbation regime; it is not itself a complete world-tube recovery certificate.

---

# 8. Covariance uncertainty to information factors and path recovery

Proposition 58 makes the end-to-end bridge explicit.

Suppose each declared observer covariance block satisfies

\[
\left\|
\Sigma_{t,S}^{-1/2}
(\widehat\Sigma_{t,S}-\Sigma_{t,S})
\Sigma_{t,S}^{-1/2}
\right\|_2
\le\delta_{t,S}<1.
\]

Define

\[
L(\delta)=-\log(1-\delta).
\]

A generic directed-integration factor radius is

\[
\boxed{
e_I(\delta)=\min\{1,4L(\delta)\}.
}
\]

A generic environmental-insulation factor radius is

\[
\boxed{
e_E(\delta)=
\min\left\{
1,
\frac{n+2s}{s}L(\delta)
\right\}.
}
\]

For persistence, define

\[
a=(1-\delta)^{-1/2},
\qquad
b=a-1,
\]

and use

\[
\boxed{
e_P(\delta)=
\min\left\{
1,
2\left[ba(1+2\delta)+2\delta a+b\right]
\right\}.
}
\]

The local score

\[
\ell=(g_Ig_Eg_P)^{1/3}
\]

and transport score

\[
\theta=(g_Eg_P)^{1/2}
\]

then inherit deterministic uncertainty intervals through the repository's positive-factor product-root perturbation theorem.

For path \(p\), define the action-error radius

\[
E(p)
=
\sum_t e^\ell_{t,p_t}
+
|\chi|\sum_t e^\theta_t(p_t,p_{t+1}).
\]

If \(p_*\) is the population-optimal path,

\[
A_*^-=A(p_*)-E(p_*),
\]

and

\[
A_{\mathrm{comp}}^+
=
\max_{p\ne p_*}[A(p)+E(p)].
\]

The path is certified whenever

\[
\boxed{
A_*^- > A_{\mathrm{comp}}^+.
}
\]

No new probability budget is spent in this deterministic bridge once the simultaneous covariance event has been established.

---

# 9. Identifiability and falsifiability

A high score is not sufficient if distinct boundaries generate observationally equivalent measured dynamics. The framework therefore treats identifiability as a separate mathematical problem rather than assuming that every preferred path represents a uniquely recoverable subsystem.

The repository includes symmetry and observational-equivalence results, controlled counterexamples, and recovery conditions. See the [Research Index](docs/research_index.md) and the [identifiability example](examples/identifiability_counterexample.py).

## 9.1 Relevant model diagnostics

- residual temporal structure inconsistent with the declared temporal family;
- multiple or drifting relaxation scales;
- oscillatory or nonmonotone temporal dependence;
- heavy-tailed or non-Gaussian innovations;
- nonseparable space-time covariance;
- calibration-to-target mismatch;
- nuisance modes selected adaptively from the same target noise;
- candidate geometry inconsistent with physically admissible boundaries;
- inferred boundaries that fail under held-out data, changes in sampling, or physically admissible coordinate transformations.

## 9.2 Evidence status

| Statement type | Status in this repository |
| --- | --- |
| operational score definitions | explicitly defined |
| finite-horizon world-tube optimizer | exact for the declared finite candidate family |
| theorem statements | conditional on their stated assumptions |
| controlled numerical recovery | demonstrated in reproducible synthetic experiments |
| finite-sample covariance certificates | proved under the declared stochastic models |
| physical applicability to a new measurement system | requires model validation and empirical testing |
| interpretation beyond operational subsystem identification | requires additional bridge assumptions and evidence |

---

# 10. Interpretive scope

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

# 11. Current frontier

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

# 12. Reproducibility, citations, and audit trail

A result is documented with the relevant combination of assumptions, theorem or operational definition, derivation, implementation, tests, machine-readable numerical data, visible figure, and source provenance.

Repository-local Markdown and image targets are checked automatically in the test suite.

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## 12.1 Recent theorem-to-artifact map

| Result | Proof | Data | Experiment | Tests | Figure |
| --- | --- | --- | --- | --- | --- |
| P55 / AP | [proof](docs/proposition_55_quadratic_relaxation_calibration.md) | [JSON](docs/quadratic_relaxation_calibration.json) | [script](examples/quadratic_relaxation_calibration.py) | [tests](tests/test_relaxation_curvature.py) | [figure](docs/quadratic_relaxation_calibration.svg) |
| P56 / AQ | [proof](docs/proposition_56_innovation_whitened_target.md) | [JSON](docs/innovation_whitened_target.json) | [script](examples/innovation_whitened_target.py) | [tests](tests/test_innovation_whitening.py) | [figure](docs/innovation_whitened_target.svg) |
| P57 / AR | [proof](docs/proposition_57_robust_innovation_whitening.md) | [JSON](docs/robust_innovation_whitened_target.json) | [script](examples/robust_innovation_whitened_target.py) | [tests](tests/test_robust_innovation_whitening.py) | [figure](docs/robust_innovation_whitened_target.svg) |
| P58 / AS | [proof](docs/proposition_58_observer_bridge.md) | [JSON](docs/observer_bridge_dimension_audit.json) | [script](examples/observer_bridge_dimension_audit.py) | [tests](tests/test_observer_bridge.py) | [figure](docs/observer_bridge_dimension_audit.svg) |

For a complete audit, use the [Research Index](docs/research_index.md), [Assumption Ledger](docs/assumption_ledger.md), [Reproducible Results](docs/reproducible_results.md), and [Visual Research Guide](docs/visual_research_guide.md).

## 12.2 Citation architecture

The repository separates three forms of provenance:

1. **Conceptual lineage**, including Tegmark's observer-factorization question.
2. **Standard mathematical foundations**, including information theory, canonical correlation, dynamic programming, matrix analysis, covariance concentration, Gaussian relaxation, and e-value methods.
3. **Repository-specific definitions and theorems**, cited to their derivation and proof records.

| Citation layer | Purpose |
| --- | --- |
| [Bibliography and Citation Map](docs/bibliography.md) | full references and the role each source plays |
| [`references.bib`](references.bib) | machine-readable BibTeX |
| [`CITATION.cff`](CITATION.cff) | citation metadata for this repository |
| [Physics + Mathematics + Citation Map](docs/physics_mathematics_citation_map.md) | equation-by-equation provenance |

### 12.2.1 Source-role map

| Source | Role in this research |
| --- | --- |
| [Tegmark 2015](docs/bibliography.md#tegmark-2015) | primary conceptual observer-factorization starting point |
| [Tegmark 2016](docs/bibliography.md#related-tegmark-work-tegmark-2016) | related integrated-information and factorization context |
| [Shannon 1948](docs/bibliography.md#shannon-1948) | information-theoretic foundation |
| [Cover and Thomas 2006](docs/bibliography.md#cover-and-thomas-2006) | standard mutual-information and conditional-information identities |
| [Hotelling 1936](docs/bibliography.md#hotelling-1936) | canonical-correlation foundation |
| [Jaccard 1901](docs/bibliography.md#jaccard-1901) | set-overlap continuity geometry |
| [Bellman 1952](docs/bibliography.md#bellman-1952) | dynamic-programming lineage |
| [Wishart 1928](docs/bibliography.md#wishart-1928) | Gaussian covariance sampling law |
| [Aitken 1936](docs/bibliography.md#aitken-1936) | generalized least-squares lineage |
| [Bhatia 1997](docs/bibliography.md#bhatia-1997) | matrix perturbation and matrix-analysis tools |
| [Davidson and Szarek 2001](docs/bibliography.md#davidson-and-szarek-2001) | Gaussian random-matrix concentration context |
| [Laurent and Massart 2000](docs/bibliography.md#laurent-and-massart-2000) | chi-square concentration |
| [Hsu, Kakade, and Zhang 2012](docs/bibliography.md#hsu-kakade-and-zhang-2012) | quadratic-form concentration |
| [Tropp 2012](docs/bibliography.md#tropp-2012) | matrix concentration methodology |
| [Uhlenbeck and Ornstein 1930](docs/bibliography.md#uhlenbeck-and-ornstein-1930) | physical stochastic relaxation context |
| [Doob 1942](docs/bibliography.md#doob-1942) | Gaussian Markov-process context |
| [Vovk and Wang 2021](docs/bibliography.md#vovk-and-wang-2021) | e-value calibration methodology |
| [Shafer 2021](docs/bibliography.md#shafer-2021) | betting/e-value statistical context |
| [Vovk and Wang 2023](docs/bibliography.md#vovk-and-wang-2023) | confidence-set context for e-values |

## 12.3 References cited in the main research narrative

1. **Tegmark, M.** "Consciousness as a State of Matter." _Chaos, Solitons & Fractals_ 76 (2015): 238-270. DOI: [10.1016/j.chaos.2015.03.014](https://doi.org/10.1016/j.chaos.2015.03.014). Preprint: [arXiv:1401.1219](https://arxiv.org/abs/1401.1219).
2. **Tegmark, M.** "Improved Measures of Integrated Information." _PLOS Computational Biology_ 12(11) (2016): e1005123. DOI: [10.1371/journal.pcbi.1005123](https://doi.org/10.1371/journal.pcbi.1005123).
3. **Tononi, G.** "An Information Integration Theory of Consciousness." _BMC Neuroscience_ 5 (2004): 42. DOI: [10.1186/1471-2202-5-42](https://doi.org/10.1186/1471-2202-5-42).
4. **Balduzzi, D., and Tononi, G.** "Integrated Information in Discrete Dynamical Systems: Motivation and Theoretical Framework." _PLOS Computational Biology_ 4(6) (2008): e1000091. DOI: [10.1371/journal.pcbi.1000091](https://doi.org/10.1371/journal.pcbi.1000091).
5. **Oizumi, M., Albantakis, L., and Tononi, G.** "From the Phenomenology to the Mechanisms of Consciousness: Integrated Information Theory 3.0." _PLOS Computational Biology_ 10(5) (2014): e1003588. DOI: [10.1371/journal.pcbi.1003588](https://doi.org/10.1371/journal.pcbi.1003588).
6. **Shannon, C. E.** "A Mathematical Theory of Communication." _Bell System Technical Journal_ 27 (1948), Parts I and II. DOI Part I: [10.1002/j.1538-7305.1948.tb01338.x](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x).
7. **Cover, T. M., and Thomas, J. A.** _Elements of Information Theory_, 2nd ed. Wiley, 2006. DOI: [10.1002/047174882X](https://doi.org/10.1002/047174882X).
8. **Hotelling, H.** "Relations Between Two Sets of Variates." _Biometrika_ 28(3-4) (1936): 321-377. DOI: [10.1093/biomet/28.3-4.321](https://doi.org/10.1093/biomet/28.3-4.321).
9. **Jaccard, P.** "Etude comparative de la distribution florale dans une portion des Alpes et du Jura." _Bulletin de la Societe Vaudoise des Sciences Naturelles_ 37(142) (1901): 547-579. DOI: [10.5169/seals-266450](https://doi.org/10.5169/seals-266450).
10. **Bellman, R.** "On the Theory of Dynamic Programming." _Proceedings of the National Academy of Sciences_ 38(8) (1952): 716-719. DOI: [10.1073/pnas.38.8.716](https://doi.org/10.1073/pnas.38.8.716).
11. **Wishart, J.** "The Generalised Product Moment Distribution in Samples from a Normal Multivariate Population." _Biometrika_ 20A(1-2) (1928): 32-52. DOI: [10.1093/biomet/20a.1-2.32](https://doi.org/10.1093/biomet/20a.1-2.32).
12. **Aitken, A. C.** "On Least Squares and Linear Combination of Observations." _Proceedings of the Royal Society of Edinburgh_ 55 (1936): 42-48. DOI: [10.1017/S0370164600014346](https://doi.org/10.1017/S0370164600014346).
13. **Bhatia, R.** _Matrix Analysis_. Graduate Texts in Mathematics 169. Springer, 1997. DOI: [10.1007/978-1-4612-0653-8](https://doi.org/10.1007/978-1-4612-0653-8).
14. **Davidson, K. R., and Szarek, S. J.** "Local Operator Theory, Random Matrices and Banach Spaces." In _Handbook of the Geometry of Banach Spaces_, Vol. 1, 317-366. Elsevier, 2001. DOI: [10.1016/S1874-5849(01)80010-3](https://doi.org/10.1016/S1874-5849(01)80010-3).
15. **Laurent, B., and Massart, P.** "Adaptive Estimation of a Quadratic Functional by Model Selection." _The Annals of Statistics_ 28(5) (2000): 1302-1338. DOI: [10.1214/aos/1015957395](https://doi.org/10.1214/aos/1015957395).
16. **Hsu, D., Kakade, S. M., and Zhang, T.** "A Tail Inequality for Quadratic Forms of Subgaussian Random Vectors." _Electronic Communications in Probability_ 17(52) (2012): 1-6. DOI: [10.1214/ECP.v17-2079](https://doi.org/10.1214/ECP.v17-2079).
17. **Tropp, J. A.** "User-Friendly Tail Bounds for Sums of Random Matrices." _Foundations of Computational Mathematics_ 12 (2012): 389-434. DOI: [10.1007/s10208-011-9099-z](https://doi.org/10.1007/s10208-011-9099-z).
18. **Vovk, V., and Wang, R.** "E-values: Calibration, Combination, and Applications." _The Annals of Statistics_ 49(3) (2021): 1736-1754. DOI: [10.1214/20-AOS2020](https://doi.org/10.1214/20-AOS2020).
19. **Shafer, G.** "Testing by Betting: A Strategy for Statistical and Scientific Communication." _Journal of the Royal Statistical Society: Series A_ 184(2) (2021): 407-431. DOI: [10.1111/rssa.12647](https://doi.org/10.1111/rssa.12647).
20. **Vovk, V., and Wang, R.** "Confidence and Discoveries with E-values." _Statistical Science_ 38(2) (2023): 329-354. DOI: [10.1214/22-STS874](https://doi.org/10.1214/22-STS874).
21. **Uhlenbeck, G. E., and Ornstein, L. S.** "On the Theory of the Brownian Motion." _Physical Review_ 36 (1930): 823-841. DOI: [10.1103/PhysRev.36.823](https://doi.org/10.1103/PhysRev.36.823).
22. **Doob, J. L.** "The Brownian Movement and Stochastic Equations." _Annals of Mathematics_ 43(2) (1942): 351-369. DOI: [10.2307/1968873](https://doi.org/10.2307/1968873).

The wider proposition-to-literature map, including Helmert contrasts and additional theorem-specific sources, is maintained in the [Bibliography and Citation Map](docs/bibliography.md) and [`references.bib`](references.bib).

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
