# Proposition 53B: finite-sample physical relaxation-time calibration on irregular timestamps

Proposition 53A established that the exponential physical-time covariance

\[
R_\tau(i,j)=\exp\!\left(-\frac{|t_i-t_j|}{\tau}\right)
\]

has an exact local Gaussian Markov representation on every strictly increasing timestamp grid. Proposition 53B uses that exact factorization to infer the **physical relaxation time** \(\tau\) directly from an irregular calibration record.

This is a finite-sample confidence statement. It does not estimate a discrete AR(1) coefficient and then convert it to seconds, and the confidence theorem does not require the true \(\tau\) to lie on a numerical grid.

---

## 1. Calibration model

Let

\[
t_1<t_2<\cdots<t_N
\]

be fixed physical timestamps. Observe \(M\) independent standardized Gaussian calibration channels

\[
X^{(1)},\ldots,X^{(M)}\in\mathbb R^N
\]

with

\[
X^{(m)}\sim \mathcal N(0,R_{\tau_*}),
\qquad
R_{\tau_*}(i,j)=\exp\!\left(-\frac{|t_i-t_j|}{\tau_*}\right),
\]

for one common unknown relaxation time

\[
\tau_*\in[\tau_-,\tau_+],
\qquad 0<\tau_-\le \tau_+<\infty.
\]

The channels have unit marginal variance and zero mean. Unknown-mean calibration is **not** included in this proposition.

Define the irregular gaps

\[
\Delta_i=t_{i+1}-t_i
\]

and, for any candidate \(\tau\),

\[
\alpha_i(\tau)=e^{-\Delta_i/\tau}.
\]

By Proposition 53A, every channel has the exact local representation

\[
X_{i+1}=\alpha_i(\tau)X_i+\sqrt{1-\alpha_i(\tau)^2}\,\varepsilon_i,
\qquad
\varepsilon_i\overset{\text{iid}}\sim\mathcal N(0,1).
\]

Therefore the dense Gaussian likelihood has an exact innovation factorization.

---

## 2. Exact irregular-time likelihood

For one channel \(x=(x_1,\ldots,x_N)\),

\[
p_\tau(x)
=
\varphi(x_1)
\prod_{i=1}^{N-1}
\frac{1}{\sqrt{2\pi(1-\alpha_i^2)}}
\exp\!\left[
-\frac{(x_{i+1}-\alpha_i x_i)^2}{2(1-\alpha_i^2)}
\right],
\]

where \(\varphi\) is the standard-normal density and \(\alpha_i=\alpha_i(\tau)\).

For \(M\) independent channels, multiply these factors across channels. Terms independent of \(\tau\) cancel from all likelihood ratios. If

\[
S_{xx,i}=\sum_{m=1}^M (X_i^{(m)})^2,
\quad
S_{xy,i}=\sum_{m=1}^M X_i^{(m)}X_{i+1}^{(m)},
\quad
S_{yy,i}=\sum_{m=1}^M (X_{i+1}^{(m)})^2,
\]

then the \(\tau\)-dependent log-likelihood kernel is

\[
\ell(\tau)
=
-\frac M2\sum_{i=1}^{N-1}\log(1-\alpha_i^2)
-\frac12\sum_{i=1}^{N-1}
\frac{S_{yy,i}-2\alpha_iS_{xy,i}+\alpha_i^2S_{xx,i}}
{1-\alpha_i^2}.
\]

This costs \(O(NM)\) once to form the transition statistics and then \(O(N)\) per candidate \(\tau\). No dense matrix inverse or determinant is needed.

---

## 3. Proposition 53B: continuum e-value confidence set

Choose before inspecting the calibration data a finite collection

\[
\tau_1,\ldots,\tau_J\in[\tau_-,\tau_+]
\]

and define the proper mixture density

\[
q(x)=\frac1J\sum_{j=1}^J p_{\tau_j}(x).
\]

For **every** candidate \(\tau\in[\tau_-,\tau_+]\), define

\[
e_\tau(x)=\frac{q(x)}{p_\tau(x)}.
\]

The mixture points define only the numerator density \(q\). They do **not** discretize the parameter values at which \(e_\tau\) can be evaluated.

### Claim

For the true \(\tau_*\),

\[
\mathbb E_{\tau_*}[e_{\tau_*}(X)]=1.
\]

