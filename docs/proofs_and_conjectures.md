# Proved results and open problems

The first seven statements below are consequences of the current definitions.
The remaining statements are targets. They are not used as assumptions in the
reported experiments.

## Proposition 1: nonstationary adjacent covariance

Let

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t),
\qquad
\varepsilon_t\perp X_t,
\]

and let \(\operatorname{Cov}(X_t)=\Sigma_t\). Then

\[
\operatorname{Cov}\!\begin{pmatrix}X_t\\X_{t+1}\end{pmatrix}
=
\begin{pmatrix}
\Sigma_t & \Sigma_tA_t^\mathsf T\\
A_t\Sigma_t & A_t\Sigma_tA_t^\mathsf T+Q_t
\end{pmatrix}.
\]

**Proof.** Linearity and independence give
\(\operatorname{Cov}(X_t,A_tX_t+\varepsilon_t)=\Sigma_tA_t^\mathsf T\).
The lower-right block follows from covariance additivity for independent
summands. The lower-left block is the transpose. This also proves the recursion
\(\Sigma_{t+1}=A_t\Sigma_tA_t^\mathsf T+Q_t\). \(\square\)

## Proposition 2: representation invariance of canonical transport

Let \(X\) and \(Y\) have nonsingular covariances. Define their canonical
correlations as the singular values of

\[
C=\Sigma_X^{-1/2}\Sigma_{XY}\Sigma_Y^{-1/2}.
\]

For any invertible maps \(R\) and \(T\), replacing \(X\) by \(RX\) and \(Y\)
by \(TY\) leaves the canonical correlations unchanged.

**Proof.** The squared canonical correlations are the generalized
eigenvalues of

\[
\Sigma_{XY}\Sigma_Y^{-1}\Sigma_{YX}v
=\rho^2\Sigma_Xv.
\]

Write \(X'=RX\) and \(Y'=TY\). Their covariance blocks are

