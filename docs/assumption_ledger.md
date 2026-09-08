# Assumption ledger

This ledger separates mathematical assumptions from conclusions. It should be read before applying a certificate to a new model, dataset, or interpretation.

A theorem can be correct while an application is invalid because one of its assumptions is false. This page exists to make that distinction visible.

## Core model assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| The analytical process is linear Gaussian where the exact Gaussian formulas are invoked | Closed covariance, mutual-information, canonical-correlation, and Gaussian concentration formulas | The implemented expressions need not equal the intended population quantities; new estimators or concentration arguments are required |
| Covariance blocks are positive definite whenever log determinants, inverses, or whitening are used | Information quantities and perturbation bounds | The formula can be undefined even if numerical regularization returns a value |
| Candidate coordinates and candidate size are declared | Score evaluation and path optimization | Recovery is only relative to the supplied family |
| Information factors use the documented transforms into `[0, 1]` | Geometric local and transport scores | A different transform defines a different objective and needs new stability constants |
| Continuity uses the documented Jaccard geometry | Current material-change penalty | Another geometry can change the optimizer and the recovery theorem |

## Recovery and identifiability assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| The target or planted candidate is present in the search family | Planted-path recovery theorems | No theorem can recover a path that was excluded before optimization |
| The planted class has multiplicity one when labeled recovery is claimed | Class-compressed recovery | A positive class margin can identify a class without identifying one labeled member |
| Feasible class edges contain every realizable transition | Class dynamic programs | Missing competitor edges can inflate the recovery slack |
| Competitor continuity lower bounds are valid uniformly | Competitor upper action | An overstated lower bound can create a false certificate |
| Planted continuity distances are exact | Planted lower action | An understated planted penalty can create a false certificate |
| Declared symmetry groups contain the transformations treated as scientifically equivalent | Propositions 13 and 14 | A labeled answer can be mistaken for an identifiable physical distinction |

## Covariance perturbation assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Every absolute covariance error is below the relevant eigenvalue floor | Propositions 7 and 8 and later localized results | Positive definiteness and the stated perturbation constants are not guaranteed |
| Every normalized covariance radius satisfies \(\delta<1\) where relative perturbation formulas are used | Proposition 37 and descendants | Relative log-determinant or inverse-square-root bounds can diverge |
| Local and transport covariance envelopes remain distinct when their geometry differs | Propositions 26 through 31 | Edge errors can be underestimated |
| Factor intervals contain every represented population member componentwise | Interval-certified class recovery | A class action interval can omit a member |
| Representative residual balls contain every represented population covariance | Residual-derived class recovery | Derived factor intervals are not valid for the class |
| Block comparison entries dominate the corresponding block operator norms | Block influence results | Covariance influence can escape the propagated envelope |
| Selected blocks contain every variable used by the declared score | Localized and screened-environment recovery | The compressed covariance no longer controls the intended factor |

## Screening and sample-splitting assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Data-dependent screening has independent or simultaneous statistical protection | Propositions 32 and 33 | Selecting and certifying on the same noise can invalidate coverage |
| Screening scores are computed from the covariance estimates covered by the stated event | Gaussian safe screening | Concentration does not control an unrelated score array |
| Structural nulls are exact and fixed independently of the data used to exploit them | Structural-null screening | A false null can make the score radius too small |
| The retained block count is a deterministic upper bound when it is used in a second-stage union bound | Proposition 32 | The certification union bound can undercount tested blocks |
| Screening and certification observations are independent when product confidence accounting is used | Proposition 32 | Conditioning does not create an independent second-stage experiment |

## Drift assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Pilot and screening covariance sequences refer to the same named variables and ordered blocks | Propositions 38 and 39 | A numerical covariance bound cannot repair a semantic mismatch |
| Every population drift is below its independently justified declared envelope | Proposition 39 | An understated envelope invalidates the current-population bound |
| Old and current calibration cohorts have the stated Gaussian population assignments | Proposition 40 | Either simultaneous covariance radius can be wrong |
| The candidate family is fixed before the calibration cohorts used to estimate drift are inspected | Proposition 40 | The confidence accounting can miss adaptively introduced blocks |

