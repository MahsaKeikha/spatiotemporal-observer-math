# Release 0.39.0

Release 0.39.0 adds Proposition 51 and Experiment AK.

## Proposition 51

Proposition 51 constructs a finite-sample confidence set directly in the two-parameter temporal covariance space

\[
R_{\phi,\eta}=(1-\eta)R_\phi+\eta I.
\]

The calibration record consists of independent Gaussian channels that share the same temporal covariance. Each channel may have its own unknown constant mean. A fixed Helmert contrast removes those means exactly before any likelihood is evaluated.

For a candidate parameter \(\theta\), let \(p_\theta\) denote the exact residual Gaussian density. Let \(q\) be a proper finite mixture density fixed before the calibration data are observed. Proposition 51 uses the pointwise e-value

\[
e_\theta(Z)=\frac{q(Z)}{p_\theta(Z)}.
\]

If \(\theta\) is the true parameter, then

\[
\mathbb E_\theta e_\theta(Z)=1.
\]

Markov's inequality therefore gives the continuum confidence set

\[
\mathcal C_\alpha(Z)
=
\left\{
\theta:
 e_\theta(Z)<1/\alpha
\right\}
\]

with coverage at least \(1-\alpha\).

The theorem does not use a union bound over parameter values. The mixture support does not need to contain the true parameter. The result is finite sample and does not rely on an asymptotic likelihood approximation.

## Experiment AK

Experiment AK compares the full-likelihood e-value geometry with Proposition 50's rectangular lag-interval propagation on one controlled two-parameter calibration problem.

At 256 independent calibration channels, the Proposition 50 rectangle spans approximately

\[
\phi\in[0.510,0.701],
\qquad
\eta\in[0,0.216].
\]

The Proposition 51 visualization grid accepts points spanning approximately

\[
\phi\in[0.55,0.65],
\qquad
\eta\in[0,0.12].
\]

The accepted grid fraction falls from about 36.5 percent at 32 channels to about 6.76 percent at 256 channels. A separate 256-trial visibility check accepted the controlled true parameter in all 256 trials. The repeated-sampling study is not the coverage proof. Proposition 51 supplies the proof.

The displayed grid is also not a certified outer discretization of the continuum confidence set. It is a numerical view of the exact pointwise function. A certified outer cover is reserved for the next theorem.

## Research record

After this release, the repository records:

- 51 propositions;
- 37 reproducible experiments, A through Z and AA through AK;
- 24 committed scientific figures;
- 171 claim-level tests.

The supported CI matrix remains Python 3.10, 3.11, and 3.12.

## Files added

- `src/observer_math/evalue_temporal_family.py`
- `tests/test_evalue_temporal_family.py`
- `docs/proposition_51_evalue_temporal_confidence_set.md`
- `examples/evalue_temporal_confidence_set.py`
- `docs/evalue_temporal_confidence_set.json`
- `examples/render_evalue_temporal_confidence_set.py`
- `docs/evalue_temporal_confidence_set.svg`

## Interpretation boundary

This release improves statistical calibration of a temporal covariance family. It does not prove or measure consciousness. The mathematical object remains observer-like dynamical organization under explicit model assumptions. Any future consciousness interpretation remains subject to the repository's separate interpretation protocol.
