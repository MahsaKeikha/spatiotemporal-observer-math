# Physics guide

This page explains the physical meaning of the mathematical objects used in **Spatiotemporal Observer Mathematics**. It is written for a reader who wants to understand the physics before reading the theorem ladder.

The guiding rule is:

> **Before asking whether a moving subsystem can be identified mathematically, state what is physically moving, what is measured, what interactions couple the measurements, what fluctuations remain unresolved, and what evidence could falsify the model.**

The mathematics is conditional on a declared physical observation model. A statistical pattern is not converted into a physical object merely by notation, and the word `observer` does not mean conscious subject by definition.

For a compact equation-by-equation provenance view, use the **[Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md)**. For the full external literature record, use the **[Bibliography and Citation Map](bibliography.md)** and [`references.bib`](../references.bib).

---

# 1. The physical problem in one picture

Imagine a dynamical system with many measurable degrees of freedom. Depending on the application, those coordinates could be:

- voltages on an electrical network;
- displacements or velocities in a mechanical array;
- pressure or velocity measurements in a fluid;
- firing-rate or field-potential channels in a neural recording;
- concentrations in a biochemical network;
- positions and internal states in a multi-agent system;
- generic sensor channels in a coupled physical process.

The full measured state at time `t` is

\[
\boxed{
X_t=(X_t^{(1)},\ldots,X_t^{(n)}).
}
\]

The repository does not assume that the same coordinates always form the subsystem of interest. Instead, it asks whether the dynamics support a moving candidate set

\[
\boxed{
S_t\subseteq\{1,\ldots,n\}.
}
\]

Its changing history is

\[
\boxed{
\mathcal W=(S_0,S_1,\ldots,S_{T-1}),
}
\]

called an **observer world-tube** in this repository.

The term `world-tube` is an analogy to the history of an extended object through time. It is not a claim that the construction is a relativistic spacetime world tube. Here the object being followed is a changing set of measured coordinates.

A useful physical picture is a coherent structure moving across a sensor field. A vortex moving across a fluid array, a localized mechanical mode moving through a lattice, or a coordinated activity pattern moving across channels can remain dynamically coherent even while the sensors that represent it change.

