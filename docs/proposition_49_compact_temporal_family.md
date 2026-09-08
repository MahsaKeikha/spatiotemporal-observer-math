# Proposition 49: matrix concentration over a compact temporal covariance family

Proposition 48 made the direct matrix concentration theorem uniform over an estimated one-parameter AR(1) interval. Proposition 49 removes the AR(1)-specific continuum argument from the theorem itself.

The new result starts from a finite deterministic cover of an arbitrary compact family of temporal covariance matrices. If the cover controls the projected temporal operator norm and projected normalization, then the exact Gaussian matrix moment-generating-function argument from Proposition 47 extends uniformly to the full family.

This separates two mathematical tasks:

1. **family geometry:** certify that every admissible temporal covariance is close to some finite cover point;
2. **matrix concentration:** turn that deterministic cover into one simultaneous covariance radius.

The first task depends on the chosen temporal model. The second no longer does.

## Setup

Let the target record be

\[
X=HB+R^{1/2}Z\Sigma^{1/2},
\]

where:

- \(H\in\mathbb R^{N\times q}\) is fixed before inspecting the target record;
- \(H\) has full column rank and \(q<N\);
- \(B\) is arbitrary and unknown;
- \(Z\) has independent standard normal entries;
- \(\Sigma\succ0\) is the spatial covariance;
- \(R\) belongs to a declared compact family \(\mathcal R\) of positive semidefinite temporal covariance matrices.

Let \(U\in\mathbb R^{N\times(N-q)}\) have orthonormal columns spanning the orthogonal complement of the nuisance design. Then

\[
P=UU^\mathsf T
\]

is the nuisance projector, and the nonzero projected temporal spectrum is exactly the spectrum of

\[
C(R)=U^\mathsf T R U.
\]

The projected normalization is

\[
d(R)=\operatorname{tr}(PR)=\operatorname{tr}(C(R)).
\]

## Step 1: a certified finite cover

Choose deterministic cover matrices

\[
R_1,\ldots,R_G.
\]

For every admissible \(R\in\mathcal R\), assume there is at least one cover point \(R_j\) such that

\[
\|C(R)-C(R_j)\|_2\le\delta_\lambda
\]

and

\[
|d(R)-d(R_j)|\le\delta_d.
\]

The two radii serve different purposes. The operator radius controls every temporal eigenvalue. The normalization radius controls the denominator of the observable projected covariance estimator.

Define the cover-point normalizations

\[
d_j=\operatorname{tr}(C(R_j)).
\]

Then the complete family obeys

\[
d_-\le d(R)\le d_+,
\]

where

\[
d_-=\min_j d_j-\delta_d,
\qquad
d_+=\max_j d_j+\delta_d.
\]

The theorem requires \(d_->0\).

## Step 2: control the complete projected spectrum

Let

\[
0\le\lambda_{1j}\le\cdots\le\lambda_{rj},
\qquad r=N-q,
\]

be the eigenvalues of \(C(R_j)\).

If \(R\) is assigned to cover point \(R_j\), Weyl's inequality gives

\[
|\lambda_i(C(R))-\lambda_{ij}|\le\delta_\lambda
\]

for every ordered eigenvalue.

Therefore the inflated cover spectrum

\[
\widetilde\lambda_{ij}=\lambda_{ij}+\delta_\lambda
\]

satisfies

\[
\lambda_i(C(R))\le\widetilde\lambda_{ij}.
\]

Define

\[
S_+=\max_{i,j}\widetilde\lambda_{ij}.
\]

## Step 3: reuse the exact Gaussian matrix mgf

Proposition 47 evaluates the exact Gaussian rank-one matrix exponential moment through the scalar factors

\[
f_+(a)=\log\left[
 e^{-a}\frac{m-1+(1-2a)^{-m/2}}{m}
\right],
\qquad 0\le a<1/2,
\]

and

\[
f_-(a)=\log\left[
 e^{a}\frac{m-1+(1+2a)^{-m/2}}{m}
\right],
\qquad a\ge0.
\]

Proposition 48 proved that both factors are nondecreasing in \(a\). Hence, for every admissible temporal covariance assigned to cover point \(j\),

\[
\sum_i f_+(\theta\lambda_i(C(R)))
\le
\sum_i f_+(\theta\widetilde\lambda_{ij})
\]

and

\[
\sum_i f_-(\theta\lambda_i(C(R)))
\le
\sum_i f_-(\theta\widetilde\lambda_{ij}).
\]

Taking the maximum over the deterministic cover points yields a valid moment bound for the entire compact family.

