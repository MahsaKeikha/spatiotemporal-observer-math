# Assumption ledger

This ledger separates mathematical assumptions from conclusions. It should be read before applying a certificate to a new model, dataset, or interpretation.

A theorem can be correct while an application is invalid because one of its assumptions is false. This page exists to make that distinction visible.

---

# 1. Core model assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| The analytical process is linear Gaussian where exact Gaussian formulas are invoked | Closed covariance, mutual-information, canonical-correlation, likelihood, and Gaussian concentration formulas | The implemented expressions need not equal the intended population quantities; new estimators or concentration arguments are required |
| Covariance blocks are positive definite whenever log determinants, inverses, or whitening are used | Information quantities and perturbation bounds | A formula can be undefined even if numerical regularization returns a value |
| Candidate coordinates and candidate size are declared | Score evaluation and path optimization | Recovery is only relative to the supplied candidate family |
| Information factors use the documented transforms into `[0, 1]` | Geometric local and transport scores | A different transform defines a different objective and needs new stability constants |
| Continuity uses the documented Jaccard geometry | Current material-change penalty | Another geometry can change the optimizer and the recovery theorem |

---

# 2. Recovery and identifiability assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| The target or planted candidate is present in the search family | Planted-path recovery theorems | No theorem can recover a path excluded before optimization |
| The planted class has multiplicity one when labeled recovery is claimed | Class-compressed recovery | A positive class margin can identify a class without identifying one labeled member |
| Feasible class edges contain every realizable transition | Class dynamic programs | Missing competitor edges can inflate the recovery slack |
| Competitor continuity lower bounds are valid uniformly | Competitor upper action | An overstated lower bound can create a false certificate |
| Planted continuity distances are exact | Planted lower action | An understated planted penalty can create a false certificate |
| Declared symmetry groups contain the transformations treated as scientifically equivalent | Propositions 13 and 14 | A labeled answer can be mistaken for an identifiable physical distinction |

Recovery is always relative to declared observables, model assumptions, candidate families, and admissible symmetries.

---

# 3. Covariance perturbation assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Every absolute covariance error is below the relevant eigenvalue floor | Propositions 7 and 8 and later localized results | Positive definiteness and the stated perturbation constants are not guaranteed |
| Every normalized covariance radius satisfies \(\delta<1\) where relative perturbation formulas are used | Proposition 37 and descendants, including Proposition 58 | Relative log-determinant or inverse-square-root bounds can diverge |
| Local and transport covariance envelopes remain distinct when their geometry differs | Propositions 26 through 31 | Edge errors can be underestimated |
| Factor intervals contain every represented population member componentwise | Interval-certified class recovery | A class action interval can omit a member |
| Representative residual balls contain every represented population covariance | Residual-derived class recovery | Derived factor intervals are not valid for the class |
| Block comparison entries dominate the corresponding block operator norms | Block influence results | Covariance influence can escape the propagated envelope |
| Selected blocks contain every variable used by the declared score | Localized and screened-environment recovery | The compressed covariance no longer controls the intended factor |

A failed sufficient covariance condition does not prove that recovery fails. It means only that the stated certificate cannot establish recovery.

---

# 4. Screening and sample-splitting assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Data-dependent screening has independent or simultaneous statistical protection | Propositions 32 and 33 | Selecting and certifying on the same noise can invalidate coverage |
| Screening scores are computed from the covariance estimates covered by the stated event | Gaussian safe screening | Concentration does not control an unrelated score array |
| Structural nulls are exact and fixed independently of the data used to exploit them | Structural-null screening and Proposition 58 null refinement | A false or data-selected null can make the score radius too small |
| The retained block count is a deterministic upper bound when used in a second-stage union bound | Proposition 32 | The certification union bound can undercount tested blocks |
| Screening and certification observations are independent when product confidence accounting is used | Proposition 32 | Conditioning does not create an independent second-stage experiment |

---

