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

## Experimental contributions

Every experiment should record:

- the generative model and all parameters
- whether covariances are analytical or estimated
- random seeds when sampling is used
- how hyperparameters were selected
- the candidate family given to the optimizer
- success and failure cases
- the exact command that regenerates each figure or table

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

## Language and interpretation

Use *observer-like process* or *candidate boundary* for the implemented object.
Do not describe the score as a detector of consciousness. Keep established
results, definitions introduced in this repository, numerical findings, and
open conjectures visibly separate.

References should point to the primary paper or official publication page when
available.
