# Proposition 47: matrix-Laplace concentration for weighted Gaussian covariance

Propositions 41-46 all inherit one deliberately conservative step: a scalar Gaussian quadratic-form bound is transferred to operator norm through a `1/4`-net of the unit sphere. That produces the familiar `9^m` factor and a leading constant `4`.

Proposition 47 removes that reduction entirely. For a weighted Gaussian covariance, the matrix exponential moment of each rank-one summand can be computed exactly. The resulting matrix-Laplace/Chernoff bound uses the full temporal eigenvalue profile and works directly in operator norm.

This matters because a covariance radius above one cannot be fed into several downstream relative perturbation arguments. The new result moves important strongly correlated regimes back below that threshold.

## Setup

After nuisance projection and population whitening, the covariance estimator has distribution

\[
S=\frac{1}{d}\sum_{i=1}^r \lambda_i g_i g_i^\mathsf T,
\qquad g_i\stackrel{\mathrm{iid}}\sim\mathcal N(0,I_m),
\]

where \(\lambda_i>0\) are the positive eigenvalues of

\[
P_HRP_H,
\]

and

\[
d=\sum_{i=1}^r\lambda_i=\operatorname{tr}(P_HR).
\]

Thus \(\mathbb E S=I_m\). Define

\[
X_i=\lambda_i(g_i g_i^\mathsf T-I_m).
\]

Then

\[
d(S-I_m)=\sum_i X_i.
\]

## Exact matrix exponential moment

For \(a\in[0,1/2)\), rank-one structure gives

\[
\exp(a g g^\mathsf T)
=I+\frac{e^{a\|g\|^2}-1}{\|g\|^2}gg^\mathsf T.
\]

Rotational invariance implies that its expectation is a scalar multiple of the identity. Taking traces determines that scalar exactly:

\[
\mathbb E\,e^{a(gg^\mathsf T-I)}=c_m^+(a)I_m,
\]

where

\[
c_m^+(a)=e^{-a}\frac{m-1+(1-2a)^{-m/2}}{m}.
\]

For the lower tail,

\[
\mathbb E\,e^{a(I-gg^\mathsf T)}=c_m^-(a)I_m,
\]

with

\[
c_m^-(a)=e^{a}\frac{m-1+(1+2a)^{-m/2}}{m}.
\]

These are exact identities, not norm inequalities.

## Upper-tail bound

The matrix Laplace transform method gives, for every

\[
0<\theta<\frac{1}{2\lambda_{\max}},
\]

\[
\Pr\!\left[\lambda_{\max}\!\left(\sum_i X_i\right)\ge t\right]
\le m\exp(-\theta t)\prod_i c_m^+(\theta\lambda_i).
\]

For \(B_0\) declared covariance blocks and total upper-tail failure budget \(\alpha/2\), it is enough to choose

\[
t_+(\theta)
=\frac{\log(2B_0m/\alpha)+\sum_i\log c_m^+(\theta\lambda_i)}{\theta}.
\]

Any admissible \(\theta\) yields a valid bound. Minimizing over a deterministic finite set of candidates improves tightness without introducing a discretization assumption into the probability statement.

Define

\[
\varepsilon_+=\frac{1}{d}\min_{\theta\in\Theta_+}t_+(\theta).
\]

## Lower-tail bound

Applying the same argument to \(-X_i\) gives, for every \(\theta>0\),

\[
\Pr\!\left[\lambda_{\max}\!\left(-\sum_i X_i\right)\ge t\right]
\le m\exp(-\theta t)\prod_i c_m^-(\theta\lambda_i).
\]

Hence

\[
\varepsilon_-
=\frac{1}{d}\min_{\theta\in\Theta_-}
\frac{\log(2B_0m/\alpha)+\sum_i\log c_m^-(\theta\lambda_i)}{\theta}.
\]

Because \(S\succeq0\), the downward relative deviation from \(I_m\) is deterministically at most one, so the implementation safely replaces \(\varepsilon_-\) by \(\min\{1,\varepsilon_-\}\).

## Proposition 47

Let

\[
\varepsilon_{\mathrm{mat}}=\max\{\varepsilon_+,\varepsilon_-\}.
\]

Then, simultaneously over \(B_0\) declared Gaussian covariance blocks of dimension at most \(m\),

\[
\|S-I\|_2\le\varepsilon_{\mathrm{mat}}
\]

with confidence at least \(1-\alpha\).

For blocks smaller than \(m\), one may couple the block to the corresponding principal submatrix of an \(m\)-dimensional weighted Gaussian covariance. The operator norm of a symmetric principal submatrix cannot exceed the operator norm of the full matrix, so the same dimension-\(m\) bound remains valid.

No independence between different declared blocks is needed. The final simultaneous statement uses a union bound.

## Why the full eigenvalue profile matters

The previous sphere-net radius depends on the projected temporal matrix only through

\[
\|P_HRP_H\|_F
\quad\text{and}\quad
\|P_HRP_H\|_2.
\]

Proposition 47 instead contains

\[
\sum_i \log c_m^\pm(\theta\lambda_i),
\]

so every temporal eigenvalue contributes separately. Two temporal spectra with the same trace can therefore receive different finite-sample covariance radii when one spectrum is more concentrated than the other.

## Experiment AG: removing the sphere-net bottleneck

[![Experiment AG: matrix Chernoff versus sphere-net covariance bounds](weighted_wishart_matrix_chernoff.svg)](weighted_wishart_matrix_chernoff.svg)

Experiment AG uses a fixed affine nuisance design and exact projected AR(1) covariance geometry. It compares Proposition 47 with the earlier exact-geometry sphere-net radius at three record lengths and four correlations.

At `N=850`:

| true AR(1) `phi` | sphere-net radius | Proposition 47 | reduction |
| ---: | ---: | ---: | ---: |
| 0.10 | 0.579 | 0.278 | 52.0% |
| 0.40 | 0.731 | 0.331 | 54.7% |
| 0.65 | 1.077 | 0.459 | 57.3% |
| 0.80 | 1.630 | 0.653 | 59.9% |

At `phi=0.65`, the previous radius is above one (`1.077`) while Proposition 47 gives `0.459`. At `phi=0.80`, the previous radius is `1.630` while the new matrix radius remains below one at `0.653`.

At `N=300`, `phi=0.65`, the radius improves from `2.165` to `0.832`.

A seeded 96-trial weighted-Wishart check at `N=300`, `phi=0.65`, and dimension four had every observed covariance error below the Proposition 47 radius. This numerical check is not the proof. It is included to make the scale of the theorem visible.

[Machine-readable Experiment AG results](weighted_wishart_matrix_chernoff.json) · [reproducible script](../examples/weighted_wishart_matrix_chernoff.py) · [claim-level tests](../tests/test_matrix_chernoff.py)

## What Proposition 47 closes

The result removes the `9^m` sphere-net factor and its associated leading `4` from the known-temporal-geometry covariance layer. It also shows that a substantial part of the high-correlation radius problem came from the concentration technique rather than from Gaussian temporal dependence itself.

## Remaining frontier

Proposition 47 currently assumes the projected temporal eigenvalues are known. Propositions 45-46 handle an estimated AR(1) interval, but through norm envelopes. The next step is to build a uniform matrix-Chernoff covariance radius over the calibrated AR(1) interval while retaining the actual nuisance design.
