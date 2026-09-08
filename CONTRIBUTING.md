# Contributing

The useful contributions to this project are the ones that make a claim harder
to fool.

## Before changing a measure

Open an issue or explain in the pull request:

1. Which failure in the current definition does the change address?
2. Which property should remain invariant?
3. What null or counterexample could make the proposed change fail?
4. Is the change a new definition, a theorem, or an empirical estimator?

A new scalar score without those answers is difficult to interpret, even when
it performs well on the planted example.

## Physical accountability

Every major theorem or experiment should state what its mathematical objects
mean physically before presenting the result as part of the observer program.
A reader should be able to answer the following without reverse-engineering the
code:

1. What physical degrees of freedom does `X_t` represent?
2. What mechanism or effective coupling does `A_t` represent?
3. What unresolved process or fluctuation is represented by `Q_t`?
4. What physically defines the candidate boundary `S_t`?
5. What observable experiment, residual diagnostic, intervention, or model
   comparison could make the physical interpretation fail?

When relevant, also state:

- observable units;
- sampling interval and sensor bandwidth;
- coordinate scaling and preprocessing;
- physical geometry of the candidate family;
- temporal relaxation interpretation;
- nuisance modes removed from the record;
- conservation laws or symmetries expected of the application;
- whether covariance eigenmodes are merely statistical fluctuation modes or
  have an independently justified energetic interpretation.

Do not call an optimization objective physical action unless a derivation gives
it the meaning and units of a physical action functional. Do not call mutual
information thermodynamic entropy, causal influence, semantic information, or
subjective information without an explicit bridge.

For the canonical terminology and physical mapping, see
[`docs/physics_guide.md`](docs/physics_guide.md).

## Citation accountability

Every new proposition, method, or physical model must identify the external
literature it materially uses. Attribution is part of the scientific audit
trail, not a cosmetic step at release time.

Before merging a result, check whether it uses any of the following:

- an external theorem or inequality;
- a named probability distribution or concentration result;
- a statistical testing or confidence-set construction;
- an optimization or multivariate-statistics method;
- a physical stochastic-process model;
- a conceptual framework that motivates the scientific question.

If so, cite the primary source or a standard authoritative source close to the
claim when practical, and update both:

- [`docs/bibliography.md`](docs/bibliography.md), which explains why the source
  matters to the project;
- [`references.bib`](references.bib), which stores the machine-readable
  citation.

Use one of three roles in the bibliography:

1. **Primary conceptual source** for work that directly launched the research
   question. Max Tegmark's 2015 paper *Consciousness as a State of Matter* has
   this role for the present project.
2. **Direct mathematical or statistical source** for a theorem, inequality,
   distributional fact, or method materially used in a proof or algorithm.
3. **Background lineage** for scientifically important context that is not
   being claimed as the source of a repository proposition.

Do not add references merely because they are famous or adjacent to the topic.
Do not imply endorsement by a cited author. When a repository result is a new
derivation built using an established method, state both facts clearly.

## Mathematical contributions

A mathematical result should state its domain and assumptions before the claim.
Proofs involving singular covariances must specify whether pseudoinverses,
regularization, or a limiting argument is used. Claims of invariance should name
the transformation group exactly. When a proof is incomplete, label it as a
conjecture or proof sketch and identify the missing step.

Please include at least one of the following:

- a proof checked against a numerical example
- a counterexample to a current conjecture
- a bound with a test of its tightness
- an equivalence or non-equivalence result relative to an existing method

For new proposition pages, prefer the following order when it is applicable:

1. physical problem;
2. declared measurement model;
3. mathematical statement;
4. proof;
5. physical interpretation of the bound;
6. reproducible experiment;
7. failure conditions and what remains open;
8. literature context for any external method or model materially used.

## Experimental contributions

Every experiment should record:

- the generative model and all parameters
- whether covariances are analytical or estimated
- random seeds when sampling is used
- how hyperparameters were selected
- the candidate family given to the optimizer
- success and failure cases
- the exact command that regenerates each figure or table
- which quantities are dimensionless and which retain physical units
- whether the displayed example is a physical model, a statistical benchmark,
  or an abstract mathematical stress test

Do not tune on a displayed test instance without saying so. Comparisons should
give competing methods the same data and a comparable tuning budget.

## Code contributions

Install the development dependencies and run:

```bash
python -m pip install -e ".[dev,viz]"
python -m pytest
python -m ruff check .
```

New behavior needs a test. Numerical tests should use tolerances justified by
the conditioning of the matrices rather than broad tolerances chosen only to
make a test pass. Keep example outputs deterministic whenever possible.

## Documentation style

Write for a reader who was not present while the result was developed. State
what problem a proposition solves, what assumptions it needs, what is proved,
and what a numerical experiment only illustrates. Keep physical interpretation,
proof, implementation, empirical evidence, and literature attribution visibly
distinct.

Do not use Unicode en dash or em dash characters in Markdown documentation.
Use ordinary hyphens, commas, colons, semicolons, or parentheses instead. CI
enforces this rule across the repository documentation.

Prefer natural technical prose over repetitive templates. A figure or table
should have a clear scientific purpose, a reproducible source, and enough
context to be understood without reconstructing the development history.

## Language and interpretation

Use *observer-like process* or *candidate boundary* for the implemented object.
Do not describe the score as a detector of consciousness. Keep established
results, physical interpretation, definitions introduced in this repository,
numerical findings, and open conjectures visibly separate.

References should point to the primary paper or official publication page when
available.