**There is no probability union bound over cover points.** The cover is used only to construct one deterministic worst-case mgf envelope before the probability inequality is applied.

## Step 4: uniform matrix Chernoff tails

Let \(B_0\) be the number of declared covariance blocks and let their dimension be at most \(m\). Let the desired covariance confidence be \(1-\alpha\).

For any

\[
0<\theta<\frac{1}{2S_+},
\]

define

\[
T_+(\theta)
=
\frac{
\log(2B_0m/\alpha)
+
\max_j\sum_i f_+(\theta\widetilde\lambda_{ij})
}{\theta d_-}.
\]

For \(\theta>0\), define

\[
T_-(\theta)
=
\frac{
\log(2B_0m/\alpha)
+
\max_j\sum_i f_-(\theta\widetilde\lambda_{ij})
}{\theta d_-}.
\]

For any deterministic finite candidate sets \(\Theta_+\) and \(\Theta_-\), let

\[
\varepsilon_+=\min_{\theta\in\Theta_+}T_+(\theta)
\]

and

\[
\varepsilon_-
=
\min\left\{1,
\min_{\theta\in\Theta_-}T_-(\theta)
\right\}.
\]

The finite theta sets affect numerical tightness only. Every individual theta already gives a valid family-uniform Chernoff bound.

With probability at least \(1-\alpha\), the oracle-normalized estimator satisfies

\[
-\varepsilon_- I
\preceq
\Sigma^{-1/2}
\left(
\frac{X^\mathsf TPX}{d(R)}-\Sigma
\right)
\Sigma^{-1/2}
\preceq
\varepsilon_+ I
\]

uniformly for every \(R\in\mathcal R\) covered by the declared deterministic envelope.

## Step 5: remove the unknown normalization

The exact normalization \(d(R)\) is not assumed known. Define the deterministic reference

\[
d_\star=\frac{d_-+d_+}{2}
\]

and the observable estimator

\[
\widehat\Sigma_\star=\frac{X^\mathsf TPX}{d_\star}.
\]

Put

\[
a=\frac{d_-}{d_\star},
\qquad
b=\frac{d_+}{d_\star}.
\]

The final upper and lower deviations are

\[
\varepsilon_{\rm final,+}=b(1+\varepsilon_+)-1
\]

and

\[
\varepsilon_{\rm final,-}
=
\max\{0,1-a(1-\varepsilon_-)\}.
\]

Therefore

\[
\varepsilon_{49}
=
\max\{\varepsilon_{\rm final,+},
\varepsilon_{\rm final,-}\}
\]

satisfies

\[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma_\star-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le\varepsilon_{49}
\]

with probability at least \(1-\alpha\).

## Proposition 49

**Proposition 49 (compact temporal-family matrix concentration).** Consider the Gaussian separable target model above with a nuisance design fixed before the target record is inspected. Suppose a deterministic finite cover of the declared compact temporal covariance family satisfies the projected operator and normalization covering conditions with radii \(\delta_\lambda\) and \(\delta_d\), and suppose \(d_->0\). Then the estimator

\[
\widehat\Sigma_\star=\frac{X^\mathsf TPX}{d_\star}
\]

obeys

\[
\Pr\left[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma_\star-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le\varepsilon_{49}
\right]
\ge1-\alpha.
\]

The theorem is conditional on the deterministic cover being valid for the entire intended temporal family. It does not infer that cover from the same target record.

## Exact reductions

Two consistency reductions are important.

### One cover point, zero covering radii

If \(G=1\), \(\delta_\lambda=0\), and \(\delta_d=0\), the temporal covariance is known exactly. Proposition 49 reduces to Proposition 47.

The claim-level test suite verifies equality of the upper tail, lower tail, and final relative covariance radius to numerical precision.

### AR(1) interval

Proposition 48 is recovered by choosing the cover points from an AR(1) grid and supplying the Proposition 46 spectral and normalization continuum radii. Proposition 49 therefore contains the concentration mechanism of Proposition 48, while allowing the geometry layer to be replaced.

---

# A two-parameter corollary

Experiment AI uses the family

\[
R_{\phi,\eta}
=
(1-\eta)R_\phi+\eta I,
\]

where

\[
\phi\in[\ell,\rho],
\qquad
\eta\in[\eta_-,\eta_+].
\]

The parameter \(\eta\) is a white-noise fraction. Every family member remains positive semidefinite with unit diagonal.

## Product-grid operator cover

For AR(1), a row-sum derivative bound gives

