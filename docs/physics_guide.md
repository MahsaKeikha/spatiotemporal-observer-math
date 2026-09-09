# Physics guide

This guide explains **Spatiotemporal Observer Mathematics** from the physics outward. The goal is to make every mathematical object answer a physical question and to keep the model assumptions, units, citations, and falsification conditions visible.

The guiding rule is:

> **Before asking whether a moving subsystem can be identified mathematically, state what is measured, what can physically move, what interactions couple the measurements, what remains unresolved, and what evidence could falsify the model.**

The mathematics is conditional on a declared observation model. A statistical pattern does not become a physical object merely because it has a compact equation, and the word `observer` does not mean conscious subject by definition.

For equation-level provenance, use the [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md). For full references, use the [Bibliography and Citation Map](bibliography.md) and [`references.bib`](../references.bib).

---

# 1. Physical problem

Consider a physical system with many measured degrees of freedom. Depending on the application, the coordinates might be voltages, displacements, pressure measurements, neural channels, concentrations, positions, or other sensor variables.

The measured state is

\[
\boxed{
X_t=(X_t^{(1)},\ldots,X_t^{(n)}).
}
\]

The repository does not assume that the same coordinates always form the subsystem of interest. Instead, a candidate boundary is

\[
\boxed{
S_t\subseteq\{1,\ldots,n\}.
}
\]

Its history is

\[
\boxed{
\mathcal W=(S_0,S_1,\ldots,S_{T-1}).
}
\]

The physical picture is a coherent organization that can move through the coordinates used to observe it. A vortex crossing a sensor array or a localized collective mode moving through a lattice can remain physically coherent even while its sensor membership changes.

[![Physics to inference pipeline](physics_pipeline.svg)](../README.md#2-physics-first-observation-model-and-fluctuation-geometry)

## Conceptual lineage

The primary conceptual starting point is Max Tegmark's observer-factorization question in [Tegmark 2015](bibliography.md#tegmark-2015). This repository develops a separate mathematical direction in which the subsystem boundary is explicitly time dependent and must be inferred as a dynamical path.

The world-tube, transport score, recovery theorems, finite-sample certification program, physical-time calibration, and covariance-to-world-tube bridge are repository developments, not results attributed to Tegmark.

---

# 2. Observation model and fluctuation geometry

The main analytical model is

\[
\boxed{
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t),
\qquad
\varepsilon_t\perp X_t.
}
\]

| Symbol | Mathematical role | Physical reading |
| --- | --- | --- |
| \(X_t\) | measured state | physical observables at time \(t\) |
| \(A_t\) | transition operator | effective one-step coupling and propagation |
| \(\varepsilon_t\) | innovation | unresolved stochastic input represented by the model |
| \(Q_t\) | innovation covariance | fluctuation geometry of unresolved input |
| \(S_t\) | candidate coordinate set | proposed subsystem boundary |

If

\[
\Sigma_t=\operatorname{Cov}(X_t),
\]

then

\[
\boxed{
\Sigma_{t+1}=A_t\Sigma_tA_t^{\mathsf T}+Q_t
}
\]

and

\[
\boxed{
\operatorname{Cov}(X_t,X_{t+1})=\Sigma_tA_t^{\mathsf T}.
}
\]

Hence

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

This adjacent-state covariance is the fluctuation geometry used by the Gaussian information factors.

The model is an analytical approximation. A physical application must justify the coordinate basis, units, sampling interval, preprocessing, approximate linearity, Gaussianity, and the meaning of the unresolved forcing.

---

# 3. Gaussian information geometry

For Gaussian subvectors \(X\) and \(Y\),

\[
\boxed{
I(X;Y)
=
\frac{1}{2}\log_2
\frac{\det\Sigma_X\det\Sigma_Y}{\det\Sigma_{XY}}.
}
\]

For conditioning vector \(Z\),

\[
\boxed{
I(X;Y\mid Z)
=
\frac{1}{2}\log_2
\frac{\det\Sigma_{XZ}\det\Sigma_{YZ}}
{\det\Sigma_Z\det\Sigma_{XYZ}}.
}
\]

