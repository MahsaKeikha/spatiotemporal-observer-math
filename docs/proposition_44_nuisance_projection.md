# Proposition 44 — finite-sample covariance screening with a predeclared time-varying nuisance mean

This note closes one of the explicit gaps left after Propositions 42–43: the unknown mean no longer has to be constant. It may vary over time inside any **fixed, predeclared finite-dimensional temporal subspace**.

## Statement

Let the observed record be an \(N\times p\) matrix

\[
X = H B + R^{1/2} Z \Sigma^{1/2},
\]

where:

- \(H\in\mathbb R^{N\times q}\) is fixed before observing the record, has full column rank, and \(q<N\);
- \(B\in\mathbb R^{q\times p}\) is arbitrary and unknown;
- \(R\succeq0\) is the temporal covariance factor;
- \(\Sigma\succ0\) is the spatial covariance factor;
- \(Z\) has independent standard normal entries.

Define the orthogonal nuisance projector

\[
P_H = I-H(H^\mathsf T H)^{-1}H^\mathsf T,
\]

and the projected normalization

\[
d_H=\operatorname{tr}(P_HR).
\]

Assume \(d_H>0\). Then

\[
\widehat\Sigma_H = \frac{X^\mathsf T P_H X}{d_H}
\]

is exactly unbiased:

\[
\mathbb E\widehat\Sigma_H=\Sigma.
\]

Put

\[
F_H=\|P_HRP_H\|_F,
\qquad
S_H=\|P_HRP_H\|_2.
\]

For \(B_0\) predeclared covariance blocks of dimension at most \(m\), define

\[
u=
\log\!\left(
\frac{2B_0 9^m}{\alpha}
\right).
\]

With probability at least \(1-\alpha\), simultaneously over all those blocks,

\[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma_H-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le
\frac{4\left(F_H\sqrt{u}+S_Hu\right)}{d_H}.
\]

Equivalently, the projection has effective sample sizes

\[
N_{F,H}=\frac{d_H^2}{F_H^2},
\qquad
N_{\mathrm{op},H}=\frac{d_H}{S_H}.
\]

When \(H=\mathbf 1\), this reduces to Proposition 42. When \(H=[\mathbf 1,t]\), arbitrary unknown affine temporal drift is removed exactly.

## Proof

Because \(P_HH=0\), the nuisance mean disappears identically:

\[
P_HX=P_HR^{1/2}Z\Sigma^{1/2}.
\]

Therefore

\[
X^\mathsf T P_HX
=
\Sigma^{1/2}
Z^\mathsf T
R^{1/2}P_HR^{1/2}
Z
\Sigma^{1/2}.
\]

Let

\[
A=R^{1/2}P_HR^{1/2}.
\]

Since \(A\succeq0\),

\[
\mathbb E[Z^\mathsf TAZ]=\operatorname{tr}(A)I_p
=\operatorname{tr}(P_HR)I_p=d_HI_p,
\]

which proves unbiasedness.

The nonzero eigenvalues of \(A\) are the nonzero eigenvalues of \(P_HRP_H\). Hence

\[
\|A\|_F=F_H,
\qquad
\|A\|_2=S_H.
\]

After population whitening, for any fixed unit vector \(v\),

\[
v^\mathsf T
\Sigma^{-1/2}(\widehat\Sigma_H-\Sigma)\Sigma^{-1/2}
v
=
\frac{1}{d_H}
\sum_i\lambda_i(g_i^2-1),
\]

with independent \(g_i\sim N(0,1)\) and \(\lambda_i\) the eigenvalues of \(A\). Gaussian quadratic-form concentration gives

\[
\left|
\sum_i\lambda_i(g_i^2-1)
\right|
\le
2\left(F_H\sqrt{u}+S_Hu\right)
\]

with failure probability at most \(2e^{-u}\) for that direction. A \(1/4\)-net of the unit sphere has at most \(9^m\) points, and the standard net argument multiplies the directional bound by at most two. Union-bounding over \(B_0\) fixed blocks gives the displayed simultaneous radius. \(\square\)

## What changed relative to Proposition 42

Proposition 42 removed one nuisance direction, the constant vector \(\mathbf1\). Proposition 44 replaces that rank-one projection by an arbitrary fixed rank-\(q\) design. The concentration argument does not otherwise change.

This permits, for example:

- intercept + linear trend;
- predeclared polynomial drift;
- a fixed set of harmonic regressors;
- known acquisition or batch regressors;
- any other scientifically declared finite-dimensional temporal nuisance basis.

The nuisance coefficients \(B\) can be arbitrarily large. They do not enter the covariance radius because the projection removes \(HB\) exactly.

## Experiment AD

[![Experiment AD: nuisance-projected covariance calibration](nuisance_projection_calibration.svg)](nuisance_projection_calibration.svg)

Experiment AD uses four-dimensional Gaussian spatial covariance, stationary AR(1) temporal dependence with \(\phi=0.4\), \(N=800\), and an unknown affine mean. Across 96 trials at each of five trend amplitudes:

- the projected estimator retained essentially the same covariance error as the trend amplitude increased from 0 to 10;
- ordinary constant mean-centering became severely biased, with median population-relative error rising from about 0.14 to more than 120;
- every recorded projected covariance error was below the 97.5% analytical radius \(0.7581\);
- adding an arbitrary extra mean inside the declared affine subspace changed the projected covariance only at numerical roundoff (below \(10^{-15}\) in the recorded runs).

[Machine-readable Experiment AD results](nuisance_projection_calibration.json) · [reproducible script](../examples/nuisance_projection_calibration.py) · [claim-level tests](../tests/test_nuisance_projection.py)

## Scope and remaining gap

The result is exact only when the nuisance subspace is fixed before the same data are inspected. Choosing basis functions, knots, frequencies, or rank adaptively from the record creates a data-dependent projector and needs sample splitting or separate concentration.

The temporal covariance factor \(R\) is still treated as known by this proposition. Proposition 43 separately estimates a shared nonnegative AR(1) coefficient for the constant-mean setting. A future step is to compose **estimated temporal dependence with a general nuisance projector**, including uncertainty in \(d_H=\operatorname{tr}(P_HR)\), \(F_H\), and \(S_H\).

The result also retains exact Gaussian separability. Nonseparable sliding windows and non-Gaussian concentration remain open.
