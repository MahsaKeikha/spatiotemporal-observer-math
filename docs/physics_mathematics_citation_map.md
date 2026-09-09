# Physics, mathematics, and citation map

This page is the compact equation-level provenance map for **Spatiotemporal Observer Mathematics**. Each major object is presented with four pieces of information: its physical interpretation, its mathematical definition, its source lineage, and the repository location where it is derived or verified.

The project begins from Max Tegmark's observer-factorization question and develops a time-dependent mathematical framework for dynamically inferred subsystem boundaries.

For complete references, see the [Bibliography and Citation Map](bibliography.md) and machine-readable [`references.bib`](../references.bib). For the full physical narrative, see the [Physics Guide](physics_guide.md).

---

# 1. Scientific question and moving subsystem

The central physical question is

> **If a coherent subsystem moves through the coordinates used to observe a larger physical system, when can its boundary be inferred from the dynamics rather than fixed in advance?**

The conceptual starting point is [Tegmark 2015](bibliography.md#tegmark-2015), which examines the observer-factorization problem and considers information, integration, independence, and dynamics as organizing principles.

The time-dependent objects studied here are

\[
\boxed{
S_t\subseteq\{1,\ldots,n\},
\qquad
\mathcal W=(S_0,S_1,\ldots,S_{T-1}).
}
\]

Here \(S_t\) is a candidate subsystem at time \(t\), and \(\mathcal W\) is its moving history, called an **observer world-tube** in this research program.

**Mathematical status:** repository definition motivated by the observer-factorization question.

**Verification:** [Derivations](derivations.md) | [README Section 13](../README.md#13-relationship-to-tegmarks-observer-factorization-question)

---

# 2. Physical observables and effective dynamics

The measured state is

\[
X_t=(X_t^{(1)},\ldots,X_t^{(n)}),
\]

with effective stochastic dynamics

\[
\boxed{
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t),
\qquad
\varepsilon_t\perp X_t.
}
\]

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

**Physical reading:** \(A_t\) is an effective one-step propagation operator in the declared measured coordinates; \(Q_t\) represents unresolved stochastic forcing within the model.

**Mathematical status:** declared observation model plus standard covariance propagation.

**Verification:** [Physics Guide](physics_guide.md) | [Derivations](derivations.md)

---

# 3. Gaussian information geometry

For a Gaussian vector \(Z\) of dimension \(k\),

\[
h(Z)=\frac{1}{2}\log_2\left[(2\pi e)^k\det\Sigma_Z\right].
\]

For subvectors \(X\) and \(Y\),

\[
\boxed{
I(X;Y)=\frac{1}{2}\log_2
\frac{\det\Sigma_X\det\Sigma_Y}{\det\Sigma_{XY}}.
}
\]

For conditioning vector \(Z\),

\[
\boxed{
I(X;Y\mid Z)=\frac{1}{2}\log_2
\frac{\det\Sigma_{XZ}\det\Sigma_{YZ}}
{\det\Sigma_Z\det\Sigma_{XYZ}}.
}
\]

**Physical reading:** these quantities describe statistical dependence and conditional predictive dependence in the declared Gaussian model.

**Lineage:** [Shannon 1948](bibliography.md#shannon-1948) and [Cover and Thomas 2006](bibliography.md#cover-and-thomas-2006).

**Mathematical status:** standard information-theoretic identities specialized to multivariate Gaussian variables.

---

# 4. Four operational subsystem factors

## 4.1 Internal integration

For a nontrivial bipartition \(S=U\sqcup V\), define

\[
J_t(U,V)
=
I(X_U^{t+1};X_V^t\mid X_U^t)
+
I(X_V^{t+1};X_U^t\mid X_V^t).
\]

The weakest directed internal cut is

\[
\boxed{
\mathcal J_t(S)
=
\frac{1}{|S|}
\min_{U\sqcup V=S}J_t(U,V),
}
\]

with normalized factor

\[
\boxed{
G_t(S)=1-2^{-\mathcal J_t(S)}.
}
\]

**Physical reading:** internal components contribute predictive information about one another across the time step after each side's own present is conditioned upon.

**Lineage:** information theory from [Shannon 1948](bibliography.md#shannon-1948) and [Cover and Thomas 2006](bibliography.md#cover-and-thomas-2006); conceptual integration context from [Tegmark 2015](bibliography.md#tegmark-2015), [Tegmark 2016](bibliography.md#tegmark-2016), and the integrated-information literature.

**Mathematical status:** repository operational definition.

## 4.2 Environmental insulation

Let \(\bar S\) denote measured coordinates outside \(S\). Define

\[
\boxed{
\mathcal L_t(S)
=
\frac{1}{|S|}
I(X_S^{t+1};X_{\bar S}^t\mid X_S^t)
}
\]

and

\[
\boxed{
K_t(S)=2^{-\mathcal L_t(S)}.
}
\]

**Physical reading:** once the candidate's present state is known, the measured exterior contributes comparatively limited additional prediction about the candidate's immediate future.

**Mathematical status:** repository operationalization of relative environmental independence.

## 4.3 Persistence

Define the whitened cross-covariance

\[
M=\Sigma_X^{-1/2}\operatorname{Cov}(X,Y)\Sigma_Y^{-1/2}.
\]

Let \(\rho_i\) be its singular values. Then

\[
\boxed{
P(X,Y)=\frac{1}{r}\sum_{i=1}^{r}\rho_i^2,
\qquad
r=\min(\dim X,\dim Y).
}
\]

For fixed candidate \(S\), use \(X=X_S^t\) and \(Y=X_S^{t+1}\).

**Physical reading:** collective fluctuation directions within the candidate retain predictive structure into the future.

**Lineage:** canonical correlation analysis from [Hotelling 1936](bibliography.md#hotelling-1936) and matrix analysis from [Bhatia 1997](bibliography.md#bhatia-1997).

**Mathematical status:** standard canonical-correlation geometry with the repository's averaging convention.

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

and

\[
\boxed{
\Theta_t(S\to R)
=
\sqrt{P_t(S\to R)\,2^{-L_t(S\to R)}}.
}
\]

**Physical reading:** predictive organization can persist while its support moves into different measured coordinates.

**Mathematical status:** repository definition built from information-theoretic and canonical-correlation ingredients.

---

# 5. Local candidate score and world-tube objective

The local score is

\[
\boxed{
\Omega_t(S)
=
\left[
G_t(S)K_t(S)P(X_S^t,X_S^{t+1})
\right]^{1/3}.
}
\]

For candidate family

\[
\mathcal C=\{S^{(1)},\ldots,S^{(C)}\}
\]

and path \(p=(j_0,\ldots,j_{T-1})\), define

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

**Physical reading:** the path rewards local dynamical organization and predictive transport while controlling abrupt changes in candidate membership.

**Lineage:** Jaccard geometry from [Jaccard 1901](bibliography.md#jaccard-1901); finite-horizon optimization through dynamic programming in the lineage of [Bellman 1952](bibliography.md#bellman-1952).

**Mathematical status:** repository world-tube objective using standard set geometry and dynamic-programming machinery.

The term `action margin` denotes the optimization margin between the best and runner-up paths throughout this work.

---

# 6. Exact path optimization and recovery margin

Let \(V_t(j)\) be the best partial-path objective ending at candidate \(j\) at time \(t\):

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

Backpointers recover the global optimum, and a two-best extension recovers the exact runner-up path.

If \(m\) denotes the population objective difference between the best and second-best paths, then \(m\) is the recovery margin used by the robustness theory.

**Lineage:** [Bellman 1952](bibliography.md#bellman-1952).

**Mathematical status:** standard dynamic-programming principle specialized to the repository objective, with repository runner-up and recovery constructions.

---

# 7. Finite-sample covariance certification

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

**Physical reading:** after normalization by the population fluctuation geometry, covariance distortion is controlled uniformly over collective directions.

When \(\epsilon<1\), the inverse-covariance perturbation arguments used by the information-factor bounds remain in their controlled regime.

**Lineage:** Gaussian covariance laws from [Wishart 1928](bibliography.md#wishart-1928), matrix concentration from [Tropp 2012](bibliography.md#tropp-2012), and perturbation tools from [Bhatia 1997](bibliography.md#bhatia-1997).

**Verification:** [Research Index](research_index.md) | [P47](proposition_47_weighted_wishart_matrix_chernoff.md)

---

# 8. Physical time and sampling-consistent temporal memory

The recent theorem sequence parameterizes temporal dependence by a physical relaxation time \(\tau\):

\[
\boxed{
K_\tau(t_i,t_j)
=
\exp\left(-\frac{|t_i-t_j|}{\tau}\right).
}
\]

Under uniform acquisition interval \(\Delta t\),

\[
\boxed{
\phi_{\Delta t}=e^{-\Delta t/\tau},
\qquad
\tau=-\frac{\Delta t}{\log\phi_{\Delta t}}.
}
\]

**Physical reading:** \(\tau\) remains the physical timescale while the one-step correlation changes with sampling interval.

**Lineage:** [Uhlenbeck and Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930) and Gaussian Markov-process context from [Doob 1942](bibliography.md#doob-1942).

**Mathematical status:** declared exponential temporal model with repository derivations in Proposition 53.

---

# 9. Exact irregular-grid innovation representation

For irregular adjacent gaps

\[
\Delta_i=t_{i+1}-t_i,
\qquad
\alpha_i=e^{-\Delta_i/\tau},
\]

Proposition 53 gives

\[
\boxed{
X_{i+1}
=
\alpha_iX_i+
\sqrt{1-\alpha_i^2}\,\varepsilon_i.
}
\]

The lower-bidiagonal temporal whitener satisfies

\[
\boxed{
W_\tau R_\tau W_\tau^{\mathsf T}=I,
\qquad
R_\tau^{-1}=W_\tau^{\mathsf T}W_\tau.
}
\]

**Physical reading:** the predictable exponential relaxation component is transformed into local innovation coordinates before covariance inference.

**Lineage:** stochastic-relaxation and Gaussian Markov context from [Uhlenbeck and Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930) and [Doob 1942](bibliography.md#doob-1942).

**Mathematical status:** repository theorem for the declared irregular-grid exponential covariance family.

---

# 10. Nuisance removal in temporal covariance geometry

For target model

\[
Y=HB+E,
\qquad
\operatorname{vec}(E)\sim\mathcal N(0,R_\tau\otimes\Gamma),
\]

innovation coordinates are

\[
Z=W_\tau Y,
\qquad
G=W_\tau H.
\]

With

\[
P_G=I-G(G^{\mathsf T}G)^{-1}G^{\mathsf T},
\]

Proposition 56 uses

\[
\boxed{
\widehat\Gamma_{\mathrm{IW}}
=
\frac{1}{N-q}Z^{\mathsf T}P_GZ.
}
\]

Under the stated Gaussian model,

\[
\boxed{
(N-q)\widehat\Gamma_{\mathrm{IW}}
\sim
\operatorname{Wishart}_d(\Gamma,N-q).
}
\]

**Physical reading:** deterministic nuisance modes are fitted after transformation into the temporal covariance geometry implied by the relaxation model.

**Lineage:** generalized least-squares context from [Aitken 1936](bibliography.md#aitken-1936) and Gaussian covariance law from [Wishart 1928](bibliography.md#wishart-1928).

**Mathematical status:** repository exact innovation and residual-Wishart construction.

---

# 11. Finite-sample physical-time calibration

The temporal calibration sequence uses likelihood-ratio e-values. For tested parameter \(\tau\), an e-value \(e_\tau\) satisfies

\[
\mathbb E_\tau[e_\tau]\le1.
\]

Markov's inequality gives a finite-sample test, and inversion produces a confidence set for \(\tau\).

**Lineage:** [Vovk and Wang 2021](bibliography.md#vovk-and-wang-2021), [Shafer 2021](bibliography.md#shafer-2021), and [Vovk and Wang 2023](bibliography.md#vovk-and-wang-2023).

**Repository development:** Propositions 51-55 specialize this methodology to the declared temporal families and construct certified outer covers for independent target inference.

---

# 12. Robust innovation inference under calibrated physical time

Proposition 57 chooses a calibration-derived working time \(\tau_0\) with whitener \(W_0\). For every admissible true \(\tau\), define

\[
\boxed{
C_\tau=W_0R_\tau W_0^{\mathsf T}.
}
\]

The transformed eigenvalue geometry is controlled by a deterministic operator cover. The projected normalization is controlled separately through

\[
\boxed{
d(\tau)=\operatorname{tr}(P_GC_\tau).
}
\]

For the exponential covariance family,

\[
\boxed{
\frac{\partial R_\tau(i,j)}{\partial\tau}
=
\frac{D_{ij}}{\tau^2}e^{-D_{ij}/\tau}.
}
\]

This gives the trace-specific Lipschitz certificate used in release 0.47.1.

On Experiment AR,

\[
\tau\in[0.686875,0.8515625]\ \mathrm{s},
\]

and the uniform scalar target radius is

\[
\boxed{
\epsilon_{57}=0.7195879984<1.
}
\]

**Mathematical status:** Proposition 57 with the 0.47.1 trace-cover tightening.

**Verification:** [P57](proposition_57_robust_innovation_whitening.md) | [AR JSON](robust_innovation_whitened_target.json) | [0.47.1 record](release_0_47_1.md)

---

# 13. Return from covariance uncertainty to the observer objective

For future candidate \(S\), Proposition 58 uses

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

For candidate count \(C\) and horizon \(T\), the simultaneous target-indexed block count is

\[
\boxed{
B_{\mathrm{obs}}=TC.
}
\]

Proposition 58 propagates simultaneous relative covariance radii through integration, insulation, persistence, transport, and the complete path objective on the same covariance event.

On Experiment AS, the current observer-scale exact-\(\tau\) concentration radius at 118 residual innovation degrees is

\[
\boxed{
\epsilon_{\mathrm{observer}}=1.8573569119>1.
}
\]

**Physical reading:** the present frontier is observer-scale dimension and structural propagation of covariance uncertainty through the full moving-boundary objective.

**Mathematical status:** repository deterministic composition theorem and controlled numerical diagnostic.

**Verification:** [P58](proposition_58_observer_bridge.md) | [AS JSON](observer_bridge_dimension_audit.json)

---

# 14. Provenance table for the core mathematical objects

| Object | Physical role | Mathematical status | Primary lineage | Repository location |
| --- | --- | --- | --- | --- |
| Observer-factorization question | why one subsystem decomposition is distinguished | conceptual starting point | [Tegmark 2015](bibliography.md#tegmark-2015) | [README Section 13](../README.md#13-relationship-to-tegmarks-observer-factorization-question) |
| \(S_t\), \(\mathcal W\) | moving subsystem boundary and history | repository definition | observer-factorization lineage | [Derivations](derivations.md) |
| Gaussian MI / CMI | predictive statistical dependence | standard identity | [Shannon 1948](bibliography.md#shannon-1948); [Cover and Thomas 2006](bibliography.md#cover-and-thomas-2006) | [Derivations](derivations.md#gaussian-information-quantities) |
| \(\mathcal J_t\), \(\mathcal L_t\) | internal integration and external leakage | repository operational definitions | information theory and integration lineage | [Derivations](derivations.md#internal-directed-integration) |
| canonical persistence | predictive continuity of collective modes | CCA ingredient with repository averaging | [Hotelling 1936](bibliography.md#hotelling-1936) | [Derivations](derivations.md#predictive-persistence) |
| \(\Theta_t\) | transport into changed coordinates | repository definition | information theory + CCA | [Derivations](derivations.md#transport-between-different-boundaries) |
| Jaccard continuity | membership continuity | standard set geometry | [Jaccard 1901](bibliography.md#jaccard-1901) | [Derivations](derivations.md#world-tube-objective) |
| dynamic program | global moving-path optimizer | standard algorithm specialized here | [Bellman 1952](bibliography.md#bellman-1952) | [Derivations](derivations.md#exact-dynamic-program) |
| Wishart covariance law | finite Gaussian covariance distribution | classical probability law | [Wishart 1928](bibliography.md#wishart-1928) | [P56](proposition_56_innovation_whitened_target.md) |
| matrix concentration | simultaneous covariance certification | standard method specialized here | [Tropp 2012](bibliography.md#tropp-2012) | [P47](proposition_47_weighted_wishart_matrix_chernoff.md) |
| e-value confidence set | finite-sample temporal calibration | statistical method specialized here | [Vovk and Wang 2021](bibliography.md#vovk-and-wang-2021) | [P51-P55](research_index.md) |
| exponential relaxation | sampling-consistent temporal model | declared model with repository derivations | [Uhlenbeck and Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930); [Doob 1942](bibliography.md#doob-1942) | [P53](proposition_53_physical_relaxation_time.md) |
| innovation nuisance removal | fit nuisance in temporal covariance geometry | classical lineage + repository construction | [Aitken 1936](bibliography.md#aitken-1936) | [P56](proposition_56_innovation_whitened_target.md) |
| robust transformed temporal family | uncertainty in \(\tau\) after whitening | repository theorem | Bhatia/Tropp matrix methodology | [P57](proposition_57_robust_innovation_whitening.md) |
| covariance-to-world-tube bridge | measurement uncertainty to path uncertainty | repository theorem | information, CCA, matrix, and DP foundations | [P58](proposition_58_observer_bridge.md) |

---

# 15. Claim classification

Every major statement in the repository is classified by mathematical role:

| Type | Meaning |
| --- | --- |
| **External foundation** | standard concept, identity, probability law, or method from cited literature |
| **Repository definition** | operational mathematical object introduced for this research program |
| **Repository theorem** | proved statement under explicit assumptions |
| **Controlled experiment** | reproducible numerical illustration or diagnostic tied to a declared model and parameter set |

This classification keeps source provenance and mathematical status visible throughout the documentation.

---

# 16. Citation standard

The attribution rule used throughout the project is:

> **Cite conceptual lineage explicitly; identify repository definitions as definitions; identify repository theorems through their proof records; and cite external mathematical tools at the point where they enter the derivation.**

The complete reference record is maintained in:

- [Bibliography and Citation Map](bibliography.md)
- [`references.bib`](../references.bib)
- [`CITATION.cff`](../CITATION.cff)

Primary conceptual citation:

**Max Tegmark. "Consciousness as a State of Matter." _Chaos, Solitons & Fractals_ 76 (2015): 238-270. DOI: 10.1016/j.chaos.2015.03.014.**

Repository-specific results should cite **Spatiotemporal Observer Mathematics** through [`CITATION.cff`](../CITATION.cff), together with the external method citation appropriate to the theorem being used.
