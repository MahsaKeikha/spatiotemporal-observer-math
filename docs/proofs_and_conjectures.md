# Proved results and open problems

The first twenty-one statements below are consequences of the current definitions.
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

## Proposition 10: positive-factor stability of geometric scores

For \(x,y\in[0,1]^r\), define

\[
F(x)=\left(\prod_{i=1}^r x_i\right)^{1/r},
\qquad |x_i-y_i|\leq e_i.
\]

The zero-safe bound

\[
|F(x)-F(y)|\leq\left(\sum_{i=1}^r e_i\right)^{1/r}
\]

always holds. If \(a_i=x_i-e_i>0\) for every factor, then the sharper local
bound

\[
|F(x)-F(y)|
\leq
\frac{1}{r}\sum_{i=1}^r\frac{e_i}{a_i^{(r-1)/r}}
\]

also holds.

**Proof.** A telescoping product expansion gives

\[
\left|\prod_i x_i-\prod_i y_i\right|\leq\sum_i e_i.
\]

The first result follows from
\(|u^{1/r}-v^{1/r}|\leq|u-v|^{1/r}\). For the second, every point on the
line segment between \(x\) and \(y\) has coordinate \(i\) at least \(a_i\).
On that segment,

\[
\left|\frac{\partial F}{\partial x_i}\right|
=\frac{1}{r}
\left(\prod_{k\ne i}x_k\right)^{1/r}x_i^{-(r-1)/r}
\leq\frac{1}{r a_i^{(r-1)/r}}.
\]

The multivariate mean-value inequality proves the claim. \(\square\)

For the local observer score, \(r=3\); for transport, \(r=2\). Unlike the
global Hölder step in Proposition 9, this result recovers ordinary Lipschitz
behavior on candidates whose factors remain separated from zero.

## Proposition 11: localized finite-sample path certificate

Let there be \(C\) candidates of size \(s\). For time \(t\) and target candidate
\(j\), let \(B_{tj}\) be the covariance block containing all \(n\) present
variables and the \(s\) future variables in candidate \(j\). Suppose its
eigenvalues lie in \([m_{tj},M_{tj}]\). Define

\[
u_N^{\mathrm{loc}}
=\frac{
\sqrt{n+s}+\sqrt{2\ln(2TC/\delta)}
}{\sqrt{N-1}},
\qquad
\eta_{tj}=M_{tj}\left(2u_N^{\mathrm{loc}}+(u_N^{\mathrm{loc}})^2\right).
\]

When every \(\eta_{tj}<m_{tj}\), Propositions 7 and 8 give factor-error radii
for each local candidate and every transport edge entering that candidate.
Apply Proposition 10 to obtain candidate-dependent score errors
\(e^\Omega_{tj}\) and edge-dependent errors \(e^\Theta_{tij}\).

For a path \(p=(j_0,\ldots,j_{T-1})\), put

\[
b(p)=
\sum_{t=0}^{T-1}e^\Omega_{t j_t}
+|\chi|\sum_{t=0}^{T-2}e^\Theta_{t j_t j_{t+1}}.
\]

If the population optimizer \(p^*\) satisfies

\[
A(p^*)-b(p^*)
>
\max_{p\ne p^*}\{A(p)+b(p)\},
\]

then the empirical optimizer equals \(p^*\) with probability at least
\(1-\delta\).

**Proof.** Apply the Gaussian singular-value inequality separately to the
\(TC\) blocks and take a union bound. Each block then obeys its stated spectral
error simultaneously with probability at least \(1-\delta\). It contains every
principal covariance required for the target candidate's local score and for
all incoming transport scores. Propositions 7, 8, and 10 therefore imply

\[
|\widehat A(p)-A(p)|\leq b(p)
\]

for every path on the same event. Thus
\(\widehat A(p^*)\geq A(p^*)-b(p^*)\), while every competitor obeys
\(\widehat A(p)\leq A(p)+b(p)\). The strict displayed inequality separates
the two sets. \(\square\)

The right-hand maximum is not enumerated. It is another dynamic program with
local rewards \(\Omega+e^\Omega\) and transport rewards chosen so that their
weighted value is \(\chi\Theta+|\chi|e^\Theta\). This retains
\(O(TC^2)\) complexity.

## Proposition 12: parameter-level linear-Gaussian certificate

Consider a finite sequence

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad \varepsilon_t\sim\mathcal N(0,Q_t),
\]

with specified \(\Sigma_0\), candidate family, and action weights. The
population optimizer, every factor in Propositions 10 and 11, and every local
spectral envelope \((m_{tj},M_{tj})\) are deterministic functions of

\[
\Sigma_0,\quad \{A_t,Q_t\}_{t=0}^{T-1},\quad \text{and the candidate family}.
\]

Consequently, a positive localized slack in Proposition 11 is an end-to-end
parameter-level certificate of finite-sample path recovery.

**Proof.** Proposition 1 recursively determines \(\Sigma_t\) and each adjacent
joint covariance from \(\Sigma_0,A_t,Q_t\). Principal submatrices determine the
local spectral envelopes. The Gaussian information and canonical-correlation
formulas determine all score factors. Exact dynamic programming determines the
population path and the adversarial upper path. Proposition 11 then supplies
the probability statement. \(\square\)

This is a computable parameter-level result, not yet a symbolic separation
condition stated only through internal coupling and external drive. Deriving
such an interpretable condition remains Conjecture C1.

## Proposition 13: objective identifiability modulo symmetry

Let a permutation group \(G\) act on node labels and therefore on candidate
paths. Suppose the population action is equivariant:

\[
A(gp;gP)=A(p;P),\qquad g\in G,
\]

where \(P\) is the trajectory law. If \(P\) is invariant under \(G\), every
path in the orbit \([p]=\{gp:g\in G\}\) has the same population action.
Consequently, labeled paths inside one orbit are not distinguishable by this
objective. The maximizing boundary is identifiable modulo \(G\) precisely when
all population maximizers belong to one orbit.

**Proof.** Invariance gives \(gP=P\), and equivariance then gives
\(A(gp;P)=A(gp;gP)=A(p;P)\). Thus the action is constant on every orbit. If all
maximizers share one orbit, that orbit is uniquely determined by the population
objective. If two maximizing paths occupy different orbits, the objective
cannot select between their equivalence classes. \(\square\)

The implementation computes canonical orbit representatives for an explicitly
supplied finite permutation group. The user must specify which relabelings are
scientifically admissible; treating every coordinate permutation as a symmetry
would erase physically meaningful labels.

## Proposition 14: two-model impossibility bound

Let models \(P_0\) and \(P_1\) have correct boundary paths in disjoint admissible
orbits, and let their observation laws have total-variation distance
\(\tau=\operatorname{TV}(P_0,P_1)\). For every estimator \(\widehat p\) based
only on those observations,

\[
\min\left\{
P_0(\widehat p\in[p_0]),
P_1(\widehat p\in[p_1])
\right\}
\leq\frac{1+\tau}{2}.
\]

In particular, observationally identical models with incompatible correct
orbits cannot both be recovered with probability greater than \(1/2\).

**Proof.** Let \(E=\{\widehat p\in[p_0]\}\). Since the two correct orbits are
disjoint,

\[
P_1(\widehat p\in[p_1])\leq1-P_1(E).
\]

By the definition of total variation,
\(P_0(E)-P_1(E)\leq\tau\). Therefore the sum of the two success probabilities
is at most \(1+\tau\), so at least one is no greater than
\((1+\tau)/2\). \(\square\)

This result places an explicit ceiling on what any observational boundary
method can establish. Interventions or additional structural assumptions are
necessary when distinct physical decompositions generate identical trajectory
laws.

## Proposition 15: sufficient near-competitor graph

