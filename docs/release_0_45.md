# Release 0.45.0 research record

## Proposition 56 and Experiment AQ

Release 0.45.0 changes the target covariance estimator rather than continuing to tighten temporal calibration.

Proposition 55 established an important negative diagnostic: even with the true relaxation time supplied exactly, the existing raw-space target theorem still produced a relative covariance radius above one on the AP benchmark. Proposition 56 asks whether that limitation belongs to the physical record or to the order in which the estimator handles temporal dependence and nuisance structure.

The answer is estimator-dependent under the declared Gaussian separable model.

## Proposition 56

Let the target record satisfy

\[
X=HB+E,
\qquad
\operatorname{Cov}(\operatorname{vec}E)=R\otimes\Sigma,
\]

where \(R\) is known and positive definite and \(H\) is a fixed full-rank nuisance design of rank \(q\).

Let \(W\) be an exact temporal whitener:

\[
W R W^{\mathsf T}=I.
\]

The nuisance design must be transformed by the same map:

\[
A=WH,
\qquad
P_A=I-A(A^{\mathsf T}A)^{-1}A^{\mathsf T}.
\]

Define

\[
\widehat\Sigma_{\mathrm{white}}
=
\frac{1}{N-q}
X^{\mathsf T}W^{\mathsf T}P_AWX.
\]

Under the declared Gaussian separable model,

\[
\boxed{
(N-q)\widehat\Sigma_{\mathrm{white}}
\sim
W_p(\Sigma,N-q).
}
\]

Thus exact temporal whitening followed by nuisance projection restores an ordinary Wishart law with exactly \(N-q\) independent Gaussian residual degrees of freedom.

The operation does not create observations. It exposes the innovation coordinates already implied by the known temporal covariance law.

## Experiment AQ

Experiment AQ uses the same controlled target sampling geometry that exposed the Proposition 55 oracle bottleneck:

- physical relaxation time: `0.78 s`;
- target sample count: `120`;
- nuisance rank: `2`;
- residual degrees of freedom after exact whitening: `118`;
- covariance confidence: `0.975`;
- scalar block dimension: `1`;
- scalar block count: `1`.

The certificate comparison is

\[
\boxed{
2.167136193997473
\longrightarrow
0.43643844034822693
\longrightarrow
0.3142366148262574.
}
\]

The three numbers are, respectively:

1. the existing raw-space known-relaxation-time theorem;
2. the Proposition 56 innovation-whitened matrix certificate;
3. the exact scalar chi-square certificate available when \(p=1\).

The matrix certificate is approximately `79.86%` smaller than the raw-space known-parameter theorem. The exact scalar certificate is approximately `85.50%` smaller.

This is the first benchmark in the current physical-time chain where the target covariance certificate crosses from a relative radius above one to a radius below one under an exactly known temporal law.

## Visibility study

A separate deterministic 256-trial target study gives:

- median absolute relative error: `0.07704982028955165`;
- 95th percentile: `0.2324178368027294`;
- maximum: `0.37414671347209993`;
- exact 97.5% scalar interval coverage: `252/256 = 0.984375`;
- maximum nuisance-invariance error: `4.6629367034256575e-15`.

These trials illustrate scale and numerical invariance. The confidence theorem comes from the exact Wishart and chi-square identities, not from empirical trial coverage.

## Physical reading

The result says that a known temporal model can be used as a coordinate transformation before deterministic nuisance modes are removed.

For the exponential physical-time model, Proposition 53 supplies the exact irregular-time innovation whitener. In those coordinates, the Gaussian residuals are independent across time. The transformed nuisance subspace is then projected out, leaving \(N-q\) independent residual coordinates.

The result does not say that physical temporal memory disappears. It says that, under the declared model, temporal memory is represented by a known invertible linear filter whose innovations can be exposed exactly.

## Scope and failure conditions

The exact Proposition 56 law requires:

- Gaussian target innovations;
- temporal-spatial covariance separability;
- a correct positive-definite temporal covariance used for whitening;
- a fixed declared nuisance design containing the deterministic target mean;
- nuisance-design choice independent of the target stochastic realization.

If the whitened residuals still contain temporal dependence, nonstationary innovation variance, heavy tails, or other systematic structure, the exact Wishart interpretation is not justified for that record.

Most importantly, Proposition 56 does **not** justify inserting an estimated relaxation time into the exact-known-law whitener and treating it as exact. Robust whitening under temporal uncertainty is the next theorem problem.

## Literature lineage

The whitening and correlated-error viewpoint belongs to the classical generalized least-squares lineage, including Aitken's 1935 work on least squares with correlated observations. The Wishart distribution supplies the exact Gaussian covariance law. Proposition 56's estimator and proof are written directly in this repository.

See `docs/bibliography.md` and `references.bib` for the role-based citation record.

## Reproducibility assets

- proof: `docs/proposition_56_innovation_whitened_target_covariance.md`
- implementation: `src/observer_math/whitened_target_covariance.py`
- theorem tests: `tests/test_whitened_target_covariance.py`
- public API test: `tests/test_whitened_target_covariance_public_api.py`
- experiment: `examples/innovation_whitened_target_covariance.py`
- machine-readable results: `docs/innovation_whitened_target_covariance.json`
- deterministic figure renderer: `examples/render_innovation_whitened_target_covariance.py`
- visible figure: `docs/innovation_whitened_target_covariance.svg`
- artifact reproducibility test: `tests/test_innovation_whitened_target_covariance_artifact.py`

## Intended release record

The intended 0.45.0 record is:

- 56 propositions;
- 43 reproducible experiments, A-Z and AA-AQ;
- 31 scientific-result figures;
- 214 claim-level tests;
- Python 3.10, 3.11, and 3.12 CI;
- Ruff clean;
- Markdown punctuation guard clean.

These counts become verified release counts only after the exact release candidate is merged and the resulting `main` workflow succeeds.