\[
\Sigma_{X'}=R\Sigma_XR^\mathsf T,
\quad
\Sigma_{Y'}=T\Sigma_YT^\mathsf T,
\quad
\Sigma_{X'Y'}=R\Sigma_{XY}T^\mathsf T.
\]

Using invertibility of \(T\), the left matrix in the transformed generalized
eigenproblem reduces to

\[
\Sigma_{X'Y'}\Sigma_{Y'}^{-1}\Sigma_{Y'X'}
=R\Sigma_{XY}\Sigma_Y^{-1}\Sigma_{YX}R^\mathsf T.
\]

Set \(v'=R^{-\mathsf T}v\). Multiplying the original generalized eigenvalue
equation by \(R\) shows

\[
\Sigma_{X'Y'}\Sigma_{Y'}^{-1}\Sigma_{Y'X'}v'
=\rho^2\Sigma_{X'}v'.
\]

The transformed problem therefore has the same generalized eigenvalues
\(\rho^2\), including multiplicity. Its canonical correlations and their mean
square are unchanged. \(\square\)

This is a block-coordinate invariance result. It is not yet invariance under an
arbitrary mixing of observer and environment coordinates.

## Proposition 3: bounded transport score

Define

\[
P(S\to T)=\frac{1}{r}\sum_{i=1}^{r}\rho_i^2,
\qquad
K(S\to T)=2^{-I(X_T^{t+1};X_{\bar S}^{t}\mid X_S^t)/|T|},
\]

where \(r=\min(|S|,|T|)\). Then

\[
\Theta(S\to T)=\sqrt{P(S\to T)K(S\to T)}\in[0,1].
\]

**Proof.** Canonical correlations lie in \([0,1]\), so their mean square lies
in \([0,1]\). Conditional mutual information is nonnegative, so \(K\in(0,1]\).
The result follows by closure of \([0,1]\) under multiplication and square
root. \(\square\)

## Proposition 4: finite-horizon path robustness certificate

Let a path \(p=(j_0,\ldots,j_{T-1})\) have action

\[
A(p)=\sum_{t=0}^{T-1}\ell_t(j_t)
+\chi\sum_{t=0}^{T-2}\theta_t(j_t,j_{t+1})
-\lambda\sum_{t=0}^{T-2}d(j_t,j_{t+1}).
\]

Suppose the unique maximizing path has margin \(m>0\) over the exact runner-up.
If every local score and every raw transport score is perturbed in absolute
value by at most \(\epsilon\), while distances and weights remain fixed, the
maximizer cannot change whenever

\[
\epsilon < \frac{m}{2[T+|\chi|(T-1)]}.
\]

**Proof.** The action of any one path changes by at most
\(B\epsilon=[T+|\chi|(T-1)]\epsilon\). Therefore the difference between the
winning path and any competitor changes by at most \(2B\epsilon\). If
\(2B\epsilon<m\), every perturbed difference remains positive. \(\square\)

The implementation obtains the exact runner-up using a two-best dynamic program
with \(O(TC^2)\) time for \(C\) candidates. The reported radius is conservative:
it protects against all simultaneous bounded entrywise perturbations, including
the worst possible sign pattern.

## Proposition 5: componentwise planted-path recovery

For candidate indices \(j_0^*,\ldots,j_{T-1}^*\), write

\[
e_t(i,j)=\ell_t(j)+\chi\theta_{t-1}(i,j)-\lambda d(i,j),
\qquad t\geq 1.
\]

Define the initial and edge margins

\[
\delta_0=\ell_0(j_0^*)-\max_{j\neq j_0^*}\ell_0(j)
\]

and

\[
\delta_t=e_t(j_{t-1}^*,j_t^*)
-\max_{(i,j)\neq(j_{t-1}^*,j_t^*)}e_t(i,j).
\]

If every \(\delta_t>0\), the planted path is the unique global maximizer and
its action margin is at least \(\min_t\delta_t\).

**Proof.** The path action decomposes into one initial term and \(T-1\) edge
terms. By assumption, the planted path maximizes every term separately. Any
distinct path must differ either at its initial state or on at least one edge.
It therefore loses at least the corresponding positive component margin and
cannot gain on any other component. \(\square\)

This condition is sufficient, not necessary. The committed moving-module
example has the correct unique global optimum but fails the componentwise test,
with minimum component margin `-0.046147`. In that example, smaller losses and
gains cancel across time in favor of the complete planted path.

## Proposition 6: finite-sample recovery from uniform score bounds

Suppose a population action has unique maximizing path \(p^*\) with margin
\(m>0\), with candidate distances and action weights held fixed. Let estimated
local and transport scores obey, jointly with probability at least
\(1-\alpha\),

\[
\max_{t,j}|\widehat\ell_t(j)-\ell_t(j)|\leq\epsilon_L,
\qquad
\max_{t,i,j}|\widehat\theta_t(i,j)-\theta_t(i,j)|\leq\epsilon_\Theta.
\]

If

\[
m>2\left[T\epsilon_L+|\chi|(T-1)\epsilon_\Theta\right],
\]

then the empirical maximizer equals \(p^*\) with probability at least
\(1-\alpha\).

**Proof.** On the stated joint event, the action error of any path is at most

\[
B=T\epsilon_L+|\chi|(T-1)\epsilon_\Theta.
\]

The empirical action difference between \(p^*\) and any competitor can be at
most \(2B\) smaller than its population difference. Since every population
difference is at least \(m>2B\), every empirical difference remains positive.
The joint event occurs with probability at least \(1-\alpha\). \(\square\)

This proposition reduces statistical recovery to uniform concentration of the
score arrays. It does not itself supply \(\epsilon_L\), \(\epsilon_\Theta\), or
\(\alpha\). Deriving those quantities from Gaussian sample-covariance
concentration is still open.

## Proposition 7: covariance perturbation bound for Gaussian CMI

Let \(\Gamma\) be positive definite with
\(\lambda_{\min}(\Gamma)\geq m>0\), and let
\(\widehat\Gamma=\Gamma+E\) satisfy
\(\|E\|_2\leq\eta<m\). For Gaussian subvectors of dimensions \(d_X,d_Y,d_Z\),

\[
\left|
\widehat I(X;Y\mid Z)-I(X;Y\mid Z)
\right|
\leq
\frac{d_X+d_Y+2d_Z}{\ln 2}
\left[-\ln\left(1-\frac{\eta}{m}\right)\right].
\]

**Proof.** Consider any \(k\)-dimensional principal covariance block \(B\).
Cauchy interlacing gives \(\lambda_{\min}(B)\geq m\), and the corresponding
error block \(E_B\) obeys \(\|E_B\|_2\leq\eta\). Therefore

\[
R=B^{-1/2}E_BB^{-1/2}
\quad\text{satisfies}\quad
\|R\|_2\leq q=\eta/m<1.
\]

Every eigenvalue of \(R\) lies in \([-q,q]\), so

\[
|\ln\det(B+E_B)-\ln\det B|
=|\ln\det(I+R)|
\leq -k\ln(1-q).
\]

Gaussian conditional mutual information is one half of the signed sum of log
determinants for blocks \(XZ\), \(YZ\), \(Z\), and \(XYZ\). Their dimensions
sum to \(2(d_X+d_Y+2d_Z)\). Applying the triangle inequality and converting
nats to bits proves the result. \(\square\)

The bound is implemented by `gaussian_cmi_covariance_error_bound`. It can be
applied to mutual information by setting \(d_Z=0\). It does not yet control the
canonical-correlation part of the score.

## Open conjectures

### C1. Parameter-level planted world-tube recovery

For a moving linear Gaussian module with internal predictive strength separated
from external drive by a parameter-level margin \(\delta>0\), the score-space
conditions of Proposition 5 follow on a nonempty interval of regularization
weights. Combined with covariance concentration, Proposition 6 would then imply
recovery probability approaching one as sample size grows.

### C2. Complete score stability under covariance perturbation

Proposition 7 controls the Gaussian mutual-information terms. A corresponding
bound for mean squared canonical correlation, followed through the nonlinear
geometric means and minimum bipartition, would give an explicit finite-horizon
world-tube action bound away from singular covariance blocks.

### C3. Gauge-consistent quantum lift

A quantum transport functional can be defined on equivalence classes of tensor
factorizations so that local unitaries within observer and environment factors
have zero path length, while changes that mix the factors have positive length.

### C4. Anti-triviality

Under explicit nondegeneracy conditions, jointly requiring integration,
insulation, and predictive transport excludes the dynamically frozen solutions
that can maximize independence alone.

Each conjecture remains open until its assumptions are fully specified and a
proof or a counterexample is committed with a reproducible test.