# 5. Drift assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Pilot and screening covariance sequences refer to the same named variables and ordered blocks | Propositions 38 and 39 | A numerical covariance bound cannot repair a semantic mismatch |
| Every population drift is below its independently justified declared envelope | Proposition 39 | An understated envelope invalidates the current-population bound |
| Old and current calibration cohorts have the stated Gaussian population assignments | Proposition 40 | Either simultaneous covariance radius can be wrong |
| The candidate family is fixed before the calibration cohorts used to estimate drift are inspected | Proposition 40 | Confidence accounting can miss adaptively introduced blocks |

---

# 6. Temporally dependent Gaussian sampling

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Covariance is separable as temporal factor times spatial covariance where the weighted Gaussian reduction is used | Propositions 41 through 57 | The weighted Wishart, matrix-mgf, or innovation covariance law no longer describes the estimator |
| Deterministic bounds supplied for temporal Frobenius and spectral norms are valid | Proposition 41 | The effective-sample-size covariance radius can be too small |
| An unknown mean is constant when ordinary temporal centering is used | Proposition 42 | Mean removal can leave uncontrolled time-varying structure |
| The corrected centering normalization \(\operatorname{tr}(PR)\) is valid | Proposition 42 | The covariance estimator can be biased by the wrong normalization |
| AR(1) calibration channels are independent across space, standardized to known unit marginal variance, and share one stationary coefficient | Proposition 43 | Increment calibration can be biased or too narrow |
| Same-record calibration and covariance events use union-bound confidence accounting rather than an unjustified independence assumption | Proposition 43 | Joint confidence can be overstated |

---

# 7. Time-varying nuisance projection

| Assumption | Used for | If it fails |
| --- | --- | --- |
| The target mean lies exactly in a fixed full-rank temporal nuisance subspace selected before target inspection | Propositions 44 through 57 | Projection can leave uncontrolled mean structure or become data dependent |
| The projected covariance normalization remains strictly positive | Propositions 44 through 57 | The observable covariance normalization is not certified |
| The nuisance design used by design-specific bounds is the same design used by the estimator | Propositions 46, 48, 52-57 | The projected spectral or whitening geometry can describe the wrong subspace |
| The same innovation whitener is applied to both target values and the nuisance design | Propositions 56 and 57 | The nuisance term is not removed in the covariance geometry assumed by the proof |

---

# 8. Matrix concentration assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Proposition 47 receives the actual nonnegative temporal eigenvalue profile when temporal covariance is treated as known | Proposition 47 | The exact matrix-mgf calculation is applied to the wrong weighted Gaussian law |
| Proposition 48 inflates every ordered projected eigenvalue by a valid between-grid Weyl radius | Proposition 48 | A between-grid temporal spectrum can have a larger matrix mgf than the certificate allows |
| Proposition 49 receives a deterministic finite temporal-family cover whose operator and normalization radii dominate every admissible family member | Propositions 49, 52-54, and 57 | An uncovered temporal covariance can invalidate the family-wide matrix bound |
| Proposition 49 treats its finite cover as deterministic geometry, not as a set of stochastic events | Proposition 49 and descendants | Probability accounting can be misstated |
| Numerical Chernoff theta grids remain inside their admissible domains and are fixed independently of target data | Propositions 47-57 | An invalid or data-selected theta can break the matrix-mgf argument |
| Chernoff theta grids are interpreted as numerical tightness devices rather than statistical discretizations | Propositions 47-57 | Numerical optimization error can be confused with probability coverage |
| Block dimension and simultaneous block count correspond to the actual covariance problem being certified | Proposition 47 and Proposition 58 composition | A scalar or single-block radius can be incorrectly presented as an observer-scale simultaneous guarantee |

The last row is central to Experiment AS. A scalar covariance result is not automatically valid at observer block dimension 10 and block count 175.

---

