# Proposition 50: observable calibration of a two-parameter temporal family

Proposition 49 gives a matrix covariance certificate for any compact temporal covariance family once a valid deterministic finite cover is supplied. Proposition 50 adds the statistical layer that Proposition 49 deliberately left open.

The goal is to learn a confidence region for a two-parameter temporal covariance family from an independent calibration record, then use that random region safely in the Proposition 49 concentration theorem for a separate target record.

The result is still conditional mathematics. It strengthens the reliability of the dependent-Gaussian covariance layer used elsewhere in this repository. It does not establish a claim about consciousness.

## Temporal model

The temporal covariance family is

\[
R_{\phi,\eta}=(1-\eta)R_\phi+\eta I,
\]

where

\[
(R_\phi)_{ij}=\phi^{|i-j|}.
\]

The declared parameter box is

\[
0<\phi_-\le \phi\le \phi_+<1,
\qquad
0\le \eta_-\le \eta\le \eta_+<1.
\]

The parameter \(\eta\) is a white-noise fraction. Every member of the family is positive semidefinite and has unit diagonal.

For this family, the lag correlations are

\[
r_k=(1-\eta)\phi^k.
\]

In particular,

\[
r_1=(1-\eta)\phi,
\qquad
r_2=(1-\eta)\phi^2.
\]

Whenever \(r_1,r_2>0\), the parameter map is invertible:

\[
\phi=\frac{r_2}{r_1},
\qquad
\eta=1-\frac{r_1^2}{r_2}.
\]

This identity is the reason two lag statistics are enough for this two-parameter model.

---

# Calibration record

Let

\[
Y^{(1)},\ldots,Y^{(M)}\in\mathbb R^N
\]

be independent Gaussian calibration channels with common temporal covariance

\[
R_{\phi,\eta}.
\]

Each channel has known unit marginal variance and may have its own arbitrary unknown constant mean:

\[
\mathbb E Y^{(j)}=\mu_j\mathbf 1.
\]

The calibration channels are independent across \(j\). They are also independent of the target covariance record used later in the theorem.

The constant means are not estimated. They are removed algebraically by differencing.

## Lag operators

For \(k\in\{1,2\}\), define the lag-\(k\) difference operator

\[
D_k\in\mathbb R^{(N-k)\times N}
\]

by

\[
(D_k y)_t=y_{t+k}-y_t.
\]

Then

\[
D_k\mathbf 1=0,
\]

so every constant channel mean disappears exactly:

\[
D_kY^{(j)}=D_k\bigl(Y^{(j)}-\mu_j\mathbf 1\bigr).
\]

This is an exact invariance, not an approximation and not a preprocessing assumption.

---

# Step 1: lag-energy estimators

Define the total lag-\(k\) increment energy

\[
Q_k=\sum_{j=1}^M\|D_kY^{(j)}\|_2^2.
\]

Let

\[
B_k(\phi,\eta)=D_kR_{\phi,\eta}D_k^\mathsf T.
\]

Since each temporal marginal variance is one,

\[
\operatorname{tr} B_k(\phi,\eta)
=2(N-k)(1-r_k).
\]

Therefore

\[
\mathbb E Q_k
=2M(N-k)(1-r_k).
\]

The observable estimator

\[
\widehat r_k
=1-\frac{Q_k}{2M(N-k)}
\]

is exactly unbiased for \(r_k\).

The main technical question is how sharply \(Q_k\) concentrates.

---

# Step 2: use the increment spectrum instead of the raw process spectrum

A generic bound would start from

\[
\|D_kR_{\phi,\eta}D_k^\mathsf T\|_2
\le
\|D_k\|_2^2\|R_{\phi,\eta}\|_2.
\]

That is valid but can be extremely pessimistic when \(\phi\) is large, because the raw AR(1) spectral norm grows like

\[
\frac{1+\phi}{1-\phi}.
\]

The differencing filter suppresses exactly the low-frequency direction responsible for that growth. Proposition 50 therefore analyzes the increment covariance itself.

## AR(1) spectral symbol

The stationary AR(1) covariance sequence \(\phi^{|h|}\) has Fourier symbol

\[
s_\phi(\omega)
=
\frac{1-\phi^2}
{1+\phi^2-2\phi\cos\omega}.
\]

The lag-\(k\) difference filter has squared frequency response

\[
|e^{ik\omega}-1|^2
=2(1-\cos k\omega).
\]

Hence the AR(1) increment symbol is

\[
g_k(\omega)
=
2(1-\cos k\omega)
\frac{1-\phi^2}
{1+\phi^2-2\phi\cos\omega}.
\]

Every finite increment covariance is a finite Toeplitz section of this stationary increment process, so its spectral norm is bounded by the supremum of the corresponding symbol.

