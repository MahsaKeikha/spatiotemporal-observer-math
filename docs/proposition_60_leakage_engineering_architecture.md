# Proposition 60: engineering architecture of the leakage bottleneck

## Engineering objective

Proposition 59 showed that integration and persistence can be evaluated on smaller covariance blocks, but environmental leakage retains the full \(n+s\) block. Proposition 60 converts that observation into an explicit measurement-design constraint.

The quantity used by the current local observer score is

\[
L_S = I(X_{t+1}^{S};X_t^{\bar S}\mid X_t^S).
\]

For transport from \(U\) to \(S\), the corresponding leakage is

\[
L_{U\to S}=I(X_{t+1}^{S};X_t^{\bar U}\mid X_t^U).
\]

These are conditional-information quantities. Reducing the covariance dimension by simply dropping environmental channels changes the estimand unless the omitted channels are conditionally irrelevant under an independently justified structural assumption or certificate.

## Proposition

For a candidate of size \(s\) in an \(n\)-coordinate state, exact evaluation of the present leakage definition is supported by the covariance block

\[
(X_t^S,X_t^{\bar S},X_{t+1}^S)=(X_t,X_{t+1}^S),
\]

which has dimension

\[
\boxed{d_E=n+s.}
\]

Suppose the environment is partitioned into retained coordinates \(R\) and omitted coordinates \(O\). The reduced calculation

\[
I(X_{t+1}^S;X_t^R\mid X_t^S)
\]

equals the original leakage only if the omitted contribution vanishes:

\[
\boxed{I(X_{t+1}^S;X_t^O\mid X_t^S,X_t^R)=0.}
\]

This follows immediately from the conditional mutual-information chain rule,

\[
I(Y;R,O\mid S)=I(Y;R\mid S)+I(Y;O\mid S,R).
\]

Therefore environmental screening is scientifically admissible as an exact dimensional reduction only when the second term is zero by declared model structure or by a separate valid certificate. A data-dependent screen cannot be silently treated as exact using the same data and probability budget.

## Engineering interpretation

This proposition changes the next research step from a generic search for tighter concentration to a system-identification problem:

1. define the measured environment and sensor channels;
2. identify a physically justified conditional dependency graph or predeclared screening rule;
3. certify omitted channels against a separate statistical budget or independent pilot record;
4. compute leakage on the retained block;
5. propagate both screening uncertainty and covariance uncertainty into the world-tube action margin.

The architecture is therefore

\[
\text{sensor state}
\to
\text{structural/pilot screen}
\to
\text{certified retained environment}
\to
\text{conditional-information estimator}
\to
\text{factor interval}
\to
\text{path certificate}.
\]

## Experiment AU

Experiment AU performs a design sweep for the existing seven-coordinate benchmark with \(s=3\), 175 simultaneous time-candidate blocks, and 118 residual innovation degrees. The exact model has four environmental coordinates and dimension ten. Hypothetical retained-environment sizes from zero through four are evaluated only as engineering design points.

The sweep deliberately marks every reduced row as **not exact without additional structure**. This prevents a smaller numerical radius from being mistaken for a theorem about the original score.

The experiment reports, for each retained-environment size:

- covariance dimension \(2s+|R|\);
- exact-\(\tau\) matrix radius at 118 residual innovation degrees;
- first residual innovation count at which that dimension enters the relative perturbation regime;
- whether the row is exact under the original leakage definition without an additional assumption.

## Scientific boundary

Proposition 60 does not claim that environmental coordinates are sparse in the benchmark or in a physical system. It proves the condition under which a future sparsity or screening result would preserve the existing leakage estimand.

This distinction is important for engineering validity: dimensional reduction is not free. It requires a physical or statistical justification that can itself be audited.

## Next theorem

The next useful result is a **sample-split conditional screening theorem**. A pilot record should select a retained environmental set, and an independent certification record should evaluate the selected leakage block and world-tube margin. That construction can reduce simultaneous dimension without reusing the same noise realization for selection and certification.

## Reproducibility

Implementation: `src/observer_math/leakage_geometry.py`

Claim-level tests: `tests/test_leakage_geometry.py`

Experiment: `examples/leakage_engineering_audit.py`

Machine-readable record: `docs/leakage_engineering_audit.json`