## Temporally dependent Gaussian sampling

| Assumption | Used for | If it fails |
| --- | --- | --- |
| The covariance is separable as temporal factor times spatial covariance where the weighted Gaussian reduction is used | Propositions 41 through 50 | The weighted Wishart or quadratic-form law no longer describes the estimator |
| Deterministic bounds supplied for temporal Frobenius and spectral norms are valid | Proposition 41 | The effective-sample-size covariance radius can be too small |
| An unknown mean is constant when ordinary temporal centering is used | Proposition 42 | Mean removal can leave uncontrolled time-varying structure |
| The corrected centering normalization \(\operatorname{tr}(PR)\) is valid | Proposition 42 | The covariance estimator can be biased by the wrong normalization |
| AR(1) calibration channels are independent across space, standardized to known unit marginal variance, and share one stationary coefficient | Proposition 43 | Increment calibration can be biased or too narrow |
| Same-record calibration and covariance events use union-bound confidence accounting rather than an unjustified independence assumption | Proposition 43 | Joint confidence can be overstated |

## Time-varying nuisance projection

| Assumption | Used for | If it fails |
| --- | --- | --- |
| The target mean lies exactly in a fixed full-rank temporal nuisance subspace selected before target inspection | Propositions 44 through 50 | Projection can leave uncontrolled mean structure or become data dependent |
| The projected covariance normalization remains strictly positive | Propositions 44 through 50 | The observable covariance normalization is not certified |
| The nuisance design used by design-specific bounds is the same design used by the estimator | Propositions 46 and 48 | The projected spectral envelope can describe the wrong subspace |

## Matrix concentration assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Proposition 47 receives the actual nonnegative projected temporal eigenvalue profile when temporal covariance is treated as known | Proposition 47 | The exact matrix-mgf calculation is applied to the wrong weighted Gaussian law |
| Proposition 48 inflates every ordered projected eigenvalue by a valid between-grid Weyl radius | Proposition 48 | A between-grid temporal spectrum can have a larger matrix mgf than the certificate allows |
| Proposition 49 receives a deterministic finite temporal-family cover whose operator and normalization radii dominate every admissible family member | Proposition 49 | An uncovered temporal covariance can invalidate the family-wide matrix bound |
| Proposition 49 treats its finite cover as deterministic geometry, not as a set of stochastic events | Proposition 49 | Probability accounting can be misstated |
| Numerical Chernoff theta grids remain inside their admissible domains and are fixed independently of the target data | Propositions 47 through 50 | An invalid or data-selected theta can break the mgf argument |
| Chernoff theta grids are interpreted as numerical tightness devices rather than statistical discretizations | Propositions 47 through 50 | Numerical optimization error can be confused with probability coverage |

## Proposition 50 assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Calibration channels are independent Gaussian channels with known unit marginal variance, arbitrary constant means, and one common stationary \(R_{\phi,\eta}=(1-\eta)R_\phi+\eta I\) covariance | Proposition 50 and Experiment AJ | Lag-energy expectations or concentration can be misspecified |
| The declared box satisfies \(0<\phi_-\le\phi\le\phi_+<1\) and \(0\le\eta_-\le\eta\le\eta_+<1\) | Proposition 50 | The ratio map from lag correlations can cross a singular boundary or leave the proved family |
| Lag-1 and lag-2 increment norm bounds dominate the transformed temporal covariance throughout the declared box | Proposition 50 | Lag-correlation error radii can be too small |
| The calibrated parameter rectangle is nonempty before it is passed to Proposition 49 | Proposition 50 | The calibration data are incompatible with the declared family at the requested confidence level |
| Calibration data are independent of the target record and both records share the same temporal parameters | Proposition 50 | Conditioning on the random calibrated family does not leave an independent target experiment; product confidence is not justified |
| The rectangular map is interpreted as a conservative confidence region, not as an exact likelihood contour or equal-plausibility set | Proposition 50 | The geometry can be overinterpreted |

