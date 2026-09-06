# Spatiotemporal Observer Mathematics

An open research project led by **Mahsa Keikha, PhD**.

This repository studies a question motivated by Max Tegmark's
*Consciousness as a State of Matter*:

> Can an observer be identified from mathematics alone when its boundary and
> internal representation are allowed to change through time?

Tegmark's framework connects information, integration, independence, dynamics,
and tensor factorization. This project begins by reproducing those ideas in
tractable models, then extends the factorization problem from a static choice to
a path through factorization space.

## Proposed contribution

The core object is an **observer world-tube**. Instead of representing an observer
as one fixed subsystem \(S\), we represent it as a sequence of factorizations
\(F_t\), or a sequence of classical subsystem boundaries \(S_t\). Persistent
identity is then organizational continuity along this path, not permanent
membership of the same physical components.

![Observer world-tube baseline](docs/worldtube_baseline.png)

The first baseline combines:

- directed integration across an internal minimum-information partition
- conditional insulation from the environment
- predictive persistence across time

The current score is a candidate measure of observer-like organization. It is
not a test for phenomenal consciousness.

## Repository map

| Path | Purpose |
| --- | --- |
| `src/observer_math/` | Exact Gaussian information measures and subsystem search |
| `examples/` | Reproducible numerical experiments |
| `tests/` | Mathematical and numerical invariants |
| `docs/mathematical_framework.md` | Definitions, proposed action, and open proofs |
| `docs/research_program.md` | Staged path from baseline to quantum formulation |
| `manuscript/` | Paper source and bibliography |
| `notebooks/` | Explanatory and exploratory computations |

## Working paper

Read the current manuscript:
[`The Observer World-Tube Principle`](manuscript/observer-world-tube-principle.pdf).

## Run the baseline

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,viz]"
pytest
python examples/baseline_experiment.py
```

## Research discipline

The repository separates four levels of statement:

1. established results reproduced from cited work
2. definitions introduced in this project
3. numerical evidence
4. conjectures requiring proof or experiment

Novelty is not asserted until comparisons with temporal integrated information,
PhiID, dynamical independence, causal emergence, and dynamic community methods
are complete.

## Primary reference

Max Tegmark, "Consciousness as a State of Matter," *Chaos, Solitons & Fractals*
76 (2015), 238-270. [arXiv:1401.1219](https://arxiv.org/abs/1401.1219),
[journal DOI](https://doi.org/10.1016/j.chaos.2015.03.014).

## Status

Version 0.1 is a research scaffold. The Gaussian baseline is implemented. The
time-dependent factorization geometry is a defined research target and is not
yet presented as a completed theory.
