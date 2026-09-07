# Experimental protocol

This document describes the two committed experiments closely enough to rebuild
them without guessing from the figures.

## 1. Deterministic computation

The current experiments use analytical covariances. They do not draw finite
samples. Consequently, repeated runs on the same NumPy and SciPy numerical
stack should agree up to floating-point roundoff. There is no fitted model and
no random seed in either reported calculation.

## 2. Fixed modular system

The first system has six variables split into blocks \((0,1,2)\) and
\((3,4,5)\). Before spectral scaling, the transition matrix has

- diagonal entries `0.42`
- off-diagonal entries `0.25` within a block
- off-diagonal entries `0.005` between blocks

The full matrix is rescaled to spectral radius `0.86`. Process noise is
\(Q=0.16I\). The code solves the discrete Lyapunov equation for the stationary
covariance and ranks all \(\binom{6}{3}=20\) three-variable candidates.

The expected result is not assumed by the optimizer. It is known from the way
the matrix was constructed: the two planted blocks should rank ahead of mixed
three-variable subsets.

### Correlation-only control

The control has four variables with transition matrix \(A=0.65I\). Its process
noise has diagonal entries `0.2` and pairwise correlation `0.55`. This creates
instantaneous correlation without cross-variable dynamics. The directed
integration should therefore vanish even though static mutual information does
not.

## 3. Moving-boundary system

The second system has seven variables and five candidate times. The planted
boundary is

\[
(0,1,2),\ (1,2,3),\ (2,3,4),\ (3,4,5),\ (4,5,6).
\]

At time \(t\), the unscaled transition matrix begins with diagonal `0.32` for
all variables. Each variable in the active boundary receives diagonal `0.46`
and directed coefficient `0.18` from each of the other two active variables.
The matrix is then rescaled to spectral radius `0.84`. Process noise is
\(Q_t=0.18I\).

The initial covariance is the stationary covariance associated with the first
transition matrix. Subsequent covariances follow the actual chronological
recursion

\[
\Sigma_{t+1}=A_t\Sigma_tA_t^\mathsf T+Q_t.
\]

For each time, all \(\binom{7}{3}=35\) three-variable boundaries are scored.
For each adjacent pair of times, all \(35^2=1225\) source-target transitions are
scored from the same \((\Sigma_t,A_t,Q_t)\) edge used by covariance propagation.
This shared indexing matters: local dynamics, transport, and covariance must
describe one generative timeline.

The world-tube search uses:

| Parameter | Value |
| --- | ---: |
| Local-score weight | 1.00 |
| Transport weight \(\chi\) | 0.25 |
| Jaccard continuity weight \(\lambda\) | 0.08 |
| Candidate size | 3 |
| Number of candidates per time | 35 |
| Number of candidate times | 5 |

These weights were chosen for the initial construction and must not be treated
as universal constants. The phase diagram scans \(\chi\in[0,0.6]\) and
\(\lambda\in[0,0.8]\) on a 25 by 25 grid.

## 4. What the figures show

`worldtube_baseline.png` displays local fixed-boundary scores for the twelve
candidates with the largest maximum score across time. Cyan outlines mark the
candidate selected by the full path objective. Because the heat map shows local
scores while the outline comes from the full action, it should not be read as a
plot of the action itself.

`worldtube_phase_diagram.png` records the fraction of the five planted
boundaries recovered at each pair of regularization weights. The abrupt loss of
recovery at large continuity weight is expected: sufficiently strong Jaccard
penalization favors retaining physical members even when the active module has
moved.

## 5. Tests tied to scientific claims

| Test | Property checked |
| --- | --- |
| `test_covariance_propagation_matches_recursion` | The implemented nonstationary covariance follows the analytical recursion |
| `test_canonical_correlations_are_block_coordinate_invariant` | Transport persistence survives invertible basis changes within source and target |
| `test_environmental_drive_reduces_transport_independence` | Added external drive increases leakage and lowers insulation |
| `test_static_correlation_is_not_mistaken_for_directed_integration` | Common correlated noise does not create directed integration |
| `test_certificate_finds_exact_runner_up_and_positive_radius` | The two-best dynamic program agrees with hand-enumerated path scores |
| `test_perturbation_below_certificate_radius_preserves_path` | A bounded perturbation inside the certificate leaves the optimum unchanged |

## 6. Known weaknesses of the current experiment

The moving example is a proof of implementation, not a demanding benchmark.
Its limitations are concrete:

1. Ground truth is encoded directly in the transition matrices.
2. Covariances are known exactly rather than estimated from data.
3. Candidate size is fixed and supplied in advance.
4. The active module moves smoothly with two of three members retained.
5. There are no latent confounders, missing observations, or nonlinearities.
6. Hyperparameters are scanned against the same construction used for display.
7. No competing method is evaluated in the current script.

A stronger benchmark should vary coupling, noise, overlap, speed, candidate
size, observation length, latent drive, and model misspecification. It should
choose weights on separate training systems and evaluate them on held-out
generative families.

## 7. Reproduction commands

From the repository root:

```bash
python -m pip install -e ".[dev,viz]"
python examples/baseline_experiment.py
python examples/worldtube_experiment.py
python -m pytest
python -m ruff check .
```

Both figures are overwritten by the world-tube experiment so that committed
images can always be traced back to the current script.
