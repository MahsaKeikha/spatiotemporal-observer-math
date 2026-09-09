# Physics, mathematics, and citation map

This page is the compact scientific map for **Spatiotemporal Observer Mathematics**. It places the physical meaning, mathematical object, provenance, and verification route for the core equations in one place.

The project begins from Max Tegmark's observer-factorization question and develops an independent mathematical program for time-dependent subsystem boundaries. The repository does **not** claim that its world-tube objective, recovery theorems, or finite-sample certification results appear in Tegmark's work, and no endorsement is implied.

For full references, see the [Bibliography and Citation Map](bibliography.md) and machine-readable [`references.bib`](../references.bib). For interpretation limits, see the [Interpretation Protocol](interpretation_protocol.md).

---

# 1. Scientific question

The central physical question is

> **If a coherent subsystem moves through the coordinates used to observe a larger physical system, when can its boundary be inferred from the dynamics rather than fixed in advance?**

The conceptual starting point is [Tegmark 2015](bibliography.md#tegmark-2015), which asks why an observer should correspond to one factorization of the physical world rather than another and discusses information, integration, independence, and dynamics as organizing principles.

The mathematical extension studied here is explicit time dependence:

\[
S_t\subseteq\{1,\ldots,n\},
\qquad
\mathcal W=(S_0,S_1,\ldots,S_{T-1}).
\]

`S_t` is a candidate subsystem at time `t`; `\mathcal W` is its moving history, called an **observer world-tube** in this repository.

**Status:** repository definition motivated by the observer-factorization problem; not attributed to Tegmark as a theorem or construction.

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

Therefore

\[
\operatorname{Cov}
\begin{pmatrix}
X_t\\X_{t+1}
\end{pmatrix}
=
\begin{pmatrix}
\Sigma_t & \Sigma_tA_t^{\mathsf T}\\
A_t\Sigma_t & A_t\Sigma_tA_t^{\mathsf T}+Q_t
\end{pmatrix}.
\]

**Physical reading:** `A_t` is an effective one-step coupling or propagation operator in the chosen measured coordinates; `Q_t` is unresolved stochastic forcing represented by the model.

**Status:** repository observation model and standard covariance propagation identity. The repository does not claim that every physical system is fundamentally linear or Gaussian.

---

# 3. Gaussian information geometry

For a Gaussian vector `Z` of dimension `k`,

\[
h(Z)=\frac{1}{2}\log_2\left[(2\pi e)^k\det\Sigma_Z\right].
\]

For subvectors `X` and `Y`,

\[
\boxed{
I(X;Y)=\frac{1}{2}\log_2
\frac{\det\Sigma_X\det\Sigma_Y}{\det\Sigma_{XY}}.
}
\]

For conditioning vector `Z`,

\[
\boxed{
I(X;Y\mid Z)=\frac{1}{2}\log_2
\frac{\det\Sigma_{XZ}\det\Sigma_{YZ}}
{\det\Sigma_Z\det\Sigma_{XYZ}}.
}
\]

**Physical reading:** these quantities measure statistical dependence and conditional predictive dependence in the declared Gaussian model. They are not automatically thermodynamic entropy, energy, causality, semantic information, or consciousness.

**Lineage:** [Shannon 1948](bibliography.md#shannon-1948) and [Cover and Thomas 2006](bibliography.md#cover-and-thomas-2006).

---

# 4. Four operational subsystem factors

The observer score is built from four distinct ideas. Each has a physical reading and a mathematical definition.

## 4.1 Internal integration

For nontrivial bipartition `S=U\sqcup V`, define

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
\min_{U\sqcup V=S}J_t(U,V).
}
\]

The normalized integration factor is

\[
\boxed{
G_t(S)=1-2^{-\mathcal J_t(S)}.
}
\]

**Physical reading:** internal components add predictive information about one another's future after each side's own present is known.