# 9. Proposition 50 assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Calibration channels are independent Gaussian channels with known unit marginal variance, arbitrary constant means, and one common stationary \(R_{\phi,\eta}=(1-\eta)R_\phi+\eta I\) covariance | Proposition 50 and Experiment AJ | Lag-energy expectations or concentration can be misspecified |
| The declared box satisfies \(0<\phi_-\le\phi\le\phi_+<1\) and \(0\le\eta_-\le\eta\le\eta_+<1\) | Proposition 50 | The ratio map from lag correlations can cross a singular boundary or leave the proved family |
| Lag-1 and lag-2 increment norm bounds dominate the transformed temporal covariance throughout the declared box | Proposition 50 | Lag-correlation error radii can be too small |
| The calibrated parameter rectangle is nonempty before it is passed to Proposition 49 | Proposition 50 | Calibration data are incompatible with the declared family at the requested confidence level |
| Calibration data are independent of the target record and both records share the same temporal parameters | Proposition 50 | Product confidence is not justified |
| The rectangular map is interpreted as a conservative confidence region, not an exact likelihood contour | Proposition 50 | The geometry can be overinterpreted |

---

# 10. Proposition 51 assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Calibration channels are independent Gaussian channels | Proposition 51 and Experiment AK | The product residual Gaussian density is misspecified |
| All calibration channels share one temporal covariance from the declared family | Proposition 51 | No single tested parameter may describe the actual calibration law |
| Each channel mean is constant in time | Helmert mean removal | A fixed contrast need not remove the mean exactly |
| The contrast is fixed before calibration data, has orthonormal rows, and annihilates the constant vector | Proposition 51 | The residual density can retain mean structure or acquire selection effects |
| Every compressed covariance is positive definite for every admissible parameter | Proposition 51 likelihood | The Gaussian residual density can be singular or undefined |
| The mixture density \(q\) is proper and fixed independently of the observed calibration record | Proposition 51 e-value identity | The expectation-one e-value identity is not guaranteed |
| The true temporal parameter lies inside the declared family | Proposition 51 coverage | The confidence set is only guaranteed inside the model class |
| The numerical grid is treated only as a view of the continuum function | Experiment AK | A plotted grid can be mistaken for a certified continuum set |

---

# 11. Proposition 52 assumptions

| Assumption | Used for | If it fails |
| --- | --- | --- |
| The Proposition 51 family and declared parameter box contain the true shared temporal parameter | Proposition 52 outer-cover coverage | Retained cells need not contain the physical temporal law |
| Outer-cover grid geometry is fixed by the declared box and grid sizes before exclusion is evaluated | Proposition 52 | Data-selected partitions require separate selection control |
| Every cell-specific compressed covariance radius dominates all covariance motion inside the cell | Likelihood variation and eigenvalue cover | A cell could be excluded even though part of the exact confidence set lies inside it |
| Every finite likelihood variation bound remains inside its stated positive-definite domain | Proposition 52 cell exclusion | Determinant and inverse perturbation bounds are not valid |
| A cell is excluded only when the complete cell is proved rejected | Continuum containment | The retained union may fail to contain the exact confidence set |
| Target eigenvalue and normalization radii use the documented distinct bounds | Proposition 52 target composition | Projected normalization uncertainty can be understated |
| Calibration and target records are independent and share the same true temporal parameter | Product confidence | Conditioning on the retained random cover does not leave the stated independent target experiment |
| Target nuisance design is fixed before inspecting target stochastic noise | Target covariance | Data-selected nuisance removal can require separate selection control |
| The retained outer cover is nonempty before a target certificate is issued | Implementation | An empty family is evidence of incompatibility or numerical failure, not a valid certificate |
| The target record satisfies Proposition 49's separable Gaussian assumptions | Target matrix concentration | The family-wide matrix theorem need not describe the target estimator |

---

# 12. Proposition 53 assumptions and physical diagnostics

