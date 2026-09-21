# IEEE TCST submission strengthening record

This record turns the TCST strengthening audit into repository-traceable submission work. It is not manuscript prose and does not create claims beyond results already proved or reproduced in this repository.

## Verified submission evidence

Before submission, rerun the complete test suite and the manuscript control benchmark from the exact release candidate. The prior strengthening audit records 227 passing tests and exact regeneration of the manuscript Table I benchmark; these counts are historical verification points and must be refreshed on the release commit rather than copied forward as current CI status.

The manuscript numerical claims to audit against committed records are:

| Manuscript quantity | Repository evidence | Expected value |
| --- | --- | ---: |
| Population path margin | `docs/observer_bridge_dimension_audit.json` | 0.12642161850202815 |
| Observer-scale covariance radius | `docs/api_observer_bridge.md`, `docs/assumption_ledger.md` | 1.8573569119 |
| Known-relaxation-time scalar radius | `docs/figure_reading_guide.md`, `innovation_whitened_target.json` | about 0.43647 |
| Maximum required covariance block dimension | `docs/observer_bridge_dimension_audit.json` | 10 |
| Simultaneous covariance block count | `docs/observer_bridge_dimension_audit.json` | 175 |
| Residual-innovation degrees of freedom required for radius below one | `docs/observer_bridge_dimension_audit.json` | 346 |

These values must be regenerated or directly checked at the tagged submission commit.

## Proven contribution map

The paper should expose the theorem chain instead of compressing the framework into a benchmark narrative. Exact proposition statements live in `docs/proofs_and_conjectures.md`.

| Paper-level claim | Repository result |
| --- | --- |
| Finite-horizon robustness of the optimal boundary path under bounded score perturbations | Proposition 4 |
| Componentwise sufficient recovery condition | Proposition 5 |
| Finite-sample recovery from uniform score bounds | Proposition 6 |
| Gaussian conditional-mutual-information perturbation bound | Proposition 7 |
| Canonical-persistence perturbation bound | Proposition 8 |
| End-to-end Gaussian sample-complexity guarantee | Proposition 9 |
| Positive-factor stability of geometric scores | Proposition 10 |
| Localized finite-sample path certificate | Proposition 11 |
| Parameter-level linear-Gaussian certificate | Proposition 12 |
| Identifiability modulo an explicitly declared symmetry group | Proposition 13 |
| Two-model observational impossibility bound | Proposition 14 |
| Sufficient near-competitor graph | Proposition 15 |
| Symbolic recovery for the covariance-preserving moving-clique family | Proposition 16 |
| Covariance propagation around that moving-clique family | Proposition 17 |
| Quadratic CMI control near zero conditional cross-covariance | Proposition 18 |
| Bounded transport score | Proposition 3 |

Do not cite proposition numbers from an external planning document without checking this canonical file. In particular, temporal-calibration proposition numbering must be read from the current repository version before manuscript insertion.

## TCST control-systems gap

The repository currently establishes identification, path recovery, identifiability limits, perturbation control, and finite-sample certification. Those results do not by themselves establish closed-loop stability or closed-loop performance of a controller driven by the estimated boundary.

A TCST manuscript must therefore do one of two things:

1. **Certification-first paper:** make the control benchmark an application of the proved estimator/certification framework and explicitly state that closed-loop stability under structural-estimation error is outside the proved scope; or
2. **Control-theorem extension:** add a separately proved closed-loop result under explicit assumptions (for example, a common/multiple Lyapunov or dwell-time condition with bounded estimator mismatch), its tests, deterministic simulation, and benchmark comparison before claiming stability.

Until option 2 is completed, the manuscript and repository must not imply a stability theorem that is absent from the proof record.

## Minimum closed-loop validation if the paper claims a controller

Use one deterministic benchmark with a declared plant, estimator, supervisor, and controller. Compare at least:

- oracle structural boundary;
- fixed-boundary estimator/controller;
- a conventional switching or multiple-model baseline;
- proposed boundary-aware estimator/controller.

Report state-estimation RMSE, structural-support recovery (or IoU/F1 where appropriate), detection/switching delay, cumulative quadratic cost, control effort, settling behavior, robustness to process/measurement noise and model mismatch, and constraint violations when constraints are part of the design. Every table and figure must regenerate from committed code and machine-readable result records.

## Submission-integrity gates

Before creating the submission tag:

- rerun the complete tests from a clean environment;
- regenerate every manuscript table and scientific figure;
- verify every reported number against generated result records;
- verify every theorem/proposition citation against `docs/proofs_and_conjectures.md`;
- keep recovery, observational identifiability, finite-sample certification, and closed-loop performance as distinct claims;
- retain negative certification results, including the observer-scale radius above one, and explain them as limits of the sufficient certificate rather than hiding them;
- verify every bibliographic DOI, volume, year, and page/article number against the publisher record;
- resolve uncited bibliography entries or remove them;
- fill the final author email and ORCID;
- cite the exact tagged repository release in the code/data availability statement;
- preserve the documented Tegmark lineage if observer-factorization language remains in the manuscript.

## Release criterion

The IEEE submission package is repository-supported only when the exact manuscript version points to a frozen commit/tag for which tests, benchmark regeneration, figure/table regeneration, numerical claim checks, reference checks, and manuscript-to-proposition mapping all pass. A release checklist should record the exact commit SHA and commands used.

## Scientific boundary

Passing repository tests establishes consistency with the implemented mathematics and deterministic benchmarks. It is not external experimental validation, a general proof of closed-loop stability, or evidence that every sufficient finite-sample certificate is tight. The paper should state those boundaries explicitly.