## Lag 1

Set

\[
x=1-\cos\omega\in[0,2].
\]

Then

\[
g_1(\omega)
=
\frac{2x(1-\phi^2)}
{(1-\phi)^2+2\phi x}.
\]

For \(0<\phi<1\), this expression is increasing in \(x\). Its maximum occurs at \(x=2\), or \(\omega=\pi\):

\[
\sup_\omega g_1(\omega)
=4\frac{1-\phi}{1+\phi}.
\]

The white-noise increment symbol is

\[
2(1-\cos\omega),
\]

whose maximum is four at the same frequency. Therefore the mixture satisfies

\[
\|B_1(\phi,\eta)\|_2
\le
4\left[
(1-\eta)\frac{1-\phi}{1+\phi}+\eta
\right].
\]

Over the declared parameter box, the right-hand side is largest at \((\phi_-,\eta_+)\). Define

\[
S_1
=
4\left[
(1-\eta_+)\frac{1-\phi_-}{1+\phi_-}+\eta_+
\right].
\]

## Lag 2

Write \(c=\cos\omega\). Since

\[
1-\cos 2\omega=2(1-c^2),
\]

we have

\[
g_2(\omega)
=
4(1-c^2)
\frac{1-\phi^2}
{1+\phi^2-2\phi c}.
\]

Differentiating the rational factor with respect to \(c\) gives the interior critical point

\[
c=\phi.
\]

That point gives the maximum:

\[
\sup_\omega g_2(\omega)
=4(1-\phi^2).
\]

The lag-2 white-noise difference has spectral norm at most four. By convexity of the mixture,

\[
\|B_2(\phi,\eta)\|_2
\le
4\left[(1-\eta)(1-\phi^2)+\eta\right].
\]

Again the declared-box maximum occurs at \((\phi_-,\eta_+)\). Define

\[
S_2
=
4\left[(1-\eta_+)(1-\phi_-^2)+\eta_+\right].
\]

These are increment-specific bounds. They are the main sharpening step in Proposition 50.

---

# Step 3: Frobenius bounds from trace and spectral control

For every positive semidefinite matrix \(B\),

\[
\|B\|_F^2
=\sum_i\lambda_i(B)^2
\le
\lambda_{\max}(B)\sum_i\lambda_i(B)
=
\|B\|_2\operatorname{tr}B.
\]

The smallest possible lag correlation over the declared box is

\[
r_{k,-}^{\rm dec}
=(1-\eta_+)\phi_-^k.
\]

Hence

\[
\operatorname{tr}B_k(\phi,\eta)
\le
T_k
=
2(N-k)\left[1-(1-\eta_+)\phi_-^k\right].
\]

With the spectral bounds above,

\[
\|B_k(\phi,\eta)\|_F
\le
F_k
=\sqrt{T_kS_k}.
\]

The code tests these three bounds, trace, Frobenius, and spectral, against dense exact matrices across a two-parameter rectangle.

---

# Step 4: simultaneous Gaussian quadratic-form concentration

Stack the \(M\) independent lag-\(k\) increment channels. Their joint covariance is block diagonal:

\[
I_M\otimes B_k.
\]

Therefore

\[
\|I_M\otimes B_k\|_F
=\sqrt M\,\|B_k\|_F
\le\sqrt M\,F_k,
\]

and

\[
\|I_M\otimes B_k\|_2
=\|B_k\|_2
\le S_k.
\]

For a centered Gaussian quadratic form with positive semidefinite covariance \(A\), the standard Gaussian quadratic-form inequality gives, for every \(t>0\),

\[
\Pr\left(
|Q-\operatorname{tr}A|
>
2\|A\|_F\sqrt t+2\|A\|_2t
\right)
\le2e^{-t}.
\]

Applying this to each lag yields

\[
|\widehat r_k-r_k|
\le
\varepsilon_k,
\]

where

\[
\varepsilon_k
=
\frac{F_k\sqrt t}{\sqrt M\,(N-k)}
+
\frac{S_kt}{M(N-k)}.
\]

Let the desired simultaneous calibration confidence be

\[
1-\alpha_{\rm cal}.
\]

Choose

\[
t=\log\frac{4}{\alpha_{\rm cal}}.
\]

Each two-sided lag event then fails with probability at most \(\alpha_{\rm cal}/2\). A union bound gives

\[
\Pr\left(
|\widehat r_1-r_1|\le\varepsilon_1,
\quad
|\widehat r_2-r_2|\le\varepsilon_2
\right)
\ge1-\alpha_{\rm cal}.
\]

No independence between the lag-1 and lag-2 statistics is required. They are computed from the same calibration data and are allowed to be dependent.