| Assumption | Used for | If it fails |
| --- | --- | --- |
| Temporal covariance is modeled by the single exponential kernel \(K_\tau(t,s)=\exp(-|t-s|/\tau)\) | Proposition 53 | Multiple timescales, oscillatory memory, nonstationarity, or other kernels can make \(\tau\) inadequate |
| Physical sample times are known, finite, and strictly increasing | Irregular-time covariance construction | The elapsed-time model is not defined as implemented |
| \(\tau>0\) and the declared interval satisfies \(0<\tau_-\le\tau_+\) | Relaxation inversion and covers | The exponential model or derivative bounds are undefined |
| One \(\tau\) is intended to describe the same temporal law across sampling schedules being compared | Sampling-consistency interpretation | Different recovered \(\tau\) values can indicate model failure or a changed physical regime |
| Time-unit changes rescale both timestamps and \(\tau\) by the same positive factor | Time-unit invariance | Rescaling only one side changes the physical model |
| The analytic operator-Lipschitz constant is computed over the full declared interval and actual timestamp grid | Continuum cover | Between-grid covariance matrices can be uncovered |
| Dense Experiment AM evaluation is treated as a numerical scale check, not the continuum proof | Experiment AM | A finite visualization grid can be mistaken for the theorem |

A real application should challenge the one-timescale model. Useful checks include:

1. fit or calibrate the model at more than one sampling interval and compare implied \(\tau\) values;
2. inspect residual autocorrelation for unexplained structure;
3. inspect the spectrum for oscillatory or multi-timescale behavior;
4. compare predictions on held-out irregular time separations;
5. test stationarity across time blocks;
6. widen or replace the temporal family when diagnostics fail.

Systematic violation of

\[
\phi_{k\Delta t}=\phi_{\Delta t}^{k}
\]

beyond uncertainty is evidence against one common exponential relaxation time.

---

# 13. Proposition 53B and Proposition 54 assumptions

## Proposition 53B

The finite-sample irregular-time \(\tau\) confidence set assumes independent calibration channels, Gaussianity, known zero mean, unit marginal variance, one common stationary exponential relaxation time, a predeclared positive \(\tau\) interval, and a mixture numerator fixed before inspecting the calibration record.

Target composition additionally assumes calibration and target records are independent and inherits Proposition 49's target covariance assumptions.

## Proposition 54

Proposition 54 additionally assumes:

- the fine calibration-cell cover is a valid deterministic outer enclosure of the Proposition 53B continuum set;
- the target temporal cover is built only after conditioning on the independent calibration result;
- compression from the calibration cover to the target cover retains a valid operator and normalization envelope for every retained \(\tau\);
- changing numerical cover resolution does not change the underlying probability event.

The two scales are numerical certification devices, not two physical relaxation times.

---

# 14. Proposition 55 assumptions

**Assumptions.** The Proposition 53B calibration model remains in force: independent standardized Gaussian calibration channels, one stationary exponential physical relaxation time, strictly increasing timestamps, a mixture density fixed before calibration observations, and a declared finite relaxation-time interval. Target composition additionally requires an independent target record, fixed target timestamps, and fixed nuisance design.

**What the curvature theorem certifies.** The analytic first derivative and deterministic second-derivative bound give a valid quadratic lower enclosure of the observed continuum log e-value on every calibration cell. A cell is excluded only when the complete cell is proved rejected.

**Failure modes.** Multi-timescale relaxation, oscillation, nonstationarity, heavy-tailed innovations, dependent calibration channels, or calibration-target mismatch can invalidate the physical model even when the mathematical cell certificate is correct.

**Oracle diagnostic.** The known-\(\tau\) target calculation is not an implementable inference procedure. It is used only to identify whether temporal-parameter uncertainty remains the dominant source of the target radius.

---

# 15. Proposition 56 assumptions: exact innovation whitening

Proposition 56 assumes:

