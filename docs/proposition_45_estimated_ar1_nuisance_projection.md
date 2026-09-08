# Proposition 45: estimated AR(1) calibration with a predeclared time-varying nuisance mean

Proposition 44 permits an arbitrary unknown mean inside a fixed temporal nuisance subspace, but its covariance radius assumes the temporal covariance factor is known. Proposition 45 removes that requirement for a shared **nonnegative stationary AR(1)** coefficient by composing Proposition 43's observable increment-energy confidence interval with Proposition 44's projection argument.

## Statement

Let the target record satisfy

\[
X = HB + R_\phi^{1/2}Z\Sigma^{1/2},
\]

where \(H\in\mathbb R^{N\times q}\) is fixed before observing the target record, has full column rank \(q<N\), \(B\) is arbitrary and unknown, \(\Sigma\succ0\), and

\[
(R_\phi)_{ij}=\phi^{|i-j|},\qquad 0\le \phi<1.
\]

Let

\[
P_H=I-H(H^\mathsf TH)^{-1}H^\mathsf T.
\]

Assume standardized Gaussian calibration channels obey the Proposition 43 assumptions: unit marginal variance, constant unknown channel means, a common nonnegative AR(1) coefficient \(\phi\), and a declared prior bound \(0\le\phi\le\phi_{\max}<1\). Proposition 43 returns an observable confidence interval

\[
\phi\in[\underline\phi,\overline\phi]
\]

with calibration confidence \(1-\alpha_{\rm cal}\). Put \(\rho=\overline\phi\).

For target sample count \(N\), let

\[
F_\rho^2=N+2\sum_{k=1}^{N-1}(N-k)\rho^{2k},
\]

and

\[
S_\rho=\min\!\left\{N,\frac{1+\rho}{1-\rho}\right\}.
\]

Define

\[
d_- = N-qS_\rho,\qquad d_+=N,
\]

and require \(d_->0\). Use the observable reference normalization

\[
d_\star=\frac{d_-+d_+}{2}
\]

and estimator

\[
\widehat\Sigma_\star=\frac{X^\mathsf TP_HX}{d_\star}.
\]

For \(B_0\) predeclared covariance blocks of dimension at most \(m\), let

\[
u=\log\!\left(\frac{2B_0 9^m}{\alpha_{\rm cov}}\right)
\]

and

\[
\varepsilon_{\rm oracle}=\frac{4(F_\rho\sqrt{u}+S_\rho u)}{d_-}.
\]

Set

\[
a=\frac{d_-}{d_\star},\qquad b=\frac{d_+}{d_\star},
\]

and

\[
\varepsilon_\star
=\max\left\{|a-1|+a\varepsilon_{\rm oracle},|b-1|+b\varepsilon_{\rm oracle}\right\}.
\]

Then, with confidence at least

\[
1-\alpha_{\rm cal}-\alpha_{\rm cov},
\]

simultaneously over all declared blocks,

\[
\left\|\Sigma^{-1/2}(\widehat\Sigma_\star-\Sigma)\Sigma^{-1/2}\right\|_2
\le \varepsilon_\star.
\]

No independence between the calibration event and the target covariance event is needed for this final confidence statement. The result uses a union bound.

## Proof

On the Proposition 43 calibration event, \(0\le\phi\le\rho\). The AR(1) Frobenius norm is monotone in \(|\phi|\), so

\[
\|R_\phi\|_F\le F_\rho.
\]

The AR(1) Toeplitz row-sum bound gives

\[
\|R_\phi\|_2
\le \min\!\left\{N,\frac{1+\phi}{1-\phi}\right\}
\le S_\rho.
\]

Let \(Q_H=I-P_H\), an orthogonal projector of rank \(q\). Since \(R_\phi\succeq0\),

\[
0\le\operatorname{tr}(Q_HR_\phi)\le q\|R_\phi\|_2\le qS_\rho.
\]

Because \(\operatorname{tr}(R_\phi)=N\), the exact projected normalization

\[
d_\phi=\operatorname{tr}(P_HR_\phi)
=N-\operatorname{tr}(Q_HR_\phi)
\]

obeys

\[
d_-\le d_\phi\le d_+.
\]

Projection is contractive in Frobenius and spectral norm:

\[
\|P_HR_\phi P_H\|_F\le F_\rho,
\qquad
\|P_HR_\phi P_H\|_2\le S_\rho.
\]

Using the inaccessible oracle normalization \(d_\phi\), Proposition 44's Gaussian quadratic-form argument gives the oracle radius \(\varepsilon_{\rm oracle}\) with covariance confidence \(1-\alpha_{\rm cov}\).

Now write \(s=d_\phi/d_\star\). Since \(s\in[a,b]\),

\[
\widehat\Sigma_\star
=s\left(\frac{X^\mathsf TP_HX}{d_\phi}\right).
\]

The triangle inequality gives

\[
\left\|\Sigma^{-1/2}(\widehat\Sigma_\star-\Sigma)\Sigma^{-1/2}\right\|_2
\le |s-1|+s\varepsilon_{\rm oracle}.
\]

The right-hand side is maximized at an endpoint of \([a,b]\), yielding \(\varepsilon_\star\). A union bound combines calibration failure and covariance-concentration failure. \(\square\)

## Exact reduction to Proposition 43

When \(q=1\), the rank-only lower normalization becomes

\[
d_-=N-S_\rho,
\]

which is exactly the normalization lower bound used by Proposition 43 for ordinary constant mean-centering. The implementation includes a regression test checking that the full numerical bound agrees with Proposition 43 in this case.

## Experiment AE

[![Experiment AE: estimated AR(1) plus affine nuisance projection](estimated_ar1_nuisance_projection.svg)](estimated_ar1_nuisance_projection.svg)

Experiment AE uses 20 standardized calibration channels of length 700 and a separate four-dimensional target record of length 850. The target mean contains a large unknown affine drift. For each true \(\phi\in\{0.10,0.40,0.65\}\), 64 seeded trials were run.

Across the recorded trials:

- all 192 AR(1) intervals contained the true \(\phi\);
- all 192 calibrated projected covariance errors lay below the Proposition 45 radius;
- median calibrated relative covariance error was about 0.108, 0.139, and 0.170 at \(\phi=0.10,0.40,0.65\), respectively;
- corresponding median oracle errors were about 0.109, 0.140, and 0.169;
- ordinary constant mean-centering had median relative error above 61 in every regime.

The radius becomes conservative for strong temporal dependence. At \(\phi=0.65\), its median value is about 1.217. That covariance statement remains valid, but a downstream perturbation theorem that requires relative error below one cannot use it. This limitation led directly to Propositions 46 and 47.

[Machine-readable Experiment AE results](estimated_ar1_nuisance_projection.json) · [reproducible script](../examples/estimated_ar1_nuisance_projection.py) · [claim-level tests](../tests/test_estimated_nuisance.py)

## What this closes

The target covariance layer now supports all of the following at once:

1. an unknown time-varying mean \(HB\) inside a fixed declared temporal subspace;
2. non-IID Gaussian sampling with a shared nonnegative stationary AR(1) coefficient;
3. estimation of that coefficient from observable standardized calibration channels;
4. uncertainty in the unknown projected covariance normalization;
5. a finite-sample simultaneous population-relative covariance radius.

## Remaining frontier

Proposition 45 is still conservative because it uses only the nuisance rank and a sphere-net concentration argument. Proposition 46 addresses the first issue. Proposition 47 addresses the second when the projected temporal spectrum is known.