Suppose deterministic score-error radii give

\[
|\widehat A(p)-A(p)|\leq b(p)
\]

simultaneously for every path. Let \(p^*\) maximize the population action and
put \(L^*=A(p^*)-b(p^*)\). For state \(j\) at time \(t\), define

\[
U_{tj}=\max_{p:j_t=j}\{A(p)+b(p)\}.
\]

Retain the state when \(U_{tj}\geq L^*\). Define retained edges analogously by
maximizing over paths that traverse a specified edge. On the simultaneous error
event, every empirical maximizing path lies entirely in the retained state-edge
graph.

**Proof.** If a path \(p\) traverses a state with \(U_{tj}<L^*\), then

\[
\widehat A(p)
\leq A(p)+b(p)
\leq U_{tj}
<L^*
\leq\widehat A(p^*).
\]

Such a path cannot be an empirical maximizer. The same argument applies to an
excluded edge. \(\square\)

All \(U_{tj}\) and edge upper actions are computed by one forward and one
backward max-sum pass. The screen therefore costs \(O(TC^2)\), not enumeration
of \(C^T\) paths. The result is a sufficient screen: retained states are not
asserted to be genuinely competitive, but discarded states provably cannot win
under the supplied error event.

## Proposition 16: symbolic recovery for covariance-preserving moving cliques

Let every candidate be an \(s\)-node subset. At time \(t\), designate a planted
subset \(S_t^*\). Define \(A_t\) to have diagonal coefficient \(\alpha\),
off-diagonal coefficient \(\beta\) between ordered pairs in \(S_t^*\), and zero
other off-diagonal coefficients. Let

\[
Q_t=I-A_tA_t^\mathsf T,
\qquad \Sigma_0=I,
\]

and assume

\[
\max\{|\alpha|,|\alpha-\beta|,
|\alpha+(s-1)\beta|\}<1.
\]

Then \(Q_t\succ0\) and \(\Sigma_t=I\) at every time. Define

\[
d_r=\alpha^2+(r-1)\beta^2,
\qquad
o_r=2\alpha\beta+(r-2)\beta^2,
\]

\[
D(k,r)=
(1-d_r+o_r)^{k-1}
[1-d_r-(k-1)o_r].
\]

The planted directed-integration rate is

\[
J_*=
\min_{1\leq k<s}
\frac{1}{2s}
\log_2
\frac{D(k,k)D(s-k,s-k)}{D(k,s)D(s-k,s)}.
\]

Its insulation is \(K_*=1\), persistence and local score are

\[
P_*=\alpha^2+(s-1)\beta^2,
\qquad
\Omega_*=
\left[(1-2^{-J_*})P_*\right]^{1/3}.
\]

Every incorrect \(s\)-node candidate has local score zero. Consequently, for
bounded transport scores, \(\lambda\geq0\), and minimum consecutive planted
overlap \(r_{\min}\), define

\[
d_*^{\max}=1-\frac{r_{\min}}{2s-r_{\min}}.
\]

The planted path is the unique action maximizer whenever

\[
\Omega_*>2(|\chi|+\lambda d_*^{\max}).
\]

Its action margin is at least

\[
\Omega_*-2(|\chi|+\lambda d_*^{\max}).
\]

**Proof.** The eigenvalues of the active block of \(A_t\) are
\(\alpha+(s-1)\beta\) and \(\alpha-\beta\); outside it they are \(\alpha\).
The spectral assumption makes \(I-A_tA_t^\mathsf T\) positive definite, and
the covariance recursion gives \(\Sigma_{t+1}=I\).

For \(k\) selected future rows and \(r\) active present columns, the Gram
matrix has diagonal \(d_r\) and off-diagonal \(o_r\). Hence
\(D(k,r)=\det(I-A_{k,r}A_{k,r}^\mathsf T)\). Substitution into the two Gaussian
conditional-information determinants for a \(k:(s-k)\) split gives \(J_*\).
No present environment coordinate enters a planted future coordinate, so the
leakage is zero and \(K_*=1\). With identity source and target covariances, the
mean squared canonical correlations equal \(\|A_{S_t^*,S_t^*}\|_F^2/s=P_*\).

Any incorrect candidate contains a node outside \(S_t^*\). Isolating that node
in the weakest bipartition gives zero directed information in both directions,
so its integration strength and local score are zero. A path with \(h\geq1\)
mismatched times therefore loses \(h\Omega_*\) in local action. Changing one
time can affect at most two adjacent edges, and each affected edge can improve
transport by at most \(|\chi|\). Its continuity advantage is no larger than the
planted edge cost, which is at most \(\lambda d_*^{\max}\). The competitor's
net gain is at most
\(h[2(|\chi|+\lambda d_*^{\max})-\Omega_*]\), proving both statements.
\(\square\)

This family is deliberately exact. It supplies an interpretable theorem in
\(\alpha,\beta,Q_t\), and the action weights, while also exposing its own
limitation: the weakest-cut score makes every partially incorrect clique
locally degenerate.

## Proposition 17: covariance propagation around the moving-clique family

Use the base matrices \(A_t^0,Q_t^0\) from Proposition 16 and write

\[
A_t=A_t^0+E_t,
\qquad
Q_t=Q_t^0+F_t,
\qquad
\|E_t\|_2\leq\gamma,
\qquad
\|F_t\|_2\leq\nu.
\]

The matrices \(F_t\) are symmetric, but need not be diagonal or isotropic. Put

\[
\rho=\max\{|\alpha|,|\alpha-\beta|,
|\alpha+(s-1)\beta|\},
\qquad a=\rho+\gamma<1,
\]

\[
c=2\rho\gamma+\gamma^2+\nu,
\qquad
\delta_0=0,
\qquad
\delta_{t+1}=a^2\delta_t+c,
\]

and

\[
\kappa_t=a\delta_t+\gamma.
\]

If \(\Sigma_0=I\), then

\[
\|\Sigma_t-I\|_2\leq\delta_t.
\]

For the actual adjacent covariance \(\Gamma_t\) and the base adjacent
covariance \(\Gamma_t^0\), define

\[
\eta_t=\frac{1}{2}\left[
\delta_t+\delta_{t+1}
+\sqrt{(\delta_t-\delta_{t+1})^2+4\kappa_t^2}
\right].
\]

Then

\[
\|\Gamma_t-\Gamma_t^0\|_2\leq\eta_t.
\]

Moreover, \(Q_t\succ0\) is guaranteed whenever
\(\nu<1-\rho^2\).

**Proof.** Let \(\Delta_t=\Sigma_t-I\). Since
\(Q_t^0=I-A_t^0(A_t^0)^\mathsf T\), expansion of the covariance recursion gives

\[
\Delta_{t+1}
=A_t\Delta_tA_t^\mathsf T
+E_t(A_t^0)^\mathsf T+A_t^0E_t^\mathsf T
+E_tE_t^\mathsf T+F_t.
\]

Because \(\|A_t^0\|_2=\rho\) and \(\|A_t\|_2\leq a\), induction gives

\[
\|\Delta_{t+1}\|_2
\leq a^2\|\Delta_t\|_2+2\rho\gamma+\gamma^2+\nu
\leq\delta_{t+1}.
\]

The upper-right cross-covariance error is

\[
\Sigma_tA_t^\mathsf T-(A_t^0)^\mathsf T
=\Delta_tA_t^\mathsf T+E_t^\mathsf T,
\]

whose norm is at most \(\kappa_t\). For a symmetric block operator, its norm is
bounded by the norm of the two-by-two matrix of block norms. Applying this to
the diagonal bounds \(\delta_t,\delta_{t+1}\) and the cross bound \(\kappa_t\)
gives its largest eigenvalue, which is \(\eta_t\). Finally,
\(\lambda_{\min}(Q_t^0)=1-\rho^2\), so Weyl's inequality gives
\(\lambda_{\min}(Q_t)\geq1-\rho^2-\nu>0\). \(\square\)

