# Release 0.43.0 research record

## Proposition 54 and Experiment AO

Release 0.43.0 adds a two-scale finite-sample propagation theorem for irregular-time physical relaxation calibration.

The previous Proposition 53B pipeline used the same retained calibration-cell centers as the target temporal cover. Proposition 54 removes that numerical coupling.

A fine calibration partition is used only to certify containment of the continuum e-value confidence set. The resulting retained physical-time span is then covered by a separate target grid whose size can be selected from calibration-derived geometry and declared target design information without inspecting target observations.

## New theorem

For a retained physical-time interval

\[
I_Z=[\tau_-,\tau_+]
\]

and \(K\) equally spaced target representatives, let

\[
h=\frac{\tau_+-\tau_-}{K-1}.
\]

Every retained \(\tau\) is within \(h/2\) of a representative. If the target temporal family obeys

\[
\|R_\tau-R_{\tau'}\|_2
\le L_Z|\tau-\tau'|,
\]

then the temporal eigenvalue cover radius is

\[
\delta_\lambda=L_Zh/2.
\]

For nuisance rank \(q\), equal trace of the exponential correlation matrices gives projected-normalization radius

\[
\delta_d=q\delta_\lambda.
\]

These quantities plug directly into Proposition 49.

## Experiment AO

Experiment AO reuses the exact physical calibration problem from Experiment AN.

At 160 calibration cells, the certified relaxation-time interval is

\[
[0.495625,1.1065625]\ \mathrm{s}
\]

with width `0.6109375 s`.

At 2560 cells it contracts to

\[
[0.66396484375,0.8761328125]\ \mathrm{s}
\]

with width `0.21216796875 s`.

For the final benchmark, 1280 calibration cells are used and a calibration-only target-cover search selects \(K=65\).

The Proposition 53B baseline relative covariance radius is

\[
3.155489544511118.
\]

The Proposition 54 two-scale radius is

\[
\boxed{2.572074694777741}.
\]

This is an absolute reduction of `0.5834148497333773`, or approximately `18.49%`.

The temporal eigenvalue covering radius falls from approximately `0.10916` to `0.06363`.

## Interpretation

The result establishes that calibration-grid and target-cover coupling was a real source of looseness, but not the dominant one.

The final radius remains above one. Therefore this release does not yet activate downstream inverse-covariance perturbation results that require \(\epsilon<1\).

The next mathematical target is a sharper local certificate for the temporal family, especially a curvature or second-order replacement for the current first-derivative worst-case propagation bound.

## Reproducibility assets

- theorem: `docs/proposition_54_two_scale_irregular_tau_cover.md`
- implementation: `src/observer_math/two_scale_relaxation_cover.py`
- tests: `tests/test_two_scale_relaxation_cover.py`
- experiment: `examples/two_scale_irregular_tau_cover.py`
- machine-readable results: `docs/two_scale_irregular_tau_cover.json`
- visible result figure: `docs/two_scale_irregular_tau_cover.svg`

## Verified release target

The intended post-merge record for 0.43.0 is:

- 54 propositions;
- 41 reproducible experiments, A-Z and AA-AO;
- 29 scientific-result figures;
- 200 claim-level tests;
- Python 3.10, 3.11, and 3.12 CI;
- Ruff clean.

These counts are release targets until the exact release candidate is merged and its `main` workflow succeeds.