---

# Step 5: intersect with the declared model

The declared parameter box itself implies

\[
(1-\eta_+)\phi_-^k
\le r_k\le
(1-\eta_-)\phi_+^k.
\]

The observable lag interval is therefore

\[
L_k
=
\max\left\{
(1-\eta_+)\phi_-^k,
\widehat r_k-\varepsilon_k
\right\},
\]

\[
U_k
=
\min\left\{
(1-\eta_-)\phi_+^k,
\widehat r_k+\varepsilon_k
\right\}.
\]

If either interval is empty, the calibration data and declared model are inconsistent at the requested confidence level and the end-to-end API refuses to issue a certificate.

---

# Step 6: map the lag box into a parameter rectangle

On the simultaneous event,

\[
r_1\in[L_1,U_1],
\qquad
r_2\in[L_2,U_2].
\]

Because \(\phi=r_2/r_1\), a valid interval is

\[
\phi_{\rm cal,-}
=
\max\left\{
\phi_-,
\frac{L_2}{U_1}
\right\},
\]

\[
\phi_{\rm cal,+}
=
\min\left\{
\phi_+,
\frac{U_2}{L_1}
\right\}.
\]

Because

\[
\eta=1-\frac{r_1^2}{r_2},
\]

and this expression decreases with \(r_1\) and increases with \(r_2\), a valid interval is

\[
\eta_{\rm cal,-}
=
\max\left\{
\eta_-,
1-\frac{U_1^2}{L_2}
\right\},
\]

\[
\eta_{\rm cal,+}
=
\min\left\{
\eta_+,
1-\frac{L_1^2}{U_2}
\right\}.
\]

Thus, with probability at least \(1-\alpha_{\rm cal}\), the true temporal covariance belongs to the random rectangle

\[
\mathcal R_{\rm cal}
=
\left\{
R_{\phi,\eta}:
\phi\in[\phi_{\rm cal,-},\phi_{\rm cal,+}],
\eta\in[\eta_{\rm cal,-},\eta_{\rm cal,+}]
\right\}.
\]

This rectangle is conservative because it propagates the two marginal lag intervals by interval arithmetic. The theorem does not assume that every point in the resulting rectangle is equally plausible.

---

# Step 7: compose the random rectangle with Proposition 49

Now consider an independent target record

\[
X=HB+R_{\phi,\eta}^{1/2}Z\Sigma^{1/2},
\]

where:

- \(H\) is a fixed nuisance design selected before the target record is inspected;
- \(B\) is arbitrary and unknown;
- \(Z\) has independent standard normal entries;
- \(\Sigma\succ0\) is the spatial covariance;
- the target shares the same \((\phi,\eta)\) as the calibration record;
- the target record is independent of the calibration record.

Condition on the complete calibration record. Once conditioned, the calibrated rectangle and its finite cover are deterministic.

Let \(A\) be the event that the calibrated rectangle contains the true \((\phi,\eta)\). Proposition 50 gives

\[
\Pr(A)\ge1-\alpha_{\rm cal}.
\]

On event \(A\), Proposition 49 applies to the target record with any requested covariance confidence

\[
1-\alpha_{\rm cov}.
\]

Because the target is independent of the calibration record,

\[
\Pr(B\mid\text{calibration data})
\ge1-\alpha_{\rm cov}
\]

whenever \(A\) holds, where \(B\) is the Proposition 49 covariance event.

Therefore

\[
\Pr(A\cap B)
\ge
(1-\alpha_{\rm cal})(1-\alpha_{\rm cov}).
\]

The implementation reports exactly this product lower bound.

For the default Experiment AJ split,

\[
1-\alpha_{\rm cal}
=1-\alpha_{\rm cov}
=0.9875,
\]

so

\[
(0.9875)^2
=0.97515625.
\]

---

# Proposition 50

**Proposition 50 (data-calibrated two-parameter temporal-family covariance certificate).**

Assume:

1. the calibration channels are independent Gaussian channels with known unit marginal variance, arbitrary constant channel means, and common temporal covariance \(R_{\phi,\eta}\);
2. the true parameters lie in a declared box with \(0<\phi_-\le\phi\le\phi_+<1\) and \(0\le\eta_-\le\eta\le\eta_+<1\);
3. the target record is independent of the calibration record and shares the same temporal parameters;
4. the target obeys the separable Gaussian model with an arbitrary mean inside a fixed predeclared nuisance subspace;
5. the calibrated parameter rectangle is nonempty;
6. the Proposition 49 finite cover is constructed over that calibrated rectangle with valid deterministic cover radii.

