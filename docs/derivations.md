# Derivations and computational definitions

This note fixes the notation used by the code. All random variables are real,
all logarithms in information quantities are base two, and covariance matrices
are assumed positive definite unless a limiting argument is stated.

## 1. Time-varying Gaussian dynamics

Let \(X_t\in\mathbb R^n\) obey

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t),
\qquad
\varepsilon_t\perp X_t.
\]

If \(\Sigma_t=\operatorname{Cov}(X_t)\), then

\[
\Sigma_{t+1}=A_t\Sigma_tA_t^\mathsf T+Q_t,
\qquad
\operatorname{Cov}(X_t,X_{t+1})=\Sigma_tA_t^\mathsf T.
\]

Thus the adjacent-time joint covariance is

\[
\Gamma_t=
\begin{pmatrix}
\Sigma_t & \Sigma_tA_t^\mathsf T\\
A_t\Sigma_t & \Sigma_{t+1}
\end{pmatrix}.
\]

Nothing in this recursion requires \(A_t\) or \(Q_t\) to be constant. The
stationary helper in the package is used only when a fixed model is explicitly
requested or when an initial covariance is needed.

## 2. Gaussian information quantities

For a Gaussian vector \(Z\in\mathbb R^k\) with covariance \(\Sigma_Z\),

\[
h(Z)=\frac{1}{2}\log_2\left[(2\pi e)^k\det\Sigma_Z\right].
\]

The constants cancel in mutual information. For subvectors \(X\) and \(Y\),

\[
I(X;Y)=\frac{1}{2}\log_2
\frac{\det\Sigma_X\det\Sigma_Y}{\det\Sigma_{XY}}.
\]

For a conditioning vector \(Z\),

\[
I(X;Y\mid Z)=\frac{1}{2}\log_2
\frac{
\det\Sigma_{XZ}\det\Sigma_{YZ}
}{
\det\Sigma_Z\det\Sigma_{XYZ}
}.
\]

The implementation evaluates log determinants from eigenvalues rather than
forming determinants directly. Eigenvalues below
\(10^{-12}\max(1,\lambda_{\max})\) are floored. This prevents numerical failure
near singularity, but it also means results for badly conditioned covariances
must be treated as regularized quantities.

## 3. Internal directed integration

Take a candidate subsystem \(S\subset\{0,\ldots,n-1\}\). For every nontrivial
bipartition \(S=U\sqcup V\), define

\[
J_t(U,V)=
I(X^{t+1}_U;X^t_V\mid X^t_U)
+I(X^{t+1}_V;X^t_U\mid X^t_V).
\]

Each term asks whether one side improves prediction of the other side's future
after that side's own present is known. The weakest internal cut is

\[
\mathcal J_t(S)=\frac{1}{|S|}
\min_{U\sqcup V=S}J_t(U,V).
\]

Only one of the two labelings \((U,V)\) and \((V,U)\) is evaluated. The search is
exponential in \(|S|\), which is acceptable for the small exact examples here
but not for large systems. A singleton has no nontrivial bipartition and is
assigned zero directed integration.

For comparison, the code also records the weakest instantaneous mutual
information,

\[
\mathcal I_t(S)=\frac{1}{|S|}
\min_{U\sqcup V=S}I(X^t_U;X^t_V).
\]

This static value is diagnostic only. It does not enter the final score.

## 4. Environmental leakage

Let \(\bar S\) be the variables outside \(S\). The fixed-boundary leakage is

\[
\mathcal L_t(S)=\frac{1}{|S|}
I(X^{t+1}_S;X^t_{\bar S}\mid X^t_S).
\]

It measures predictive input from the current environment that is not already
contained in the subsystem's present. It does not measure every possible form
of dependence on the environment. In particular, it ignores future-to-future
coupling and latent variables not represented in \(X_t\).

The two information rates are mapped to \([0,1]\):

\[
G_t(S)=1-2^{-\mathcal J_t(S)},
\qquad
K_t(S)=2^{-\mathcal L_t(S)}.
\]

The first map increases from zero with integration. The second decreases from
one with leakage. Their exponential forms keep the units explicit: one bit per
node maps to \(1/2\) in either direction.

## 5. Predictive persistence

Let \(C_{XY}=\operatorname{Cov}(X,Y)\). The canonical correlations between
vectors \(X\) and \(Y\) are the singular values of

\[
M=\Sigma_X^{-1/2}C_{XY}\Sigma_Y^{-1/2}.
\]

If \(r=\min(\dim X,\dim Y)\), define

