# Proposition 48: uniform matrix concentration over a calibrated AR(1) interval

Proposition 47 sharply improves the dependent Gaussian covariance radius when the projected temporal spectrum is known. Proposition 48 removes that oracle requirement for the current AR(1) model class.

The result combines three earlier ideas:

1. Proposition 43 supplies an observable confidence interval for a shared nonnegative AR(1) coefficient.
2. Proposition 46 uses the actual nuisance design to control projected temporal geometry over the entire interval.
3. Proposition 47 gives direct matrix concentration when the temporal eigenvalues are known.

The new step is to control the **full projected eigenvalue profile between AR(1) grid points**, not only its largest eigenvalue and Frobenius norm.

## Setup

Let the target record be

\[
X=HB+R_\phi^{1/2}Z\Sigma^{1/2},
\]

where:

- \(H\in\mathbb R^{N\times q}\) is fixed before inspecting the target record;
- \(H\) has full column rank and \(q<N\);
- \(B\) is arbitrary and unknown;
- \(Z\) has independent standard normal entries;
- \(\Sigma\succ0\) is the spatial covariance;
- \(R_\phi\) is the stationary AR(1) temporal correlation matrix,

\[
(R_\phi)_{ij}=\phi^{|i-j|},
\qquad 0\le\phi<1.
\]

Define

\[
P=I-H(H^\mathsf TH)^{-1}H^\mathsf T
\]

and

\[
A(\phi)=PR_\phi P.
\]

Suppose the calibration layer reports

\[
\phi\in[\ell,\rho]
\]

with confidence \(1-\alpha_{\rm cal}\).

## Step 1: a rigorous AR(1) grid

Choose a deterministic grid

\[
\ell=\phi_1<\phi_2<\cdots<\phi_G=\rho
\]

with maximum spacing \(h\). Every coefficient in the interval is within \(h/2\) of at least one grid point.

Proposition 46 gives a uniform spectral Lipschitz constant \(L_2\) such that

\[
\|A(\phi)-A(\psi)\|_2
\le L_2|\phi-\psi|.
\]

Therefore, if \(\phi_j\) is the nearest grid point,

\[
\|A(\phi)-A(\phi_j)\|_2
\le \delta_\lambda,
\qquad
\delta_\lambda=\frac{L_2h}{2}.
\]

## Step 2: control every temporal eigenvalue

Let the ordered eigenvalues of \(A(\phi)\) be

\[
0\le\lambda_1(\phi)\le\cdots\le\lambda_N(\phi).
\]

Weyl's eigenvalue perturbation inequality gives

\[
|\lambda_i(\phi)-\lambda_i(\phi_j)|
\le\|A(\phi)-A(\phi_j)\|_2
\le\delta_\lambda
\]

for every \(i\).

Proposition 46 also supplies a uniform spectral upper bound \(S_+\), so

\[
\lambda_i(\phi)
\le
\min\{S_+,\lambda_i(\phi_j)+\delta_\lambda\}.
\]

Define the inflated grid spectrum

\[
\widetilde\lambda_{ij}
=
\min\{S_+,\lambda_i(\phi_j)+\delta_\lambda\}.
\]

This is the bridge from the finite grid to the full interval.

## Step 3: the exact Gaussian matrix mgf is monotone in each eigenvalue

Proposition 47 uses

\[
f_+(a)=\log c_m^+(a)
\]

with

\[
c_m^+(a)
=e^{-a}\frac{m-1+(1-2a)^{-m/2}}{m},
\qquad 0\le a<1/2,
\]

and

\[
f_-(a)=\log c_m^-(a)
\]

with

\[
c_m^-(a)
=e^a\frac{m-1+(1+2a)^{-m/2}}{m},
\qquad a\ge0.
\]

Both log-mgf factors are nondecreasing on their domains.

For the upper tail,

\[
f_+'(a)
=-1+
\frac{m(1-2a)^{-m/2-1}}
{m-1+(1-2a)^{-m/2}}
\ge0.
\]

For the lower tail,

\[
f_-'(a)
=1-
\frac{m(1+2a)^{-m/2-1}}
{m-1+(1+2a)^{-m/2}}
\ge0.
\]

The inequalities follow directly from \((1-2a)^{-1}\ge1\) in the upper case and \((1+2a)^{-1}\le1\) in the lower case.

Therefore, for any admissible \(\theta\),

\[
\sum_i f_+(\theta\lambda_i(\phi))
\le
\sum_i f_+(\theta\widetilde\lambda_{ij})
\]

and

\[
\sum_i f_-(\theta\lambda_i(\phi))
\le
\sum_i f_-(\theta\widetilde\lambda_{ij}).
\]

Taking the maximum over grid points gives a matrix-mgf bound that is valid for **every** \(\phi\in[\ell,\rho]\).

## Step 4: uniform matrix Chernoff tails

Let \(B_0\) be the number of declared covariance blocks, each of dimension at most \(m\), and let \(1-\alpha_{\rm cov}\) be the covariance confidence.

Proposition 46 supplies

\[
d_-\le\operatorname{tr}(A(\phi))\le d_+,
\qquad d_->0.
\]

For any

\[
0<\theta<\frac{1}{2S_+},
\]

define

\[
T_+(\theta)
=
\frac{
\log(2B_0m/\alpha_{\rm cov})
+
\max_j\sum_i f_+(\theta\widetilde\lambda_{ij})
}{\theta d_-}.
\]

For the lower tail, for any \(\theta>0\), define

\[
T_-(\theta)
=
\frac{
\log(2B_0m/\alpha_{\rm cov})
+
\max_j\sum_i f_-(\theta\widetilde\lambda_{ij})
}{\theta d_-}.
\]

Let

\[
\varepsilon_+
=
\min_{\theta\in\Theta_+}T_+(\theta),
\]