\[
\left\|\frac{\partial R_\phi}{\partial\phi}\right\|_2
\le
L_\phi
=
2\sum_{k=1}^{N-1}k\rho^{k-1}.
\]

For the second parameter,

\[
\frac{\partial R_{\phi,\eta}}{\partial\eta}
=I-R_\phi.
\]

Using

\[
\|R_\phi\|_2
\le
\frac{1+\rho}{1-\rho},
\]

a valid bound is

\[
L_\eta
=
\max\left\{1,
\frac{1+\rho}{1-\rho}-1
\right\}.
\]

If the maximum product-grid spacings are \(h_\phi\) and \(h_\eta\), every family member is within

\[
\delta_R
=
\frac{L_\phi h_\phi}{2}
+
\frac{L_\eta h_\eta}{2}
\]

in operator norm of a grid point.

Orthogonal compression cannot increase spectral norm, so

\[
\delta_\lambda=\delta_R.
\]

Every family member has trace \(N\). Therefore the trace difference of two family members is zero, and

\[
\operatorname{tr}(P\Delta R)
=-\operatorname{tr}(Q_H^\mathsf T\Delta RQ_H),
\]

where \(Q_H\) has \(q\) orthonormal columns spanning the nuisance space. Hence

\[
|\operatorname{tr}(P\Delta R)|
\le q\|\Delta R\|_2,
\]

so a valid normalization covering radius is

\[
\delta_d=q\delta_R.
\]

This provides a fully analytic deterministic cover certificate for the two-parameter family.

---

# Experiment AI

[![Experiment AI: compact temporal family concentration](compact_temporal_family.svg)](compact_temporal_family.svg)

Experiment AI fixes:

- record length `N=400`;
- spatial covariance dimension `4`;
- one declared covariance block;
- affine nuisance design `intercept + linear trend`;
- covariance confidence `0.975`;
- temporal family `R(phi, eta) = (1 - eta) R_phi + eta I`;
- `phi in [0.45, 0.72]`;
- `eta in [0.00, 0.05]`;
- 1024 deterministic Chernoff theta candidates per tail.

The product cover is refined while the temporal family itself stays fixed.

| Product cover | Cover points | Proposition 49 radius | Sphere-net family radius | Reduction |
| --- | ---: | ---: | ---: | ---: |
| `5 x 3` | 15 | 1.104 | 3.002 | 63.2% |
| `9 x 5` | 45 | **0.957** | 2.572 | 62.8% |
| `17 x 9` | 153 | **0.891** | 2.358 | 62.2% |

The scientific transition is the crossing of the relative-error threshold one. A coarse certified cover is too loose at `1.104`. Refining only the deterministic temporal geometry, without changing the data length, confidence, spatial dimension, or parameter family, lowers the certificate to `0.957` and then `0.891`.

The corresponding sphere-net family certificate remains above two throughout the displayed refinement.

## Seeded target-record visibility checks

The final `17 x 9` family certificate was also compared with seeded target records containing a large unknown affine mean.

| True `(phi, eta)` | Trials | Median error | 95th percentile | Maximum | Proposition 49 radius | Covered |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `(0.60, 0.02)` | 96 | 0.250 | 0.339 | 0.403 | 0.891 | 96 / 96 |
| `(0.70, 0.04)` | 96 | 0.272 | 0.417 | 0.660 | 0.891 | 96 / 96 |

For 96 successes in 96 trials, the two-sided 95% Wilson interval is approximately `[0.962, 1.000]`. These runs are visibility and scale checks. They are not the proof of Proposition 49.

[Machine-readable Experiment AI results](compact_temporal_family.json) · [reproducible script](../examples/compact_temporal_family.py) · [claim-level tests](../tests/test_compact_temporal_family.py)

## What Proposition 49 changes

Proposition 48 solved uncertainty in one scalar AR(1) coefficient. Proposition 49 changes the architecture of the argument:

```text
known temporal covariance
        -> Proposition 47
one-dimensional AR(1) interval
        -> Proposition 48
arbitrary compact family with a certified finite cover
        -> Proposition 49
```

The concentration theorem is now modular. A future temporal model only needs its own deterministic cover theorem; the direct Gaussian matrix concentration layer can be reused unchanged.

## Remaining frontier

The result is still conditional on exact Gaussian temporal-spatial separability and on a deterministic cover that is valid independently of the target record.

The next major statistical question is therefore no longer how to cover a known parametric family. It is how to construct a **data-calibrated confidence set for a multi-parameter or nonparametric temporal covariance family** and compose that random family with Proposition 49 without overstating confidence.
