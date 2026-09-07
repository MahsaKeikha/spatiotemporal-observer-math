# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)

An open research project by **Mahsa Keikha, PhD**.

## The question

Most mathematical treatments begin by choosing a system and its environment.
That is often the right place to start, but it leaves a prior question
unanswered: what makes one boundary persist as the system changes?

Here the boundary is allowed to move. At time \(t\), a candidate observer is a
subset \(S_t\) of the available variables. Its history is the path

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1}).
\]

I call this path an **observer world-tube**. The name is operational. It means a
temporally linked sequence of subsystem boundaries, not a claim about subjective
experience.

The working question is:

> Can a changing boundary be inferred from internal dynamical integration,
> insulation from external drive, and transport of predictive structure?

## What is implemented

The present model is a time-varying linear Gaussian process,

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad \varepsilon_t\sim\mathcal N(0,Q_t).
\]

This setting is limited, but useful: the covariance evolves exactly, every
information quantity has a closed form, and failures cannot be blamed on a
neural estimator.

For each candidate boundary the code measures:

- cross-prediction across its weakest internal bipartition
- prediction imported from the present environment
- canonical-correlation persistence into the next state
- transport from one candidate boundary to another

A dynamic program then finds the globally maximizing path. A second dynamic
program finds the exact runner-up and reports the action margin. That margin
gives a deterministic radius within which bounded score perturbations cannot
change the selected path.

## Current numerical result

The first nonstationary test contains a planted three-variable module whose
membership shifts by one variable at every step:

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

The optimizer recovers all five boundaries in this construction.

| Quantity | Value |
| --- | ---: |
| Recovered boundaries | 5 / 5 |
| Winning action | 1.254324 |
| Runner-up action | 1.127902 |
| Action margin | 0.126422 |
| Certified uniform score radius | 0.010535 |

This is a controlled calculation with known ground truth. It is not yet a
general recovery result. The phase diagram below is included because it shows
both success and failure: too much penalty on changing physical membership
forces the optimizer away from the moving process.

![Regularization phase diagram](docs/worldtube_phase_diagram.png)

The fixed-boundary control is also intentionally simple. Correlated process
noise produces nonzero static integration, while the directed integration and
the combined score remain zero. This checks that correlation by itself is not
being mistaken for continuing internal organization.

### Recovery from estimated covariances

A second benchmark replaces analytical covariances with estimates from sampled
trajectories. Across 32 trials per sample size, exact world-tube recovery rises
from `0.313` at 80 trajectories to `0.750` at 160, `0.938` at 320, and `1.000`
at 640.

![Finite-sample recovery and baseline comparison](docs/finite_sample_benchmark.png)

The comparison is not uniformly favorable to the full method. Independent
local selection performs better at intermediate sample sizes on this easy
construction. That negative result is recorded because it defines the next
test: a generative family in which local evidence is ambiguous and cross-time
transport is necessary.

The end-to-end 95% theorem is intentionally worst case. For the same population
margin it gives a sufficient sample count of approximately
\(1.263\times10^{19}\), compared with empirical recovery at hundreds of
trajectories. This gap is reported as a limitation and a target for sharper,
candidate-sensitive concentration bounds.

The rate calculation isolates the main cause: allowing a score factor to
approach zero changes the worst-case local-score rate from \(N^{-1/2}\) to
\(N^{-1/6}\), creating sixth-power dependence on the inverse action margin.

## Read the project

| Document | Contents |
| --- | --- |
| [Mathematical framework](docs/mathematical_framework.md) | Definitions and the world-tube objective |
| [Space, time, and observer identity](docs/space_time_observer.md) | The conceptual bridge and the mathematics still missing |
| [Derivations](docs/derivations.md) | Gaussian information formulas, canonical transport, and dynamic programming |
| [Proved results and open problems](docs/proofs_and_conjectures.md) | Nine proved statements and the remaining parameter-level questions |
| [Experimental protocol](docs/experimental_protocol.md) | Exact model construction, parameters, controls, and known weaknesses |
| [Reproducible results](docs/reproducible_results.md) | Recorded outputs and validation commands |
| [Relation to existing work](docs/novelty_audit.md) | Scope comparison and conditions that would narrow the project |
| [API guide](docs/api.md) | Public functions and minimal examples |
| [Research program](docs/research_program.md) | Completed work and next tests |

The implementation lives in [`src/observer_math`](src/observer_math), the
experiments are in [`examples`](examples), and each mathematical invariant used
by the code has a corresponding test in [`tests`](tests).

## Reproduce the calculations

```bash
git clone https://github.com/MahsaKeikha/spatiotemporal-observer-math.git
cd spatiotemporal-observer-math
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,viz]"
python -m pytest
python -m ruff check .
python examples/baseline_experiment.py
python examples/worldtube_experiment.py
python examples/finite_sample_benchmark.py --trials 32 --jobs 6
```

The automated checks run on Python 3.10, 3.11, and 3.12.

## Interpretation boundary

The score is a tool for studying a sharply defined identification problem. A
high value does not establish consciousness, sentience, agency, intelligence,
or moral status. The current evidence consists of exact identities, unit tests,
and small synthetic examples. A preliminary finite-sample simulation and a
conservative analytical sampling bound are included; practically sharp bounds,
broader null families, external-method comparisons, and the quantum
construction remain open work.

## Primary reference

Max Tegmark, "Consciousness as a State of Matter," *Chaos, Solitons & Fractals*
76 (2015), 238-270. [arXiv:1401.1219](https://arxiv.org/abs/1401.1219),
[doi:10.1016/j.chaos.2015.03.014](https://doi.org/10.1016/j.chaos.2015.03.014).

## Status

This is an ongoing study, not a finished paper. Version 0.3 adds score-space
recovery theorems and finite-sample experiments to the exact Gaussian baseline.
The repository will change as counterexamples, comparisons, and stronger proofs
are added.
