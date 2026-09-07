# Proof ledger and conjecture register

This file separates mathematical results that already follow from the
definitions from claims that still require proof or experiment.

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

**Proof sketch.** The squared canonical correlations are the generalized
eigenvalues of

\[
\Sigma_{XY}\Sigma_Y^{-1}\Sigma_{YX}v
=\rho^2\Sigma_Xv.
\]

Under the two coordinate maps, the matrix pencil is transformed by invertible
congruences. With \(v'=R^{-\mathsf T}v\), the generalized eigenvalue equation
has the same \(\rho^2\). Thus the multiset of canonical correlations, and its
mean square used here, is unchanged. \(\square\)

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

## Open conjectures

### C1. Planted world-tube recovery

For a moving linear Gaussian module with internal predictive strength separated
from external drive by margin \(\delta>0\), there exists an interval of
regularization weights for which the global action uniquely recovers the
planted boundary path with probability approaching one as sample size grows.

### C2. Stability under covariance perturbation

If all relevant covariance blocks have eigenvalues bounded below by
\(m>0\), then the finite-horizon world-tube action is locally Lipschitz in the
transition and noise matrices away from path-score ties.

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
