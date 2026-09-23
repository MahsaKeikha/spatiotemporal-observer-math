# Proposition 61: Sample-Split Boundary Freeze for Downstream Sufficiency Tests

## Engineering question

Research I estimates a moving subsystem boundary from stochastic dynamics. Research II tests a declared physical descriptor against an independently specified target. If the same downstream outcomes are allowed to influence boundary selection and then certify the selected descriptor, the two stages are no longer cleanly separated.

P61 gives the first exact handoff rule.

## Setup

Let the available observations be divided into a pilot block \(D_B\) for boundary identification and a certification block \(D_C\) for the downstream test. Let

\[
\widehat{\mathcal W}=A(D_B)
\]

be any measurable Research I boundary-selection algorithm, including the world-tube dynamic program and its declared engineering screens.

The selected world-tube induces a physical descriptor

\[
Z^{\widehat{\mathcal W}}=F(X,\widehat{\mathcal W}).
\]

Let \(T(D_C;\widehat{\mathcal W})\) be a downstream level-\(\alpha\) test with the conditional validity property

\[
\Pr_{H_0(\widehat{\mathcal W})}
\left(
T(D_C;\widehat{\mathcal W})=1
\mid D_B
\right)
\le \alpha
\]

almost surely.

## Result

If the certification block has its declared null law conditionally on the pilot information, then selecting the world-tube from \(D_B\) does not inflate the downstream type-I error:

\[
\boxed{
\Pr_{H_0(\widehat{\mathcal W})}
\left(
T(D_C;\widehat{\mathcal W})=1
\right)
\le \alpha.
}
\]

### Proof

By the tower property,

\[
\begin{aligned}
\Pr(T=1)
&=\mathbb E\left[\Pr(T=1\mid D_B)\right]\\
&\le \mathbb E[\alpha]\\
&=\alpha.
\end{aligned}
\]

The theorem does not require the boundary estimator \(A\) to be unbiased or correct. It requires the downstream test to be conditionally valid for the descriptor selected from pilot information.

## What the theorem protects

P61 protects downstream calibration from *selection of the physical boundary* when that selection is frozen before the certification outcomes are inspected.

It permits the pilot stage to choose:

- the world-tube;
- retained environmental channels under separately justified screening;
- descriptor dimension;
- model hyperparameters that are explicitly designated as pilot-stage choices.

## What it does not protect

P61 does not justify:

- using certification outcomes to revise the boundary and then testing that revised boundary on the same outcomes;
- claiming the selected world-tube is the true physical boundary;
- ignoring dependence between pilot and certification blocks when conditional validity fails;
- identifying the downstream target with consciousness;
- treating non-rejection as validation of the descriptor.

## Engineering protocol

1. Freeze the data split before target-aware certification.
2. Run Research I only on the pilot boundary block.
3. Store the selected world-tube and all pilot-selected engineering choices.
4. Construct the downstream descriptor from the frozen path.
5. Run the declared Research II test on certification data.
6. Record whether the conditional-validity assumptions are satisfied.
7. If the boundary is not sufficiently stable, pass an uncertainty set rather than one path to P62.

## Scientific role

P61 is intentionally modest. It does not solve boundary uncertainty. It establishes a clean interface on which stronger boundary-robust results can be built.
