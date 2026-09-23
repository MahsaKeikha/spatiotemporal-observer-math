# IEEE Transactions on Automatic Control submission record

## Manuscript

**Title:** Inferring Moving Subsystem Boundaries From Stochastic Dynamics: Recovery and Finite-Sample Certification of Spatiotemporal World-Tubes

**Author:** Mahsa Keikha, Member, IEEE  
**Article type:** Full Paper  
**Journal:** IEEE Transactions on Automatic Control  
**Submission number:** 26-2855  
**Submitted:** 22 September 2026  
**Status:** Submitted for peer review. This record does not imply acceptance or publication.

## Scope represented by this repository

The manuscript treats moving-subsystem identification as an operational stochastic inference and certification problem. The repository provides the broader auditable record for:

- the spatiotemporal world-tube objective and finite-horizon optimization;
- population recovery margins and strongest-competitor comparisons;
- observational identifiability and explicit non-identifiability cases;
- covariance perturbation and propagation to information and persistence scores;
- finite-sample path-level certification under declared assumptions;
- physical-time dependence and innovation-whitening analyses;
- controlled moving-module experiments, baseline comparisons, sensitivity studies, and reproducible figures.

## Reproducibility map

| Manuscript layer | Repository record |
| --- | --- |
| Problem formulation and notation | [Research Overview](research_overview.md) |
| Formal results and proof status | [Proofs and Conjectures](proofs_and_conjectures.md) |
| Assumptions and validity boundaries | [Assumption Ledger](assumption_ledger.md) |
| Numerical results and benchmark values | [Reproducible Results](reproducible_results.md) |
| Physical model and time calibration | [Physics Guide](physics_guide.md) |
| Equation and literature provenance | [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md) |
| Figure-level evidence | [Visual Research Guide](visual_research_guide.md) |
| Executable verification | [tests/](../tests/) |

## Interpretation boundary

A recovered or certified world-tube is a result about a declared physical subsystem-identification problem. It is not, by itself, evidence that the recovered subsystem is conscious, a proof of a physical-to-experiential bridge, or evidence that the assumptions of the statistical model hold universally.

Repository content may continue to develop after the submitted manuscript. Where later repository extensions go beyond the submitted paper, they should be read as subsequent research rather than as content of submission 26-2855.