The recursion also has the closed form

\[
\delta_t=c\frac{1-a^{2t}}{1-a^2}.
\]

The implementation uses the recursion because it exposes the largest error over
the stated finite horizon directly.

## Proposition 18: quadratic CMI bound at a zero conditional cross-covariance

Let \(\Gamma^0\) and \(\Gamma\) be positive-definite joint covariances for
\((X,Y,Z)\), where

\[
mI\preceq\Gamma^0\preceq MI,
\qquad
\|\Gamma-\Gamma^0\|_2\leq\eta<m.
\]

Assume the base conditional cross-covariance vanishes:

\[
C^0_{XY\mid Z}
=\Sigma^0_{XY}
-\Sigma^0_{XZ}(\Sigma^0_{ZZ})^{-1}\Sigma^0_{ZY}=0.
\]

Put \(a=m-\eta\) and

\[
c_\eta=\eta\left[
1+\frac{M+\eta}{a}
+\frac{M(M+\eta)}{ma}
+\frac{M}{m}
\right],
\qquad
z_\eta=\frac{c_\eta}{a}.
\]

If \(z_\eta<1\), then, for
\(r=\min\{\dim X,\dim Y\}\),

\[
I_\Gamma(X;Y\mid Z)
\leq-\frac{r}{2\ln2}\ln(1-z_\eta^2).
\]

**Proof.** Write

\[
C_{XY\mid Z}
=\Sigma_{XY}-\Sigma_{XZ}\Sigma_{ZZ}^{-1}\Sigma_{ZY}.
\]

Every covariance block perturbation has norm at most \(\eta\). The actual
inverse obeys \(\|\Sigma_{ZZ}^{-1}\|_2\leq1/a\), while the resolvent identity
gives

\[
\|\Sigma_{ZZ}^{-1}-(\Sigma^0_{ZZ})^{-1}\|_2
\leq\frac{\eta}{ma}.
\]

Expanding \(C_{XY\mid Z}-C^0_{XY\mid Z}\) into perturbations of its four
covariance factors, and using base and actual block norms \(M\) and
\(M+\eta\), gives \(\|C_{XY\mid Z}\|_2\leq c_\eta\).

The two actual conditional covariance Schur complements have minimum
eigenvalue at least \(a\). Consequently, the largest partial canonical
correlation is at most \(z_\eta\). If their \(r\) partial canonical
correlations are \(\rho_i\), Gaussian conditional mutual information satisfies

\[
I_\Gamma(X;Y\mid Z)
=-\frac{1}{2}\sum_{i=1}^r\log_2(1-\rho_i^2)
\leq-\frac{r}{2\ln2}\ln(1-z_\eta^2).
\]

This proves the result. \(\square\)

The bound is quadratic in \(z_\eta\) near zero. This is the appropriate local
behavior when the base partial correlation vanishes, in contrast with a
general log-determinant perturbation bound that is first order in \(\eta\).

## Proposition 19: robust recovery with external coupling and anisotropic noise

Retain the assumptions and notation of Proposition 17. Let

\[
\eta=\max_{0\leq t<T}\eta_t,
\qquad m=1-\rho,
\qquad M=1+\rho,
\]

and require \(\eta<m\). Define

\[
L_\eta=\frac{-\ln(1-\eta/m)}{\ln 2},
\]

\[
e_G=\min\{1,4\ln(2)L_\eta\},
\qquad
e_K=\min\left\{1,\ln(2)\frac{n+2s}{s}L_\eta\right\},
\]

and let \(e_P\) be the canonical-persistence bound in Proposition 8 evaluated
at \((m,M,\eta)\). Let \(z_\eta\) be defined by Proposition 18 and put

\[
G_{\mathrm{wrong}}^{\max}
=1-(1-z_\eta^2)^{1/s}.
\]

Let

\[
e_*=B_3\big((G_*,1,P_*),(e_G,e_K,e_P)\big),
\]

where \(B_3\) denotes the smaller of the zero-safe and positive-factor
geometric-mean bounds in Proposition 10. Every planted local score is at least
\(\Omega_*-e_*\), while every incorrect local score is at most
\((G_{\mathrm{wrong}}^{\max})^{1/3}\).
Consequently, put

\[
\Delta_\Omega
=\Omega_*-e_*-(G_{\mathrm{wrong}}^{\max})^{1/3}.
\]

For minimum consecutive planted overlap \(r_{\min}\), the perturbed planted
path is the unique action maximizer whenever

\[
\nu<1-\rho^2,
\qquad z_\eta<1,
\quad\text{and}\quad
\Delta_\Omega>2(|\chi|+\lambda d_*^{\max}).
\]

Its action margin is at least

\[
\Delta_\Omega-2(|\chi|+\lambda d_*^{\max}).
\]

**Proof.** Each \(\Gamma_t^0\) has eigenvalues in \([1-\rho,1+\rho]\).
Proposition 17 supplies a uniform perturbation of at most \(\eta<m\), so the
log-determinant argument of Proposition 7 applies to every relevant principal
block. Across the two directed conditional mutual informations, the dimension
coefficients sum to \(4s\); after division by \(s\), the integration-rate error
is at most \(4L_\eta\). The map \(1-2^{-x}\) is \(\ln 2\)-Lipschitz, which
gives \(e_G\). The leakage dimensions are \((s,n-s,s)\), giving the rate error
\((n+2s)L_\eta/s\) and hence \(e_K\). Proposition 8 gives \(e_P\), and
Proposition 10 then gives the planted score error \(e_*\).

An incorrect candidate contains a base-model outside node. Isolate that node in
the candidate's weakest-cut minimization. Both directed conditional
cross-covariances across this cut vanish in the base model. Proposition 18, with
canonical rank one for each direction, bounds their sum per node by

\[
-\frac{1}{s\ln2}\ln(1-z_\eta^2).
\]

Applying \(G=1-2^{-J}\) gives
\(G\leq G_{\mathrm{wrong}}^{\max}\). Since insulation and persistence do not
exceed one, the complete incorrect local score is at most
\((G_{\mathrm{wrong}}^{\max})^{1/3}\). Thus every mismatched time loses at least
\(\Delta_\Omega\) in local action. The edge comparison from Proposition 16
permits at most two incident-edge gains of
\(|\chi|+\lambda d_*^{\max}\) per mismatch. The stated strict inequality makes
every nonplanted path worse. \(\square\)

This result admits nonzero coupling between the planted set and its complement,
and permits incorrect candidates to have positive integration scores. It is a
uniform operator-norm neighborhood of Proposition 16. It is not a theorem for
arbitrary modular dynamics. The cube root still limits the certified
neighborhood, but Proposition 18 replaces the earlier first-order control of the
wrong integration factor by a second-order bound.

## Proposition 20: support-resolved finite-horizon recovery

Keep the moving-clique reference family of Proposition 19, but now fix the
actual matrices \(A_t,Q_t\), propagate their covariance from
\(\Sigma_0=I\), and write \(\Gamma_t^0,\Gamma_t\) for the base and actual
adjacent covariances. Let \(\Pi_D\) select a coordinate set \(D\). For the
planted boundary \(S_t^*\), define the local and leakage block errors

\[
\eta_t^{\rm loc}=\|\Pi_{S_t^*\cup(S_t^*+n)}
(\Gamma_t-\Gamma_t^0)\Pi_{S_t^*\cup(S_t^*+n)}^\mathsf T\|_2,
\]

\[
\eta_t^{\rm leak}=\|\Pi_{[n]\cup(S_t^*+n)}
(\Gamma_t-\Gamma_t^0)\Pi_{[n]\cup(S_t^*+n)}^\mathsf T\|_2.
\]