These are standard Gaussian information identities from the information-theory lineage of [Shannon 1948](bibliography.md#shannon-1948) and [Cover and Thomas 2006](bibliography.md#cover-and-thomas-2006).

**Physical caution:** mutual information is statistical dependence under the declared model. It is not automatically thermodynamic entropy, energy, causality, semantics, or conscious information.

---

# 4. Four operational subsystem properties

## 4.1 Integration

For nontrivial bipartition \(S=U\sqcup V\),

\[
J_t(U,V)
=
I(X_U^{t+1};X_V^t\mid X_U^t)
+
I(X_V^{t+1};X_U^t\mid X_V^t).
\]

Define

\[
\boxed{
\mathcal J_t(S)
=
\frac{1}{|S|}
\min_{U\sqcup V=S}J_t(U,V),
}
\]

and

\[
\boxed{
G_t(S)=1-2^{-\mathcal J_t(S)}.
}
\]

**Physical reading:** internal parts add predictive information about one another's future after each side's own present is known.

The broader conceptual lineage includes [Tegmark 2015](bibliography.md#tegmark-2015), [Tegmark 2016](bibliography.md#related-tegmark-work-tegmark-2016), and the integrated-information literature. The particular directed minimum-cut functional is a repository definition.

## 4.2 Environmental insulation

Let \(\bar S\) denote measured coordinates outside \(S\). Define

\[
\boxed{
\mathcal L_t(S)
=
\frac{1}{|S|}
I(X_S^{t+1};X_{\bar S}^t\mid X_S^t),
}
\]

\[
\boxed{
K_t(S)=2^{-\mathcal L_t(S)}.
}
\]

**Physical reading:** once the candidate's present is known, the measured exterior adds comparatively limited prediction of its next state.

This is relative predictive closure, not thermodynamic isolation.

## 4.3 Persistence

For vectors \(X\) and \(Y\), define the whitened cross-covariance

\[
C
=
\Sigma_X^{-1/2}
\operatorname{Cov}(X,Y)
\Sigma_Y^{-1/2}.
\]

Let \(\rho_i\) be its singular values. Then

\[
\boxed{
P(X,Y)=\frac{1}{r}\sum_{i=1}^{r}\rho_i^2,
\qquad
r=\min(\dim X,\dim Y).
}
\]

**Physical reading:** collective fluctuation directions in a candidate retain predictive continuity into the future.

**Lineage:** canonical correlation from [Hotelling 1936](bibliography.md#hotelling-1936), with matrix-analysis background from [Bhatia 1997](bibliography.md#bhatia-1997).

## 4.4 Transport

For source \(S\) at time \(t\) and target \(R\) at time \(t+1\),

\[
P_t(S\to R)=P(X_S^t,X_R^{t+1}),
\]

\[
L_t(S\to R)
=
\frac{1}{|R|}
I(X_R^{t+1};X_{\bar S}^t\mid X_S^t),
\]

\[
\boxed{
\Theta_t(S\to R)
=
\sqrt{P_t(S\to R)2^{-L_t(S\to R)}}.
}
\]

**Physical reading:** the organization may move into new measured coordinates while preserving predictive structure and remaining comparatively insulated from the measured exterior.

This transport functional is a repository definition built from information-theoretic and canonical-correlation ingredients.

---

# 5. Moving world-tube objective

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

For path \(p=(j_0,\ldots,j_{T-1})\),

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

with

\[
\boxed{
d_J(S,R)=1-\frac{|S\cap R|}{|S\cup R|}.
}
\]

**Lineage:** Jaccard geometry from [Jaccard 1901](bibliography.md#jaccard-1901). The complete score is a repository definition.

The exact finite-horizon optimizer uses dynamic programming in the lineage of [Bellman 1952](bibliography.md#bellman-1952):

\[
V_0(j)=\Omega_0(S^{(j)}),
\]

\[
\boxed{
V_t(j)
=
\Omega_t(S^{(j)})+
\max_i
\left[
V_{t-1}(i)
+
\chi\Theta_{t-1}(S^{(i)}\to S^{(j)})
-
\lambda d_J(S^{(i)},S^{(j)})
\right].
}
\]

The `action margin` is the objective difference between the best and strongest competing paths. It is not physical action in joule-seconds.

---

# 6. Why covariance certification matters physically

For multivariate fluctuations,

\[
\boxed{
\Sigma
=
\mathbb E[(X-\mu)(X-\mu)^{\mathsf T}].
}
\]

Diagonal entries are coordinate variances, off-diagonal entries are co-fluctuations, and covariance eigenvectors describe collective fluctuation directions.

Covariance eigenvalues are **not automatically physical energies**. An energy interpretation requires a separate derivation connecting the measured coordinates to a Hamiltonian, temperature, spectrum, or other physical energetic quantity.

Because the Gaussian information factors depend on covariance blocks, the boundary inference is only as trustworthy as its covariance estimates.

The central relative event is

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

When \(\epsilon<1\), inverse-covariance perturbation remains in a controlled regime. The value one is a mathematical threshold, not a physical phase transition.

**Lineage:** [Wishart 1928](bibliography.md#wishart-1928), [Tropp 2012](bibliography.md#tropp-2012), and [Bhatia 1997](bibliography.md#bhatia-1997).

---

# 7. Temporal memory in physical time

A discrete AR(1) coefficient depends on sampling interval. To use a sampling-consistent parameter, the later theorem chain uses

\[
\boxed{
K_\tau(t_i,t_j)
=
\exp\left(-\frac{|t_i-t_j|}{\tau}\right).
}
\]

Under uniform interval \(\Delta t\),

\[
\boxed{
\phi_{\Delta t}=e^{-\Delta t/\tau},
\qquad
\tau=-\frac{\Delta t}{\log\phi_{\Delta t}}.
}
\]

For irregular adjacent gaps,

\[
\alpha_i=e^{-(t_{i+1}-t_i)/\tau},
\]

and Proposition 53 gives

\[
\boxed{
X_{i+1}
=
\alpha_iX_i+
\sqrt{1-\alpha_i^2}\,\varepsilon_i.
}
\]

It also constructs an exact lower-bidiagonal whitener

\[
\boxed{
W_\tau R_\tau W_\tau^{\mathsf T}=I,
\qquad
R_\tau^{-1}=W_\tau^{\mathsf T}W_\tau.
}
\]

**Lineage:** [Uhlenbeck and Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930) and Gaussian Markov-process context from [Doob 1942](bibliography.md#doob-1942). The irregular-grid identities used here are proved directly in P53.

A real system may require multiple timescales, oscillatory kernels, long memory, or nonstationarity. One exponential relaxation time is a declared model, not a universal physical law.

---

# 8. Nuisance structure and innovation covariance

Suppose

\[
Y=HB+E,
\qquad
\operatorname{vec}(E)
\sim
\mathcal N(0,R_\tau\otimes\Gamma).
\]

Here \(H\) contains predeclared deterministic temporal modes such as baseline or drift.

In exact innovation coordinates,

\[
Z=W_\tau Y,
\qquad
G=W_\tau H,
\]

and

\[
P_G=I-G(G^{\mathsf T}G)^{-1}G^{\mathsf T}.
\]

Proposition 56 uses

\[
\boxed{
\widehat\Gamma_{\mathrm{IW}}
=
\frac{1}{N-q}Z^{\mathsf T}P_GZ.
}
\]

Under its declared assumptions,

\[
\boxed{
(N-q)\widehat\Gamma_{\mathrm{IW}}
\sim
\operatorname{Wishart}_d(\Gamma,N-q).
}
\]

**Physical reading:** fit deterministic nuisance modes after transforming the measurements into the temporal covariance geometry implied by the physical model.

**Lineage:** generalized least squares from [Aitken 1936](bibliography.md#aitken-1936) and Gaussian covariance laws from [Wishart 1928](bibliography.md#wishart-1928).

---

# 9. Finite-sample calibration of the physical timescale

The repository does not assume that \(\tau\) is known. An independent calibration record is used to construct a finite-sample confidence set with e-values.

For tested parameter \(\tau\), an e-value satisfies

\[
\mathbb E_\tau[e_\tau]\le1.
\]

Markov's inequality gives a finite-sample test, and inversion yields a confidence set.

**Lineage:** [Vovk and Wang 2021](bibliography.md#vovk-and-wang-2021), [Shafer 2021](bibliography.md#shafer-2021), and [Vovk and Wang 2023](bibliography.md#vovk-and-wang-2023).

On Experiment AP, Proposition 55 gives

\[
\boxed{
\tau\in[0.686875,0.8515625]\ \mathrm{s}
}
\]

at calibration confidence `0.975`.

---

# 10. Robust innovation whitening under uncertain physical time

Proposition 57 chooses one calibration-derived working timescale

\[
\tau_0=0.76921875\ \mathrm{s}
\]

and lets \(W_0\) be its exact whitener. For every admissible true \(\tau\),

\[
\boxed{
C_\tau=W_0R_\tau W_0^{\mathsf T}.
}
\]

Two deterministic covers are used for two different purposes.

## Operator cover

\[
\|C_\tau-C_{\tau'}\|_2
\le
L_C|\tau-\tau'|,
\]

so for maximum grid spacing \(h\),

\[
\boxed{
\delta_\lambda=\frac{h}{2}L_C.
}
\]

This controls projected temporal eigenvalues.

## Trace-specific normalization cover

Let

\[
d(\tau)=\operatorname{tr}(P_GC_\tau),
\qquad
M=W_0^{\mathsf T}P_GW_0.
\]

Then

\[
d(\tau)=\operatorname{tr}(MR_\tau).
\]

For distance \(D_{ij}=|t_i-t_j|\),

\[
\frac{\partial R_\tau(i,j)}{\partial\tau}
=
\frac{D_{ij}}{\tau^2}e^{-D_{ij}/\tau}.
\]

Its scalar maximum on the calibrated interval is obtained at \(D_{ij}/2\) clipped to the interval. This gives the deterministic trace Lipschitz constant

\[
\boxed{
L_d
=
\sum_{i,j}|M_{ij}|
\sup_\tau
\left|
\frac{\partial R_\tau(i,j)}{\partial\tau}
\right|.
}
\]

Hence

\[
\boxed{
\delta_d=\frac{h}{2}L_d.
}
\]

This is substantially tighter than multiplying the operator radius by the full residual rank.

On Experiment AR,

\[
L_d=176.55489\ \mathrm{s}^{-1},
\qquad
\delta_d=0.01419745,
\]

and the final uniform scalar target radius is

\[
\boxed{
\epsilon_{57}=0.7195879984<1.
}
\]

The reduction relative to the P55 calibrated raw-time theorem is about

\[
\boxed{70.2\%}.
\]

With calibration and target confidence each `0.975`, the combined lower bound is

\[
\boxed{0.950625}.
\]

[![Experiment AR](robust_innovation_whitened_target.svg)](proposition_57_robust_innovation_whitening.md)

---

# 11. Return to the moving-boundary problem

The original goal is not scalar covariance estimation. It is world-tube recovery.

For future candidate \(S\), Proposition 58 defines

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

For candidate count \(C\) and horizon \(T\), the required target-indexed block count is

\[
\boxed{
B_{\mathrm{obs}}=TC.
}
\]

Proposition 58 propagates simultaneous covariance uncertainty through integration, insulation, persistence, transport, and the complete path objective without spending another probability budget.

On Experiment AS,

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

At 118 residual innovation degrees, the current exact-\(\tau\) observer-scale matrix theorem gives

\[
\boxed{
\epsilon_{\mathrm{observer}}=1.8573569119>1.
}
\]

This negative result is important. Scalar covariance success does not automatically imply observer-scale path certification. The current bottleneck is dimensional and structural.

[![Experiment AS](observer_bridge_dimension_audit.svg)](proposition_58_observer_bridge.md)

---

# 12. P41-P58 as one measurement-certification chain

| Result | Physical or statistical question |
| ---: | --- |
| P41 | How much information remains when measurements have temporal dependence? |
| P42 | How does removing an unknown baseline change covariance information? |
| P43 | Can temporal persistence be calibrated rather than assumed? |
| P44 | Can deterministic nuisance modes be removed without calling them covariance? |
| P45 | Can dependence uncertainty and nuisance removal be combined? |
| P46 | Can the actual nuisance geometry replace a rank-only worst case? |
| P47 | Can the full Gaussian covariance matrix be certified directly? |
| P48 | Can the matrix guarantee be uniform over AR(1) uncertainty? |
| P49 | Can a complete compact temporal covariance family be covered? |
| P50 | Can a multi-parameter temporal family be learned from independent calibration? |
| P51 | Can e-values create a finite-sample temporal confidence set? |
| P52 | Can that continuum confidence set be propagated to an independent target? |
| P53 | Can temporal memory be represented by a physical relaxation time and exact local innovations? |
| P53B | Can physical \(\tau\) be calibrated directly on irregular timestamps? |
| P54 | Can calibration resolution and target resolution be separated? |
| P55 | Can local likelihood slope and curvature tighten the \(\tau\) cover? |
| P56 | If \(\tau\) is exact, can local innovations change the covariance estimator? |
| P57 | How much of that gain survives finite-sample \(\tau\) uncertainty? |
| P58 | Can covariance uncertainty be returned to the complete moving-boundary objective? |

P41-P58 are measurement-certification machinery supporting the moving-subsystem problem. They are not a separate theory of consciousness.

---

# 13. Units and dimensional accountability

A physical application should state units explicitly.

- \(X_t\) carries the units of the measured observables.
- covariance carries squared observable units.
- \(Q_t\) carries covariance units.
- \(A_t\) maps coordinate units from one sample to the next and is dimensionless only when the coordinate convention permits it.
- \(\tau\) carries physical time units.
- canonical correlations are dimensionless.
- relative covariance radii are dimensionless.
- mutual information is measured in bits because the implemented logarithms are base two.

If variables with different units are combined, scaling conventions must be explicit. A physically meaningful result should not change under an arbitrary unit conversion unless the model itself says why it should.

---

# 14. Physics accountability and falsification checklist

Before applying the framework to an experimental system, document:

## Observables

- what each coordinate measures;
- units and sensor calibration;
- sampling interval and sensor bandwidth;
- spatial or functional geometry;
- preprocessing and filtering.

## Dynamics

- what interaction is represented by \(A_t\);
- over what interval linearization is plausible;
- what omitted processes are absorbed into \(Q_t\);
- relevant conservation laws or symmetries.

## Boundary geometry

- what makes a candidate set physically admissible;
- whether membership may change arbitrarily or only through local movement;
- whether the candidate family respects physical adjacency or material constraints.

## Temporal statistics

- whether one exponential relaxation time is adequate;
- whether the process is stationary over the analyzed window;
- whether oscillations, multiple timescales, or long memory are visible;
- whether innovation residuals are still temporally correlated after whitening.

## Nuisance structure

- what deterministic modes are removed;
- whether those modes were declared before inspecting the same target noise;
- whether projection could remove real physical dynamics.

## Distributional assumptions

- whether Gaussian residuals are plausible;
- whether separability is adequate when a theorem requires it;
- whether heavy tails or outliers invalidate the stated Gaussian guarantee.

## Validation

- held-out covariance and correlation structure;
- robustness to sampling-rate and unit changes;
- calibration-to-target transfer;
- stability across sensors or coordinate representations;
- intervention tests that can separate competing subsystem hypotheses.

If the physical model fails these checks, the correct response is to change the model rather than over-interpret a narrow mathematical certificate.

---

# 15. Interpretation boundary

The repository separates three scientific claims:

1. **Mathematical claim:** a theorem follows from explicit assumptions.
2. **Physical-model claim:** a real system is adequately described by those assumptions and mapped observables.
3. **Consciousness claim:** an additional theory connects the physical structure to subjective experience.

Proof establishes only the first. The second requires experiment and model validation. The third requires a separate bridge theory and evidence.

See [README Section 13](../README.md#13-relationship-to-tegmarks-observer-factorization-question) and the [Interpretation Protocol](interpretation_protocol.md).

---

# 16. Recommended physics-first reading order

1. [Main README](../README.md)
2. this Physics Guide
3. [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md)
4. [Visual Research Guide](visual_research_guide.md)
5. [Research Overview](research_overview.md)
6. [Assumption Ledger](assumption_ledger.md)
7. [Bibliography and Citation Map](bibliography.md)
8. theorem pages only after the physical objects and assumptions are clear

The theorem pages should be read as certification layers supporting one physical inference pipeline, not as isolated inequalities.
