# Proposition 56: innovation-whitened target covariance

## Physical question

Proposition 55 showed that the remaining error on the AP benchmark was no longer dominated by uncertainty in the physical relaxation time. Even when the true relaxation time was supplied exactly, the existing raw-space target covariance theorem still produced a relative radius above one.

That diagnostic points to a different question:

> If the temporal law is known, should a covariance estimator continue to pay an effective-sample penalty for temporal memory, or can the independent innovations implied by that law be exposed before nuisance removal?

Proposition 56 answers this question under the declared separable Gaussian model.

The key operation is **temporal whitening before nuisance projection**.

Whitening does not add observations. It applies a deterministic invertible transformation derived from the declared temporal covariance. Under a correct model, that transformation exposes independent Gaussian innovation coordinates that were already present in the stochastic law.

---

# 1. Measurement model

Let the target record be an \(N\times p\) matrix

\[
X = H B + E,
\]

where

- \(H\in\mathbb R^{N\times q}\) is a fixed full-rank nuisance design;
- \(B\in\mathbb R^{q\times p}\) is an unknown nuisance coefficient matrix;
- the stochastic term has separable covariance

\[
\operatorname{Cov}(\operatorname{vec}E)
=
R\otimes\Sigma;
\]

- \(R\in\mathbb R^{N\times N}\) is a known positive-definite temporal covariance;
- \(\Sigma\in\mathbb R^{p\times p}\) is the spatial covariance to be estimated.

Equivalently, one may write

\[
E = R^{1/2} Z \Sigma^{1/2},
\]

with \(Z\) containing independent standard Gaussian entries.

Let \(W\) be any exact temporal whitener satisfying

\[
\boxed{
W R W^{\mathsf T}=I_N.
}
\]

For the exponential physical-time model of Proposition 53, \(W\) is available directly from the irregular-grid innovation factorization.

---

# 2. Whitening changes the nuisance geometry too

The transformed record is

\[
Y = W X.
\]

Its mean is

\[
\mathbb E[Y]=W H B.
\]

Therefore the nuisance design must also be transformed:

\[
A = W H.
\]

Define the Euclidean orthogonal projector onto the complement of this transformed nuisance space:

\[
P_A
=
I_N
-
A(A^{\mathsf T}A)^{-1}A^{\mathsf T}.
\]

Because \(W\) is nonsingular and \(H\) has rank \(q\),

\[
\operatorname{rank}(A)=q
\]

and

\[
\operatorname{rank}(P_A)=N-q.
\]

Also,

\[
P_A W H = 0.
\]

So the declared deterministic nuisance mean is removed exactly after whitening.

## Why the order matters

Projecting \(H\) in the original correlated coordinates and then analyzing the result is not equivalent to whitening first and projecting \(WH\).

The latter operation uses the metric induced by the known temporal covariance. It removes the nuisance directions after the correlated noise has been transformed into independent innovations.

---

# 3. Proposition 56 estimator

Define

\[
\boxed{
\widehat\Sigma_{\mathrm{white}}
=
\frac{1}{N-q}
X^{\mathsf T}
W^{\mathsf T}
P_A
W X.
}
\]

Equivalently,

\[
\widehat\Sigma_{\mathrm{white}}
=
\frac{1}{N-q}
Y^{\mathsf T}P_A Y.
\]

Since \(P_AWH=0\), the nuisance term vanishes from the quadratic form.

The estimator therefore depends only on the whitened stochastic residuals.

---

# 4. Exact Wishart law

## Proposition 56

Under the measurement model above,

\[
\boxed{
(N-q)\widehat\Sigma_{\mathrm{white}}
\sim
W_p(\Sigma,N-q).
}
\]

In particular,

\[
\boxed{
\mathbb E[\widehat\Sigma_{\mathrm{white}}]=\Sigma.
}
\]

### Proof

Because \(W R W^{\mathsf T}=I_N\), the whitened stochastic matrix

\[
G=WE
\]

has temporal covariance \(I_N\) and spatial covariance \(\Sigma\).