## Proposition 51 assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Calibration channels are independent Gaussian channels | Proposition 51 and Experiment AK | The product residual Gaussian density \(p_\theta\) is misspecified |
| All calibration channels share one temporal covariance from the declared family | Proposition 51 | The pointwise denominator density need not equal the true data density for any single \(\theta\) |
| Each channel mean is constant in time | Helmert mean removal in Proposition 51 | A fixed contrast need not remove the mean exactly |
| The contrast matrix is fixed before seeing the calibration data, has orthonormal rows, and annihilates the constant vector | Proposition 51 | The residual density can acquire data-dependent selection effects or retain mean structure |
| Every compressed covariance \(HR_\theta H^\mathsf T\) is positive definite for every admissible \(\theta\) | Proposition 51 likelihood | The Gaussian residual density can be singular or undefined |
| The mixture density \(q\) is a proper density fixed independently of the observed calibration record | Proposition 51 e-value identity | \(\mathbb E_\theta[q(Z)/p_\theta(Z)]=1\) is no longer guaranteed by the stated proof |
| The true temporal parameter lies inside the declared parameter family | Proposition 51 coverage | The confidence set is only guaranteed for parameters inside the model class |
| The numerical grid in Experiment AK is treated only as a view of the pointwise continuum function | Experiment AK | A plotted grid can be incorrectly presented as a certified outer cover |
| The accepted grid bounding box is treated as a visualization summary, not as the exact confidence set | Experiment AK | Irregular or between-grid portions of the continuum set can be omitted |

## Confidence accounting rules

| Rule | Used for | If violated |
| --- | --- | --- |
| Use a union bound when two events may depend on the same observations unless a stronger argument is proved | Same-record results such as Proposition 43 | Multiplying confidence levels can overstate coverage |
| Multiply confidence levels only when the conditioning and independence argument is explicit | Proposition 50 | Product confidence can be invalid under data reuse |
| Proposition 51 needs no parameterwise union bound because the confidence set is defined by one e-value at the true parameter | Proposition 51 | Adding a grid union penalty would describe a different and unnecessarily weaker procedure |

## Interpretation rules

- A positive sufficient condition proves robustness only inside its declared model, candidate family, and perturbation envelope.
- A failed sufficient condition does not prove failed recovery.
- Numerical recovery on a planted construction validates implementation but does not establish external validity.
- Symmetry can make labeled recovery impossible even when an optimizer returns one representative.
- None of the scores is a measurement or proof of phenomenal consciousness.
- A future consciousness interpretation requires an explicit bridge hypothesis; observer structure alone does not supply that bridge.
- Any such bridge should meet the requirements in the [interpretation protocol](interpretation_protocol.md), including identifiability, representation invariance, causal discriminability, temporal identity, falsifiability, competing explanations, and independent empirical anchoring.

## Application checklist

Before reporting a certificate or confidence set, record:

1. the model family and candidate family;
2. the source of every eigenvalue, covariance, and temporal-dependence bound;
3. which quantities were fixed before inspecting each dataset;
4. the exact confidence accounting rule;
5. whether calibration and target data are reused or independent;
6. every symmetry under which only equivalence-class recovery is meaningful;
7. the result when uncertain bounds or model ranges are widened;
8. whether a plotted numerical grid is a theorem object, a certified cover, or only a visualization;
9. for Proposition 50, the calibration-target independence argument and declared parameter box;
10. for Proposition 51, the contrast, mixture construction, declared family, and distinction between the continuum confidence set and its plotted grid view;
11. whether any interpretation goes beyond the proved observer-structure claim and, if so, which additional bridge assumptions it uses.