Then the lag-1 and lag-2 increment statistics construct a random parameter rectangle containing the true \((\phi,\eta)\) with probability at least \(1-\alpha_{\rm cal}\). Conditional on that event, Proposition 49 gives the target covariance certificate with probability at least \(1-\alpha_{\rm cov}\). Consequently the complete observable procedure has confidence at least

\[
(1-\alpha_{\rm cal})(1-\alpha_{\rm cov}).
\]

The returned covariance radius is the Proposition 49 family-uniform relative covariance radius computed over the calibrated rectangle.

---

# Experiment AJ

[![Experiment AJ: observable temporal-family calibration](calibrated_temporal_family.svg)](calibrated_temporal_family.svg)

Experiment AJ fixes:

- target sample count `400`;
- calibration sample count `400`;
- spatial dimension `4`;
- affine nuisance design `intercept + linear trend`;
- declared `phi` interval `[0.45, 0.75]`;
- declared `eta` interval `[0.00, 0.05]`;
- controlled-study truth `(phi, eta) = (0.60, 0.02)`;
- calibration confidence `0.9875`;
- covariance confidence `0.9875`;
- combined confidence lower bound `0.97515625`;
- a fixed `9 x 5` Proposition 49 cover;
- 1024 deterministic Chernoff parameters per tail.

Only the number of independent calibration channels changes.

| Calibration channels | Calibrated `phi` interval | Proposition 50 radius | Full-family radius |
| ---: | --- | ---: | ---: |
| 16 | `[0.487, 0.750]` | `1.117` | `1.142` |
| 32 | `[0.504, 0.737]` | `1.054` | `1.142` |
| 64 | `[0.517, 0.679]` | **`0.871`** | `1.142` |
| 128 | `[0.545, 0.659]` | **`0.814`** | `1.142` |
| 256 | `[0.559, 0.640]` | **`0.772`** | `1.142` |

The main numerical transition occurs between 32 and 64 calibration channels. The target problem, target sample count, covariance dimension, nuisance design, confidence split, and cover resolution remain fixed. Learning the temporal uncertainty alone moves the rigorous covariance radius from above one to below one.

## Why the increment-specific calculation matters

At 64 calibration channels, the lag-1 correlation error radius from the increment-specific theorem is about `0.021`, compared with about `0.091` from the generic spectral-product bound. For lag 2, the corresponding comparison is about `0.035` versus `0.108`.

This is not a change in confidence. It is a change in mathematical use of structure.

## Independent target-record visibility checks

Two fixed 96-trial target studies were run using the same controlled temporal parameters and a large unknown affine mean.

| Calibration channels | Theorem radius | 95th percentile observed error | Maximum observed error | Covered |
| ---: | ---: | ---: | ---: | ---: |
| 64 | `0.871` | `0.367` | `0.438` | `96 / 96` |
| 256 | `0.772` | `0.369` | `0.409` | `96 / 96` |

For 96 successes in 96 trials, the two-sided 95% Wilson interval is approximately `[0.962, 1.000]`.

These simulations are visibility checks. They do not prove the probability statement.

[Machine-readable results](calibrated_temporal_family.json) · [reproduce Experiment AJ](../examples/calibrated_temporal_family.py) · [render publication SVG](../examples/render_calibrated_temporal_family.py) · [claim-level tests](../tests/test_calibrated_temporal_family.py)

---

# What changed from Proposition 49

The theorem ladder is now:

```text
known temporal covariance
        -> Proposition 47
one-dimensional calibrated AR(1) interval
        -> Proposition 48
arbitrary compact family with a deterministic cover
        -> Proposition 49
random two-parameter confidence family learned from independent data
        -> Proposition 50
```

Proposition 49 made the concentration layer modular. Proposition 50 demonstrates how to place a finite-sample statistical calibration layer in front of that module without hiding the confidence accounting.

---

# Limitations and next mathematical target

Proposition 50 does not solve arbitrary temporal dependence. Its assumptions are explicit:

- exact Gaussian calibration channels;
- unit marginal variance in those calibration channels;
- independence across calibration channels;
- independent calibration and target records;
- a common stationary AR(1) plus white-noise temporal family;
- nonnegative positive AR(1) coefficient bounded away from zero by the declared model;
- exact temporal-spatial separability in the target covariance theorem;
- a target nuisance design fixed before target inspection.

The `eta` interval can remain prior-limited when the lag correlations are not estimated precisely enough. Experiment AJ intentionally shows that possibility rather than hiding it.

The next statistical target is a sharper joint confidence region for \((r_1,r_2)\), or a direct likelihood or martingale confidence set for \((\phi,\eta)\), that uses the dependence between the two lag statistics instead of rectangular interval arithmetic. A second frontier is to replace the two-parameter family by a finite-sample spectral-density confidence set while preserving the matrix concentration layer.