Since the model is Gaussian, the rows of \(G\) are independent and each row has distribution

\[
\mathcal N_p(0,\Sigma).
\]

The estimator numerator is

\[
X^{\mathsf T}W^{\mathsf T}P_AWX
=
G^{\mathsf T}P_A G,
\]

because the transformed nuisance term is annihilated.

The projector \(P_A\) is symmetric, idempotent, and has rank

\[
d=N-q.
\]

Choose an \(N\times d\) matrix \(U\) with orthonormal columns spanning the range of \(P_A\). Then

\[
P_A=UU^{\mathsf T}.
\]

Hence

\[
G^{\mathsf T}P_A G
=
(U^{\mathsf T}G)^{\mathsf T}(U^{\mathsf T}G).
\]

Rotational invariance of the Gaussian law implies that the \(d\) rows of \(U^{\mathsf T}G\) remain independent \(\mathcal N_p(0,\Sigma)\) vectors.

Therefore

\[
G^{\mathsf T}P_A G
\sim
W_p(\Sigma,d).
\]

Substituting \(d=N-q\) proves the statement.

---

# 5. What happened to temporal effective sample size?

Nothing physical disappeared and no information was created.

Before whitening, temporal persistence appears as a nonuniform spectrum in the quadratic form used by the raw-space covariance estimator. That produces a weighted Wishart law and a reduced effective-information scale.

After exact whitening, the residual temporal spectrum is simply

\[
\underbrace{1,\ldots,1}_{N-q\text{ times}}.
\]

The only exact loss of independent Gaussian residual coordinates is the \(q\)-dimensional declared nuisance subspace.

Thus the relevant residual degrees of freedom become

\[
\boxed{N-q.}
\]

This is an estimator-design result, not a claim that correlated measurements are literally independent before transformation.

---

# 6. Matrix covariance certificate

Proposition 47 applies immediately because the whitened residual law is an ordinary Wishart with \(N-q\) unit temporal weights.

For any declared spatial block dimension and block count, Proposition 56 therefore uses

\[
\lambda_1=\cdots=\lambda_{N-q}=1
\]

inside the existing matrix-Laplace certificate.

No temporal covering radius is needed when the whitening law is known exactly.

On the Experiment AQ scalar benchmark,

\[
N=120,
\qquad
q=2,
\qquad
N-q=118.
\]

The resulting matrix certificate is

\[
\boxed{
\varepsilon_{\mathrm{white,matrix}}
=0.43643844034822693.
}
\]

This is below one.

---

# 7. Exact scalar chi-square certificate

When \(p=1\), the Wishart identity reduces to

\[
\frac{(N-q)\widehat\sigma^2}{\sigma^2}
\sim
\chi^2_{N-q}.
\]

For one scalar block at confidence \(0.975\) with \(N-q=118\), the exact simultaneous two-sided interval is

\[
0.7311633508199835
\le
\frac{\widehat\sigma^2}{\sigma^2}
\le
1.3142366148262574.
\]

Therefore

\[
\boxed{
\left|
\frac{\widehat\sigma^2}{\sigma^2}-1
\right|
\le
0.3142366148262574
}
\]

with the declared confidence.

For multiple scalar blocks, the implementation uses a Bonferroni split over both tails and the declared block count. Independence between blocks is not required for that simultaneous statement.

---

# 8. Experiment AQ

Experiment AQ reuses the same target sampling geometry used in Proposition 55:

- physical relaxation time: \(0.78\) s;
- target timestamps: \(120\);
- nuisance rank: \(2\);
- residual degrees of freedom after whitening: \(118\);
- covariance confidence: \(0.975\);
- scalar block dimension: \(1\);
- block count: \(1\).

The certificate comparison is:

| Method | Relative covariance radius |
| --- | ---: |
| Raw-space known-\(\tau\) theorem, 4096-point theta search | 2.167136193997473 |
| Innovation-whitened matrix certificate | 0.43643844034822693 |
| Innovation-whitened exact scalar chi-square certificate | 0.3142366148262574 |