and

\[
\varepsilon_-
=
\min\left\{1,
\min_{\theta\in\Theta_-}T_-(\theta)
\right\}.
\]

The finite theta sets \(\Theta_+\) and \(\Theta_-\) affect tightness only. Every individual theta in those deterministic sets already gives a valid continuum bound.

With covariance confidence at least \(1-\alpha_{\rm cov}\), the oracle-normalized covariance therefore satisfies

\[
-(\varepsilon_-)I
\preceq
\Sigma^{-1/2}
\left(
\frac{X^\mathsf TPX}{d(\phi)}-\Sigma
\right)
\Sigma^{-1/2}
\preceq
\varepsilon_+I,
\]

where

\[
d(\phi)=\operatorname{tr}(A(\phi)).
\]

## Step 5: remove the unknown normalization

The exact normalization \(d(\phi)\) is unknown because \(\phi\) is unknown. Use the observable midpoint

\[
d_\star=\frac{d_-+d_+}{2}
\]

and estimator

\[
\widehat\Sigma_\star
=
\frac{X^\mathsf TPX}{d_\star}.
\]

Put

\[
a=\frac{d_-}{d_\star},
\qquad
b=\frac{d_+}{d_\star}.
\]

Since \(d(\phi)/d_\star\in[a,b]\), the final upper deviation is bounded by

\[
\varepsilon_{\rm final,+}
=b(1+\varepsilon_+)-1,
\]

and the final lower deviation by

\[
\varepsilon_{\rm final,-}
=
\max\{0,1-a(1-\varepsilon_-)\}.
\]

Thus

\[
\varepsilon_{48}
=
\max\{\varepsilon_{\rm final,+},\varepsilon_{\rm final,-}\}
\]

satisfies

\[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma_\star-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le\varepsilon_{48}.
\]

## Proposition 48

Under the stated Gaussian separable AR(1) model and a fixed predeclared nuisance design, if the calibration interval has confidence \(1-\alpha_{\rm cal}\) and the matrix covariance event has confidence \(1-\alpha_{\rm cov}\), then

\[
\Pr\left[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma_\star-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le\varepsilon_{48}
\right]
\ge
1-\alpha_{\rm cal}-\alpha_{\rm cov}.
\]

No independence between the calibration event and covariance event is required for this union-bound statement. On the calibration event, the true \(\phi\) lies in the reported interval. The Proposition 48 interval radius then dominates the valid known-\(\phi\) Proposition 47 covariance radius at that true coefficient. The deterministic normalization algebra completes the implication.

## Exact reduction when the interval collapses

If \(\ell=\rho=\phi\), then \(h=0\) and \(\delta_\lambda=0\). There is one temporal spectrum and no continuum inflation. Proposition 48 reduces to the known-\(\phi\) Proposition 47 matrix bound, apart from negligible floating-point outward protection in the shared normalization envelope.

The test suite checks this reduction numerically and also checks 41 intermediate coefficients in a nondegenerate interval against their exact Proposition 47 bounds.

## Experiment AH

[![Experiment AH: interval-uniform matrix concentration](uniform_matrix_chernoff_ar1.svg)](uniform_matrix_chernoff_ar1.svg)

Experiment AH fixes `N=500`, dimension four, an affine nuisance design, 97.5% covariance confidence, 17 AR(1) grid points, and 1024 matrix-Chernoff theta candidates per tail.

| AR(1) interval | Proposition 46 sphere-net radius | Proposition 48 matrix radius | known midpoint oracle | reduction |
| --- | ---: | ---: | ---: | ---: |
| `[0.05, 0.15]` | 0.812 | **0.378** | 0.369 | 53.4% |
| `[0.35, 0.45]` | 1.086 | **0.473** | 0.442 | 56.5% |
| `[0.60, 0.70]` | 1.740 | **0.705** | 0.619 | 59.5% |
| `[0.70, 0.80]` | 2.409 | **0.931** | 0.770 | 61.3% |

The last interval is the main result. Proposition 46 remains above one at `2.409`. Proposition 48 is below one at `0.931` even though the exact AR(1) coefficient is not supplied.

Two seeded finite-sample visibility checks were also run with a large unknown affine target mean:

- true `phi=0.65`, declared interval `[0.60, 0.70]`: all 96 target errors were below the `0.705` radius; median error was `0.226`, and the maximum was `0.457`;
- true `phi=0.75`, declared interval `[0.70, 0.80]`: all 96 target errors were below the `0.931` radius; median error was `0.269`, and the maximum was `0.574`.

These simulations make the scale visible. They are not the proof.

[Machine-readable Experiment AH results](uniform_matrix_chernoff_ar1.json) · [reproducible script](../examples/uniform_matrix_chernoff_ar1.py) · [claim-level tests](../tests/test_uniform_matrix_chernoff.py)

## What Proposition 48 closes

Within the current Gaussian separable AR(1) model class, the covariance layer can now combine all of the following in one certificate:

- an unknown time-varying mean inside a fixed declared nuisance subspace;
- an unknown shared nonnegative AR(1) coefficient;
- observable finite-sample calibration of that coefficient;
- the actual geometry of the nuisance design over the entire calibrated interval;
- direct matrix concentration using the full projected temporal eigenvalue profile;
- uncertainty in the projected covariance normalization.

## Remaining frontier

The strongest current result is still model dependent. It assumes Gaussianity, temporal and spatial separability, stationary AR(1) dependence, valid standardized calibration channels, and a nuisance design fixed before inspecting the target record.

The next research step should move beyond the single-parameter AR(1) temporal family. Natural directions include a multi-parameter stationary temporal model, a spectral-density envelope, or a nonparametric dependence class with a finite-sample matrix concentration certificate.
