# Proved results and open problems

The first nine statements below are consequences of the current definitions.
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
score arrays. Propositions 7 through 9 supply one explicit Gaussian route to
\(\epsilon_L\), \(\epsilon_\Theta\), and \(\alpha\); sharpening that route is an
open problem.

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
canonical-correlation part of the score; that is the subject of Proposition 8.

## Proposition 8: canonical-persistence perturbation bound

Let \(\Gamma\) and \(\widehat\Gamma=\Gamma+E\) be positive-definite joint
covariances for \((X,Y)\), with

\[
m\leq\lambda_{\min}(\Gamma),
\qquad
\lambda_{\max}(\Gamma)\leq M,
\qquad
\|E\|_2\leq\eta<m.
\]

Put \(a=m-\eta\),

\[
h=\frac{\eta}{\sqrt m\sqrt a(\sqrt m+\sqrt a)},
\]

and

\[
D=
\frac{h(M+\eta)}{\sqrt a}
+\frac{\eta}{\sqrt{ma}}
+\frac{Mh}{\sqrt m}.
\]

If \(P\) and \(\widehat P\) are the mean squared canonical correlations computed
from the two covariances, then

\[
|\widehat P-P|\leq\min(1,2D).
\]

**Proof.** Write

\[
W=\Sigma_X^{-1/2}\Sigma_{XY}\Sigma_Y^{-1/2}
\]

and define \(\widehat W\) analogously. The integral representation

\[
A^{-1/2}=\frac{2}{\pi}\int_0^\infty(A+t^2I)^{-1}\,dt
\]

and the resolvent identity give

\[
\|\widehat A^{-1/2}-A^{-1/2}\|_2
\leq
\frac{2\eta}{\pi}
\int_0^\infty\frac{dt}{(m+t^2)(a+t^2)}
=\frac{\eta}{\sqrt m\sqrt a(\sqrt m+\sqrt a)}=h
\]

for either marginal covariance. Principal-block compression gives
\(\|\widehat\Sigma_{XY}-\Sigma_{XY}\|_2\leq\eta\), while
\(\|\Sigma_{XY}\|_2\leq M\) and
\(\|\widehat\Sigma_{XY}\|_2\leq M+\eta\). Expanding
\(\widehat W-W\) into perturbations of the left inverse square root, cross block,
and right inverse square root yields \(\|\widehat W-W\|_2\leq D\).

Both \(W\) and \(\widehat W\) are contractions because they are whitened cross
blocks of positive-semidefinite joint covariances. If
\(r=\min(\dim X,\dim Y)\), then

\[
\begin{aligned}
|\widehat P-P|
&=\frac{1}{r}\left|
\|\widehat W\|_F^2-\|W\|_F^2
\right|\\
&\leq\frac{1}{r}\|\widehat W-W\|_F
\left(\|\widehat W\|_F+\|W\|_F\right)\\
&\leq 2\|\widehat W-W\|_2
\leq 2D.
\end{aligned}
\]

Since both persistence values lie in \([0,1]\), the bound can be clipped at one.
\(\square\)

## Proposition 9: end-to-end Gaussian sample-complexity guarantee

Assume \(N\) independent zero-mean Gaussian trajectories and use the centered,
unbiased sample covariance at each of \(T\) adjacent-time pairs. Suppose every
population joint covariance has dimension \(2n\) and eigenvalues in \([m,M]\).
For failure probability \(\delta\), define

\[
u_N=
\frac{\sqrt{2n}+\sqrt{2\ln(2T/\delta)}}{\sqrt{N-1}},
\qquad
\eta_N=M(2u_N+u_N^2).
\]

If \(\eta_N<m\), set

\[
c_N=\frac{-\ln(1-\eta_N/m)}{\ln 2},
\]

\[
\epsilon_J=4c_N,
\qquad
\epsilon_{\mathrm{leak}}=\frac{n+2s}{s}c_N,
\]

\[
\epsilon_G=\min(1,\ln 2\,\epsilon_J),
\qquad
\epsilon_K=\min(1,\ln 2\,\epsilon_{\mathrm{leak}}),
\]

and let \(\epsilon_P\) be the bound from Proposition 8 with
\(\eta=\eta_N\). The local and transport score errors obey

\[
\epsilon_\Omega
\leq
\min\left(1,
(\epsilon_G+\epsilon_K+\epsilon_P)^{1/3}
\right),
\]