| Assumption | Why it is needed | If it fails |
| --- | --- | --- |
| Target covariance is exactly separable as \(R_\tau\otimes\Gamma\) | Converts temporal whitening into independent Gaussian innovation rows with common spatial covariance | Residual rows need not be independent or share one \(\Gamma\) |
| The target temporal law is the declared one-timescale exponential kernel | Supplies the exact Proposition 53 bidiagonal whitener | Whitening can leave residual temporal dependence |
| The true target \(\tau\) is known exactly for Proposition 56 | Gives \(W_\tau R_\tau W_\tau^\mathsf T=I\) | The exact Wishart reduction no longer follows; use a robustness theorem such as Proposition 57 |
| Target timestamps are strictly increasing | Defines local transition correlations and innovation variances | The factorization is not defined as implemented |
| Nuisance design is fixed, full rank, and transformed by the same \(W_\tau\) | Makes nuisance removal exact in innovation coordinates | The residual covariance can retain deterministic structure |
| Declared covariance blocks and block count are fixed before target concentration | Supports simultaneous probability accounting | Adaptive post-selection can invalidate the stated block guarantee |

Under these assumptions,

\[
(N-q)\widehat\Gamma_{\mathrm{IW}}
\sim\operatorname{Wishart}_d(\Gamma,N-q).
\]

The seeded Experiment AQ repetitions are visibility checks. The finite-sample probability statement comes from the exact reduction and Proposition 47.

---

# 16. Proposition 57 assumptions: robust innovation whitening

Proposition 57 replaces exact target \(\tau\) by an independently calibrated finite-sample interval. It assumes:

| Assumption | Why it is needed | If it fails |
| --- | --- | --- |
| The calibration interval contains the true target \(\tau\) on the calibration event | Makes the transformed family cover physically relevant | A true target law outside the interval is not certified |
| Calibration and target records are independent when confidence levels are multiplied | Gives the documented product-confidence lower bound | Product confidence can be overstated |
| The target shares the same declared exponential temporal family as calibration | Lets the calibration interval constrain target temporal covariance | Calibration-target mismatch invalidates the composition |
| One working \(\tau_0\) and whitener \(W_0\) are fixed from calibration information before target stochastic noise is inspected | Keeps the target estimator fixed conditional on calibration | Target-adaptive whitener selection needs additional control |
| The deterministic transformed-family operator cover dominates \(W_0R_\tau W_0^\mathsf T\) for every admissible \(\tau\) | Makes Proposition 49 uniform over the true transformed family | An uncovered true covariance invalidates the target radius |
| The projected-normalization envelope is valid over the full transformed family | Controls the estimator's deterministic reference normalization | The final relative radius can be understated |

The pointwise AR diagnostic radii are not substitutes for the uniform theorem. They measure conservatism at selected parameter values.

---

# 17. Proposition 58 assumptions: covariance uncertainty to world-tube recovery

Proposition 58 is a **deterministic bridge**. Its probability statement is inherited from whatever simultaneous covariance event is supplied to it.

It assumes:

| Assumption | Why it is needed | If it fails |
| --- | --- | --- |
| Candidate family, node count, subset size, local factors, transport factors, and score weights describe the same declared world-tube problem | The bridge must propagate uncertainty through the actual objective being optimized | A covariance certificate for one model cannot certify a different score or candidate geometry |
| For candidate \(S\) at time \(t\), the supplied relative covariance radius controls the complete observer block \(B_{t,S}=(X_t,X_{t+1}^{S})\) | That block is used to control the candidate's local factors and all incoming transport edges | Missing score variables can leave a factor uncontrolled |
| Every relative covariance radius used by the generic formulas satisfies \(\delta_{t,S}<1\) | Keeps log-determinant and inverse-square-root perturbation bounds finite | The current relative bridge is outside its admissible regime |
| The simultaneous covariance event covers every observer block claimed by the final certificate | Allows one deterministic path statement on that event | Omitting a block can leave a competitor or factor statistically unprotected |
| Structural integration nulls are exact and declared independently of the covariance noise when the null-specific refinement is used | Makes the sharper quadratic null bound valid | A false or post-selected null can produce an invalidly small score radius |
| Continuity penalties are deterministic and use the same candidate geometry as the population world-tube objective | They enter both the planted and competitor action bounds | Mismatched geometry changes the optimization problem |
| The population factor arrays used to evaluate the deterministic theorem lie in the documented `[0,1]` range | Required by the product-root stability bounds | The stated score-error formulas do not apply |