Use the minimum and maximum eigenvalues of the corresponding base blocks with
Propositions 7, 8, and 10 to obtain a planted-score error \(e_t^*\). Thus

\[
L_t=\max\{0,\Omega_*-e_t^*\}
\]

is a valid planted-score lower bound. For every incorrect size-\(s\) candidate
\(C\), set

\[
\eta_t(C)=\|\Pi_{C\cup(C+n)}
(\Gamma_t-\Gamma_t^0)\Pi_{C\cup(C+n)}^\mathsf T\|_2,
\]

and let \(m_t(C),M_t(C)\) be the extreme eigenvalues of the corresponding base
block. Apply Proposition 18 with these three local quantities to obtain
\(z_t(C)<1\), and define

\[
U_t(C)=\left[1-\{1-z_t(C)^2\}^{1/s}\right]^{1/3},
\qquad U_t=\max_{C\ne S_t^*}U_t(C).
\]

Let \(g_t=L_t-U_t\). For each planted edge define

\[
b_t^{\rm edge}=|\chi|+\lambda d_J(S_t^*,S_{t+1}^*),
\]

and let \(b_t^{\rm inc}\) be the sum of the one or two planted-edge bounds
incident to time \(t\). If every local covariance condition required above is
valid and

\[
\delta_{\rm supp}=\min_t\{g_t-b_t^{\rm inc}\}>0,
\]

then the planted path is the unique action maximizer. Its action margin is at
least \(\delta_{\rm supp}\).

**Proof.** The planted block errors are restrictions of the full covariance
error, so the log-determinant and canonical-correlation arguments in
Propositions 7 and 8 apply with the displayed block-specific spectra. Their
factor errors pass through the complete planted score by Proposition 10.

Every incorrect candidate contains a node outside the planted clique. Isolate
one such node in its weakest cut. The two base conditional cross-covariances
for that cut vanish. Proposition 18, applied only to
\(C\cup(C+n)\), bounds its directed integration factor by
\(1-(1-z_t(C)^2)^{1/s}\). The other two factors are at most one, giving the
stated bound \(U_t(C)\) for the complete score.

Consider any competing path and let \(M\) be its nonempty set of mismatched
times. Its local-action deficit is at least \(\sum_{t\in M}g_t\). An edge can
improve on the planted edge only if at least one endpoint is in \(M\), and its
improvement is at most \(b_t^{\rm edge}\). Charging that edge to all incident
mismatched endpoints can only overcount the possible gain. The competitor's
action deficit is therefore at least

\[
\sum_{t\in M}(g_t-b_t^{\rm inc})
\geq |M|\delta_{\rm supp}\geq\delta_{\rm supp}>0.
\]

This proves uniqueness and the margin claim. \(\square\)

The certificate is support-resolved in two distinct senses. The perturbation
is compressed to the coordinates used by each score, and the base spectrum of
an incorrect candidate depends on its overlap with the planted clique. It also
uses the exact planted edge penalty at each time instead of a uniform two-edge
penalty. The result is deterministic and parameter-level: it requires the
specified transition and noise matrices and enumerates all size-\(s\)
candidates. It is not an a priori certificate from perturbation radii alone.

## Proposition 21: a priori row-local recovery

Let \(A_t^0,Q_t^0\) be the covariance-preserving moving-clique family and
write

\[
A_t=A_t^0+E_t,\qquad Q_t=Q_t^0+F_t.
\]

Assume every \(Q_t\) is positive definite and \(\Sigma_0=I\). Define the
covariance forcing and global scalar recursion

\[
H_t=A_t^0E_t^\mathsf T+E_t(A_t^0)^\mathsf T
    +E_tE_t^\mathsf T+F_t,
\]

\[
\delta_0=0,\qquad
\delta_{t+1}=\|A_t\|_2^2\delta_t+\|H_t\|_2.
\]

For a coordinate set \(D\), put

\[
d_0(D)=0,
\]

\[
d_t(D)=
\|\Pi_DA_{t-1}\|_2^2\delta_{t-1}
+\|\Pi_DH_{t-1}\Pi_D^\mathsf T\|_2
\quad (t\geq1).
\]

Define

\[
\Phi(u,w,v)=
\frac{u+w+\sqrt{(u-w)^2+4v^2}}{2}.
\]

The adjacent-covariance error on \(D\) is bounded a priori by

\[
\bar\eta_t(D)=
\Phi\left(
d_t(D),
d_{t+1}(D),
\|\Pi_DA_t\|_2\delta_t+
\|\Pi_DE_t\Pi_D^\mathsf T\|_2
\right).
\]

For the planted leakage calculation, which uses every present coordinate and
only the future coordinates in \(S_t^*\), use

\[
\bar\eta_t^{\rm leak}=
\Phi\left(
\delta_t,
d_{t+1}(S_t^*),
\|\Pi_{S_t^*}A_t\|_2\delta_t+
\|\Pi_{S_t^*}E_t\|_2
\right).
\]

Replace the realized block errors in Proposition 20 by
\(\bar\eta_t(S_t^*)\), \(\bar\eta_t^{\rm leak}\), and
\(\bar\eta_t(C)\). If the resulting local spectral conditions hold and the
minimum mismatch margin is positive, then \(S^*\) is the unique action
maximizer in any declared size-\(s\) candidate family \(\mathcal C\) that
contains every \(S_t^*\). When
\(\mathcal C=\{C\subset[n]:|C|=s\}\), the result is unique recovery over the
complete fixed-size family.

**Proof.** Write \(\Delta_t=\Sigma_t-I\). Since
\(Q_t^0=I-A_t^0(A_t^0)^\mathsf T\), direct expansion of the covariance
recursion gives

\[
\Delta_{t+1}=A_t\Delta_tA_t^\mathsf T+H_t.
\]

Taking operator norms inductively proves
\(\|\Delta_t\|_2\leq\delta_t\). Principal compression of the same identity
gives

\[
\|\Pi_D\Delta_t\Pi_D^\mathsf T\|_2\leq d_t(D).
\]

The cross block of the adjacent-covariance error restricted to present and
future \(D\) is

\[
\Pi_D(A_t\Sigma_t-A_t^0)\Pi_D^\mathsf T
=\Pi_DA_t\Delta_t\Pi_D^\mathsf T
 +\Pi_DE_t\Pi_D^\mathsf T,
\]

whose norm is bounded by the third argument of
\(\bar\eta_t(D)\). For any symmetric block operator

\[
\begin{bmatrix}B&C^\mathsf T\\C&D\end{bmatrix}
\]

with \(\|B\|_2\leq u\), \(\|D\|_2\leq w\), and
\(\|C\|_2\leq v\), its operator norm is at most the largest eigenvalue of
\(\left[\begin{smallmatrix}u&v\\v&w\end{smallmatrix}\right]\), namely
\(\Phi(u,w,v)\). This proves the candidate-local joint bound. Keeping all
present coordinates changes the first diagonal bound to \(\delta_t\) and the
cross-error term to
\(\|\Pi_{S_t^*}A_t\|_2\delta_t+\|\Pi_{S_t^*}E_t\|_2\), proving the leakage
bound.

These a priori radii dominate the corresponding realized block errors.
Propositions 7, 8, 10, and 18 therefore give the same planted lower and
incorrect upper score construction as Proposition 20. Its mismatch-set edge
charging proof applies without change to the declared candidate family.
\(\square\)

This theorem uses the spatial structure of the supplied perturbation matrices
before any actual covariance is propagated. It can operate on a scientifically
declared reduced candidate family, but its guarantee is then relative to that
family. It does not justify selecting the family after inspecting the same
data, and it does not yet replace the matrices \(E_t,F_t\) by only sparsity,
degree, or block-radius summaries.

