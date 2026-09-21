# Research I contribution provenance ledger

This page distinguishes results developed in Research I from the external mathematical and conceptual foundations used to formulate or analyze them. Its purpose is scientific provenance: a reader should be able to tell which constructions are repository contributions, which statements are proved here under declared assumptions, and which ingredients come from prior literature.

## Contribution boundary

Research I does **not** claim invention of mutual information, conditional mutual information, canonical correlation, Jaccard similarity, dynamic programming, Wishart theory, matrix concentration, Ornstein-Uhlenbeck dynamics, or the observer-factorization question. Those ingredients have their own literature and are cited in the bibliography.

The original contribution of this research program is the particular moving-boundary inference problem and the mathematical chain developed around it: a time-indexed candidate boundary, a world-tube objective combining declared dynamical factors and cross-time transport, exact finite-horizon path optimization and margins, recovery under score and covariance perturbations, symmetry-aware identifiability, structural compression/localization, dependent-data calibration in physical time, innovation-whitened covariance inference, and propagation of uncertainty back to the complete moving-boundary decision.

Originality here means **developed in this research record**, not "proved absent from all prior literature." Priority claims require a separate literature review.

## Provenance map

| Research object or result | Status in Research I | External foundation or lineage |
| --- | --- | --- |
| Time-dependent candidate boundary and world-tube inference target | Developed here | Observer-factorization question provides conceptual motivation |
| Four-factor operational construction: integration, insulation, persistence, transport | Developed here as a combined criterion | Information theory and canonical correlation supply mathematical ingredients |
| Cross-time transport functional for changing coordinate membership | Developed here | Conditional information and canonical-correlation geometry |
| Complete world-tube action with transport and Jaccard continuity | Developed here | Jaccard similarity and Bellman dynamic programming are prior tools |
| Exact winning path, runner-up, and action margin | Developed here for the declared objective | Finite-state dynamic programming |
| Path robustness and finite-sample recovery chain | Proved here under stated assumptions | Gaussian covariance perturbation/concentration tools |
| Symmetry-aware boundary identifiability and two-model impossibility analysis | Developed and proved here under stated models | Statistical decision and total-variation ideas are prior foundations |
| Moving-clique symbolic recovery and perturbative extensions | Developed and proved here for declared model families | Linear-Gaussian dynamics |
| Influence-cone, overlap-class, and screen-first structural reductions | Developed here | Matrix norm and graph/locality techniques |
| Dependent Gaussian measurement certification | Developed here for this inference chain | Gaussian/Wishart and matrix-concentration literature |
| Physical relaxation-time calibration on irregular grids | Developed here for the declared exponential temporal family | Ornstein-Uhlenbeck / Gaussian Markov lineage |
| Exact and robust innovation-whitened target inference | Developed here for this certification problem | Gaussian innovation and Wishart identities |
| Observer-scale covariance-to-world-tube uncertainty bridge | Developed here | Matrix concentration and perturbation theory |

## Claim discipline

Repository-developed does not automatically mean globally novel. Public novelty statements should use precise language such as "we formulate," "we derive," "we prove under the stated model," or "to our knowledge" only after a documented literature search supports the comparison.

Every strong contribution claim should be traceable through four layers:

```text
claim
  -> proposition / derivation
  -> assumptions
  -> deterministic or stochastic test
  -> reproducible result record
```

A numerical experiment is not a proof. A sufficient certificate that fails is not evidence that recovery is impossible. A unique optimizer is not proof of labeled physical identifiability. A successful synthetic benchmark is not external validation.

## Distinctive theorem chain

The canonical proposition statements are maintained in [proofs_and_conjectures.md](proofs_and_conjectures.md). The contribution chain most directly associated with the moving-boundary inference problem is:

1. bounded transport and a finite world-tube objective;
2. exact path robustness from a positive action margin;
3. finite-sample recovery through factor perturbation bounds;
4. Gaussian CMI and canonical-persistence perturbation control;
5. end-to-end covariance-to-path sample-complexity composition;
6. symmetry-aware identifiability and observational impossibility;
7. structural localization and compression for moving partitions;
8. temporal-dependence calibration and physical-time inference;
9. exact/robust innovation whitening;
10. observer-scale propagation back to the complete path decision.

The exact proposition number attached to each item must always be read from the canonical proof record rather than copied from an older planning document.

## Novelty stress tests

A contribution should survive the following questions before it is described as novel:

- Is the inferred object genuinely different from a standard switching-mode label, support estimate, community assignment, or change-point sequence?
- Does the transport term add information that cannot be reduced to independent local scoring plus continuity regularization?
- Is the recovery theorem materially different from a generic argmax perturbation lemma once the world-tube structure is removed?
- Does structural localization produce a new certificate or only a computational restatement?
- Does physical-time calibration change the inferential guarantee rather than merely reparameterize an AR(1) model?
- Does innovation whitening yield a theorem specific to the moving-boundary decision chain?
- Which assumptions make each result stronger or weaker than nearby work?

Negative answers are useful. They identify where the research needs a stronger theorem, experiment, or literature comparison instead of stronger wording.

## Current boundary

The established record concerns moving-boundary identification and certification. A closed-loop controller driven by the inferred boundary is a natural extension, but general closed-loop stability is not part of the established theorem record unless and until it receives its own assumptions, proof, implementation, tests, and reproducible validation.

## Reader audit route

For the complete mathematical statements, see [Proofs and Conjectures](proofs_and_conjectures.md). For the conservative neighboring-literature audit structure, see [Closest-Method Comparison Protocol](closest_method_comparison.md). For assumptions and failure conditions, see [Assumption Ledger](assumption_ledger.md). For numerical evidence, see [Reproducible Results](reproducible_results.md). For literature provenance, see [Bibliography and Citation Map](bibliography.md). For the current validation-strengthening record, see [Research I validation strengthening](tcst_submission_strengthening.md).