## Probability accounting for Proposition 58

Proposition 58 spends **no new probability budget**.

If the simultaneous covariance event holds with probability at least \(1-\alpha\), and the deterministic recovery slack returned by Proposition 58 is positive on that event, then the population world-tube is certified with probability at least \(1-\alpha\).

No independence assumption is introduced by the deterministic covariance-to-score-to-path map itself.

## What Experiment AS does not mean

Experiment AS records:

- an observer-scale exact-\(\tau\) covariance radius `1.8573569119 > 1` at 118 residual innovation degrees;
- entry into the current matrix theorem's \(\epsilon<1\) regime at 346 residual innovation degrees;
- a current generic uniform path-certifying relative radius of approximately `1.11e-4`;
- a very large residual-degree value implied by combining that tiny uniform radius with the current unit-weight matrix theorem.

The last value is **not a fundamental sample-complexity lower bound** and is **not a physical sample requirement**. It is a conservatism diagnostic for the current proof chain.

A failed Proposition 58 sufficient condition does not imply the population path is unrecoverable.

---

# 18. Confidence accounting rules

| Rule | Used for | If violated |
| --- | --- | --- |
| Use a union bound when two events may depend on the same observations unless a stronger argument is proved | Same-record results such as Proposition 43 | Multiplying confidence levels can overstate coverage |
| Multiply confidence levels only when the conditioning and independence argument is explicit | Propositions 50, 52, 54, 55, and 57 | Product confidence can be invalid under data reuse |
| Proposition 51 needs no parameterwise union bound because the confidence set is defined by one e-value at the true parameter | Proposition 51 | Adding a grid union penalty describes a different weaker procedure |
| Propositions 52, 54, 55, and 57 use deterministic covers or enclosures rather than independent stochastic tests at every cell or grid point | Temporal-family geometry | Adding a probability penalty confuses geometric certification with confidence accounting |
| Proposition 58 adds no probability event after the simultaneous covariance event | Covariance-to-world-tube bridge | Adding another arbitrary confidence penalty would understate the proved guarantee |

---

# 19. Interpretation rules

- A positive sufficient condition proves robustness only inside its declared model, candidate family, and perturbation envelope.
- A failed sufficient condition does not prove failed recovery.
- Numerical recovery on a planted construction validates implementation but does not establish external validity.
- Symmetry can make labeled recovery impossible even when an optimizer returns one representative.
- None of the scores is a measurement or proof of phenomenal consciousness.
- A future consciousness interpretation requires an explicit bridge hypothesis; observer structure alone does not supply that bridge.
- Any such bridge should meet the [Interpretation Protocol](interpretation_protocol.md), including identifiability, representation invariance, causal discriminability, temporal identity, falsifiability, competing explanations, and independent empirical anchoring.

---

# 20. Application checklist

Before reporting a certificate or confidence set, record:

1. the physical observables, units, timestamps, preprocessing, and candidate geometry;
2. the model family and every assumption used by the selected proposition;
3. the source of every eigenvalue, covariance, temporal-dependence, and nuisance bound;
4. which quantities were fixed before inspecting each dataset;
5. the exact confidence accounting rule;
6. whether calibration and target data are reused or independent;
7. every symmetry under which only equivalence-class recovery is meaningful;
8. whether a plotted grid is a theorem object, a certified cover, or only a visualization;
9. whether residual diagnostics support the declared temporal model;
10. for P56, whether the target \(\tau\) is genuinely known rather than estimated;
11. for P57, how the calibration interval, working whitener, transformed-family cover, and product confidence were obtained;
12. for P58, the observer-block dimension, simultaneous block count, candidate-local covariance radii, structural-null declarations, and path recovery slack;
13. the result when uncertain bounds or model ranges are widened;
14. whether any interpretation goes beyond the proved observer-structure claim and, if so, which additional bridge assumptions it uses.

The correct scientific question is not only whether the code returns a certificate. It is whether the declared physical and statistical assumptions justify applying that certificate to the system under study.
