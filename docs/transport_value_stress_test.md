# Transport-value stress test

This experiment is designed to answer a specific scientific question raised by the existing finite-sample benchmark:

> **When does cross-time transport provide information that local candidate scores plus a continuity penalty do not already provide?**

The current benchmark is deliberately retained as a negative result: at intermediate sample sizes, independent local choices and local score plus continuity outperform the full transport objective. That result is informative because it prevents the transport term from being presented as automatically beneficial.

## Hypothesis under test

A transport term should help only when two conditions coexist:

1. local evidence is sufficiently ambiguous that several candidates have similar local scores; and
2. the correct successor retains a distinctive cross-time predictive relationship that is not reducible to set overlap alone.

If either condition is absent, transport can add estimation variance without adding useful discrimination.

## Required benchmark families

### Family A: local-evidence-dominant control

Use the existing moving-module benchmark without redesign. It is the control case in which local evidence is already strong.

Required comparison:

- independent local;
- local + continuity;
- full distributional transport;
- coefficient-based transport;
- best fixed boundary.

Expected interpretation is empirical, not predetermined: the committed result already shows that full transport is not best at intermediate sample sizes.

### Family B: transport-informative ambiguity

Construct a model in which two or more candidate successors have deliberately matched or near-matched one-step local observer scores, while only the planted successor preserves the declared cross-time transport relationship.

The construction is acceptable only if the ambiguity is verified numerically at population level before finite-sample trials. Report the gap between the best and second-best local scores and the corresponding transport gaps.

### Family C: continuity-confounded motion

Construct a case in which a high-overlap successor is not the dynamically correct successor. This tests whether the transport functional can distinguish predictive organizational transfer from mere material overlap.

The planted path must be declared before simulation and the continuity-only baseline must use the same continuity weight as the full method.

### Family D: transport-null control

Construct a case in which transport scores carry no discriminative information after conditioning on local evidence. A robust method should not gain a fictitious advantage from transport in this control.

## Primary outcomes

For every family and sample size, report:

- mean boundary accuracy;
- exact path recovery;
- Jaccard overlap with the planted boundary;
- winning-minus-runner-up action margin;
- local-score top-two gap;
- planted-edge transport rank;
- runtime.

Use Wilson intervals for exact-recovery probabilities and standard errors (or bootstrap intervals, declared in advance) for continuous summaries.

## Weight-sensitivity protocol

Do not select transport or continuity weights using the same Monte Carlo trials used for the final comparison.

Use one of these designs:

- fixed weights inherited from the population construction and never tuned on finite-sample outcomes; or
- a training/validation/test split in seed space, with the final test seeds frozen before comparison.

Report a two-dimensional sensitivity surface over transport weight \(\chi\) and continuity weight \(\lambda\). The purpose is to identify robustness regions, not to display only the best point.

## Mechanistic ablation

The full objective should be decomposed into:

\[
\text{local only},
\qquad
\text{local + continuity},
\qquad
\text{local + transport},
\qquad
\text{local + transport + continuity}.
\]

This 2x2 ablation is necessary to attribute any gain specifically to transport rather than to regularization.

A second ablation should replace the information-geometric transport score with the existing coefficient-based structural transport baseline. If both behave identically, the stronger interpretation of the information-geometric transport term is not supported by that experiment.

## Falsification criteria

The experiment is valuable even if it weakens the proposed method.

Transport is **not supported as adding practical information** on a benchmark if, across frozen test seeds:

- local + continuity matches or exceeds full transport within uncertainty;
- the planted edge is not systematically ranked above competing edges;
- gains appear only at a narrowly tuned weight;
- or the coefficient-based baseline produces indistinguishable performance.

Those outcomes should be reported rather than optimized away.

## Reproducibility contract

The final implementation must commit:

1. model-construction code for all four families;
2. a frozen root seed and deterministic seed-generation rule;
3. machine-readable population diagnostics;
4. machine-readable trial-level results, not only aggregates;
5. an aggregation script;
6. figure-generation code;
7. tests that verify planted paths, dimensions, score identities, and deterministic regeneration.

## Promotion rule

No statement that transport improves recovery should enter the established contribution record until Family B or C demonstrates the effect on frozen test seeds with uncertainty reporting and the mechanistic ablation attributes the improvement to transport.

Conversely, the existing negative result remains part of the record. A method that exposes where its own component is unnecessary is scientifically stronger than one that reports only favorable regimes.
