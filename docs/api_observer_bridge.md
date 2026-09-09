# Observer bridge API

This page documents the public module interface for **Proposition 58**, relative covariance uncertainty propagated to observer world-tube recovery.

The implementation lives in

```text
src/observer_math/observer_bridge.py
```

The complete theorem and derivation are in [Proposition 58](proposition_58_observer_bridge.md). The controlled numerical audit is [Experiment AS](observer_bridge_dimension_audit.json), with the visible result figure below.

[![Experiment AS observer-scale audit](observer_bridge_dimension_audit.svg)](proposition_58_observer_bridge.md)

---

# 1. Main result type

```python
from observer_math.observer_bridge import RelativeCovarianceWorldTubeRecoveryBound
```

`RelativeCovarianceWorldTubeRecoveryBound` records the complete deterministic covariance-to-path certificate.

| Field | Meaning |
| --- | --- |
| `covariance_relative_errors` | Candidate-local relative covariance radii \(\delta_{t,S}\) |
| `local_factor_errors` | Propagated integration, independence, and persistence factor radii |
| `transport_factor_errors` | Propagated independence and persistence radii for transport edges |
| `local_score_errors` | Candidate-local observer-score error radii |
| `transport_score_errors` | Candidate-edge transport-score error radii |
| `structural_integration_null_mask` | Declared exact integration-null states using the sharper null-specific refinement |
| `population_path` | Population-optimal world-tube path under the supplied factor arrays |
| `adversarial_competitor` | Competitor maximizing the error-inflated action, when present |
| `population_action_margin` | Exact population objective difference between best and runner-up paths |
| `planted_lower_action` | Lower action bound for the population-optimal path |
| `competitor_upper_action` | Maximum upper action bound among competitors |
| `recovery_slack` | `planted_lower_action - competitor_upper_action` |
| `near_competitor_screen` | Near-competitor graph implied by the supplied score radii |
| `all_blocks_valid` | Whether all supplied relative covariance radii lie in the theorem's admissible regime |
| `guarantees_population_path` | `True` exactly when the deterministic recovery certificate succeeds |

A positive `recovery_slack` is the key end-to-end quantity.

---

# 2. Main function

```python
from observer_math.observer_bridge import relative_covariance_worldtube_recovery_bound
```

Signature conceptually:

```python
relative_covariance_worldtube_recovery_bound(
    local_factors,
    transport_factors,
    candidates,
    node_count,
    subset_size,
    *,
    covariance_relative_errors,
    structural_integration_null_mask=None,
    transport_weight=0.35,
    continuity_weight=0.15,
)
```

## Required arrays

### `local_factors`

Shape:

```text
(time_count, candidate_count, 3)
```

The last axis is ordered as

```text
(integration, independence, persistence)
```

and every factor must lie in `[0, 1]`.

### `transport_factors`

Shape:

```text
(time_count - 1, candidate_count, candidate_count, 2)
```

The last axis is ordered as

```text
(independence, persistence)
```

for each candidate-to-candidate transport edge.

### `candidates`

A sequence of fixed-size candidate coordinate sets. Every candidate must contain `subset_size` distinct indices in

```text
0, ..., node_count - 1
```

### `covariance_relative_errors`

Shape:

```text
(time_count, candidate_count)
```

For candidate \(S\) at time \(t\), the entry \(\delta_{t,S}\) must certify the complete observer covariance block

\[
B_{t,S}=(X_t,X_{t+1}^{S}).
\]

For the generic relative-covariance perturbation theorem, every radius used in the certificate must satisfy

\[
\delta_{t,S}<1.
\]

---

# 3. Observer-block geometry

If the measured physical state has \(n\) coordinates and every candidate contains \(s\) coordinates, each observer covariance block has dimension

\[
\boxed{d_{\mathrm{obs}}=n+s.}
\]

With \(T\) times and \(C\) candidates, the simultaneous block count is

\[
\boxed{B_{\mathrm{obs}}=TC.}
\]

A key Proposition 58 observation is that all incoming transport edges to a future candidate reuse the same target-indexed observer block. The simultaneous covariance count therefore does not grow as the raw edge count.

For Experiment AS,

\[
n=7,
\quad
s=3,
\quad
T=5,
\quad
C=35,
\]

so

\[
\boxed{d_{\mathrm{obs}}=10,\qquad B_{\mathrm{obs}}=175.}
\]

---

# 4. Probability accounting

This function is deterministic.

It does **not** estimate covariance and it does **not** create a new stochastic event.

If a previous theorem supplies the complete simultaneous observer-block covariance event with probability at least

\[
1-\alpha,
\]

then a positive Proposition 58 recovery slack certifies the population path with at least the same probability

\[
1-\alpha.
\]

If the covariance theorem itself was obtained by composing independent calibration and target events, the already established combined confidence is inherited unchanged.

Do not add another arbitrary union bound over world-tube paths. The path comparison is deterministic conditional on the simultaneous covariance event.

---

# 5. Structural integration nulls

`structural_integration_null_mask` is optional.

When it is supplied, entries marked `True` assert an **exact population integration null** that was declared independently of the covariance noise.

At those states, Proposition 58 uses the repository's sharper relative structural-null integration bound and then propagates it through the cube-root local score.

Do not use this option for nulls selected after inspecting the same noisy covariance estimates. Data-selected structural nulls require separate statistical protection.

---

# 6. Output interpretation

A typical successful certificate has

```text
all_blocks_valid = True
guarantees_population_path = True
recovery_slack > 0
```

A failed certificate is not proof that the population path is unrecoverable.

For example, Experiment AS deliberately records that the current observer-scale exact-tau covariance radius is

\[
1.8573569119>1
\]

at 118 residual innovation degrees. That places the current relative perturbation theorem outside its admissible regime. It does not prove that the planted moving module cannot be recovered from 118 observations by another estimator, theorem, or structural argument.

Likewise, the very large residual-degree diagnostic reported by Experiment AS is a measure of conservatism in the current theorem composition, not a physical sample requirement.

---

# 7. Reproducible reference implementation

Experiment:

```text
examples/observer_bridge_dimension_audit.py
```

Renderer:

```text
examples/render_observer_bridge_dimension_audit.py
```

Tests:

```text
tests/test_observer_bridge.py
```

Machine-readable result:

```text
docs/observer_bridge_dimension_audit.json
```

Visible figure:

```text
docs/observer_bridge_dimension_audit.svg
```

Direct links:

[Proof](proposition_58_observer_bridge.md) | [JSON](observer_bridge_dimension_audit.json) | [Experiment](../examples/observer_bridge_dimension_audit.py) | [Renderer](../examples/render_observer_bridge_dimension_audit.py) | [Tests](../tests/test_observer_bridge.py) | [Figure](observer_bridge_dimension_audit.svg)

---

# 8. Physical interpretation boundary

The API certifies a path in a declared stochastic-dynamical observer model. It does not establish that the model applies to a real physical system without validation, and it does not establish consciousness.

Before applying it to measured data, use the [Assumption Ledger](assumption_ledger.md), [Physics Guide](physics_guide.md), and [Interpretation Protocol](interpretation_protocol.md).