\[
\epsilon_\Theta
\leq
\min\left(1,
\sqrt{\epsilon_K+\epsilon_P}
\right).
\]

Therefore a population path with action margin \(q>0\) is recovered with
probability at least \(1-\delta\) whenever

\[
q>
2\left[
T\epsilon_\Omega+|\chi|(T-1)\epsilon_\Theta
\right].
\]

**Proof.** For a centered Gaussian sample covariance,
\((N-1)\widehat\Gamma\) is Wishart. The Gaussian extreme-singular-value bound of
Davidson and Szarek [1, Theorem II.13] implies

\[
\|\widehat\Gamma_t-\Gamma_t\|_2
\leq M(2u_N+u_N^2)=\eta_N
\]

at all \(T\) times with probability at least \(1-\delta\), after a union bound.
On this event, Proposition 7 applies simultaneously to every principal block,
candidate, and bipartition; no additional union over candidates is needed. The
two directed CMI terms have total dimension coefficient \(4s\), giving
\(\epsilon_J=4c_N\) after per-node normalization. Leakage has dimensions
\((s,n-s,s)\), giving \(\epsilon_{\mathrm{leak}}=(n+2s)c_N/s\).

The maps \(1-2^{-x}\) and \(2^{-x}\) are \(\ln 2\)-Lipschitz on the nonnegative
line. For products in \([0,1]\), the product error is no greater than the sum of
factor errors. Finally,

\[
|x^{1/3}-y^{1/3}|\leq|x-y|^{1/3},
\qquad
|\sqrt x-\sqrt y|\leq\sqrt{|x-y|}.
\]

These inequalities give \(\epsilon_\Omega\) and \(\epsilon_\Theta\).
Proposition 6 then gives the path-recovery statement. \(\square\)

The implemented guarantee assumes an unregularized centered covariance.
A deterministic ridge can be included by adding its spectral norm to
\(\eta_N\). The present finite-sample benchmark uses a ridge, so its Wilson
intervals and this theorem answer related but not identical questions.

### Rate interpretation

Let \(\kappa=M/m\), hold \(n,s,T,\chi\) fixed, and consider the small-error
regime. Then

\[
\eta_N/m
=O\left(
\kappa\sqrt{\frac{n+\ln(T/\delta)}{N}}
\right).
\]

The canonical-persistence term adds another condition-number factor, so the
factor-product error is

\[
O\left(
\kappa^2\sqrt{\frac{n+\ln(T/\delta)}{N}}
\right).
\]

Without a positive lower bound on the score factors, the cube-root map in the
local score is only Hölder continuous. It makes the local-score error decay as
\(N^{-1/6}\), rather than \(N^{-1/2}\). Consequently, the worst-case sufficient
sample complexity has the scaling

\[
N
=O\left(
\kappa^4\,[n+\ln(T/\delta)]
\left(\frac{T}{q}\right)^6
\right),
\]

up to dimension-ratio and transport-weight constants. This sixth-power margin
dependence explains much of the numerical looseness. If every competitive
path has integration, independence, and persistence bounded away from zero,
the product roots become locally Lipschitz and a candidate-sensitive analysis
can in principle replace the \(q^{-6}\) dependence by \(q^{-2}\).

## Open conjectures

### C1. Parameter-level planted world-tube recovery

For a moving linear Gaussian module with internal predictive strength separated
from external drive by a parameter-level margin \(\delta>0\), the score-space
conditions of Proposition 5 follow on a nonempty interval of regularization
weights. Combined with covariance concentration, Proposition 6 would then imply
recovery probability approaching one as sample size grows.

### C2. Sharper score stability under covariance perturbation

Propositions 7 through 9 complete a worst-case route from covariance error to
path recovery. The remaining problem is to replace the global Hölder bound with
candidate-sensitive local bounds that use positive factor margins and avoid
paying for irrelevant near-zero candidates.

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

## Reference for the concentration step

1. K. R. Davidson and S. J. Szarek, "Local operator theory, random matrices and
   Banach spaces," in *Handbook of the Geometry of Banach Spaces*, vol. 1,
   2001, pp. 317-366. [Author-hosted preprint](https://www.math.uwaterloo.ca/~krdavids/Preprints/DavSzHB.pdf).
