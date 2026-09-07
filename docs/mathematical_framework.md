# Mathematical framework

## 1. Starting point

The source framework studies a density matrix \(\rho\), a Hamiltonian \(H\), and candidate
factorizations

\[
\mathcal H \cong \mathcal H_S \otimes \mathcal H_E.
\]

For a chosen factorization, the Hamiltonian can be written as

\[
H = H_S \otimes I_E + I_S \otimes H_E + H_{SE}.
\]

Small interaction \(H_{SE}\) supports independence. Exact maximization of this
independence, however, can select an energy basis with no nontrivial dynamics.
This is the Quantum Zeno tension identified in the source paper.

## 2. Baseline classical model

Version 0.1 begins with a stationary Gaussian process

\[
X_{t+1}=AX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q),
\qquad
\rho(A)<1.
\]

Its stationary covariance is the solution of

\[
\Sigma=A\Sigma A^\mathsf{T}+Q.
\]

This model is deliberately modest. It lets us compute every information term
exactly before moving to nonlinear or quantum systems.

For candidate subsystem \(S\) and internal bipartition \(S=U\sqcup V\), define
bidirectional directed integration at lag \(\tau\):

\[
J_\tau(U,V)=
I(X^{t+\tau}_U;X^t_V\mid X^t_U)
+
I(X^{t+\tau}_V;X^t_U\mid X^t_V).
\]

The subsystem's directed integration is its weakest normalized internal cut:

\[
\mathcal J_\tau(S)=
\frac{1}{|S|}
\min_{U\sqcup V=S}J_\tau(U,V).
\]

Conditioning on each part's own present matters. It prevents common static
correlation from automatically counting as continuing internal organization.

Environmental leakage is

\[
\mathcal L_\tau(S)=
\frac{1}{|S|}
I(X^{t+\tau}_S;X^t_{\bar S}\mid X^t_S).
\]

The current bounded factors are

\[
G_\tau(S)=1-2^{-\mathcal J_\tau(S)},
\qquad
K_\tau(S)=2^{-\mathcal L_\tau(S)}.
\]

Predictive persistence \(P_\tau(S)\) is the mean squared canonical correlation
between \(X^t_S\) and \(X^{t+\tau}_S\). The fixed-boundary baseline score is

\[
\Omega_\tau(S)=
\left[G_\tau(S)K_\tau(S)P_\tau(S)\right]^{1/3}.
\]

This score is not proposed as a consciousness meter. It is a reproducible test
of three necessary properties for an observer-like process.

## 3. Nonstationary extension

For time-varying dynamics,

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\Sigma_{t+1}=A_t\Sigma_tA_t^\mathsf T+Q_t.
\]

No equilibrium covariance is assumed. For a source boundary \(S_t\) and target
boundary \(S_{t+1}\), define transport persistence by the mean squared canonical
correlations between \(X^t_{S_t}\) and \(X^{t+1}_{S_{t+1}}\):

\[
P_t(S_t\to S_{t+1})
=\frac{1}{r}\sum_{i=1}^{r}\rho_i^2,
\qquad r=\min(|S_t|,|S_{t+1}|).
\]

This quantity is invariant under any invertible linear reparameterization made
separately within the source and target representations. Transition leakage is

\[
L_t(S_t\to S_{t+1})
=\frac{1}{|S_{t+1}|}
I(X^{t+1}_{S_{t+1}};X^t_{\bar S_t}\mid X^t_{S_t}).
\]

The implemented bounded transition score is

\[
\Theta_t(S_t\to S_{t+1})
=\sqrt{P_t(S_t\to S_{t+1})2^{-L_t(S_t\to S_{t+1})}}.
\]

Unlike a coefficient-energy comparison, \(\Theta_t\) depends on the joint law
of the process and does not reward prediction imported from outside the source
boundary.

## 4. Proposed contribution: observer world-tubes

A fixed factorization assumes that the material or informational components of
an observer remain unchanged. That assumption is too strong for organisms,
adaptive machines, and changing representations.

Let \(\mathfrak F_{d,n}\) denote the space of factorizations with observer
dimension \(d\) inside total dimension \(n\). An identity candidate is a curve

\[
\gamma:t\mapsto F_t\in\mathfrak F_{d,n},
\]

not a single fixed factorization. In a discrete classical model, the analogous
object is a sequence of subsets \(S_0,S_1,\ldots,S_T\). Its spacetime support

\[
\mathcal W=\{(i,t):i\in S_t\}
\]

is an observer world-tube.

We propose to infer \(\mathcal W\) through a regularized variational objective:

\[
\mathcal A(\mathcal W)=
\sum_{t=0}^{T-\tau}
\left[
\alpha\Omega_t(S_t)
+\chi\Theta_t(S_t\to S_{t+\tau})
\right]
-\lambda\sum_{t=0}^{T-1}d_{\mathfrak F}(S_t,S_{t+1}).
\]

The local term jointly rewards directed integration, insulation, and predictive
persistence. The transition term rewards transport of an insulated
representation rather than retention of identical material components. The
final term is a geometric regularizer on movement through factorization space.

The quantum formulation replaces subset distance with a gauge-invariant metric
on a quotient of unitary space. A candidate form is

\[
\mathfrak F_{d,n}
\simeq
U(n) / \bigl(U(d)\otimes U(n/d)\bigr),
\]

with local changes of basis treated as gauge transformations. The horizontal
component of \(U_t^\dagger\dot U_t\) then measures genuine factorization drift,
while vertical motion represents a relabeling internal to observer or
environment.

This geometric statement is a research proposal, not yet a theorem. Establishing
the exact quotient, stabilizers, metric, and existence conditions is part of the
study.

## 5. Falsifiable hypotheses

1. On a system containing a coherent module that moves between physical nodes,
   world-tube optimization will recover the moving module while every fixed-cut
   method will fragment it.
2. Correlated but dynamically uncoupled controls will have nonzero static mutual
   information but near-zero directed integration.
3. Maximizing independence alone will favor dynamically trivial solutions, while
   the full action will retain nontrivial predictive dynamics.
4. In systems with no persistent organizational boundary, the inferred action
   will not contain a stable optimum across lags or regularization scales.

## 6. What remains to prove

- Invariance under coordinate changes that mix candidate and environment
  variables, and under local quantum gauge transformations.
- Bounds relating directed integration, entropy production, and autonomy time.
- Conditions for existence and uniqueness of a maximizing world-tube.
- Recovery guarantees for planted moving modules.
- Relationship to geometric integrated information, PhiID, dynamical
  independence, causal emergence, and computational mechanics.