## Proposition 22: overlap-class recovery without candidate enumeration

Retain the setting of Proposition 21, let \(s=|S_t^*|\), and put
\(q_t(C)=|C\cap S_t^*|\). Suppose the following nonnegative numbers are known:

\[
\gamma_t\geq\|E_t\|_2,\qquad \nu_t\geq\|F_t\|_2,
\]

\[
e^{\rm row}_{tq}\geq
 \max_{q_t(C)=q}\|\Pi_CE_t\|_2,
\quad
e^{\rm in}_{tq}\geq
 \max_{q_t(C)=q}\|\Pi_CE_t\Pi_C^\mathsf T\|_2,
\quad
f_{tq}\geq
 \max_{q_t(C)=q}\|\Pi_CF_t\Pi_C^\mathsf T\|_2.
\]

The maxima range over all \(s\)-subsets. These are assumptions on supplied
budgets; the theorem does not require the matrices \(E_t,F_t\) themselves.
Define

\[
\rho=\max\{|\alpha|,|\alpha-\beta|,
                 |\alpha+(s-1)\beta|\},
\]

and, with \(d=\alpha^2+(s-1)\beta^2\) and
\(o=2\alpha\beta+(s-2)\beta^2\), let \(r_q\) be the square root of the
largest applicable member of

\[
\{d+(q-1)o\}\cup
\{d-o:q\geq2\}\cup
\{\alpha^2:q<s\}.
\]

For \(q=0\), set \(r_0=|\alpha|\). Thus \(r_q\) is exactly
\(\|\Pi_CA_t^0\|_2\) for every candidate in overlap class \(q\). Likewise,

\[
b_q=\|\Pi_CA_t^0\Pi_C^\mathsf T\|_2
\]

is \(|\alpha|\) for \(q\leq1\), and for \(q\geq2\) it is

\[
\max\{|\alpha|,|\alpha-\beta|,
              |\alpha+(q-1)\beta|\}.
\]

Use the scalar recursion

\[
\delta_0=0,\qquad
\delta_{t+1}=(\rho+\gamma_t)^2\delta_t
             +2\rho\gamma_t+\gamma_t^2+\nu_t,
\]

and the class-local next-state bounds

\[
d_{t+1,q}=(r_q+e^{\rm row}_{tq})^2\delta_t
 +2r_qe^{\rm row}_{tq}+(e^{\rm row}_{tq})^2+f_{tq}.
\]

To bound a present-state error at time \(t>0\), a current overlap \(q\) must
be coupled to a feasible previous overlap \(p\). Write
\(r=|S_{t-1}^*\cap S_t^*|\). The pair \((p,q)\) is feasible exactly when
there is an integer \(x\) satisfying

\[
\max\{0,p-s+r,q-s+r,p+q-s\}
\leq x\leq
\min\{r,p,q,n-3s+r+p+q\}.
\]

Here \(x\) counts candidate nodes in the intersection of the two planted
boundaries. Define

\[
d^-_{tq}=\max\{d_{t,p}:(p,q)\text{ is feasible}\},
\qquad d^-_{0q}=0,
\]

and the overlap-class joint radius

\[
\eta_{tq}=\Phi\left(
d^-_{tq},d_{t+1,q},
(r_q+e^{\rm row}_{tq})\delta_t+e^{\rm in}_{tq}
\right).
\]

For the planted local radius, use \(q=s\) and the actual preceding planted
overlap rather than maximizing over feasible \(p\). For the planted leakage
radius, replace the first argument by \(\delta_t\) and the last perturbation
term by \(e^{\rm row}_{ts}\). If \(\nu_t<1-\rho^2\), all score-domain
conditions of Propositions 18 and 20 hold for these radii, and every resulting
per-time mismatch margin is positive, then the planted path is the unique
maximizer over all \(\binom ns\) fixed-size candidates.

**Proof.** The row and compressed forcing terms satisfy

\[
\|\Pi_CH_t\Pi_C^\mathsf T\|_2
\leq 2r_qe^{\rm row}_{tq}+(e^{\rm row}_{tq})^2+f_{tq}.
\]

Also \(\|A_t\|_2\leq\rho+\gamma_t\),
\(\|\Pi_CA_t\|_2\leq r_q+e^{\rm row}_{tq}\), and the within-candidate
cross perturbation is at most \(e^{\rm in}_{tq}\). Hence the recursions above
dominate every corresponding quantity in Proposition 21.

It remains to show that no candidate is lost by class compression. Partition
the node set into \(S_{t-1}^*\cap S_t^*\), the two one-sided differences, and
the complement of their union. Their capacities are respectively
\(r,s-r,s-r,n-2s+r\). Writing the candidate occupancies as
\(x,p-x,q-x,s-p-q+x\) gives exactly the displayed lower and upper limits on
\(x\). Thus the feasible-pair maximum contains the present-state error of
every candidate with current overlap \(q\).

There are

\[
N_q=\binom{s}{q}\binom{n-s}{s-q}
\]

candidates in class \(q\), and \(\sum_qN_q=\binom ns\). Every incorrect
candidate has \(q<s\), so its base model has the zero cut used in Proposition
18 and base joint eigenvalue interval \([1-b_q,1+b_q]\). Applying the same
score perturbation and mismatch-set argument as Proposition 20 proves the
claim. \(\square\)

The certificate evaluates at most \(s+1\) overlap classes per time and at most
\((s+1)^2\) consecutive class pairs. Its time is \(O(Ts^2)\), its stored
class-pair representation is \(O(Ts^2)\), and neither depends on
\(\binom ns\). Obtaining valid class budgets remains a separate modeling
obligation. In the finite audit example they are computed by enumeration so
they can be checked against the matrix-level theorem; in a scalable use they
must instead follow from declared sparsity, degree, locality, or block-norm
assumptions.

## Proposition 23: structural budgets from block sparsity

At each time, partition coordinates into type \(0=S_t^*\) and type
\(1=[n]\setminus S_t^*\). Let \(M^{ab}\) denote the block of a matrix \(M\)
with row type \(a\in\{0,1\}\) and column type \(b\in\{0,1\}\). Suppose

\[
|M_{ij}^{ab}|\leq\epsilon^{ab},\qquad
\max_i|\operatorname{supp}M_{i,:}^{ab}|\leq d_{\rm r}^{ab},qquad
\max_j|\operatorname{supp}M_{:,j}^{ab}|\leq d_{\rm c}^{ab}.
\]

For a row selection containing \(u_a\) coordinates of type \(a\) and a
column selection containing \(v_b\) coordinates of type \(b\), define the
nonnegative comparison matrix

\[
K_{ab}(u,v)=\epsilon^{ab}
\sqrt{\min(d_{\rm r}^{ab},v_b)
      \min(d_{\rm c}^{ab},u_a)}.
\]

Then

\[
\|\Pi_U M\Pi_V^\mathsf T\|_2\leq\|K(u,v)\|_2.
\]

Consequently, let \(N=(s,n-s)\) and \(c_q=(q,s-q)\). Applying the construction
to the transition perturbation \(E_t\) gives valid Proposition 22 budgets

\[
\gamma_t=\|K_t^E(N,N)\|_2,
\quad
e^{\rm row}_{tq}=\|K_t^E(c_q,N)\|_2,
\quad
e^{\rm in}_{tq}=\|K_t^E(c_q,c_q)\|_2.
\]

Applying it to the noise perturbation \(F_t\) gives

\[
\nu_t=\|K_t^F(N,N)\|_2,
\qquad
f_{tq}=\|K_t^F(c_q,c_q)\|_2.
\]

If these derived budgets satisfy the spectral and mismatch-margin conditions
of Proposition 22, its complete-family unique-recovery conclusion follows.