**Lineage:** information theory from [Shannon 1948](bibliography.md#shannon-1948) and [Cover and Thomas 2006](bibliography.md#cover-and-thomas-2006); integration as conceptual background from [Tegmark 2015](bibliography.md#tegmark-2015), [Tegmark 2016](bibliography.md#related-tegmark-work-tegmark-2016), and the integrated-information literature. The particular directed minimum-cut score is a repository definition.

## 4.2 Environmental insulation

Let `\bar S` denote measured coordinates outside `S`. Define leakage

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

**Physical reading:** after the candidate's own present is known, the external measured coordinates add comparatively limited predictive information about its immediate future.

**Status:** repository operationalization of relative environmental independence; it does not require thermodynamic isolation.

## 4.3 Persistence

For vectors `X` and `Y`, define the whitened cross-covariance

\[
M=\Sigma_X^{-1/2}\operatorname{Cov}(X,Y)\Sigma_Y^{-1/2}.
\]

Let `\rho_i` be its singular values. Then

\[
\boxed{
P(X,Y)=\frac{1}{r}\sum_{i=1}^{r}\rho_i^2,
\qquad
r=\min(\dim X,\dim Y).
}
\]

For fixed candidate `S`, use `X=X_S^t` and `Y=X_S^{t+1}`.

**Physical reading:** collective fluctuation directions in the candidate survive predictively into its future.

**Lineage:** canonical correlation analysis from [Hotelling 1936](bibliography.md#hotelling-1936); matrix analysis from [Bhatia 1997](bibliography.md#bhatia-1997). The averaging convention is a repository modeling choice.

## 4.4 Transport

For source `S` at time `t` and target `R` at time `t+1`,

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

**Physical reading:** a coherent organization may move into different measured coordinates while preserving predictive structure and remaining comparatively insulated from the rest of the measured system.

**Status:** repository definition built from information-theoretic and canonical-correlation ingredients.

---

# 5. Local candidate score and moving world-tube objective

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

and path `p=(j_0,\ldots,j_{T-1})`, the world-tube objective is

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

**Physical reading:** the path rewards local dynamical organization and predictive transport while weakly penalizing discontinuous membership jumps.

**Lineage:** Jaccard geometry from [Jaccard 1901](bibliography.md#jaccard-1901); exact finite-horizon optimization uses dynamic programming in the lineage of [Bellman 1952](bibliography.md#bellman-1952). The complete objective and its weights are repository definitions.

The term `action` is an optimization name. It is **not** physical action in joule-seconds.

---

# 6. Exact path optimization and recovery margin

Define `V_t(j)` as the best partial-path objective ending at candidate `j` at time `t`:

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

Backpointers recover the global optimum. A two-best extension recovers the exact runner-up path.

If `m` is the population objective difference between the best and second-best paths, then `m` is an **optimization margin** used for robustness and recovery analysis.

**Lineage:** [Bellman 1952](bibliography.md#bellman-1952). The runner-up and recovery constructions are repository results.

---

# 7. Finite-sample covariance certification

Many downstream information quantities depend on covariance blocks. The central relative covariance event is

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

**Physical reading:** after normalization by the population fluctuation geometry, every collective direction is distorted by at most `\epsilon` in operator norm.

When `\epsilon<1`, inverse covariance and conditional-information perturbation arguments remain in a controlled regime. The value one is a mathematical threshold, not a physical phase transition.

**Lineage:** Gaussian covariance laws trace to [Wishart 1928](bibliography.md#wishart-1928); matrix concentration uses [Tropp 2012](bibliography.md#tropp-2012) and matrix-analysis tools from [Bhatia 1997](bibliography.md#bhatia-1997). Earlier Gaussian concentration also uses sources mapped in the [Bibliography](bibliography.md#gaussian-concentration-and-random-matrix-foundations).

---

# 8. Physical time and sampling-consistent temporal memory

A discrete AR(1) coefficient depends on sampling interval. To keep the temporal parameter physical, the recent theorem chain uses

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

**Physical reading:** `\tau` is the declared relaxation time; the one-step correlation changes when acquisition rate changes.

**Lineage:** [Uhlenbeck and Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930) and Gaussian Markov-process context from [Doob 1942](bibliography.md#doob-1942). Proposition 53 derives the exact formulas used by the repository directly from the declared exponential covariance kernel.

---

# 9. Exact irregular-grid innovation representation

For irregular adjacent gaps

\[
\Delta_i=t_{i+1}-t_i,
\qquad
\alpha_i=e^{-\Delta_i/\tau},
\]

the declared model has the transition representation

\[
\boxed{
X_{i+1}
=
\alpha_iX_i+
\sqrt{1-\alpha_i^2}\,\varepsilon_i.
}
\]

Proposition 53 constructs a lower-bidiagonal matrix `W_\tau` such that

\[
\boxed{
W_\tau R_\tau W_\tau^{\mathsf T}=I,
\qquad
R_\tau^{-1}=W_\tau^{\mathsf T}W_\tau.
}
\]

**Physical reading:** predictable exponential relaxation is converted into local innovations before covariance estimation.

**Lineage:** historical stochastic-process context from [Uhlenbeck and Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930) and [Doob 1942](bibliography.md#doob-1942). The irregular-grid whitening identities used here are proved in Proposition 53.

---

# 10. Nuisance removal in the correct temporal geometry

For target model

\[
Y=HB+E,
\qquad
\operatorname{vec}(E)\sim\mathcal N(0,R_\tau\otimes\Gamma),
\]

exact innovation coordinates are

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

Under its exact Gaussian assumptions,

\[
\boxed{
(N-q)\widehat\Gamma_{\mathrm{IW}}
\sim
\operatorname{Wishart}_d(\Gamma,N-q).
}
\]

**Physical reading:** fit the declared deterministic nuisance modes after transforming the measurements into the temporal covariance geometry implied by the physical relaxation model.

**Lineage:** generalized least-squares context from [Aitken 1936](bibliography.md#aitken-1936), exact Gaussian covariance law from [Wishart 1928](bibliography.md#wishart-1928). The local innovation implementation and exact reduction are repository results.

---

# 11. Finite-sample physical-time calibration

The repository uses likelihood-ratio e-values to obtain a finite-sample confidence set for physical relaxation time `\tau` on an independent calibration record.

The statistical principle is that an e-value `e_\tau` is nonnegative and satisfies

\[
\mathbb E_\tau[e_\tau]\le1
\]

under the tested parameter. Markov's inequality then yields a finite-sample test, and inversion yields a confidence set.

**Lineage:** [Vovk and Wang 2021](bibliography.md#vovk-and-wang-2021), [Shafer 2021](bibliography.md#shafer-2021), and [Vovk and Wang 2023](bibliography.md#vovk-and-wang-2023).

**Repository development:** Propositions 51 through 55 adapt this machinery to the declared temporal models and construct certified finite outer covers for independent target inference.

---

# 12. Robust innovation inference under calibrated physical time

Proposition 57 chooses one calibration-derived working time `\tau_0` with whitener `W_0`. For every still-admissible true `\tau`, define

\[
\boxed{
C_\tau=W_0R_\tau W_0^{\mathsf T}.
}
\]

A deterministic cover of this compact transformed covariance family is propagated through the matrix concentration theorem.

On Experiment AR,

\[
\tau\in[0.686875,0.8515625]\ \mathrm{s},
\]

and the uniform scalar target radius is

\[
\boxed{
\epsilon_{57}=0.8677117535<1.
}
\]

**Status:** repository theorem and controlled numerical benchmark. It is conditional on the declared separable Gaussian one-timescale exponential model and calibration-target separation.

---

# 13. Return from covariance uncertainty to the observer objective

For future candidate `S`, Proposition 58 uses the observer covariance block

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

For candidate count `C` and horizon `T`, the required simultaneous target-indexed block count is

\[
\boxed{
B_{\mathrm{obs}}=TC.
}
\]

Proposition 58 deterministically propagates simultaneous relative covariance radii through integration, insulation, persistence, transport, and the complete path objective without spending another probability budget.

Experiment AS shows an important negative result: scalar covariance success does not automatically imply observer-scale certification. On the controlled benchmark,

\[
\boxed{
\epsilon_{\mathrm{observer}}=1.8573569119>1
}
\]

at 118 residual innovation degrees of freedom for the current matrix theorem.

**Physical reading:** the current bottleneck is observer-scale dimension and structural worst-case propagation, not another refinement of physical-time calibration.

---

# 14. Provenance table for the core mathematical objects

| Object | Physical role | Mathematical status | Primary lineage | Repository location |
| --- | --- | --- | --- | --- |
| Observer-factorization question | why one subsystem decomposition is distinguished | conceptual starting point | [Tegmark 2015](bibliography.md#tegmark-2015) | [README §13](../README.md#13-relationship-to-tegmarks-observer-factorization-question) |
| `S_t`, `\mathcal W` | moving subsystem boundary and history | repository definition | Tegmark-inspired question | [Derivations](derivations.md) |
| Gaussian MI / CMI | predictive statistical dependence | standard identity | [Shannon 1948](bibliography.md#shannon-1948); [Cover & Thomas 2006](bibliography.md#cover-and-thomas-2006) | [Derivations §2](derivations.md#gaussian-information-quantities) |
| `\mathcal J_t`, `\mathcal L_t` | internal integration and external leakage | repository operational definitions | information-theory lineage | [Derivations §§3-4](derivations.md#internal-directed-integration) |
| canonical persistence | predictive continuity of collective modes | standard CCA ingredient + repository averaging | [Hotelling 1936](bibliography.md#hotelling-1936) | [Derivations §5](derivations.md#predictive-persistence) |
| `\Theta_t` | transport into changed coordinates | repository definition | information theory + CCA | [Derivations §6](derivations.md#transport-between-different-boundaries) |
| Jaccard continuity | weak material continuity | standard set geometry used by repository | [Jaccard 1901](bibliography.md#jaccard-1901) | [Derivations §7](derivations.md#world-tube-objective) |
| dynamic program | global moving-path optimizer | standard algorithmic principle + repository score | [Bellman 1952](bibliography.md#bellman-1952) | [Derivations §8](derivations.md#exact-dynamic-program) |
| Wishart covariance law | finite Gaussian covariance distribution | classical result | [Wishart 1928](bibliography.md#wishart-1928) | [P56](proposition_56_innovation_whitened_target.md) |
| matrix concentration | simultaneous covariance certificate | standard method specialized in repository | [Tropp 2012](bibliography.md#tropp-2012) | [P47](proposition_47_weighted_wishart_matrix_chernoff.md) |
| e-value confidence set | finite-sample temporal calibration | modern statistical method specialized in repository | [Vovk & Wang 2021](bibliography.md#vovk-and-wang-2021) | [P51-P55 map](research_index.md) |
| exponential relaxation | sampling-consistent physical temporal model | declared model with repository derivations | [Uhlenbeck & Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930); [Doob 1942](bibliography.md#doob-1942) | [P53](proposition_53_physical_relaxation_time.md) |
| GLS/innovation nuisance removal | fit nuisance in temporal covariance geometry | classical lineage + repository local construction | [Aitken 1936](bibliography.md#aitken-1936) | [P56](proposition_56_innovation_whitened_target.md) |
| covariance-to-world-tube bridge | convert measurement uncertainty to path uncertainty | repository theorem | matrix perturbation background [Bhatia 1997](bibliography.md#bhatia-1997) | [P58](proposition_58_observer_bridge.md) |

---

# 15. How to read claims correctly

Every important statement in the repository should be classifiable as one of four types:

| Type | Meaning |
| --- | --- |
| **External foundation** | a standard idea, identity, or method taken from cited literature |
| **Repository definition** | a modeling or scoring choice introduced for this research program |
| **Repository theorem** | a proved mathematical statement under explicit assumptions |
| **Controlled experiment** | a reproducible numerical illustration or diagnostic; not a substitute for proof |

This classification is essential for professional attribution. A citation to an external source never implies that the source contains the repository's later theorem, and a repository theorem never implies that the declared physical model is universally correct.

---

# 16. Citation standard

Use the following attribution rule throughout the project:

> **Cite conceptual lineage explicitly; identify repository definitions as definitions; identify repository theorems as original results in this codebase; cite external mathematical tools for the role they actually play; and never use a citation to imply endorsement.**

The complete reference record is maintained in:

- [Bibliography and Citation Map](bibliography.md)
- [`references.bib`](../references.bib)
- [`CITATION.cff`](../CITATION.cff)

For the primary conceptual source, use:

**Max Tegmark. "Consciousness as a State of Matter." _Chaos, Solitons & Fractals_ 76 (2015): 238-270. DOI: 10.1016/j.chaos.2015.03.014.**

For repository results, cite **Spatiotemporal Observer Mathematics** using [`CITATION.cff`](../CITATION.cff), together with the external method citation appropriate to the theorem being used.
