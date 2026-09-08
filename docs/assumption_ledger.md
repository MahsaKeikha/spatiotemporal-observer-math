# Assumption ledger

This ledger separates mathematical assumptions from conclusions. It should be
read before applying a certificate to a new model or dataset.

## Model and score assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| The analytical process is linear Gaussian | Closed covariance, mutual-information, and canonical-correlation formulas | The implemented formulas are no longer exact; new estimators and concentration results are required |
| Covariance blocks are positive definite with declared spectral bounds | Log determinants, whitening, and perturbation radii | A bound may be undefined or invalid even if numerical regularization produces a value |
| Candidate coordinates and size are declared | Score evaluation and path search | Recovery is only relative to the supplied family |
| Information factors are mapped to `[0, 1]` by the documented transforms | Geometric local and transport scores | A different transform defines a different model and requires new stability constants |
| Continuity uses Jaccard distance | Current material-change penalty | Other geometries may change the optimizer and theorem constants |

## Recovery assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| The planted candidate is present at every layer | All planted-path theorems | No theorem can recover a path excluded from the search space |
| The planted class has multiplicity one | Unique candidate recovery from class compression | A positive class margin identifies a class path, not one labeled candidate path |
| Feasible class edges contain every realizable candidate transition | Class dynamic programs | Excluding a realizable competitor can inflate the recovery slack |
| Competitor continuity lower bounds are valid uniformly | Upper action of every competitor | An overstated lower bound can create a false certificate |
| Planted continuity distances are exact | Planted lower action | An understated planted penalty can create a false certificate |

## Perturbation assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Every covariance error is below its eigenvalue floor | Propositions 7 and 8 | Positive definiteness and the reported perturbation constants are not guaranteed |
| Every normalized covariance radius satisfies \(\delta<1\) | Proposition 37 | The relative log-determinant and inverse-square-root bounds are not finite; the screen must return to a trivial radius |
| Local and transport covariance envelopes are kept separate | Propositions 26 through 31 | Edge errors may be underestimated when class geometry changes across time |
| Factor intervals contain every member componentwise | Proposition 28 | The class-level action bounds need not cover an omitted member |
| Representative residual balls contain every population member | Proposition 29 | Derived factor intervals are not valid for the class |
| Block comparison entries dominate the corresponding matrix-block norms | Propositions 23 through 25 and 30 | Covariance influence can exceed the propagated envelope |
| Selected future blocks contain every variable used by the class score | Propositions 26, 30, and 31 | The compressed joint covariance does not control the intended factor |

## Screened-environment assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Selected present blocks contain the candidate variables and all variables used by screened factors | Proposition 31 | Integration, persistence, or retained leakage may be uncontrolled |
| Omitted conditional leakage is at most the declared tail bound | Proposition 31 | The lower insulation endpoint can be too high |
| A zero tail is used only with proved conditional irrelevance | Exact environmental screening | Ignored predictive drive can produce a false positive margin |
| Data-dependent screening has independent or simultaneous statistical protection | Propositions 32 and 33 | Selecting and certifying on the same noise can invalidate coverage |

## Statistical assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Trajectories are independent Gaussian draws | Current Wishart concentration theorem | One long dependent series needs mixing or martingale concentration |
| Confidence parameters and covariance dimensions match the tested blocks | Sample-complexity calculations | The advertised coverage probability may be wrong |
| Any ridge contribution is included in the spectral error budget | Regularized empirical covariance | The analytical radius understates total error |
| Candidate family and spectral envelopes are fixed before the screening split | Proposition 33 | The first-stage union bound need not cover adaptively introduced blocks or bounds |
| Screening scores are computed from the covariance estimates covered by the stated first-split event | Proposition 33 | Covariance concentration does not control an unrelated score array |
| Empirical primitive factors and score centers are computed consistently | Proposition 34 | A factor-aware radius need not bound the supplied score |
| Positive-factor refinement is used only where every empirical factor lower endpoint is strictly positive | Proposition 34 | The local Lipschitz denominator can cross its singular boundary; the zero-safe fallback is required |
| Every structural integration null is exact and its mask is fixed independently of the screening observations | Proposition 35 | The quadratic boundary radius can understate the local-score error and the safe-screen guarantee is invalid |
| Wishart calibration uses exact population covariance matrices | Experiments S, U, V, and W | It cannot validate envelopes estimated from the same observations |
| Complete trajectories are independent across the sample index; dependence within each trajectory is allowed | Propositions 36 and 37 and Experiments U through W | The Wishart law and nominal screening confidence do not apply to overlapping windows treated as independent samples |
| Multi-regime axes and action weights are fixed before inspecting outcomes | Experiment V | The grid becomes an adaptive illustration rather than a predeclared sensitivity check |
| Relative candidate blocks, confidence, and dimensions are fixed before screening | Proposition 37 and Experiment W | The simultaneous relative Wishart event may not cover adaptively introduced blocks |
| Population whitening is used to state and audit the event, not estimated and silently reused | Proposition 37 | Reusing a data-dependent whitening map requires separate concentration or sample splitting |
| Candidate screening is fixed independently of certification data | Reduced union bounds | Post-selection coverage is not guaranteed |
| The first-stage screen has a proved safety probability | Proposition 32, supplied by Proposition 33 in the Gaussian construction | Combined confidence cannot be inferred from sample counts alone |
| The retained block count is a deterministic upper bound for every realized screen | Proposition 32 | The second-stage union bound can undercount tested blocks |
| Screening and certification observations are independent | Proposition 32 | Conditioning does not turn the selected block family into a valid fixed-family test |
| The admissible covariance radius comes from a valid deterministic recovery certificate | Proposition 32 | Covariance concentration alone does not imply path recovery |

## Interpretation rules

- A positive sufficient condition proves robustness only inside its declared
  model, candidate family, and perturbation envelope.
- A failed sufficient condition does not prove failed recovery.
- Numerical recovery on a planted construction validates implementation but
  does not establish external validity.
- Symmetry can make labeled recovery impossible even when an optimizer returns
  one representative.
- None of the scores is a measurement or proof of phenomenal consciousness.

## Application checklist

Before reporting a certificate, record:

1. the candidate family and whether it is complete;
2. the source of every eigenvalue and covariance-error bound;
3. the construction of every class and its multiplicity;
4. the source of every block comparison and omitted-leakage bound;
5. whether selections were fixed before observing certification data;
6. the planted lower action, competitor upper action, and recovery slack;
7. the result when each uncertain bound is widened;
8. any symmetry under which only equivalence-class recovery is meaningful.