**Proof.** For every compressed block \(B^{ab}=\Pi_{U_a}M^{ab}
\Pi_{V_b}^\mathsf T\),

\[
\|B^{ab}\|_\infty
\leq\epsilon^{ab}\min(d_{\rm r}^{ab},v_b),
\qquad
\|B^{ab}\|_1
\leq\epsilon^{ab}\min(d_{\rm c}^{ab},u_a).
\]

The standard inequality

\[
\|B^{ab}\|_2\leq
\sqrt{\|B^{ab}\|_1\|B^{ab}\|_\infty}
\]

therefore gives \(\|B^{ab}\|_2\leq K_{ab}(u,v)\). Split an input vector
\(x=(x_0,x_1)\) by column type. The triangle inequality yields

\[
\|(Bx)_a\|_2\leq\sum_bK_{ab}(u,v)\|x_b\|_2.
\]

Taking the Euclidean norm over the two row groups proves
\(\|B\|_2\leq\|K(u,v)\|_2\). A candidate with planted overlap \(q\) has row
and column count vector \(c_q\); the full population has count vector \(N\).
The five displayed substitutions are therefore valid uniformly over every
candidate in its overlap class. Proposition 22 completes the argument.
\(\square\)

The structural certificate reads only \(O(T)\) two-by-two entry and degree
tables. Budget construction takes \(O(Ts)\) arithmetic operations, and the
complete recovery calculation takes \(O(Ts^2)\) because of consecutive
overlap feasibility. These costs are independent of both \(n^2\) matrix
storage and \(\binom ns\) candidate enumeration. The theorem is conditional on
the declared envelopes actually holding. It does not estimate them from data,
and coarse degree or entry bounds can make the sufficient margin vacuous.

## Proposition 24: block-local covariance influence cones

Fix a coordinate partition \(V_1,\ldots,V_m\). For a matrix \(M\), write
\(M^{ab}=\Pi_{V_a}M\Pi_{V_b}^{\mathsf T}\). Retain

\[
\Delta_{t+1}=A_t\Delta_tA_t^\mathsf T+H_t,
\qquad
A_t=A_t^0+E_t.
\]

Suppose nonnegative comparison matrices \(B_t,G_t,R_t\) satisfy

\[
(B_t)_{ab}\geq\|A_t^{ab}\|_2,\qquad
(G_t)_{ab}\geq\|H_t^{ab}\|_2,\qquad
(R_t)_{ab}\geq\|E_t^{ab}\|_2.
\]

Let \(D_0\) be a symmetric nonnegative matrix with
\((D_0)_{ab}\geq\|\Delta_0^{ab}\|_2\), and define

\[
D_{t+1}=B_tD_tB_t^\mathsf T+G_t,
\qquad
C_t=B_tD_t+R_t.
\]

Then, for every pair of blocks,

\[
\|\Delta_t^{ab}\|_2\leq(D_t)_{ab},
\qquad
\|(A_t\Delta_t+E_t)^{ab}\|_2\leq(C_t)_{ab}.
\]

For present block indices \(I\) and future block indices \(J\), form

\[
\mathcal D_t(I,J)=
\begin{bmatrix}
D_t[I,I] & C_t[J,I]^\mathsf T\\
C_t[J,I] & D_{t+1}[J,J]
\end{bmatrix}.
\]

The adjacent-joint covariance error compressed to present blocks \(I\) and
future blocks \(J\) has operator norm at most
\(\|\mathcal D_t(I,J)\|_2\).

**Proof.** Assume the claim for \(D_t\). Block multiplication and the triangle
inequality give

\[
\begin{aligned}
\|\Delta_{t+1}^{ab}\|_2
&\leq
\sum_{c,d}\|A_t^{ac}\|_2
             \|\Delta_t^{cd}\|_2
             \|A_t^{bd}\|_2
 +\|H_t^{ab}\|_2\\
&\leq(B_tD_tB_t^\mathsf T+G_t)_{ab}.
\end{aligned}
\]

The same argument with one transition factor gives the bound \(C_t\) for the
cross-covariance error. Proposition 23's block comparison argument, applied to
the two-time partition, bounds the complete symmetric joint operator by
\(\|\mathcal D_t(I,J)\|_2\). Induction from \(D_0\) proves the result.
\(\square\)

The recursion also gives a finite-horizon support statement. With
\(P_{t:\tau+1}=B_{t-1}\cdots B_{\tau+1}\),

\[
D_t=P_{t:0}D_0P_{t:0}^\mathsf T+
\sum_{\tau=0}^{t-1}
P_{t:\tau+1}G_\tau P_{t:\tau+1}^\mathsf T.
\]

Here \(P_{t:0}=B_{t-1}\cdots B_0\), and a product with no factors is the
identity.

All matrices are nonnegative. Therefore an entry of \(D_t\) is exactly zero
whenever no pair of time-respecting paths in the comparison graph connects a
nonzero initial or forcing block to that entry. In a nearest-neighbor graph,
influence from a block at graph distance \(d\) cannot enter a local covariance
block in fewer than \(d\) transition steps. This is a support theorem, not a
small-value approximation.

## Proposition 25: moving-partition covariance influence cones

Let

\[
\mathcal P_t=\{V_{t,1},\ldots,V_{t,m_t}\}
\]

be an arbitrary coordinate partition at each time. Define rectangular
transition blocks from the present partition to the future partition by

\[
A_t^{ab}=\Pi_{V_{t+1,a}}A_t\Pi_{V_{t,b}}^\mathsf T,
\qquad
E_t^{ab}=\Pi_{V_{t+1,a}}E_t\Pi_{V_{t,b}}^\mathsf T.
\]

Suppose

\[
B_t\in\mathbb R_+^{m_{t+1}\times m_t},\quad
G_t\in\mathbb R_+^{m_{t+1}\times m_{t+1}},\quad
R_t\in\mathbb R_+^{m_{t+1}\times m_t}
\]

bound the corresponding blocks of \(A_t\), \(H_t\), and \(E_t\) in operator
norm. If \(D_t\in\mathbb R_+^{m_t\times m_t}\) bounds every covariance-error
block under \(\mathcal P_t\), then

\[
D_{t+1}=B_tD_tB_t^\mathsf T+G_t,
\qquad
C_t=B_tD_t+R_t
\]

bound the next covariance error under \(\mathcal P_{t+1}\) and the adjacent
cross-covariance error between \(\mathcal P_t\) and
\(\mathcal P_{t+1}\), respectively. For index sets
\(I\subseteq\{1,\ldots,m_t\}\) and
\(J\subseteq\{1,\ldots,m_{t+1}\}\), the compressed adjacent-joint error is at
most

\[
\left\|
\begin{bmatrix}
D_t[I,I] & C_t[J,I]^\mathsf T\\
C_t[J,I] & D_{t+1}[J,J]
\end{bmatrix}
\right\|_2.
\]

**Proof.** The proof of Proposition 24 uses only conformable block
multiplication, submultiplicativity, and the triangle inequality. None of
those steps requires the row and column partitions of \(A_t\) to coincide.
Applying the same argument with row partition \(\mathcal P_{t+1}\) and column
partition \(\mathcal P_t\) gives the two rectangular recursions. Applying the
block comparison inequality to the selected present and future blocks gives
the joint bound. Induction over the time layers completes the proof.
\(\square\)

The support graph is now a layered directed graph with \(m_t\) vertices in
layer \(t\). A zero entry remains zero unless it is reachable from an initial
or forcing entry by the paired time-respecting paths in the covariance
recursion. Thus the finite-speed statement survives arbitrary split, merge,
and reassignment of partition blocks.

No common refinement is formed. Dense evaluation costs

