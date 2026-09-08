# Proposition 46 — design-specific uniform AR(1) envelopes over a calibrated interval

Proposition 45 uses only the nuisance rank \(q\) when the AR(1) coefficient is unknown. That is safe, but it can be extremely loose because it assumes the nuisance subspace could align with the worst possible temporal directions. Proposition 46 uses the **actual predeclared nuisance geometry** \(H\) while retaining a finite-sample continuum guarantee over the calibrated AR(1) interval.

The key technical point is that evaluating a few values of \(\phi\) is not itself a proof over an interval. Proposition 46 closes the gaps between grid points analytically with Lipschitz bounds for the AR(1) Toeplitz family.

## Statement

Let

\[
R_\phi=(\phi^{|i-j|})_{i,j=1}^N,
\qquad 0\le \phi<1,
\]

and let \(H\in\mathbb R^{N\times q}\) be fixed before inspecting the target record, with full column rank \(q<N\). Define

\[
P=I-H(H^\mathsf TH)^{-1}H^\mathsf T,
\qquad Q=I-P.
\]

Suppose an observable calibration step produces a confidence interval

\[
\phi\in[\ell,\rho],
\qquad 0\le \ell\le\rho<1.
\]

Choose a deterministic grid

\[
\ell=\phi_1<\phi_2<\cdots<\phi_G=\rho
\]

with maximum spacing \(h\). At each grid point define

\[
d_j=\operatorname{tr}(PR_{\phi_j}),
\qquad
F_j=\|PR_{\phi_j}P\|_F,
\qquad
S_j=\|PR_{\phi_j}P\|_2.
\]

Define the derivative envelopes

\[
L_F(\rho)
=
\left[
2\sum_{k=1}^{N-1}(N-k)k^2\rho^{2(k-1)}
\right]^{1/2},
\]

and

\[
L_2(\rho)
=
2\sum_{k=1}^{N-1}k\rho^{k-1}.
\]

Then every \(\phi\in[\ell,\rho]\) satisfies

\[
\operatorname{tr}(PR_\phi)
\ge
\min_j d_j-rac{qL_2(\rho)h}{2},
\]

\[
\operatorname{tr}(PR_\phi)
\le
\max_j d_j+rac{qL_2(\rho)h}{2},
\]

\[
\|PR_\phi P\|_F
\le
\max_j F_j+rac{L_F(\rho)h}{2},
\]

and

\[
\|PR_\phi P\|_2
\le
\max_j S_j+rac{L_2(\rho)h}{2}.
\]

These design-specific bounds may safely be intersected with Proposition 45's global fallbacks

\[
\operatorname{tr}(PR_\phi)
\ge
N-q\,\bar S_\rho,
\qquad
\operatorname{tr}(PR_\phi)\le N,
\]

\[
\|PR_\phi P\|_F\le \bar F_\rho,
\qquad
\|PR_\phi P\|_2\le \bar S_\rho,
\]

where

\[
\bar F_\rho^2
=N+2\sum_{k=1}^{N-1}(N-k)\rho^{2k},
\qquad
\bar S_\rho
=\min\left\{N,\frac{1+\rho}{1-\rho}\right\}.
\]

Let the resulting certified bounds be

\[
d_-\le \operatorname{tr}(PR_\phi)\le d_+,
\qquad
\|PR_\phi P\|_F\le F_+,
\qquad
\|PR_\phi P\|_2\le S_+,
\]

with \(d_->0\). Set

\[
d_\star=\frac{d_-+d_+}{2}.
\]

For a target record

\[
X=HB+R_\phi^{1/2}Z\Sigma^{1/2},
\]

use the observable estimator

\[
\widehat\Sigma_\star=
\frac{X^\mathsf TPX}{d_\star}.
\]

For \(B_0\) predeclared covariance blocks of dimension at most \(m\), let

\[
u=\log\left(\frac{2B_0 9^m}{\alpha_{\rm cov}}\right)
\]

and

\[
\varepsilon_{\rm oracle}
=
\frac{4(F_+\sqrt{u}+S_+u)}{d_-}.
\]

With

\[
a=\frac{d_-}{d_\star},
\qquad
b=\frac{d_+}{d_\star},
\]

define

\[
\varepsilon_\star
=
\max\left\{
|a-1|+a\varepsilon_{\rm oracle},
|b-1|+b\varepsilon_{\rm oracle}
\right\}.
\]

If the AR(1) interval has confidence \(1-\alpha_{\rm cal}\), then with confidence at least

\[
1-\alpha_{\rm cal}-\alpha_{\rm cov},
\]

simultaneously over the declared blocks,

\[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma_\star-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le\varepsilon_\star.
\]

## Proof of the continuum envelope

For \(i\ne j\),

\[
\frac{d}{d\phi}(R_\phi)_{ij}
=|i-j|\phi^{|i-j|-1},
\]

and the diagonal derivative is zero. Therefore

