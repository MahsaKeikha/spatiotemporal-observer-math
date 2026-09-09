# Release 0.42.0

Release 0.42.0 extends Proposition 53 from a sampling-consistent physical-time representation to **finite-sample inference for the physical relaxation time itself on irregular timestamps**.

The central new statement is Proposition 53B. Under the declared calibration model, independent standardized zero-mean Gaussian channels share one exponential relaxation time \(\tau\) and one irregular timestamp grid. The exact Markov factorization from Proposition 53A gives an innovation likelihood that can be evaluated in linear time without dense covariance inversion.

A predeclared finite mixture density \(q\) defines

\[
e_\tau(X)=\frac{q(X)}{p_\tau(X)}.
\]

At the true \(\tau_*\), \(\mathbb E[e_{\tau_*}]=1\). Therefore

\[
\{\tau:\log e_\tau<\log(1/\alpha)\}
\]

is a finite-sample continuum confidence set with coverage at least \(1-\alpha\). The true parameter does not need to be a mixture-grid point and there is no parameterwise union bound.

## New research components

- `src/observer_math/irregular_relaxation_evalue.py`
  - exact irregular-time Gaussian innovation likelihood;
  - continuum e-value model and diagnostic evaluator;
  - observed-data likelihood derivative bound;
  - certified cell-local finite outer cover;
  - composition with Proposition 49 on an independent target timestamp grid.
- `tests/test_irregular_relaxation_evalue.py`
  - local versus dense likelihood-ratio identity;
  - mixture normalization identity;
  - seconds/milliseconds invariance;
  - certified continuum containment;
  - independent target composition.
- `tests/test_irregular_relaxation_evalue_artifact.py`
  - deterministic JSON-to-SVG reproducibility and XML validity.
- `examples/irregular_relaxation_evalue_calibration.py`
  - deterministic Experiment AN.
- `examples/render_irregular_relaxation_evalue.py`
  - deterministic Experiment AN renderer.
- `docs/proposition_53b_irregular_tau_evalue.md`
  - proof, assumptions, composition statement, limitations, and next theorem targets.
- `docs/irregular_relaxation_evalue_calibration.json`
  - complete machine-readable Experiment AN record.
- `docs/irregular_relaxation_evalue_calibration.svg`
  - front-page scientific result figure.

## Experiment AN

Declared setup:

- true \(\tau_*=0.78\) s;
- declared interval \([0.40,1.25]\) s;
- 96 independent calibration channels;
- 32 irregular samples per channel;
- gap range 0.03 s to 0.20 s;
- calibration confidence 0.975;
- 21-point predeclared mixture numerator;
- 160-cell certified outer cover.

Exact deterministic record:

- true-value log e-value: `-2.605413686063116`;
- 97.5% rejection threshold: `3.6888794541139354`;
- diagnostic accepted span on a 2001-point visibility grid: `[0.69155, 0.84455]` s;
- certified retained outer-cover span: `[0.495625, 1.1065625]` s;
- retained cells: `115 / 160`;
- excluded cells: `45 / 160`;
- maximum seconds-versus-milliseconds log-e-value difference: `2.0463630789890885e-12`.

The independent target composition uses a different 120-sample irregular timestamp grid and a rank-2 nuisance design. With target covariance confidence 0.975, the combined confidence is

\[
0.975^2=0.950625.
\]

The resulting target covariance relative-error radius is

\[
3.155489544511118.
\]

This value is deliberately part of the release record. The finite-sample calibration and confidence composition are valid, but this particular downstream target certificate is **not** yet in the \(\epsilon<1\) perturbative regime required by later inverse-covariance arguments.

## Scientific scope

Release 0.42.0 does not claim that every physical process follows one exponential relaxation law. Proposition 53B assumes independent standardized Gaussian calibration channels, zero known mean, unit marginal variance, one shared stationary exponential relaxation time, a fixed declared interval and predeclared mixture density, and calibration independent of the target record.

It also does not establish consciousness. The repository's use of `observer` remains an operational subsystem-identification definition.

## Next mathematical target

The immediate frontier is tightness of the certified continuum cover. The visible likelihood-compatible region in Experiment AN is much narrower than the deterministic outer cover. Candidate next steps are second-order or convexity-aware likelihood envelopes, connected rejected-interval certificates, and finite-sample-safe curvature bounds. The goal is to preserve the same validity while reducing the target temporal-family covering radius enough to enter the \(\epsilon<1\) covariance regime.