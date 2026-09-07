# Reproducible results

This page records numerical outputs generated from committed code. It is an
experiment log, not evidence for phenomenal consciousness or a claim of a
complete observer theory.

## Experiment A: fixed modular structure

Command:

```bash
python examples/baseline_experiment.py
```

For two planted three-node modules, the two highest-ranked candidates are the
two planted modules. Both receive observer score `0.237050`.

In the correlated-but-dynamically-uncoupled control:

| Quantity | Value |
| --- | ---: |
| Static integration | 0.102050 bits/node |
| Directed integration | 0.000000 bits/node |
| Predictive persistence | 0.422500 |
| Observer score | 0.000000 |

The control demonstrates a narrow but important property: static correlation
alone does not create a positive score under the implemented directed criterion.

## Experiment B: changing-boundary world-tube

Command:

```bash
python examples/worldtube_experiment.py
```

The planted and recovered paths are identical:

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

| Quantity | Value |
| --- | ---: |
| Boundaries recovered | 5 / 5 |
| Winning action | 1.275235 |
| Runner-up action | 1.138004 |
| Exact action margin | 0.137231 |
| Certified uniform score radius | 0.011436 |

The radius means that if every local score and every raw transport score changes
by less than `0.011436` in absolute value, the inferred path is guaranteed not
to change under the assumptions of Proposition 4. This is a deterministic
score-space guarantee, not yet a sampling-error confidence interval.

## Regularization result

The generated phase diagram scans transport and material-continuity weights.
It exposes both the recovery region and a failure region where an excessive
preference for retaining the same physical members overwhelms the moving
organization.

![Regularization phase diagram](worldtube_phase_diagram.png)

## Reproduce validation

```bash
python -m pip install -e ".[dev,viz]"
python -m pytest
python -m ruff check .
python examples/baseline_experiment.py
python examples/worldtube_experiment.py
```

The automated suite currently contains 14 tests. Continuous integration runs
the tests and lint checks on Python 3.10, 3.11, and 3.12.

## Required next controls

- finite-sample covariance estimation with confidence intervals
- random, shuffled, and adversarial moving-boundary nulls
- recovery curves over signal-to-noise ratio and coupling separation
- comparisons with fixed-boundary and dynamic-community baselines
- replication on independently designed generative systems