Hence for any \(0<\alpha<1\),

\[
\mathcal C_\alpha(X)
=
\left\{
\tau\in[\tau_-,\tau_+]:
\log e_\tau(X)<\log(1/\alpha)
\right\}
\]

satisfies

\[
\boxed{
\mathbb P_{\tau_*}\{\tau_*\in\mathcal C_\alpha(X)\}\ge 1-\alpha.
}
\]

### Proof

At the true parameter,

\[
\mathbb E_{\tau_*}[e_{\tau_*}(X)]
=
\int \frac{q(x)}{p_{\tau_*}(x)}p_{\tau_*}(x)\,dx
=
\int q(x)\,dx
=1.
\]

Because \(e_{\tau_*}\ge0\), Markov's inequality gives

\[
\mathbb P_{\tau_*}
\left\{
e_{\tau_*}\ge \frac1\alpha
\right\}
\le \alpha.
\]

Taking the complement proves the confidence statement. No union bound over candidate values of \(\tau\) is used. \(\square\)

---

## 4. Certified finite outer cover of the continuum set

A target theorem cannot consume an uncountable set directly. We therefore build a finite **outer cover** without spending additional probability.

Partition \([\tau_-,\tau_+]\) into cells \(I_k\) with center \(c_k\) and radius \(r_k\). Let \(L_k\) be any deterministic observed-data bound satisfying

\[
|\ell'(\tau)|\le L_k
\qquad
\text{for every }\tau\in I_k.
\]

Since

\[
\log e_\tau=\log q-\ell(\tau),
\]

the mean-value theorem gives

\[
\log e_\tau
\ge
\log e_{c_k}-L_kr_k
\qquad
(\tau\in I_k).
\]

Therefore if

\[
\log e_{c_k}-L_kr_k
\ge
\log(1/\alpha),
\]

then **every** \(\tau\in I_k\) is rejected and that entire cell can be removed safely.

Retain every other cell. The resulting finite union \(\widehat{\mathcal C}_\alpha\) satisfies, deterministically for the observed record,

\[
\boxed{
\mathcal C_\alpha(X)\subseteq \widehat{\mathcal C}_\alpha(X).
}
\]

Thus the certified cover inherits the same calibration confidence:

\[
\mathbb P_{\tau_*}
\{\tau_*\in\widehat{\mathcal C}_\alpha(X)\}
\ge 1-\alpha.
\]

The implementation uses a **cell-local** derivative bound rather than one global full-interval bound. This can only improve or preserve the deterministic certificate.

---

## 5. Time-unit invariance

Rescale physical time by any \(c>0\):

\[
t_i'=ct_i,
\qquad
\tau'=c\tau.
\]

Then

