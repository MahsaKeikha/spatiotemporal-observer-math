# Deep Dive Map

This page is the bridge between the short GitHub landing page and the full technical record.

You do not need to read the repository in file order. Choose the layer that matches the question you are asking.

---

## 1. I want to understand the idea first

Start with:

- [Visual Research Guide](visual_research_guide.md)
- [Research Overview](research_overview.md)

These pages explain the moving-boundary idea, the world-tube interpretation, the main research stages, and the current frontier without requiring you to audit every proof.

---

## 2. I want to understand the physics

Use:

- [Physics Guide](physics_guide.md)
- [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md)

The Physics Guide explains the observation model, units, physical-time interpretation, covariance geometry, and the distinction between operational quantities and stronger physical interpretations.

The citation map shows where equations come from and separates standard mathematical ingredients from repository-specific definitions and results.

---

## 3. I want the mathematical construction

Use:

- [Research Overview](research_overview.md)
- [Derivations](derivations.md)
- [Proofs and Conjectures](proofs_and_conjectures.md)

This is the route for the definitions of integration, insulation, persistence, transport, the local score, the world-tube objective, global finite-horizon optimization, recovery margins, and perturbation analysis.

---

## 4. I want every theorem and proposition

Use:

- [Research Index](research_index.md)
- [Proofs and Conjectures](proofs_and_conjectures.md)
- theorem-specific proposition pages for the later results

The Research Index is the proposition-by-proposition map. It connects each result to its scientific role and, where available, its implementation, experiment, test, data record, and figure.

---

## 5. I want to see the evidence visually

Use:

- [Visual Research Guide](visual_research_guide.md)
- [Reproducible Results](reproducible_results.md)

The Visual Research Guide is the curated atlas for the 33 scientific result figures. It is the best route for readers who want to see how the research evolved before reading equations.

The reproducibility record connects figures to the scripts and numerical data that produced them.

---

## 6. I want to understand the finite-sample statistics

Use:

- [Assumption Ledger](assumption_ledger.md)
- [Research Index](research_index.md)
- [Physics Guide](physics_guide.md)

The finite-sample sequence covers covariance perturbation, screening, temporal dependence, nuisance projection, matrix concentration, physical relaxation-time calibration, innovation whitening, and propagation of covariance uncertainty back to the world-tube objective.

Every theorem remains conditional on its stated observation and stochastic assumptions.

---

## 7. I want the current frontier

Start with:

- [Proposition 58: Observer-scale covariance to world-tube bridge](proposition_58_observer_bridge.md)

The current bottleneck is not hidden. Scalar innovation-whitened covariance certification can enter the controlled perturbative regime on the declared benchmark, while the full observer-scale problem remains limited by multivariate block dimension, simultaneous candidate coverage, and conservative uncertainty propagation.

That frontier motivates the next mathematical directions: factor-specific covariance blocks, safe screening, candidate-local uncertainty, and more direct score-margin concentration.

---

## 8. I want assumptions, limitations, and falsification conditions

Use:

- [Assumption Ledger](assumption_ledger.md)
- [Interpretation Protocol](interpretation_protocol.md)

These pages separate mathematical statements from physical assumptions and from stronger interpretation. They also record situations in which the declared model or inference should not be trusted without further validation.

---

## 9. I want the literature and intellectual lineage

Use:

- [Bibliography and Citation Map](bibliography.md)
- [`../references.bib`](../references.bib)
- [`../CITATION.cff`](../CITATION.cff)

The project begins conceptually from the observer-factorization question and draws on information theory, canonical correlation, dynamic programming, covariance concentration, Gaussian relaxation models, and finite-sample calibration methods.

The bibliography records the role each source plays rather than presenting references as a disconnected list.

---

## 10. I want the software

Use:

- [API Documentation](api.md)
- [`../src/`](../src/)
- [`../tests/`](../tests/)
- [`../examples/`](../examples/)

The code, tests, and examples are part of the scientific record. The repository is designed so that theorem statements, numerical experiments, figures, and implementation checks remain traceable to one another.

---

## Recommended reading routes

### Curious reader

[README](../README.md) -> [Visual Research Guide](visual_research_guide.md) -> [Research Overview](research_overview.md)

### Physicist

[README](../README.md) -> [Physics Guide](physics_guide.md) -> [Assumption Ledger](assumption_ledger.md) -> [Current frontier](proposition_58_observer_bridge.md)

### Mathematician

[Research Overview](research_overview.md) -> [Derivations](derivations.md) -> [Proofs and Conjectures](proofs_and_conjectures.md) -> [Research Index](research_index.md)

### Reviewer or auditor

[Research Index](research_index.md) -> [Assumption Ledger](assumption_ledger.md) -> [Reproducible Results](reproducible_results.md) -> [`../tests/`](../tests/)

### Reproducibility-focused reader

[Reproducible Results](reproducible_results.md) -> [`../examples/`](../examples/) -> [`../tests/`](../tests/) -> [API Documentation](api.md)

---

## One principle behind the documentation

The landing page should answer **why the question is interesting**.

The deeper pages should answer **exactly how the mathematics works, what assumptions it needs, what the experiments show, and where the claims stop**.

That separation is intentional: curiosity first, auditability one click deeper.