[![Physics pipeline](physics_pipeline.svg)](../README.md#2-the-complete-physical-problem-in-one-picture)

## Conceptual lineage

The primary conceptual starting point is Max Tegmark's ["Consciousness as a State of Matter"](bibliography.md#tegmark-2015), which asks why an observer should correspond to one factorization of the physical world rather than another and discusses information, integration, independence, and dynamics as organizing principles.

The present repository takes that observer-factorization question in a separate mathematical direction: the boundary is allowed to change with time and must be inferred as a persistent dynamical path. The time-dependent boundary `S_t`, the world-tube objective, the recovery theorems, and the finite-sample measurement program are repository developments rather than results attributed to Tegmark.

---

# 2. Effective dynamics and fluctuation geometry

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

This is a local stochastic dynamical model.

| Symbol | Mathematical role | Physical reading |
| --- | --- | --- |
| \(X_t\) | measured state vector | physical observables recorded at time `t` |
| \(A_t\) | transition operator | effective coupling and propagation over one sampling interval |
| \(\varepsilon_t\) | unresolved stochastic input | omitted degrees of freedom, environmental forcing, process noise, or other unresolved input represented by the model |
| \(Q_t\) | innovation covariance | covariance geometry of the unresolved input |
| \(S_t\) | candidate coordinate set | proposed subsystem boundary at time `t` |

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

Therefore the adjacent-state covariance is

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

This joint covariance is the fluctuation geometry from which the Gaussian information quantities are computed.

`A_t` should not be interpreted as a fundamental law unless an application justifies that reading. In many experiments it is an effective linearization over a chosen time interval. Gaussianity is likewise a modeling assumption used because it makes information quantities, covariance propagation, and finite-sample certification analytically tractable.

---

# 3. Gaussian information quantities

For a Gaussian vector `Z` of dimension `k`,

\[
h(Z)
=
\frac{1}{2}\log_2\left[(2\pi e)^k\det\Sigma_Z\right].
\]

For subvectors `X` and `Y`,

\[
\boxed{
I(X;Y)
=
\frac{1}{2}\log_2
\frac{\det\Sigma_X\det\Sigma_Y}{\det\Sigma_{XY}}.
}
\]

For conditioning vector `Z`,

\[
\boxed{
I(X;Y\mid Z)
=
\frac{1}{2}\log_2
\frac{\det\Sigma_{XZ}\det\Sigma_{YZ}}
{\det\Sigma_Z\det\Sigma_{XYZ}}.
}
\]

These formulas are standard Gaussian information theory; see [Shannon 1948](bibliography.md#shannon-1948) and [Cover and Thomas 2006](bibliography.md#cover-and-thomas-2006).

**Physical reading:** mutual information and conditional mutual information quantify statistical dependence in the declared probability model. They are not automatically thermodynamic entropy, free energy, causal influence, semantic information, or subjective information.

---

# 4. Four operational properties of a candidate subsystem

The implemented score uses four distinct ideas: integration, insulation, persistence, and transport. Their equations and physical meanings should be read together.

## 4.1 Internal integration

For a nontrivial bipartition

\[
S=U\sqcup V,
\]

define directed cross-prediction

\[
J_t(U,V)
=
I(X_U^{t+1};X_V^t\mid X_U^t)
+
I(X_V^{t+1};X_U^t\mid X_V^t).
\]

The weakest internal cut is

\[
\boxed{
\mathcal J_t(S)
=
\frac{1}{|S|}
\min_{U\sqcup V=S}J_t(U,V).
}
\]

The normalized integration factor is

\[
\boxed{
G_t(S)=1-2^{-\mathcal J_t(S)}.
}
\]

**Physical reading:** the candidate contains components whose present states add predictive information about one another's future even after each side's own present is known.

The broader integration lineage includes [Tegmark 2015](bibliography.md#tegmark-2015), [Tegmark 2016](bibliography.md#related-tegmark-work-tegmark-2016), and the integrated-information literature. The particular directed minimum-cut definition above is a repository operational definition, not a Tegmark theorem and not IIT Phi.

## 4.2 Environmental insulation

Let `\bar S` denote the measured variables outside `S`. Define leakage

\[
\boxed{
\mathcal L_t(S)
=
\frac{1}{|S|}
I(X_S^{t+1};X_{\bar S}^t\mid X_S^t).
}
\]

and insulation factor

\[
\boxed{
K_t(S)=2^{-\mathcal L_t(S)}.
}
\]

**Physical reading:** after the candidate's own present is known, the rest of the measured system adds comparatively limited predictive information about its immediate future.

This does not require physical isolation. Open systems exchange matter, energy, and information with their surroundings. The operational question is whether the candidate has enough relative predictive closure to be distinguished from an arbitrary cut through the measured system.

## 4.3 Persistence

For vectors `X` and `Y`, form the whitened cross-covariance

\[
M
=
\Sigma_X^{-1/2}
\operatorname{Cov}(X,Y)
\Sigma_Y^{-1/2}.
\]

Let `\rho_i` be its singular values. Define

\[
\boxed{
P(X,Y)
=
\frac{1}{r}\sum_{i=1}^{r}\rho_i^2,
\qquad
r=\min(\dim X,\dim Y).
}
\]

For a fixed candidate,

\[
X=X_S^t,
\qquad
Y=X_S^{t+1}.
\]

**Physical reading:** collective fluctuation directions in the candidate persist predictively into the next time step.

The canonical-correlation lineage is [Hotelling 1936](bibliography.md#hotelling-1936); relevant matrix tools are summarized under [Bhatia 1997](bibliography.md#bhatia-1997). The particular averaging convention is a repository modeling choice.

## 4.4 Transport across a changing boundary

For source `S` at time `t` and target `R` at time `t+1`, define

\[
P_t(S\to R)=P(X_S^t,X_R^{t+1}),
\]

\[
L_t(S\to R)
=
\frac{1}{|R|}
I(X_R^{t+1};X_{\bar S}^t\mid X_S^t),
\]

and

\[
\boxed{
\Theta_t(S\to R)
=
\sqrt{P_t(S\to R)\,2^{-L_t(S\to R)}}.
}
\]

**Physical reading:** a persistent organization may move into different measured coordinates while retaining predictive structure and remaining comparatively insulated from the rest of the measured system.

This is why a moving boundary is needed at all.

---

# 5. Local score and world-tube objective

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

For finite candidate family

\[
\mathcal C=\{S^{(1)},\ldots,S^{(C)}\}
\]

and path `p=(j_0,\ldots,j_{T-1})`, the complete moving-boundary objective is

\[
\boxed{
A(p)=
\sum_{t=0}^{T-1}\Omega_t(S^{(j_t)})
+\chi\sum_{t=0}^{T-2}\Theta_t(S^{(j_t)}\to S^{(j_{t+1})})
-\lambda\sum_{t=0}^{T-2}d_J(S^{(j_t)},S^{(j_{t+1})}).
}
\]

The continuity geometry is

\[
\boxed{
d_J(S,R)=1-\frac{|S\cap R|}{|S\cup R|}.
}
\]

The Jaccard lineage is [Jaccard 1901](bibliography.md#jaccard-1901). This use of Jaccard distance is a modeling choice, not a claim that it is the unique physically correct boundary geometry.

The exact finite-horizon optimizer uses dynamic programming in the lineage of [Bellman 1952](bibliography.md#bellman-1952). If `V_t(j)` is the best partial objective ending at candidate `j`,

\[
V_0(j)=\Omega_0(S^{(j)}),
\]

\[
\boxed{
V_t(j)=
\Omega_t(S^{(j)})+
\max_i\left[
V_{t-1}(i)
+\chi\Theta_{t-1}(S^{(i)}\to S^{(j)})
-\lambda d_J(S^{(i)},S^{(j)})
\right].
}
\]

Backpointers recover the global optimum, and the repository's two-best extension recovers the exact runner-up path.

The term `action margin` refers to the optimization difference between the best and competing paths. It is not physical action in joule-seconds.

---

# 6. Why covariance is the measurement bottleneck

For a multivariate fluctuating system,

\[
\boxed{
\Sigma=\mathbb E[(X-\mu)(X-\mu)^\mathsf T].
}
\]

The diagonal entries are coordinate variances, the off-diagonal entries are co-fluctuations, and the eigenvectors and eigenvalues describe collective variance directions and their strengths.

These eigenvalues are **not automatically physical energies**. An energy interpretation requires an additional physical model connecting the measured coordinates and covariance to a Hamiltonian, temperature, power spectrum, or other physically defined energetic quantity.

Covariance matters because, under the Gaussian model, integration, leakage, persistence, and transport are functions of covariance blocks. If those blocks are estimated badly, the candidate scores and recovered world-tube can be wrong.

The central finite-sample quantity is the relative covariance radius

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

**Physical reading:** after scaling by the population fluctuation geometry, every collective direction is distorted by at most `\epsilon` in operator norm.

When `\epsilon<1`, inverse-covariance and conditional-information perturbation calculations remain in a controlled regime. The value one is a mathematical perturbation threshold, not a physical phase transition.

Gaussian covariance laws trace to [Wishart 1928](bibliography.md#wishart-1928). Matrix concentration uses the matrix-Laplace and Chernoff lineage of [Tropp 2012](bibliography.md#tropp-2012), with matrix-analysis tools summarized under [Bhatia 1997](bibliography.md#bhatia-1997).

---

# 7. Temporal memory: from AR(1) to physical relaxation time

Repeated measurements from a physical system are generally not independent. Treating every time sample as independent can greatly exaggerate the amount of information in a finite record.

An early model in the repository is AR(1):

\[
R_\phi(i,j)=\phi^{|i-j|},
\qquad
0\le\phi<1.
\]

But `\phi` depends on sampling interval. To express temporal memory in physical time, the later theorem chain uses

\[
\boxed{
K_\tau(t_i,t_j)
=
\exp\left(-\frac{|t_i-t_j|}{\tau}\right).
}
\]

Under uniform sampling interval `\Delta t`,

\[
\boxed{
\phi_{\Delta t}=e^{-\Delta t/\tau},
\qquad
\tau=-\frac{\Delta t}{\log\phi_{\Delta t}}.
}
\]

**Physical reading:** `\tau` is the declared relaxation timescale, while the discrete one-step correlation changes when the acquisition interval changes.

The physical stochastic-process lineage is [Uhlenbeck and Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930) and the Gaussian Markov-process context of [Doob 1942](bibliography.md#doob-1942). Proposition 53 derives the exact formulas used by this repository from the declared exponential covariance kernel.

A real physical system may require multiple relaxation times, oscillatory kernels, nonstationarity, colored noise, or continuous spectral models. One exponential timescale is a declared model, not a universal physical law.

---

# 8. Irregular-grid local innovations

For adjacent irregular gaps

\[
\Delta_i=t_{i+1}-t_i,
\qquad
\alpha_i=e^{-\Delta_i/\tau},
\]

Proposition 53 gives the local transition representation

\[
\boxed{
X_{i+1}
=
\alpha_iX_i+
\sqrt{1-\alpha_i^2}\,\varepsilon_i.
}
\]

It also constructs a lower-bidiagonal temporal whitener

\[
\boxed{
W_\tau R_\tau W_\tau^{\mathsf T}=I,
\qquad
R_\tau^{-1}=W_\tau^{\mathsf T}W_\tau.
}
\]

**Physical reading:** the predictable part of the declared exponential relaxation is removed locally, leaving innovation coordinates that represent new stochastic information under the model.

This is a representation change driven by the declared temporal physics, not an assertion that correlation creates information.

---

# 9. Deterministic nuisance structure and covariance-aware fitting

A measured record may contain deterministic trends that should not be mistaken for stochastic dynamics. Write

\[
Y=HB+E,
\]

where the columns of `H` are predeclared temporal shapes such as a baseline, linear drift, known stimulation profile, or acquisition artifact.

In raw coordinates, the orthogonal projector is

\[
P_H=I-H(H^{\mathsf T}H)^{-1}H^{\mathsf T}.
\]

When the temporal covariance is known, Proposition 56 first moves into innovation coordinates:

\[
Z=W_\tau Y,
\qquad
G=W_\tau H,
\]

then uses

\[
P_G=I-G(G^{\mathsf T}G)^{-1}G^{\mathsf T}.
\]

The innovation-whitened covariance estimator is

\[
\boxed{
\widehat\Gamma_{\mathrm{IW}}
=
\frac{1}{N-q}Z^{\mathsf T}P_GZ.
}
\]

Under the declared separable Gaussian model,

\[
\boxed{
(N-q)\widehat\Gamma_{\mathrm{IW}}
\sim
\operatorname{Wishart}_d(\Gamma,N-q).
}
\]

**Physical reading:** remove deterministic nuisance modes in the covariance geometry implied by the temporal model, then estimate fluctuation covariance from the remaining innovations.

The generalized least-squares lineage is [Aitken 1936](bibliography.md#aitken-1936), and the exact Gaussian covariance law is [Wishart 1928](bibliography.md#wishart-1928). The irregular-grid local whitening construction is a repository result built from Proposition 53.

The nuisance design must be fixed before examining the same stochastic target noise unless a separate adaptive-selection argument is provided.

---

# 10. Finite-sample calibration of physical time

The later physical-time sequence does not assume that `\tau` is known. It uses an independent calibration record and finite-sample e-value inference.

For tested parameter `\tau`, an e-value is nonnegative and satisfies

\[
\mathbb E_\tau[e_\tau]\le1.
\]

Markov's inequality yields a finite-sample test, and inversion yields a confidence set for `\tau`.

The e-value lineage is [Vovk and Wang 2021](bibliography.md#vovk-and-wang-2021), [Shafer 2021](bibliography.md#shafer-2021), and [Vovk and Wang 2023](bibliography.md#vovk-and-wang-2023).

Propositions 51-55 specialize and certify this strategy for the declared temporal models used in the repository.

On Experiment AP, Proposition 55 produces the calibrated physical-time hull

\[
\boxed{
\tau\in[0.686875,0.8515625]\ \mathrm{s}
}
\]

at calibration confidence `0.975`.

---

# 11. Robust innovation inference when physical time is uncertain

Proposition 56 assumes exact target `\tau`. Proposition 57 removes that assumption.

Choose one calibration-derived working timescale `\tau_0` and let `W_0` be its exact whitener. For every still-admissible true `\tau`, the transformed temporal covariance is

\[
\boxed{
C_\tau=W_0R_\tau W_0^{\mathsf T}.
}
\]

A certified finite cover of this compact transformed family is propagated through matrix concentration.

On Experiment AR,

\[
\tau\in[0.686875,0.8515625]\ \mathrm{s},
\qquad
\tau_0=0.76921875\ \mathrm{s},
\]

and the uniform scalar target covariance radius is

\[
\boxed{
\epsilon_{57}=0.8677117535<1.
}
\]

With calibration and target confidence both `0.975`, the combined lower bound is

\[
\boxed{0.950625}.
\]

This result is conditional on the declared separable Gaussian one-timescale exponential model and on calibration-target separation.

---

# 12. Returning covariance uncertainty to the moving observer problem

The original goal is not scalar covariance estimation. It is moving-boundary inference.

For a future candidate `S`, Proposition 58 defines the observer covariance block

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

For candidate count `C` and horizon `T`, the simultaneous target-indexed block count is

\[
\boxed{
B_{\mathrm{obs}}=TC.
}
\]

One such block contains the covariance submatrices required for the candidate's local information factors and every incoming transport edge.

Proposition 58 then propagates simultaneous relative covariance uncertainty through integration, insulation, persistence, transport, and the complete path objective without spending another probability budget.

Experiment AS reveals an important negative result. On the seven-coordinate benchmark,

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

At 118 residual innovation degrees of freedom, even the exact-`\tau` observer-scale matrix theorem gives

\[
\boxed{
\epsilon_{\mathrm{observer}}=1.8573569119>1.
}
\]

This shows that scalar covariance success does not automatically imply observer-scale certification. The current bottleneck is dimensional and structural.

[![Observer-scale covariance-to-world-tube audit](observer_bridge_dimension_audit.svg)](proposition_58_observer_bridge.md)

---

# 13. The theorem sequence as one physical measurement problem

The later theorem ladder should be read as one coherent sequence rather than isolated inequalities.

| Result | Mathematical step | Physical question |
| ---: | --- | --- |
| P41 | dependent Gaussian covariance concentration | How much independent information remains when measurements have memory? |
| P42 | mean-centered normalization | How does removing an unknown baseline change usable fluctuation information? |
| P43 | AR(1) calibration from increments | Can temporal persistence be learned rather than assumed? |
| P44 | nuisance-subspace projection | Can declared deterministic drift be removed without treating it as covariance? |
| P45 | estimated dependence plus nuisance projection | Can temporal-memory uncertainty and nuisance removal be handled together? |
| P46 | design-specific temporal geometry | Can the actual nuisance geometry replace a rank-only worst case? |
| P47 | direct Gaussian matrix concentration | Can the full covariance matrix be certified without a loose directional net? |
| P48 | uniform matrix bound over AR(1) uncertainty | Does the covariance guarantee remain valid when persistence is uncertain? |
| P49 | compact temporal-family cover | Can a whole admissible family of temporal kernels be certified? |
| P50 | two-parameter temporal calibration | Can persistence and fast uncorrelated variance be learned from independent calibration? |
| P51 | likelihood-ratio e-value confidence set | Can all calibration residuals define a finite-sample temporal parameter region? |
| P52 | certified outer cover and target composition | Can a continuum confidence set be propagated safely to an independent target theorem? |
| P53 | physical relaxation time + exact irregular-grid Markov structure | Can temporal dependence be parameterized in physical time rather than sampling units? |
| P53B | irregular-time finite-sample `\tau` calibration | Can physical relaxation time be calibrated directly on irregular timestamps? |
| P54 | two-scale physical-time cover | Can calibration resolution and target-cover resolution be separated? |
| P55 | local e-value slope and curvature | Can the finite-sample `\tau` outer cover be tightened without another probability budget? |
| P56 | exact innovation-whitened covariance | If `\tau` is known, can the local temporal law change the estimator and recover innovation degrees of freedom? |
| P57 | robust innovation whitening | How much of that gain survives finite-sample uncertainty in `\tau`? |
| P58 | covariance-to-world-tube bridge | Can measurement uncertainty be propagated back to the actual moving-boundary objective? |

The important point is that P41-P58 are **measurement-certification machinery supporting the observer-boundary problem**. They are not a separate theory of consciousness.

---

# 14. A complete physical reading of the pipeline

The project should be read from left to right.

## Step 1: choose physical observables

Specify what each coordinate measures, its units, sensor bandwidth, sampling interval, and spatial or functional location.

## Step 2: declare an effective dynamical model

Specify which couplings are represented by `A_t`, which unresolved processes are represented by `Q_t`, and over what timescale the linear approximation is intended to hold.

## Step 3: separate nuisance structure from stochastic fluctuations

Declare the nuisance design `H` before using the same record for stochastic inference.

## Step 4: characterize temporal memory in physical units

Estimate or constrain the family `R_\theta`, preferably using physical time when the model supports it.

## Step 5: certify fluctuation covariance

Use finite-sample matrix probability to bound how far `\widehat\Sigma` can be from the population covariance.

## Step 6: score candidate physical boundaries

Evaluate integration, insulation, persistence, and transport for each physically admissible candidate subsystem.

## Step 7: optimize the complete moving path

Infer `\mathcal W`, not each frame independently.

## Step 8: quantify ambiguity

Compare the best path with its strongest competitors. A small margin means the data do not strongly distinguish the proposed boundary.

## Step 9: test identifiability

Ask whether another physical model could produce the same observables while implying a different boundary. If so, passive observation alone cannot resolve the ambiguity.

## Step 10: only then discuss interpretation

A persistent, identifiable observer-like subsystem is still a dynamical structure. Any claim about consciousness requires additional bridge hypotheses and empirical evidence.

---

# 15. Concrete thought experiment

Consider a two-dimensional sensor grid measuring a fluctuating medium. A localized coherent pattern moves from left to right.

At one time the best-supported region may involve sensors

```text
(0,1,2)
```

then

```text
(1,2,3)
```

then

```text
(2,3,4).
```

A fixed-boundary analysis can miss persistence because it equates identity with permanent sensor membership.

The world-tube approach instead asks whether there is a changing path for which:

1. internal measurements predict one another strongly;
2. external measurements add comparatively limited predictive information;
3. the candidate predicts its own future organization;
4. predictive structure is transported into the next physical location;
5. the path remains separated from competitors after finite-sample uncertainty is included.

That is the operational physical problem the repository is solving.

---

# 16. Terminology that should not be over-interpreted

## Observer

A candidate persistent subsystem under the declared objective. It does not mean conscious subject by definition.

## World-tube

A time-indexed path of candidate coordinate sets. It is not automatically a relativistic spacetime construction.

## Action and action margin

An optimization objective and the difference between competing paths. It is not physical action in units of joule-seconds unless a future derivation establishes such a connection.

## Information

Statistical dependence in the declared probability model. It is not automatically thermodynamic entropy, free energy, causality, semantics, or subjective information.

## Integration

A declared statistical property of the candidate dynamics. It should not be equated with phenomenal unity without an additional tested hypothesis.

## Covariance eigenvalue

Variance along a collective fluctuation direction. It is not automatically energy.

---

# 17. Units and dimensional accountability

A physical application should state units explicitly.

- `X_t` carries the units of the measured observables.
- covariance carries squared observable units.
- `Q_t` carries covariance units.
- `A_t` maps units at one sample to units at the next and is dimensionless only when the coordinate convention permits it.
- `\tau` carries physical time units.
- correlation coefficients and canonical correlations are dimensionless.
- normalized covariance errors are dimensionless.
- mutual information is measured in bits in the implementation because the logarithms are base two.

If observables with different physical units are combined, coordinate scaling must be declared. A result that changes under arbitrary unit conversion without an explicit reason is physically suspect.

---

# 18. Physics accountability checklist

Before applying the framework to an experimental system, document all of the following.

## Observables

- What does each coordinate measure?
- What are its units?
- What is the sampling interval?
- What is the sensor bandwidth and filtering pipeline?
- Is the coordinate basis physically meaningful or chosen for convenience?

## Dynamics

- What physical interaction is represented by `A_t`?
- Over what time interval is linearization plausible?
- Which omitted mechanisms are absorbed into `Q_t`?
- Are there conservation laws or symmetries the fitted model should obey?

## Boundary geometry

- What makes a candidate coordinate set physically admissible?
- May membership change arbitrarily or only through local transport?
- Does the candidate family encode physical geometry or adjacency?

## Temporal statistics

- Is one exponential relaxation time adequate?
- Is the process stationary during the analyzed window?
- Are oscillations, long-memory effects, or multiple timescales visible?
- Do innovation residuals remain temporally correlated after whitening?

## Nuisance structure

- Which trends are removed?
- Were they declared before inspecting the same stochastic residuals?
- Could the projection remove genuine physical dynamics?

## Distributional assumptions

- Are Gaussian residuals a reasonable approximation?
- Is space-time covariance approximately separable when a theorem assumes separability?
- Are heavy tails or outliers strong enough to invalidate the Gaussian theorem being used?

## Validation

- Does the model reproduce held-out correlation structure?
- Does the inferred boundary survive changes in sampling rate, units, sensors, and coordinate representation?
- Does calibration transfer to the target population?
- Can an intervention distinguish the proposed subsystem from a competing boundary?

If these questions are not answered, the mathematics may still be correct for its stated model, but the physical interpretation remains incomplete.

---

# 19. Where the consciousness question enters, and where it does not

The present physics layer asks whether a persistent subsystem can be operationally identified from dynamical organization and finite measurements.

A consciousness interpretation requires substantially more. At minimum, a bridge would need to explain why particular observer-like dynamical properties should correspond to conscious properties and then produce predictions that distinguish that bridge from alternatives.

The repository therefore separates three statements:

1. **Mathematical statement:** a theorem follows from explicit assumptions.
2. **Physical statement:** an experimental system is adequately described by those assumptions and mapped observables.
3. **Consciousness statement:** an additional theory connects the physical structure to conscious experience.

Only the first is established by proof alone. The second requires physical validation. The third requires a separate scientific theory and evidence.

See the [Interpretation Protocol](interpretation_protocol.md) and [README Section 13](../README.md#13-relationship-to-tegmarks-observer-factorization-question).

---

# 20. Citation and provenance standard

Every important object in the repository should be identifiable as one of four types:

| Type | Meaning |
| --- | --- |
| External foundation | a standard concept, identity, distribution, or method from cited literature |
| Repository definition | a modeling or scoring choice introduced for this research program |
| Repository theorem | a mathematical statement proved in the repository under explicit assumptions |
| Controlled experiment | a reproducible numerical illustration or diagnostic; not a substitute for proof |

The citation rule is:

> **Cite conceptual lineage explicitly; identify repository definitions as definitions; identify repository theorems as repository results; cite external mathematical tools for the role they actually play; and never use a citation to imply endorsement.**

Use the [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md) for equation-level provenance and the [Bibliography and Citation Map](bibliography.md) for full references.

---

# 21. Recommended reading order

For a physics-first reading:

1. [Physics pipeline on the main page](../README.md#2-the-complete-physical-problem-in-one-picture)
2. this Physics Guide
3. [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md)
4. [Visual Research Guide](visual_research_guide.md)
5. [Research Overview](research_overview.md)
6. [Assumption Ledger](assumption_ledger.md)
7. [Bibliography and Citation Map](bibliography.md)
8. detailed proposition proofs only after the physical objects and assumptions are clear

The theorem pages should be read as certification layers supporting the physical inference pipeline, not as isolated equations.