\[
P(X,Y)=\frac{1}{r}\sum_{i=1}^r\rho_i^2.
\]

For a fixed boundary, \(X=X_S^t\) and \(Y=X_S^{t+1}\). Canonical correlations
are unchanged by invertible linear coordinate transformations made separately
inside \(X\) and \(Y\). This is why the code uses them instead of a Euclidean
difference between covariance entries or transition coefficients.

The local score is the geometric mean

\[
\Omega_t(S)=\left[G_t(S)K_t(S)P(X_S^t,X_S^{t+1})\right]^{1/3}.
\]

The geometric mean makes any zero factor decisive and keeps the score in
\([0,1]\). The equal exponents are a modeling choice, not a theorem. They should
eventually be tested against weighted alternatives.

## 6. Transport between different boundaries

For source \(S\) at time \(t\) and target \(R\) at time \(t+1\), transport
persistence is

\[
P_t(S\to R)=P(X_S^t,X_R^{t+1}).
\]

The corresponding leakage is conditioned on the entire source representation:

\[
L_t(S\to R)=\frac{1}{|R|}
I(X_R^{t+1};X_{\bar S}^t\mid X_S^t).
\]

The implemented transition score is

\[
\Theta_t(S\to R)=
\sqrt{P_t(S\to R)\,2^{-L_t(S\to R)}}.
\]

A high canonical correlation is therefore insufficient when the same future
target is substantially predicted by variables outside the proposed source.
This definition is directional: \(\Theta_t(S\to R)\) need not equal
\(\Theta_t(R\to S)\), and the reverse expression generally refers to a
different pair of times.

The package retains `structural_transport` as a transparent coefficient-based
baseline. It is coordinate dependent and is not used in the reported
nonstationary experiment.

## 7. World-tube objective

Let \(\mathcal C=\{S^{(1)},\ldots,S^{(C)}\}\) be a finite candidate set. A path
is \(p=(j_0,\ldots,j_{T-1})\), where \(j_t\) selects one candidate at time \(t\).
For local weight one, transport weight \(\chi\), and continuity weight
\(\lambda\), the discrete action is

\[
A(p)=
\sum_{t=0}^{T-1}\Omega_t(S^{(j_t)})
+\chi\sum_{t=0}^{T-2}\Theta_t(S^{(j_t)}\to S^{(j_{t+1})})
-\lambda\sum_{t=0}^{T-2}d_J(S^{(j_t)},S^{(j_{t+1})}),
\]

where

\[
d_J(S,R)=1-\frac{|S\cap R|}{|S\cup R|}
\]

is Jaccard distance. This regularizer expresses a weak preference for material
continuity without requiring permanent membership.

## 8. Exact dynamic program

Define \(V_t(j)\) as the best action of a partial path ending at candidate \(j\)
at time \(t\). Then

\[
V_0(j)=\Omega_0(S^{(j)}),
\]

and

\[
V_t(j)=\Omega_t(S^{(j)})+
\max_i\left[
V_{t-1}(i)+\chi\Theta_{t-1}(S^{(i)}\to S^{(j)})
-\lambda d_J(S^{(i)},S^{(j)})
\right].
\]

Backpointers recover the global optimum. The runtime is \(O(TC^2)\); exhaustive
enumeration would require \(C^T\) paths. The certificate routine keeps the best
two distinct partial histories ending at every candidate, which is sufficient
to recover the exact global runner-up with the same asymptotic complexity.

## 9. Robustness certificate

Let \(m\) be the action difference between the best and second-best paths. If
every local and raw transport score is perturbed by at most \(\epsilon\), the
action of a path can change by at most

\[
B\epsilon=\left[T+|\chi|(T-1)\right]\epsilon.
\]

The difference between two paths can therefore change by at most
\(2B\epsilon\). The winning path is certified unchanged whenever

\[
\epsilon<\frac{m}{2[T+|\chi|(T-1)]}.
\]

This bound concerns errors in already-computed scores. Turning it into a
confidence statement about finite data requires a separate perturbation bound
from estimated covariances to information scores.

## 10. Choices that are still choices

Several parts of the construction are intentionally exposed rather than hidden
inside the implementation:

- the minimum bipartition rather than an average or soft minimum
- per-node normalization
- the exponential maps from bits to bounded factors
- equal weighting inside each geometric mean
- Jaccard distance for physical membership
- a finite, fixed-size candidate family

Changing any of them defines a related but different model. A useful extension
must show which conclusions survive those changes.
