# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.47.1-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

**Mahsa Keikha, PhD**

> ## Can the boundary of a physical subsystem be discovered from its dynamics, even when that boundary moves through time?

Most analyses begin by deciding what the subsystem is and then studying how it behaves.

This project asks whether part of that order can be reversed.

Given measurements of a larger dynamical system, can the data themselves support one **moving subsystem boundary** more strongly than the alternatives?

That question leads to the central object of this research: a **spatiotemporal world-tube**, a sequence of candidate subsystem boundaries that can change from one time step to the next.

This is an operational mathematical framework for subsystem identification. It is inspired by Max Tegmark's observer-factorization question, but it does **not** claim that an inferred subsystem is consciousness or that the present mathematics solves the physical-to-experiential problem.

<p align="center">
  <a href="docs/visual_research_guide.md">
    <img src="docs/physics_pipeline.svg" alt="From measured physical dynamics to a moving subsystem world-tube" width="900">
  </a>
</p>

<p align="center"><em>From measured dynamics to a candidate moving boundary. Click the figure for the visual research guide.</em></p>

---

## The idea in one minute

Imagine observing a complex system whose meaningful organization does not stay attached to the same coordinates forever.

At one moment, a coherent subsystem may involve one set of measured variables. Later, the same organized process may be best represented by a different set. A static partition can miss that motion.

Instead of asking only:

> Which subset looks most interesting right now?

this framework asks:

> Which **path of subsets through time** is most strongly supported by the dynamics?

A candidate path has the form

```text
S0 -> S1 -> S2 -> ... -> ST-1
```

and is evaluated through four complementary questions:

| Dynamical property | Plain-language question |
| --- | --- |
| **Integration** | Do the parts of the candidate help predict one another? |
| **Insulation** | After the candidate's present state is known, how much extra prediction comes from its measured exterior? |
| **Persistence** | Does its internal organization remain predictively coherent through time? |
| **Transport** | Can that organization continue even when its measured membership changes? |

The result is not a label attached independently at every time point. It is a **globally optimized trajectory through candidate-subsystem space**.

[Read the mathematical construction ->](docs/research_overview.md)

---

## Why this is interesting

A physical boundary and an observational coordinate boundary need not be the same thing.

A pattern can persist while matter moves. A functional organization can migrate across sensors or coordinates. A subsystem that is obvious at one instant may be ambiguous when examined over a full trajectory. And two apparently different boundaries may even be observationally indistinguishable.

That creates three scientific problems that have to be separated:

1. **Definition:** what should count as dynamical integration, insulation, persistence, and transport?
2. **Recovery:** when does one moving path actually outrank its competitors?
3. **Certification:** when is the evidence strong enough to distinguish a real recovery result from finite-sample noise, temporal dependence, nuisance structure, or model misspecification?

The repository develops these layers separately so that an attractive numerical result is never mistaken for a theorem, and a theorem under a declared model is never mistaken for universal physical truth.

---

## A first visual example

<p align="center">
  <a href="docs/reproducible_results.md">
    <img src="docs/worldtube_baseline.png" alt="Controlled moving-boundary recovery example" width="820">
  </a>
</p>

In the controlled planted example, the target boundary moves through the coordinate system:

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

The framework scores competing candidate paths and asks whether the planted world-tube can be recovered as a **global path**, not merely as a sequence of unrelated local choices.

This is only the beginning of the research program. Later results ask when such recovery is identifiable, how it behaves under perturbation, how finite data alter the conclusion, how temporal dependence should be calibrated in physical time, and how covariance uncertainty propagates back to the final path decision.

[Explore all 33 scientific figures ->](docs/visual_research_guide.md)

---

## What the research has established

The current record contains **58 proposition-level results, 45 reproducible experiments, 33 scientific result figures, and 223 claim-level tests**.

Rather than putting all of that material on this page, the main results are organized below by the question they answer.

| Research question | What the current framework provides | Go deeper |
| --- | --- | --- |
| Can a moving boundary be defined operationally? | A world-tube objective built from integration, insulation, persistence, transport, and continuity | [Research overview](docs/research_overview.md) |
| Can the best finite path be found exactly? | Dynamic-programming recovery for the declared finite candidate family, including the strongest competitor and recovery margin | [Proof record](docs/proofs_and_conjectures.md) |
| Can different boundaries be observationally indistinguishable? | Explicit identifiability and observational-equivalence analysis | [Research index](docs/research_index.md) |
| Can finite data support the same conclusion? | Covariance perturbation and finite-sample certification under stated assumptions | [Assumption ledger](docs/assumption_ledger.md) |
| Can temporal dependence be expressed in physical time? | Relaxation-time calibration on regular and irregular measurement schedules | [Physics guide](docs/physics_guide.md) |
| Can temporal dependence be removed before covariance inference? | Exact and robust innovation-whitening results under the declared Gaussian temporal model | [P56-P57 records](docs/research_index.md) |
| Can covariance uncertainty be propagated back to the final moving-boundary decision? | A deterministic covariance-to-world-tube bridge, together with an explicit current bottleneck | [Proposition 58](docs/proposition_58_observer_bridge.md) |