\[
\frac{t_{i+1}'-t_i'}{\tau'}
=
\frac{t_{i+1}-t_i}{\tau},
\]

so every \(\alpha_i\), innovation variance, likelihood ratio, and e-value is unchanged. The physical parameter changes units but not inference geometry.

The likelihood derivative with respect to the rescaled parameter transforms as \(1/c\), exactly compensating the cell-radius scaling. Hence the certified outer-cover decision is also invariant to the choice of seconds, milliseconds, or any other consistent time unit.

---

## 6. Independent target composition

Let the calibration record and target record be independent. Construct the retained physical-time family from calibration only. On target timestamps \(s_1<\cdots<s_T\), map every retained \(\tau\) to

\[
R_\tau^{\text{target}}(a,b)
=
\exp\!\left(-\frac{|s_a-s_b|}{\tau}\right).
\]

A retained cell is represented by its center covariance plus an operator-norm covering radius from the Proposition 53A physical-time Lipschitz bound. Proposition 49 can then certify projected target covariance uniformly over the retained temporal family.

If calibration confidence is \(c_{\rm cal}\) and the independent conditional target theorem has confidence \(c_{\rm cov}\), then

\[
\boxed{
c_{\rm combined}\ge c_{\rm cal}c_{\rm cov}.
}
\]

Indeed, conditional on the calibration record whenever the true \(\tau_*\) is retained, the independent target guarantee is at least \(c_{\rm cov}\); averaging gives the product lower bound.

This composition permits the calibration and target experiments to use **different irregular timestamp grids**.

---

# Experiment AN: finite-sample irregular-time relaxation calibration

The deterministic script is

```bash
python examples/irregular_relaxation_evalue_calibration.py
```

and writes the complete machine-readable record to
[`irregular_relaxation_evalue_calibration.json`](irregular_relaxation_evalue_calibration.json).

## Declared setup

- true physical relaxation time: \(\tau_*=0.78\) s;
- declared interval: \([0.40,1.25]\) s;
- calibration confidence: \(0.975\);
- calibration channels: \(M=96\);
- calibration timestamps: \(N=32\), irregular gaps from \(0.03\) s to \(0.20\) s;
- mixture numerator: 21 predeclared \(\tau\) points;
- diagnostic visibility grid: 2001 points;
- certified outer cover: 160 equal cells;
- target record: 120 samples on a different irregular timestamp schedule;
- target nuisance design: intercept plus centered physical time, rank 2;
- target covariance confidence: \(0.975\).

## Exact repository-generated record

The true value is accepted with

\[
\log e_{0.78}=-2.6054136861
\]

against the 97.5% rejection threshold

\[
\log(1/0.025)=3.6888794541.
\]

On the 2001-point **diagnostic** grid, accepted points span approximately

\[
[0.69155,\ 0.84455]\ \text{s}.
\]

This interval is descriptive only; the theorem is continuum-valued.

The certified finite outer cover retains 115 of 160 cells and excludes 45. Its retained span is

\[
[0.495625,\ 1.1065625]\ \text{s}.
\]

Every diagnostic accepted value is contained in retained cells. The wider certified span reflects the conservatism of a deterministic derivative certificate, not loss of finite-sample validity.

Changing the entire time representation from seconds to milliseconds changes the evaluated log e-values by at most

\[
2.05\times10^{-12}
\]

across 101 check points.

For the independent target record, the calibration and covariance confidences compose to

\[
0.975^2=0.950625.
\]

The target cover uses 115 retained temporal representatives. The resulting Proposition 49 quantities are

\[
\varepsilon_{\rm eig}=0.1091568357,
\qquad
\varepsilon_{\rm norm}=0.2183136714,
\]

with projected degrees-of-freedom lower bound

\[
73.4383285584.
\]

The current target relative covariance radius is

\[
\boxed{3.1554895445}.
\]

That number is intentionally reported rather than hidden: the **coverage composition is valid**, but this specific target certificate is not in the \(\varepsilon<1\) perturbative regime needed by downstream inverse-covariance results.

---

## 7. What Proposition 53B closes

It closes the specific gap between a physically meaningful exponential relaxation parameter and finite-sample calibration on irregular observations:

1. \(\tau\) is inferred directly in physical time.
2. The likelihood is exact on arbitrary increasing timestamps.
3. The confidence set is continuum-valued and finite-sample valid.
4. The true \(\tau\) need not lie on the mixture grid.
5. The retained finite cover is certified deterministically from the continuum set.
6. Seconds versus milliseconds produce the same inference.
7. A calibration family can be propagated to an independent target record with a different sampling schedule.

---

## 8. What remains open

The result remains conditional on a narrow calibration model:

- independent calibration channels;
- Gaussianity;
- zero known mean;
- unit marginal variance;
- one shared stationary exponential relaxation time;
- a fixed declared interval and predeclared mixture density;
- calibration independent of the target record;
- exponential temporal covariance and separable target covariance assumptions inherited by the downstream theorem.

The most important immediate mathematical gap is **tightness**, not validity. Experiment AN's certified target covariance radius is above one because the deterministic outer cover is substantially wider than the visible likelihood-compatible region.

Natural next proof targets are:

1. replace first-derivative cell certificates by second-order or convexity-aware likelihood envelopes;
2. exploit the one-dimensional geometry of \(\tau\) to certify connected rejected intervals rather than independent cells;
3. derive observed-information or likelihood-ratio curvature bounds that remain finite-sample safe;
4. extend calibration to unknown mean or declared nuisance subspaces;
5. extend beyond a single exponential relaxation law to mixtures, oscillatory kernels, or other physically parameterized temporal families.

Until those steps are proved, Proposition 53B should be read as a **finite-sample validity result with a conservative target-cover geometry**, not as a claim that the downstream covariance error has already been made small.