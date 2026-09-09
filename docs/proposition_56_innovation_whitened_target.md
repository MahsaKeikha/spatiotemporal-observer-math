# Proposition 56: exact innovation-whitened target covariance concentration

## Physical question

Proposition 55 showed that sharpening the calibration interval is no longer the main obstacle on the current irregular-time benchmark. Even if the true physical relaxation time is supplied exactly, the previous target theorem gives a relative covariance radius

\[
\varepsilon_{\mathrm{raw\ oracle}}
=2.1672468952>1.
\]

The next question is therefore not how to calibrate \(\tau\) more tightly. It is:

> If the physical temporal law is known, can its exact local innovation structure be used before covariance estimation so that temporal correlation no longer consumes most of the target information budget?

Proposition 56 answers yes for the declared Gaussian exponential-relaxation model.

On the exact Experiment AP target schedule, the resulting matrix concentration radius is

\[
\boxed{
\varepsilon_{56}=0.4364443814<1
}
\]

at 97.5% covariance confidence for the scalar block benchmark.

This is a change of estimator, not another refinement of the same temporal cover.

---

# 1. Target measurement model

Let the target record contain \(N\) timestamps

\[
t_1<\cdots<t_N
\]

and let the measured target matrix be

\[
Y\in\mathbb R^{N\times d}.
\]

Assume the declared separable Gaussian model

\[
Y=HB+E,
\]

where

- \(H\in\mathbb R^{N\times q}\) is a fixed, predeclared full-rank nuisance design;
- \(B\in\mathbb R^{q\times d}\) contains unknown nuisance coefficients;
- \(E\) has temporal covariance \(R_\tau\) and spatial covariance \(\Gamma\);
- \(R_\tau(i,j)=\exp(-|t_i-t_j|/\tau)\).

Equivalently,

\[
\operatorname{vec}(E)
\sim
\mathcal N\left(0,R_\tau\otimes\Gamma\right).
\]

Proposition 56 assumes that the physical relaxation time \(\tau\) used on this target record is known exactly. Uncertain \(\tau\) is deliberately left for the next robustness layer.

---

# 2. Exact local innovation whitening

Proposition 53 gives a lower-bidiagonal matrix \(W_\tau\) satisfying

\[
W_\tau R_\tau W_\tau^\mathsf T=I.
\]

For irregular gaps

\[
\Delta_i=t_{i+1}-t_i,
\qquad
\alpha_i=e^{-\Delta_i/\tau},
\]

the nontrivial rows of \(W_\tau\) implement the local transformation

\[
Z_{i+1}
=
\frac{Y_{i+1}-\alpha_iY_i}
{\sqrt{1-\alpha_i^2}}.
\]

The first row is the standardized initial state. Thus the dense temporal covariance is removed by a nearest-neighbor operation on the actual irregular timestamps.

Define

\[
Z=W_\tau Y
\]

and transform the nuisance design by the same physical operator:

\[
G=W_\tau H.
\]

Then

\[
Z=GB+\Xi,
\]

where the rows of \(\Xi\) are independent Gaussian vectors with covariance \(\Gamma\).

This is the key structural step. Temporal memory has been converted into independent innovation coordinates before covariance estimation.

---

# 3. Nuisance removal in innovation coordinates

Let

\[
P_G
=I-G(G^\mathsf TG)^{-1}G^\mathsf T.
\]

Because \(W_\tau\) is invertible and \(H\) has rank \(q\), the transformed design \(G\) also has rank \(q\). Therefore

\[
\operatorname{rank}(P_G)=N-q.
\]

Define the innovation-whitened covariance estimator

\[
\boxed{
\widehat\Gamma_{\mathrm{IW}}
=
\frac{1}{N-q}
Z^\mathsf T P_G Z
}.
\]

The nuisance term disappears exactly because \(P_GG=0\).

This estimator can also be written in the original target coordinates as

\[
\widehat\Gamma_{\mathrm{IW}}
=
\frac{1}{N-q}
Y^\mathsf T
W_\tau^\mathsf T P_G W_\tau
Y.
\]

Using \(W_\tau^\mathsf T W_\tau=R_\tau^{-1}\), the quadratic form is the usual generalized least-squares residual form:

\[
W_\tau^\mathsf T P_G W_\tau
=
R_\tau^{-1}
-
R_\tau^{-1}H
(H^\mathsf T R_\tau^{-1}H)^{-1}
H^\mathsf T R_\tau^{-1}.
\]

So Proposition 56 is not discarding the nuisance model. It is fitting that model in the covariance geometry implied by the declared temporal physics.

---

# 4. Exact Wishart reduction

Since \(P_G\) is a symmetric idempotent projector of rank

\[
r=N-q,
\]
there exists an orthogonal matrix \(U\) such that

\[
P_G
=
U
\begin{pmatrix}
I_r&0\\
0&0
\end{pmatrix}
U^\mathsf T.
\]

The rows of \(\Xi\) are independent centered Gaussian vectors. Orthogonal mixing of those rows preserves their joint law. Therefore

\[
Z^\mathsf T P_G Z
\]

has the same distribution as the sum of \(r\) independent rank-one Gaussian outer products with spatial covariance \(\Gamma\).

Hence

\[
\boxed{
r\widehat\Gamma_{\mathrm{IW}}
\sim
\operatorname{Wishart}_d(\Gamma,r)}.
\]

Equivalently, after spatial whitening by \(\Gamma^{-1/2}\), Proposition 47 applies with exactly