\[
O\!\left(\sum_t
  m_{t+1}m_t^2+m_{t+1}^2m_t
\right)
\]

arithmetic operations and stores only the declared rectangular comparisons
and time-local covariance comparisons. Sparse multiplication can reduce this
cost further. The guarantee is still conditional on valid block-norm
envelopes; changing a partition does not by itself supply those envelopes.

## Proposition 26: moving-partition path-recovery certificate

Let there be \(C\) candidates of equal size \(s\) on \(n\) variables. For each
time \(t\), suppose candidate \(j\)'s future coordinates are a union
\(J_{tj}\) of blocks in \(\mathcal P_{t+1}\). Select all present blocks and
these future blocks in Proposition 25, and call the resulting adjacent-joint
covariance radius

\[
\eta_{tj}=\left\|
\begin{bmatrix}
D_t & C_t[J_{tj},:]^\mathsf T\\
C_t[J_{tj},:] & D_{t+1}[J_{tj},J_{tj}]
\end{bmatrix}
\right\|_2.
\]

Suppose the corresponding population covariance block has spectrum in
\([m_{tj},M_{tj}]\), with \(0\leq\eta_{tj}<m_{tj}\), and define

\[
L_{tj}=-\log_2\!\left(1-\frac{\eta_{tj}}{m_{tj}}\right).
\]

Valid factor-error radii are

\[
e^G_{tj}=\min\{1,4\ln(2)L_{tj}\},
\qquad
e^K_{tj}=\min\!\left\{1,
\ln(2)\frac{n+2s}{s}L_{tj}\right\},
\]

together with the canonical-persistence error \(e^P_{tj}\) from Proposition 8
evaluated at \((m_{tj},M_{tj},\eta_{tj})\). Proposition 10 converts these into
a local-score error

\[
e^\Omega_{tj}=R_3\!\left(
(G_{tj},K_{tj},P_{tj}),
(e^G_{tj},e^K_{tj},e^P_{tj})
\right)
\]

and, for every edge entering candidate \(j\), a transport-score error

\[
e^\Theta_{tij}=R_2\!\left(
(K^\Theta_{tij},P^\Theta_{tij}),
(e^K_{tj},e^P_{tj})
\right),
\]

where \(R_d\) denotes the positive-factor geometric-mean bound of Proposition
10. For a candidate path \(p=(j_0,\ldots,j_{T-1})\), let

\[
b(p)=\sum_t e^\Omega_{t j_t}
+|\chi|\sum_{t=0}^{T-2}e^\Theta_{t j_tj_{t+1}}.
\]

If the population optimizer \(p^*\) satisfies

\[
A(p^*)-b(p^*)>
\max_{p\ne p^*}\{A(p)+b(p)\},
\]

then every covariance sequence inside the declared moving-partition envelope
has the same unique optimal path \(p^*\).

**Proof.** Proposition 25 bounds the complete block containing all present
variables and candidate \(j\)'s future variables. Every covariance used by the
candidate's directed integration, leakage, and canonical persistence is a
principal compression of this block and therefore has spectral error at most
\(\eta_{tj}\). Proposition 7 gives the two Gaussian-information bounds. The
two directed terms have total log-determinant dimension at most \(4s\), while
the leakage term has dimension \(n+2s\). The maps from information in bits to
the integration and independence factors have slopes bounded by \(\ln 2\),
which gives \(e^G_{tj}\) and \(e^K_{tj}\). Propositions 8 and 10 give the
remaining factor and score errors. Hence

\[
|\widehat A(p)-A(p)|\leq b(p)
\]

for every path. The strict robust-action inequality separates the lower action
of \(p^*\) from the upper action of every competitor. The competitor maximum is
computed by the same dynamic program with error-inflated rewards, so path
enumeration is unnecessary. \(\square\)

This is a deterministic perturbation theorem, not a sampling statement. It
also requires each candidate's future coordinates to be represented exactly
by its declared block union. Incorrect block membership or underestimated
comparison entries invalidate the certificate.

## Proposition 27: class-compressed robust path recovery

At each time \(t\), partition an implicit candidate family among \(K\) declared
classes, allowing zero multiplicity for an absent class. Suppose the three
local factors are constant within each nonempty class, the
two transport factors are constant within each ordered class pair. Suppose
local covariance radii and spectral envelopes bound every member of each state
class, while separate transport radii and envelopes bound every member of each
ordered class pair.
Let \(c_t^*\) be the class containing the planted candidate, and suppose that
class has multiplicity one.

Let \(e^\Omega_{tk}\) be obtained from the local class covariance radius, and
let \(e^\Theta_{tkl}\) be obtained separately from the ordered class-pair
transport radius, using the perturbation steps in Proposition 26. For each
feasible ordered class pair, let \(d^-_{tkl}\) be a lower bound on the
continuity distance of every member pair. Define the classwise upper rewards

\[
U_{tk}=\Omega_{tk}+e^\Omega_{tk},
\]

and

\[
V_{tkl}=\chi\Theta_{tkl}
+|\chi|e^\Theta_{tkl}-\lambda d^-_{tkl}.
\]

For the planted path, use its exact continuity distances and define

\[
L^*=A(p^*)-
\sum_t e^\Omega_{t c_t^*}
-|\chi|\sum_{t=0}^{T-2}
e^\Theta_{t c_t^*c_{t+1}^*}.
\]

Let \(U^{\rm comp}\) be the maximum sum of the class rewards \(U_{tk}\) and
\(V_{tkl}\) over every feasible class path other than
\((c_0^*,\ldots,c_{T-1}^*)\). If

\[
L^*>U^{\rm comp},
\]

then the planted candidate path is the unique optimizer for every covariance
sequence inside the declared class envelopes.

**Proof.** Proposition 26 bounds the perturbed score of every candidate in
class \(k\) by \(U_{tk}\). For any feasible edge from class \(k\) to class
\(l\), the transport perturbation inequality and
\(d\geq d^-_{tkl}\) bound its complete action contribution by \(V_{tkl}\).
Thus every nonplanted candidate path is bounded above by its class path, and
hence by \(U^{\rm comp}\). The planted class has multiplicity one at every
time, so the all-planted class path represents only \(p^*\). Proposition 26
bounds its perturbed action below by \(L^*\). The strict inequality proves
uniqueness. \(\square\)

The competitor maximum is evaluated by a dynamic program with state
\((k,h)\), where \(h\) records whether a mismatch from the planted class path
has occurred. The final maximum is restricted to \(h=1\). This costs
\(O(TK^2)\) time and \(O(K)\) value storage, regardless of class
multiplicities or the number of implicit paths. For fixed-size planted-overlap
classes, \(K\leq s+1\), while the represented candidate count can be
\(\binom ns\) at every time.

The result requires genuine class symmetry for the supplied factor values. A
lower continuity bound of zero is always valid but can make the certificate
conservative. Proposition 28 replaces the symmetry assumption by certified
componentwise factor intervals.

## Proposition 28: interval-certified class recovery

Use the candidate classes, multiplicities, feasible edges, planted singleton
classes, and continuity bounds of Proposition 27, but do not assume constant
factors within a class. Suppose instead that every member of state class \(k\)
at time \(t\) has local factor vector in the componentwise interval

\[
\ell^\Omega_{tk}\leq (G,K,P)\leq u^\Omega_{tk},
\]

and every member of ordered edge class \((k,l)\) has transport factor vector in

\[
\ell^\Theta_{tkl}\leq (K^\Theta,P^\Theta)
\leq u^\Theta_{tkl}.
\]

Let \(e^\Omega_{tk,r}\), \(r=1,2,3\), be the componentwise factor-error radii
obtained from the state-class covariance envelope by Propositions 7 and 8.
Let \(e^\Theta_{tkl,r}\), \(r=1,2\), be obtained separately from the ordered
edge-class covariance envelope. Define

