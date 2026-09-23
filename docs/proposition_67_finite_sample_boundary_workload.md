# Proposition 67: finite-sample covariance certification to physical-boundary workload

## Purpose
P67 closes the first finite-sample version of the measurement-to-boundary chain. Earlier AY begins with a declared relative covariance radius. P67 instead obtains that radius from the existing Proposition 47 weighted Gaussian covariance concentration theorem in the exact-innovation, unit-weight setting.

For residual innovation count r, observer block dimension d, simultaneous block count B, and confidence 1-alpha, Proposition 47 supplies a simultaneous relative covariance radius delta(r,d,B,alpha). P67 composes that radius with P58, P64, and P63.

## Composition
r -> Proposition 47 covariance radius -> P58 factor and score radii -> P64 path-action intervals -> P63 retained physical-boundary set.

No additional stochastic failure event is introduced by P58, P64, or P63. Their operations are deterministic conditional on the simultaneous covariance event.

## Admissibility gate
The current inverse-covariance perturbation layer requires delta < 1. When delta >= 1, P67 reports that the finite-sample record has not entered the current perturbative regime. It does not fabricate path intervals outside that theorem domain.

## Engineering outputs
For each residual count, P67 records the Proposition 47 covariance radius, perturbative-regime status, retained physical paths, retained path count, and whether the stronger P58 unique population-path certificate holds. These are distinct milestones.

## Probability statement
If Proposition 47's declared simultaneous covariance event has confidence at least 1-alpha, then every P58/P64/P63 conclusion computed on that event inherits the same confidence. P67 does not spend a second union bound over paths.

## Scope
The current implementation uses iid unit innovation weights. It is a controlled exact-innovation finite-sample theorem, not a general sensor sample-complexity claim. Temporally correlated raw measurements require appropriate projected temporal weights or a valid whitening/calibration layer.

## Reproducibility
Implementation: `src/observer_math/finite_sample_boundary.py`. Claim-level tests: `tests/test_finite_sample_boundary.py`. Experiment BA sweeps residual counts and records transition points in machine-readable form.