\[
\|R_\phi'\|_F^2
=
2\sum_{k=1}^{N-1}(N-k)k^2\phi^{2(k-1)}
\le L_F(\rho)^2.
\]

The absolute row sum is bounded by the two-sided lag sum,

\[
\|R_\phi'\|_2
\le\|R_\phi'\|_\infty
\le
2\sum_{k=1}^{N-1}k\rho^{k-1}
=L_2(\rho).
\]

Projection is contractive:

\[
\|PAP\|_F\le\|A\|_F,
\qquad
\|PAP\|_2\le\|A\|_2.
\]

Hence, by the fundamental theorem of calculus,

\[
\|P(R_\phi-R_\psi)P\|_F
\le L_F(\rho)|\phi-\psi|,
\]

and

\[
\|P(R_\phi-R_\psi)P\|_2
\le L_2(\rho)|\phi-\psi|.
\]

The reverse triangle inequality immediately gives the claimed Lipschitz bounds for the projected Frobenius and spectral norms.

For the normalization, use \(\operatorname{tr}(R_\phi)=N\) for every \(\phi\), so

\[
d(\phi)=\operatorname{tr}(PR_\phi)
=N-\operatorname{tr}(QR_\phi).
\]

Because \(Q\) is an orthogonal projector of rank \(q\),

\[
|d'(\phi)|
=|\operatorname{tr}(QR_\phi')|
\le q\|R_\phi'\|_2
\le qL_2(\rho).
\]

Every point in the interval lies within \(h/2\) of some grid point. Applying the three Lipschitz inequalities at that nearest point proves all four continuum bounds.

The global Proposition 45 inequalities are independently valid, so intersecting the two sets of bounds preserves validity and can only tighten the envelope.

Finally, on the calibration event the true \(\phi\) belongs to the reported interval, so the true projected temporal norms and normalization obey the design envelope. Proposition 44's Gaussian quadratic-form event is then dominated by the displayed worst-case oracle radius. The midpoint-normalization algebra is the same as Proposition 45. A union bound combines calibration failure and covariance-concentration failure. Independence is not required. \(\square\)

## Why this is stronger than Proposition 45

Proposition 45 lower-bounds the projected normalization using

\[
N-q\|R_\phi\|_2.
\]

That treats the nuisance space as if all \(q\) nuisance directions could simultaneously align with the strongest temporal covariance directions. For a declared smooth basis this can be much too pessimistic.

Proposition 46 directly evaluates how **this particular** \(H\) interacts with the AR(1) family and then rigorously fills the continuum between evaluations. It uses both ends of the calibrated interval, not only its upper endpoint.

## Experiment AF — when rank-only control becomes vacuous

[![Experiment AF: design-specific versus rank-only AR(1) envelopes](design_specific_ar1_envelope.svg)](design_specific_ar1_envelope.svg)

Experiment AF fixes \(N=300\), \(\phi\in[0.75,0.85]\), a four-dimensional covariance block, 97.5% covariance confidence, and a predeclared low-frequency cosine nuisance basis. The nuisance rank increases through \(q\in\{2,8,16,24,25\}\).

The result isolates the geometry effect:

- at \(q=2\), the design-specific covariance radius improves from about `4.865` to `4.561`;
- at \(q=8\), it improves from `7.764` to `5.021`;
- at \(q=16\), it improves from `18.966` to `5.348`;
- at \(q=24\), the rank-only lower normalization collapses to `4`, producing a radius of about `629.1`, while the design-specific continuum proof retains a lower normalization above `103.6` and a finite radius about `5.833`;
- at \(q=25\), Proposition 45's rank-only lower normalization is negative (`-8.33`) and cannot certify the covariance at all, while Proposition 46 retains a certified lower normalization about `99.75` and a finite radius about `5.904`.

This experiment is not claiming those large radii are useful for every downstream observer-score perturbation. Its purpose is narrower and structural: **the failure of the rank-only certificate can be an artifact of throwing away the declared nuisance geometry, not a failure of covariance identifiability after projection.**

[Machine-readable Experiment AF results](design_specific_ar1_envelope.json) · [reproducible script](../examples/design_specific_ar1_envelope.py) · [claim-level tests](../tests/test_design_interval.py)

## Remaining frontier

Proposition 46 makes the AR(1) interval geometry-aware, but it still assumes:

- Gaussian separability;
- stationary nonnegative AR(1) temporal dependence;
- a fixed nuisance design chosen before inspecting the target record;
- standardized calibration channels satisfying Proposition 43;
- the existing \(1/4\)-net Gaussian quadratic-form constant in the covariance concentration step.

The next major tightening opportunity is therefore no longer the nuisance normalization. It is the **matrix concentration layer itself**: replace the sphere-net factor with a sharper weighted-Wishart / Gaussian matrix bound that depends directly on the projected temporal eigenvalue profile. That is the most direct route to bringing the valid radius below one in strongly correlated regimes.