\[
\underline\Omega_{tk}
=\left[\prod_{r=1}^3
\max\{0,\ell^\Omega_{tk,r}-e^\Omega_{tk,r}\}\right]^{1/3},
\qquad
\overline\Omega_{tk}
=\left[\prod_{r=1}^3
\min\{1,u^\Omega_{tk,r}+e^\Omega_{tk,r}\}\right]^{1/3},
\]

with analogous two-factor geometric means
\(\underline\Theta_{tkl}\) and \(\overline\Theta_{tkl}\).
For the planted path, choose \(\underline\Theta\) when \(\chi\geq0\) and
\(\overline\Theta\) when \(\chi<0\). For each competitor edge, choose the
opposite endpoint. Thus

\[
L^*=\sum_t\underline\Omega_{t c_t^*}
+\sum_{t=0}^{T-2}
\left(\chi\Theta^{\rm plant}_{t c_t^*c_{t+1}^*}
-\lambda d_t^*\right)
\]

is a lower bound for the planted action. Let \(U^{\rm comp}\) be the maximum,
over every feasible class path other than the planted class path, of the sum of
\(\overline\Omega\), the sign-correct competitor transport endpoint weighted
by \(\chi\), and \(-\lambda d^-_{tkl}\). If

\[
L^*>U^{\rm comp},
\]

then the planted candidate path is the unique optimizer for every choice of
population factors in the declared intervals and every covariance sequence in
the declared spectral envelopes.

**Proof.** Componentwise monotonicity of the geometric mean maps each factor
box to the displayed score interval. Propositions 7 and 8 enlarge each factor
interval by a valid covariance-induced radius, with clipping to the factor
range \([0,1]\). Multiplication by \(\chi\) preserves the transport endpoints
when \(\chi\geq0\) and reverses them when \(\chi<0\). The exact planted
distances give its lower action, while the class-pair distance lower bounds give
an upper action for every competitor. The mismatch-state dynamic program from
Proposition 27 returns the maximum of those competitor upper actions. Strict
separation proves uniqueness. \(\square\)

The calculation remains \(O(TK^2)\). Its conclusion is conditional on the
factor intervals covering every represented class member. Wider valid
intervals remain correct but can make the sufficient condition inconclusive.

## Proposition 29: covariance-residual derivation of class intervals

For each local state class \((t,k)\), let \(\Gamma^0_{tk}\) be a representative
joint covariance with spectrum in \([m_{tk},M_{tk}]\). Suppose every population
member covariance \(\Gamma_{tk}^{(a)}\) in that class satisfies

\[
\left\|\Gamma_{tk}^{(a)}-\Gamma^0_{tk}\right\|_2\leq r_{tk}<m_{tk}.
\]

Make the analogous declaration for every ordered transport class pair, using
separate representatives, spectral envelopes, and residual radii. Evaluate the
three local factors and two transport factors at the representatives. Apply the
factor-error construction of Propositions 7 and 8 with covariance error \(r\)
to obtain vectors \(e^{\rm het}\). Then every population factor vector lies in

\[
\left[\max\{0,f^0-e^{\rm het}\},
      \min\{1,f^0+e^{\rm het}\}\right]
\]

componentwise. Moreover, every member covariance has spectral bounds

\[
m^{\rm member}=m-r,
\qquad
M^{\rm member}=M+r.
\]

If an additional member-to-observation covariance error \(\eta\) satisfies
\(\eta<m-r\), Proposition 28 applied to the derived factor intervals and the
member spectral envelope gives a uniform path-recovery certificate. A positive
result certifies the planted path simultaneously for every represented class
member and every admitted observation perturbation.

**Proof.** Proposition 7 bounds both Gaussian information factors under the
representative-to-member residual. Proposition 8 bounds canonical persistence.
The minimum over internal bipartitions preserves the uniform integration bound,
because the minimum of functions is nonexpansive under a common sup-norm error.
The bounded information-to-factor maps give \(e^{\rm het}\), and clipping gives
the displayed factor box. Weyl's eigenvalue inequalities give \(m-r\) and
\(M+r\). The second perturbation is therefore evaluated relative to a valid
member covariance envelope. Proposition 28 completes the path comparison.
\(\square\)

This is a two-stage deterministic construction. The residual \(r\) describes
population heterogeneity around a representative; \(\eta\) describes a further
perturbation of an individual member. Their roles are not interchangeable.
Computing the certificate remains \(O(TK^2)\) after valid representatives and
residual radii have been established.

## Proposition 30: block-structural residual class recovery

Let a moving block covariance-error envelope satisfy Proposition 25. At joint
time \(t\), let \(F_{tk}\) be the future blocks whose union represents state
class \(k\), and select every present block because the local leakage term may
use the complete present environment. Form the nonnegative joint comparison

\[
J_{tk}=
\begin{bmatrix}
D_t[V_t,V_t] & C_t[F_{tk},V_t]^\mathsf T\\
C_t[F_{tk},V_t] & D_{t+1}[F_{tk},F_{tk}]
\end{bmatrix},
\qquad
r_{tk}=\|J_{tk}\|_2,
\]

where \(V_t\) contains all present blocks. Then \(r_{tk}\) bounds the spectral
covariance residual for every local score represented by class \(k\).
For a transport edge from class \(k\) to class \(l\), the same construction
with future selection \(F_{tl}\) bounds every covariance used by its source,
environment, and target factors. It therefore gives the valid ordered-pair
radius

\[
r^\Theta_{tkl}=\|J_{tl}\|_2.
\]

Using these radii in Proposition 29 yields a uniform robust path-recovery
certificate directly from the block transition, forcing, and cross-error
comparisons. If its recovery slack is positive, the planted path is unique for
every matrix-valued perturbation dominated by the declared block comparisons
and every subsequent observation perturbation inside the second-stage radii.

**Proof.** Proposition 25 bounds the norm of every selected covariance-error
block by the spectral norm of its nonnegative comparison block. The local score
uses only principal compressions of the joint selection containing all present
variables and the candidate's future variables. A transport score from any
source in class \(k\) to a target in class \(l\) uses a subblock of the same
all-present plus future-\(l\) selection, so the stated edge radius is uniform in
the source class. Proposition 29 converts these residuals into valid factor
intervals and Proposition 28 completes the adversarial path comparison.
\(\square\)

The all-present selection is conservative but protects environmental leakage.
A sharper theorem may introduce certified source-specific present selections.
The result still requires representative factors and representative spectral
envelopes; it removes the need to supply class covariance residuals manually.

## Open conjectures

### C1. Sharper score stability under covariance perturbation

Proposition 15 constructs the sufficient near-competitor graph, but using a
graph selected from the same finite sample can invalidate a naive reduced union
bound. A sample-split, confidence-sequence, or deterministic population-screen
argument should concentrate only the retained covariance directions while
preserving the advertised coverage probability.

### C2. Gauge-consistent quantum lift

A quantum transport functional can be defined on equivalence classes of tensor
factorizations so that local unitaries within observer and environment factors
have zero path length, while changes that mix the factors have positive length.

### C3. Anti-triviality

Under explicit nondegeneracy conditions, jointly requiring integration,
insulation, and predictive transport excludes the dynamically frozen solutions
that can maximize independence alone.

Each conjecture remains open until its assumptions are fully specified and a
proof or a counterexample is committed with a reproducible test.

## Reference for the concentration step

1. K. R. Davidson and S. J. Szarek, "Local operator theory, random matrices and
   Banach spaces," in *Handbook of the Geometry of Banach Spaces*, vol. 1,
   2001, pp. 317-366. [Author-hosted preprint](https://www.math.uwaterloo.ca/~krdavids/Preprints/DavSzHB.pdf).
