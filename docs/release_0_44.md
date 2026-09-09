# Release 0.44.0 research record

## Proposition 55 and Experiment AP

Release 0.44.0 adds a second-order finite-sample calibration certificate for the physical relaxation-time model and uses Experiment AP to identify the next mathematical bottleneck.

The release has two equally important results:

1. the certified physical-time interval can be tightened substantially by using the exact observed-data log-evalue slope and a rigorous cell-local curvature bound;
2. even exact knowledge of the true relaxation time does not make the current target covariance theorem enter the relative-error regime below one on this benchmark.

The second result is a negative diagnostic, but it is scientifically useful because it shows that continued calibration refinement alone cannot solve the remaining target problem.

## Proposition 55

For a calibration cell

\[
I_j=[a_j,b_j]
\]

with center \(c_j\) and radius \(r_j\), let

\[
\ell(\tau)=\log e_\tau(Z).
\]

Proposition 55 evaluates the exact observed-data slope \(\ell'(c_j)\) and constructs a deterministic curvature bound

\[
M_j
\ge
\sup_{\tau\in I_j}|\ell''(\tau)|.
\]

Taylor's theorem then gives

\[
\ell(\tau)
\ge
\ell(c_j)
-
|\ell'(c_j)|r_j
-
\frac12M_jr_j^2
\]

for every \(\tau\in I_j\).

A cell is excluded only if this complete lower enclosure is already at or above the Proposition 53B rejection threshold. Therefore the exact continuum e-value confidence set remains inside the retained quadratic cells.

No additional probability budget is spent.

## Experiment AP

Experiment AP uses the same controlled physical-time benchmark as Experiments AN and AO:

- true relaxation time: `0.78 s`;
- declared interval: `[0.40, 1.25] s`;
- 96 independent calibration channels;
- 32 irregular calibration samples;
- 120 target samples on a different timestamp schedule;
- nuisance rank: `2`;
- calibration confidence: `0.975`;
- target covariance confidence: `0.975`;
- combined confidence lower bound: `0.950625`.

At 160 calibration cells, the first-order certified interval is

\[
[0.495625,1.1065625]\ \mathrm{s}
\]

with width `0.6109375 s`.

The Proposition 55 quadratic interval is

\[
\boxed{
[0.686875,0.8515625]\ \mathrm{s}
}
\]

with width `0.1646875 s`.

This is approximately a `73.0%` contraction at the same cell count and the same finite-sample calibration confidence.

The target covariance radius progresses as

\[
3.1554895445
\quad\longrightarrow\quad
2.5720746948
\quad\longrightarrow\quad
2.4148799294,
\]

for Propositions 53B, 54, and 55 respectively.

## Known-tau oracle diagnostic

Experiment AP also supplies the true controlled value \(\tau=0.78\) s directly to the existing target concentration theorem. This is not an implementable calibration procedure. It is a diagnostic floor for the current target theorem.

With one temporal cover point and zero temporal covering radii, the relative target covariance radius is still

\[
\boxed{
2.167246895150515>1
}.
\]

Therefore calibration uncertainty is no longer the dominant bottleneck on this target configuration.

The next theorem should improve the target covariance concentration layer itself, alter the effective target information budget, or prove a sharper design-specific target result. Further shrinking the calibration interval alone cannot cross the threshold on this benchmark.

## Physical reading

The narrower Proposition 55 interval means the declared calibration record distinguishes nearby relaxation times more sharply than a global first-order bound recognizes.

It does not mean the physical system becomes more stable, more integrated, or more conscious. The curvature is curvature of a finite-sample statistical compatibility function with respect to a physical-time parameter.

The oracle floor is also a theorem diagnostic, not a physical phase transition.

## Reproducibility assets

- proof: `docs/proposition_55_quadratic_relaxation_calibration.md`
- calibration implementation: `src/observer_math/relaxation_curvature.py`
- target composition: `src/observer_math/quadratic_relaxation_target.py`
- claim tests: `tests/test_relaxation_curvature.py`
- experiment: `examples/quadratic_relaxation_calibration.py`
- machine-readable results: `docs/quadratic_relaxation_calibration.json`
- deterministic figure renderer: `examples/render_quadratic_relaxation_calibration.py`
- visible figure: `docs/quadratic_relaxation_calibration.svg`
- figure reproducibility test: `tests/test_quadratic_relaxation_calibration_artifact.py`

## Release record

The intended 0.44.0 record is:

- 55 propositions;
- 42 reproducible experiments, A-Z and AA-AP;
- 30 scientific-result figures;
- 206 claim-level tests;
- Python 3.10, 3.11, and 3.12 CI;
- Ruff clean;
- Markdown punctuation guard clean.

These counts become verified release counts only after the exact release candidate is merged and the resulting `main` workflow succeeds.