\[
\lambda_1=\cdots=\lambda_r=1.
\]

There is no remaining temporal spectral-norm penalty and no temporal effective-sample-size correction. The usable residual information is exactly \(N-q\) Gaussian innovation degrees of freedom under the declared model.

---

# 5. Matrix concentration statement

For a declared block dimension \(d\), block count \(B\), and confidence \(1-\delta\), Proposition 47 applied to the \(r=N-q\) unit weights returns a two-sided operator-norm radius \(\varepsilon_{56}\) such that

\[
\Pr\left[
\left\|
\Gamma^{-1/2}
(\widehat\Gamma_{\mathrm{IW}}-\Gamma)
\Gamma^{-1/2}
\right\|_2
\le
\varepsilon_{56}
\right]
\ge 1-\delta
\]

simultaneously over the declared covariance blocks under the Proposition 47 union bound.

For Experiment AQ,

\[
N=120,
\qquad
q=2,
\qquad
r=118,
\]

with scalar block dimension and one block at 97.5% confidence. The certified radius is

\[
\boxed{
\varepsilon_{56}=0.4364443814
}.
\]

The previous known-\(\tau\) raw-time oracle radius was

\[
2.1672468952.
\]

The relative reduction is

\[
\boxed{79.86\%}.
\]

Most importantly, the new theorem crosses the perturbative threshold one on the same target schedule without increasing the number of samples.

---

# 6. Why the old oracle and the new theorem are different

The Proposition 55 oracle supplied the correct \(\tau\) to the existing raw-time covariance concentration layer. It did not use \(\tau\) to transform the estimator itself.

Under that old estimator, the projected temporal spectrum on the Experiment AP target has

\[
\operatorname{tr}=84.3434898959
\]

and maximum eigenvalue

\[
\lambda_{\max}=14.5246150894.
\]

The large leading temporal weight drives the upper matrix tail.

Proposition 56 instead uses the known temporal model operationally. After exact innovation whitening and transformed nuisance removal, the concentration spectrum is simply

\[
(1,1,\ldots,1)
\]

with 118 entries.

This is why the improvement is much larger than another cover-grid refinement could provide.

---

# 7. Experiment AQ

Experiment AQ reuses the exact target timestamp schedule from Experiment AP:

- physical relaxation time: \(\tau=0.78\) s;
- target sample count: 120;
- nuisance rank: 2;
- residual innovation degrees of freedom: 118;
- covariance confidence: 0.975;
- scalar block benchmark: \(d=1\), \(B=1\).

The exact local whitener contains 239 numerically nonzero entries. The corresponding tridiagonal precision matrix contains 358 nonzero entries out of 14,400 possible entries.

The whitening identity is satisfied numerically at operator error approximately

\[
5.2\times10^{-15}.
\]

A 512-trial seeded visibility check with a large affine nuisance term recorded all 512 scalar relative covariance errors below the Proposition 56 matrix radius. The median relative error was about 0.0892 and the maximum was about 0.3942.

These repeated trials are a visibility check only. The finite-sample guarantee comes from the exact Wishart reduction and Proposition 47, not from the empirical trial count.

For dimension one only, the exact chi-square quantiles give a tighter two-sided reference radius of approximately 0.31424. That scalar reference is not used as Proposition 56 because the matrix-Chernoff formulation extends directly to multidimensional covariance blocks.

---

# 8. Physical interpretation

The result has a simple physical reading:

> If a declared relaxation model really describes the target process and its physical timescale is known, repeated measurements should not be treated as merely correlated raw samples. The exact local dynamics tell us how to convert them into innovations first.

The transformed residuals represent new stochastic information after the predictable relaxation step and the declared deterministic nuisance modes have been removed.

The theorem does not say that temporal correlation creates information. It says that when the temporal law is known, the predictable part of the correlation can be modeled explicitly rather than paid for again as worst-case covariance dependence.

---

# 9. Scope and failure conditions

Proposition 56 is conditional on:

- exact separable Gaussian covariance \(R_\tau\otimes\Gamma\);
- the one-timescale stationary exponential relaxation kernel;
- exact knowledge of the target relaxation time \(\tau\);
- strictly increasing target timestamps;
- a fixed, predeclared full-rank nuisance design;
- correct use of the same whitener on both measurements and nuisance design;
- covariance blocks declared before the target concentration statement is evaluated.

Relevant falsification diagnostics include:

- residual temporal correlation after innovation whitening;
- multiple or drifting relaxation times;
- oscillatory temporal structure;
- non-Gaussian or heavy-tailed innovations;
- nonseparable space-time covariance;
- mismatch between the calibration law and the target law;
- nuisance modes that were selected adaptively from the same target noise.

If the assumed \(\tau\) is wrong, the innovation coordinates are not exactly independent. Proposition 56 alone does not cover that error.

That is now the next theorem frontier: propagate the Proposition 55 finite-sample \(\tau\) set through the innovation whitener itself while retaining as much of the \(N-q\) information gain as possible.

---

# 10. Reproducibility

Implementation:

- `src/observer_math/innovation_whitening.py`

Claim-level tests:

- `tests/test_innovation_whitening.py`

Experiment:

- `examples/innovation_whitened_target.py`

Machine-readable record:

- `docs/innovation_whitened_target.json`

Visible figure:

- `docs/innovation_whitened_target.svg`

The numerical experiment illustrates theorem scale. The probability statement comes from exact temporal whitening, exact nuisance-projection rank, the Wishart reduction, and Proposition 47 matrix concentration.
