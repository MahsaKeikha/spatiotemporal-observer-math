# Experiment BB: finite information to robust downstream conclusion

BB is the first repository experiment that executes the complete controlled chain from a finite-sample covariance certificate to a robust downstream evidence status.

## Chain
residual innovation count -> Proposition 47 covariance radius -> P58 score uncertainty -> P64 action intervals -> P63 retained physical paths -> P68/P66 robust e-evidence.

## Controlled downstream evidence
The path-specific e-values are fixed controlled inputs. This isolates the effect of physical-boundary uncertainty. A selected path can have strong evidence while a retained weak-evidence competitor blocks the robust conclusion.

## Recorded quantities
For every residual count BB records the covariance radius, perturbative-regime status, retained paths and count, robust e-value when available, threshold status, and the stronger P58 unique-recovery status.

## Interpretation discipline
A change in threshold status is attributed only to the declared composition. The experiment does not interpret the e-values as posterior probabilities and does not equate residual innovation count with general raw sensor sample count.

Generator: `../examples/finite_information_to_robust_evidence_audit.py`. The generated JSON is `finite_information_to_robust_evidence_audit.json`.
