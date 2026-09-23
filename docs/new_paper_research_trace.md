# New-paper research trace: boundary-aware downstream inference

## Purpose
This document is the reader map for the current Research I to Research II program. It is separate from manuscript submission status. Its job is to make the scientific chain, assumptions, code, experiments, and unresolved questions auditable from the repository.

## Central problem
A downstream scientific test can depend on a physical descriptor whose subsystem boundary was itself selected from data. Treating that selected boundary as fixed can hide a material source of uncertainty.

The current program asks: How should uncertainty about a data-inferred, time-varying physical subsystem be carried into downstream inference, computation, and evidence?

## Scientific chain

### P61: protect selection from certification
See `docs/proposition_61_sample_split_boundary_freeze.md`. Boundary selection is performed on protected pilot information and frozen before downstream certification outcomes are used. Implementation: `src/observer_math/boundary_bridge_split.py`.

### P62: propagate unresolved physical-boundary uncertainty
See `docs/proposition_62_boundary_confidence_set_propagation.md`. When one boundary is not justified, an admissible world-tube set is carried forward. Implementation: `src/observer_math/boundary_confidence_set.py`. Experiment AV: `examples/boundary_robust_evidence_audit.py`.

### P63: compress without deleting unresolved competitors
See `docs/proposition_63_certified_path_space_compression.md`. Simultaneous action intervals permit safe elimination of paths whose upper action bound cannot approach the best certified lower bound. Implementation: `src/observer_math/path_pruning.py`. Experiment AW: `examples/certified_path_compression_audit.py`.

### P64: measurement uncertainty to path-action intervals
See `docs/proposition_64_measurement_to_path_action_intervals.md`. P58 candidate-local score radii are accumulated along each world-tube to form an action interval. Implementation: `src/observer_math/action_intervals.py`.

### P65: precision as an engineering resource
See `docs/proposition_65_precision_to_ambiguity_workload.md`. Under a declared common scaling of valid action radii, tighter uncertainty cannot increase the retained path set. Implementation: `src/observer_math/precision_workload.py`. Experiment AX: `examples/precision_ambiguity_workload_audit.py`.

### Experiment AY: actual P58 perturbation formulas through P64 and P63
Generator: `examples/p58_p64_p63_composition_audit.py`. AY starts from declared relative covariance radii and uses the actual P58 covariance-to-score perturbation formulas before constructing P64 action intervals and applying P63 pruning. It is not yet a sample-size theorem; the covariance radii are controlled inputs.

## End-to-end architecture
measurement model -> simultaneous covariance event -> P58 factor and score uncertainty -> P64 path-action intervals -> P63 certified retained physical paths -> P62 boundary-robust downstream evidence.

P61 supplies the complementary sample-split route when one boundary is selected and frozen before downstream certification.

## What is proved versus demonstrated
P61-P65 are theorem or engineering-contract layers under their stated assumptions. AV, AW, AX, and AY are controlled demonstrations. AY is stronger than AX because it uses the actual P58 perturbation formulas, but it still sweeps declared covariance radii rather than deriving them from a sensor/sample-count model.

## Scientific boundary
None of P61 through P65 identifies a physical subsystem with consciousness or establishes an experiential interpretation. The contribution is an inference architecture for downstream claims whose physical representation is itself learned and uncertain.

## Reproducibility contract
Every numerical result intended for a future manuscript should have a generator under `examples/`, a machine-readable record under `docs/`, claim-level tests under `tests/`, assumptions and failure conditions documented, and a website explanation linking to the canonical artifact. No manuscript number should be used unless it can be traced to one of these artifacts.

## Next gates before manuscript drafting
1. Generate and commit the AY machine-readable record from the canonical script.
2. Couple P58/P64/P63 to a finite-sample covariance-radius theorem on a tractable benchmark.
3. Feed the retained set into P62 and quantify when boundary ambiguity changes robust downstream evidence.
4. Add negative controls where improved measurement does not change the conclusion and where unresolved ambiguity correctly prevents a strong conclusion.
5. Add computational scaling results for candidate/path count.
6. Only then decide whether the theorem and experiment package is mature enough for a full manuscript.