---

## The current frontier

The most important current result is not a dramatic claim of completion. It is a precise diagnosis of what still prevents the full observer-scale certificate from closing.

The physical-time and innovation-whitening sequence can move a controlled scalar covariance problem into a well-behaved perturbative regime. But when the analysis returns to the full moving-boundary problem, the simultaneous observer blocks are higher-dimensional and numerous. Under the present generic matrix bound, the controlled benchmark remains outside the required relative-perturbation regime.

That negative result matters because it identifies **where the mathematics must improve next**: factor-specific covariance blocks, safe candidate screening, heterogeneous local uncertainty, and more direct concentration of score or path margins.

[Read the current frontier in Proposition 58 ->](docs/proposition_58_observer_bridge.md)

---

## Choose how deep you want to go

You do not need to read 58 propositions to understand the idea.

| If you want to... | Start here |
| --- | --- |
| **Understand the whole project without equations** | [Visual Research Guide](docs/visual_research_guide.md) |
| **Read the scientific story from beginning to frontier** | [Research Overview](docs/research_overview.md) |
| **Understand the physical model, units, and measurement meaning** | [Physics Guide](docs/physics_guide.md) |
| **See how every research layer connects** | [Deep Dive Map](docs/deep_dive.md) |
| **Audit every proposition and experiment** | [Research Index](docs/research_index.md) |
| **Inspect assumptions, limitations, and failure conditions** | [Assumption Ledger](docs/assumption_ledger.md) |
| **Trace equations to mathematics and literature** | [Physics + Mathematics + Citation Map](docs/physics_mathematics_citation_map.md) |
| **Browse every result figure** | [Visual Research Guide](docs/visual_research_guide.md) |
| **Reproduce the computational record** | [Reproducible Results](docs/reproducible_results.md) |
| **Inspect the software API** | [API Documentation](docs/api.md) |
| **See the literature and conceptual lineage** | [Bibliography and Citation Map](docs/bibliography.md) |

---

## Where the idea came from

A conceptual starting point is Max Tegmark's question of why an observer should correspond to one factorization of a larger physical system rather than another in ["Consciousness as a State of Matter"](https://doi.org/10.1016/j.chaos.2015.03.014).

This repository takes a specific mathematical step beyond a static factorization question: the candidate subsystem is allowed to **move through time**.

The project then asks what would be required to recover that moving structure from data without quietly assuming the answer: identifiability, global path optimization, perturbation stability, finite-sample uncertainty, temporal calibration, nuisance handling, and reproducible measurement certification.

For the exact relationship to prior literature and for equation-level provenance, see the [Bibliography](docs/bibliography.md) and [Physics + Mathematics + Citation Map](docs/physics_mathematics_citation_map.md).

---

## What this project does not claim

The word **observer** is used here in an operational mathematical sense for a candidate subsystem selected by declared dynamical criteria.

The present results do **not** establish that:

- every physical system contains a uniquely recoverable observer;
- an inferred world-tube is conscious;
- the Gaussian observation model is universally valid;
- a successful synthetic recovery automatically transfers to a new experimental system;
- information-theoretic organization alone solves the consciousness problem.

Those distinctions are deliberate. The framework is designed to make its assumptions, failure modes, and unresolved steps visible rather than hiding them behind a single score.

[Read the interpretation protocol ->](docs/interpretation_protocol.md)

---

## Reproduce the research

The repository is tested on Python 3.10, 3.11, and 3.12.

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

The experiment scripts, numerical records, figures, and theorem-specific tests are linked through the [Research Index](docs/research_index.md) and [Reproducible Results](docs/reproducible_results.md).

---

## Research record

| | Current record |
| --- | ---: |
| Proposition-level results | **58** |
| Reproducible experiments | **45** |
| Scientific result figures | **33** |
| Claim-level tests | **223** |
| Research-software version | **0.47.1** |
| CI | **Python 3.10 / 3.11 / 3.12** |

---

## The shortest path through the repository

If you only open three pages, use these:

**1. [Visual Research Guide](docs/visual_research_guide.md)** - understand the idea and the evidence visually.  
**2. [Research Overview](docs/research_overview.md)** - follow the mathematics from the moving boundary to the current frontier.  
**3. [Deep Dive Map](docs/deep_dive.md)** - choose the exact proof, experiment, assumption, code, or citation layer you want next.

The central question remains simple even when the mathematics becomes technical:

> **When does the dynamics itself justify a moving subsystem boundary, and when is the evidence insufficient to identify one?**

---

## Citation and license

Repository citation metadata: [`CITATION.cff`](CITATION.cff)  
Machine-readable references: [`references.bib`](references.bib)  
License: [MIT](LICENSE)
