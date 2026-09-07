# Mathematical framework

## The boundary is part of the problem

Suppose the complete state of a model is \(X_t\). Before asking what a subsystem
does, one normally chooses which variables belong to it. This project makes that
choice variable. A candidate boundary at time \(t\) is \(S_t\), and a candidate
identity is the entire sequence

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1}).
\]

The term *observer world-tube* refers to \(\mathcal W\). It does not assume that
the selected process is conscious. The immediate mathematical problem is
subsystem identification under changing membership.

This shift matters whenever organization persists while its physical support
changes. A fixed cut can describe each time separately, but it cannot by itself
say which cut at \(t+1\) continues a cut at \(t\).

## Connection to the factorization problem

The source framework begins with a quantum factorization

\[
\mathcal H\cong\mathcal H_S\otimes\mathcal H_E
\]

and decomposes the Hamiltonian as

\[
H=H_S\otimes I_E+I_S\otimes H_E+H_{SE}.
\]

Weak \(H_{SE}\) favors independence, but independence alone can favor a basis in
which the dynamics becomes trivial. That tension suggests that a useful
subsystem criterion must retain both insulation and nontrivial internal change.

The present code does not solve the quantum factorization problem. It isolates a
classical version in which every term can be calculated exactly, then asks what
must be added when the factorization itself becomes a function of time.

## Exact classical setting

The working model is

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t),
\qquad
\varepsilon_t\perp X_t.
\]

The covariance is propagated without a stationarity assumption:

\[
\Sigma_{t+1}=A_t\Sigma_tA_t^\mathsf T+Q_t.
\]

For a boundary \(S\), three questions are asked.

### Does the boundary contain irreducible cross-prediction?

For each internal bipartition \(S=U\sqcup V\),

\[
J_t(U,V)=
I(X_U^{t+1};X_V^t\mid X_U^t)
+I(X_V^{t+1};X_U^t\mid X_V^t).
\]

The internal term \(\mathcal J_t(S)\) is the smallest \(J_t(U,V)\), divided by
\(|S|\). A boundary scores poorly if it contains even one cut across which the
parts do not dynamically inform one another.

### How much prediction enters from outside?

\[
\mathcal L_t(S)=\frac{1}{|S|}
I(X_S^{t+1};X_{\bar S}^t\mid X_S^t).
\]

This term is zero when the present environment adds no prediction of the
subsystem's next state after the subsystem's own present is known.

### Does the representation persist?

Let \(\rho_1,\ldots,\rho_r\) be the canonical correlations between \(X_S^t\)
and \(X_S^{t+1}\). Then

\[
P_t(S)=\frac{1}{r}\sum_{i=1}^{r}\rho_i^2.
\]

The local score combines bounded versions of these terms:

\[
\Omega_t(S)=
\left[
\left(1-2^{-\mathcal J_t(S)}\right)
2^{-\mathcal L_t(S)}
P_t(S)
\right]^{1/3}.
\]

The geometric mean is deliberately strict: zero directed integration makes the
whole score zero. Equal weighting is provisional and exposed as a modeling
choice.

## Crossing a changing boundary

Local scores do not decide whether \(S_t\) continues as \(S_{t+1}\). For a
source boundary \(S\) and a possibly different target boundary \(R\), define

\[
P_t(S\to R)=\frac{1}{r}\sum_{i=1}^{r}\rho_i^2,
\]

where the canonical correlations now compare \(X_S^t\) with \(X_R^{t+1}\).
The source-conditioned leakage is

\[
L_t(S\to R)=\frac{1}{|R|}
I(X_R^{t+1};X_{\bar S}^t\mid X_S^t),
\]

and the transition score is

\[
\Theta_t(S\to R)=
\sqrt{P_t(S\to R)2^{-L_t(S\to R)}}.
\]

Canonical correlations make the persistence term invariant under invertible
linear changes of coordinates made independently inside the source and target.
The leakage factor prevents a target from receiving full credit when its
predictability is imported from outside the proposed source.

## The discrete world-tube action

For a finite candidate set \(\mathcal C\), choose one boundary \(S_t\in\mathcal
C\) at every time and maximize

\[
\mathcal A(\mathcal W)=
\sum_{t=0}^{T-1}\Omega_t(S_t)
+\chi\sum_{t=0}^{T-2}\Theta_t(S_t\to S_{t+1})
-\lambda\sum_{t=0}^{T-2}d_J(S_t,S_{t+1}),
\]

with Jaccard distance

\[
d_J(S,R)=1-\frac{|S\cap R|}{|S\cup R|}.
\]

The last term favors some material continuity without imposing a fixed set of
components. The global optimum and exact runner-up are found in \(O(TC^2)\)
time for \(C\) candidates. The full recurrence and perturbation certificate are
derived in [Derivations](derivations.md).

## A possible geometric lift

In a quantum model, a boundary is not merely a subset of labeled variables. It
is a tensor-product structure. A path should therefore live in a space of
factorizations modulo changes of basis made separately within the factors.
A preliminary homogeneous-space candidate is

\[
\mathfrak F_{d,n}\sim
U(n)\big/\left(U(d)\otimes U(n/d)\right).
\]

This expression is only a starting point. A complete construction must identify
stabilizers and discrete equivalences, specify a metric, and show that vertical
motion corresponds exactly to local basis changes. Only then is it meaningful
to speak of a horizontal velocity, geodesic distance, curvature, or holonomy of
a factorization path.

The intended role of the geometric term is clear even before that construction
is complete: it should charge for genuine mixing of system and environment, but
assign zero length to relabeling within either one.

## What has and has not been shown

The repository currently establishes:

- the exact adjacent covariance for the nonstationary Gaussian model
- invariance of canonical transport under separate invertible source and target
  coordinate changes
- boundedness of the transition score
- exact global and runner-up path inference on a finite candidate set
- a deterministic score-perturbation certificate
- recovery in one small planted moving-module construction
- global and candidate-local Gaussian finite-sample recovery certificates
- a computable certificate directly from linear-Gaussian parameters
- labeled-path identifiability only modulo admissible symmetries
- a two-model impossibility bound for observationally similar systems
- a sufficient near-competitor state-edge graph
- a closed-form moving-clique recovery theorem in dynamical parameters

It does not establish:

- that the score identifies consciousness
- that the chosen functional is unique
- a practically sharp finite-sample recovery threshold
- robustness to hidden common causes or nonlinear observation maps
- a preferred metric on quantum factorization space
- equivalence or superiority relative to existing integration and emergence
  measures

Those distinctions define the next work rather than a disclaimer around it.