The matrix certificate is approximately \(79.86\%\) smaller than the raw-space known-\(\tau\) certificate. The exact scalar certificate is approximately \(85.50\%\) smaller.

The raw-space number differs slightly from the Proposition 55 published oracle value because Experiment AQ uses a finer deterministic theta search. Both are valid upper bounds from the same existing raw-space theorem.

## Visibility trials

A separate deterministic 256-trial simulation was run with a large affine nuisance mean in the declared rank-2 design.

The absolute scalar covariance errors were:

- median: `0.07704982028955165`;
- 95th percentile: `0.2324178368027294`;
- maximum: `0.37414671347209993`.

The exact 97.5% chi-square interval contained `252/256` trials, or `0.984375` of the displayed trials.

The maximum numerical change caused by adding versus removing the declared nuisance mean was

\[
4.6629367034256575\times10^{-15}.
\]

These trials illustrate scale and numerical invariance. They are not the proof of the confidence statement.

---

# 9. Physical interpretation

The result should be read carefully.

The temporal model says that a slowly relaxing measured process can be represented as a sequence of independent innovations passed through a known linear temporal filter.

Exact whitening applies the inverse of that filter. The transformed residuals are independent because the declared Gaussian temporal model says they are independent in innovation coordinates.

Projecting the nuisance subspace after that transformation removes deterministic modes in the same coordinate system in which the noise is white.

The result does **not** say:

- that temporal memory is physically unreal;
- that whitening creates new observations;
- that every correlated physical process admits the exponential one-timescale model;
- that an estimated temporal parameter may be treated as exact without additional analysis;
- that a covariance radius below one proves an observer boundary or consciousness.

A radius below one means only that the target covariance has entered the perturbative regime needed by later covariance-sensitive mathematics under the declared assumptions.

---

# 10. Assumptions and falsification

The exact Wishart law requires:

1. the target stochastic record is Gaussian;
2. temporal and spatial covariance are separable as \(R\otimes\Sigma\);
3. the temporal covariance \(R\) used for whitening is the true target temporal covariance;
4. \(R\) is positive definite;
5. the nuisance mean lies in the fixed declared column space of \(H\);
6. \(H\) is fixed independently of the target stochastic realization.

A physical application should therefore inspect the whitened residuals directly. Relevant failure diagnostics include:

- residual temporal autocorrelation after whitening;
- changing innovation variance across time;
- non-Gaussian innovation tails;
- evidence for multiple relaxation scales or oscillatory memory;
- target/calibration mismatch in the temporal law;
- sensitivity to an expanded nuisance design;
- nonseparable temporal-spatial covariance.

If the whitened residuals retain systematic temporal structure, the exact Proposition 56 Wishart law is not justified for that record.

---

# 11. What Proposition 56 changes in the research program

Proposition 55 supplied a useful negative diagnostic: calibration sharpening alone could not move the AP benchmark below one because the raw-space known-\(\tau\) target theorem itself remained above one.

Proposition 56 changes the target estimator and crosses that threshold under exact temporal knowledge:

\[
2.167136193997473
\longrightarrow
0.43643844034822693
\]

for the matrix certificate, and to

\[
0.3142366148262574
\]

for the exact scalar certificate.

The next unresolved problem is now sharply defined:

> How much of this innovation-whitening advantage survives when the physical temporal law is known only through a finite-sample confidence set rather than exactly?

That question requires a separate robustness theorem. Proposition 56 does not answer it by substituting an estimated \(\tau\) into the exact-known-law result.

---

# 12. Reproducibility

Implementation:

- `src/observer_math/whitened_target_covariance.py`

Claim-level tests:

- `tests/test_whitened_target_covariance.py`

Experiment:

- `examples/innovation_whitened_target_covariance.py`

Machine-readable result:

- `docs/innovation_whitened_target_covariance.json`

The theorem is the exact Wishart identity proved above. Experiment AQ illustrates its scale on the benchmark that exposed the raw-space oracle bottleneck.
