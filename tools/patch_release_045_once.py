from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    if text.count(old) != 1:
        raise RuntimeError(f"{path}: expected exactly one occurrence of {old!r}, found {text.count(old)}")
    write(path, text.replace(old, new, 1))


def append_once(path: str, marker: str, section: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + section.strip() + "\n")


replace_once("pyproject.toml", 'version = "0.44.0"', 'version = "0.45.0"')
replace_once("CITATION.cff", "version: 0.44.0", "version: 0.45.0")
replace_once("references.bib", "  version = {0.41.1},", "  version = {0.45.0},")

references = read("references.bib")
if "@article{Aitken1936LeastSquares" not in references:
    anchor = "@software{Keikha2026SpatiotemporalObserver,"
    if references.count(anchor) != 1:
        raise RuntimeError("references.bib: software anchor not unique")
    aitken = '''@article{Aitken1936LeastSquares,
  author = {A. C. Aitken},
  title = {On Least Squares and Linear Combination of Observations},
  journal = {Proceedings of the Royal Society of Edinburgh},
  volume = {55},
  pages = {42--48},
  year = {1936},
  doi = {10.1017/S0370164600014346}
}

'''
    write("references.bib", references.replace(anchor, aitken + anchor, 1))

bibliography = read("docs/bibliography.md")
if "## Aitken 1936" not in bibliography:
    anchor = "## Lancaster 1965\n"
    if bibliography.count(anchor) != 1:
        raise RuntimeError("bibliography Aitken insertion anchor not unique")
    section = '''## Aitken 1936

**A. C. Aitken. "On Least Squares and Linear Combination of Observations." _Proceedings of the Royal Society of Edinburgh_ 55 (1936): 42-48.**

- DOI: https://doi.org/10.1017/S0370164600014346

**Role:** Classical generalized least-squares and correlated-error lineage. Proposition 56 uses exact temporal whitening before nuisance projection. The Proposition 56 Wishart identity and estimator are proved directly in this repository; Aitken is cited for the broader whitening and correlated-error estimation lineage.

'''
    write("docs/bibliography.md", bibliography.replace(anchor, section + anchor, 1))

append_once(
    "docs/bibliography.md",
    "## Proposition 56 literature note",
    '''## Proposition 56 literature note

Proposition 56 sits at the intersection of two established lines of mathematics: Aitken's generalized least-squares treatment of correlated errors and Wishart's exact Gaussian sample-covariance law. The repository uses the Proposition 53 physical-time whitener to expose innovation coordinates, transforms the nuisance design by the same map, and then proves the resulting Wishart law directly.
''',
)

readme = read("README.md")
for old, new in (
    ("version-0.44.0-2563eb", "version-0.45.0-2563eb"),
    ("| Research record | 0.44.0 state |", "| Research record | 0.45.0 state |"),
    ("| Proved statements | **55 propositions** |", "| Proved statements | **56 propositions** |"),
    ("| Reproducible studies | **42 experiments, A-Z and AA-AP** |", "| Reproducible studies | **43 experiments, A-Z and AA-AQ** |"),
    ("| Scientific result figures | **30 figures** |", "| Scientific result figures | **31 figures** |"),
    ("| Claim-level tests | **206 tests** |", "| Claim-level tests | **214 tests** |"),
    ("| Research-software version | **0.44.0** |", "| Research-software version | **0.45.0** |"),
    ("not included in the 30 scientific-result figure count", "not included in the 31 scientific-result figure count"),
    ("# 5. Complete theorem roadmap, Proposition 1 to Proposition 55", "# 5. Complete theorem roadmap, Proposition 1 to Proposition 56"),
    ("| Propositions 44 to 55 | [Research Index](docs/research_index.md) |", "| Propositions 44 to 56 | [Research Index](docs/research_index.md) |"),
):
    if readme.count(old) != 1:
        raise RuntimeError(f"README anchor not unique: {old!r} -> {readme.count(old)}")
    readme = readme.replace(old, new, 1)

record_anchor = "The physics pipeline is an explanatory diagram and is not included in the 31 scientific-result figure count.\n"
if readme.count(record_anchor) != 1:
    raise RuntimeError("README current-record anchor not unique")
current_highlight = r'''

## Current highlight: Proposition 56 and Experiment AQ

[![Experiment AQ: innovation-whitened target covariance](docs/innovation_whitened_target_covariance.svg)](docs/proposition_56_innovation_whitened_target_covariance.md)

Proposition 55 showed that even exact knowledge of the physical relaxation time left the existing raw-space covariance theorem above the relative-error threshold one. Proposition 56 changes the estimator rather than tightening calibration again.

For a known positive-definite temporal covariance \(R\), choose an exact whitener \(W\) with

\[
W R W^\mathsf T=I.
\]

Transform the nuisance design at the same time,

\[
A=WH,
\qquad
P_A=I-A(A^\mathsf T A)^{-1}A^\mathsf T,
\]

and estimate

\[
\widehat\Sigma_{\mathrm{white}}
=
\frac{X^\mathsf T W^\mathsf T P_A W X}{N-q}.
\]

Under the declared separable Gaussian model,

\[
\boxed{
(N-q)\widehat\Sigma_{\mathrm{white}}
\sim
W_p(\Sigma,N-q).
}
\]

On the same AP target geometry, Experiment AQ changes the certificate ladder from

\[
\boxed{
2.167136194
\longrightarrow
0.436438440
\longrightarrow
0.314236615.
}
\]

The values are the raw-space known-temporal-law theorem, the innovation-whitened matrix certificate, and the exact scalar chi-square certificate. The last two are below one.

**Physical meaning:** whitening applies the inverse of a known temporal filter and exposes the independent innovations already implied by that model. It does not create new observations. The nuisance design must be transformed by the same whitener before projection.

**Scope:** this theorem assumes the target temporal covariance used for whitening is correct. Substituting an estimated relaxation time and treating it as exact is not justified by Proposition 56. Robust whitening under temporal uncertainty is the next theorem problem.
'''
if "## Current highlight: Proposition 56 and Experiment AQ" not in readme:
    readme = readme.replace(record_anchor, record_anchor + current_highlight, 1)

ap_image = "[![Experiment AP: quadratic finite-sample relaxation calibration](docs/quadratic_relaxation_calibration.svg)](docs/proposition_55_quadratic_relaxation_calibration.md)\n"
aq_image = "\n[![Experiment AQ: innovation-whitened target covariance](docs/innovation_whitened_target_covariance.svg)](docs/proposition_56_innovation_whitened_target_covariance.md)\n"
if ap_image not in readme:
    raise RuntimeError("README Experiment AP image anchor missing")
if "Experiment AQ: innovation-whitened target covariance" not in readme.split("# 4. Visual research history", 1)[1]:
    readme = readme.replace(ap_image, ap_image + aq_image, 1)

p55_text_anchor = "**Proposition 55 / Experiment AP:**"
p56_phase_text = '''**Proposition 56 / Experiment AQ:** exact temporal whitening is applied before nuisance projection. The transformed nuisance design is removed in innovation coordinates, restoring an ordinary Wishart law with `N-q = 118` residual degrees of freedom on the controlled benchmark. The raw known-tau radius `2.16714` falls to `0.43644` for the matrix certificate and to `0.31424` for the exact scalar chi-square certificate. This result assumes the target temporal law used for whitening is correct.

'''
if p55_text_anchor not in readme:
    raise RuntimeError("README P55 phase text anchor missing")
if "**Proposition 56 / Experiment AQ:**" not in readme:
    readme = readme.replace(p55_text_anchor, p56_phase_text + p55_text_anchor, 1)

how_anchor = "| Release 0.44.0 audit | [0.44.0 Research Record](docs/release_0_44.md) |"
if how_anchor not in readme:
    raise RuntimeError("README release audit anchor missing")
if "Release 0.45.0 audit" not in readme:
    readme = readme.replace(
        how_anchor,
        "| Release 0.45.0 audit | [0.45.0 Research Record](docs/release_0_45.md) |\n" + how_anchor,
        1,
    )

frontier_start = readme.index("# 15. Current frontier\n")
frontier_end = readme.index("\n---\n\n# 16. Citation, bibliography, and conceptual source", frontier_start)
new_frontier = r'''# 15. Current frontier

Proposition 56 changes the target estimator itself. Under an exactly known temporal covariance, whitening first and then projecting the transformed nuisance design restores \(N-q\) independent Gaussian residual coordinates and moves the controlled AP/AQ benchmark below the relative-error threshold one.

The new matrix certificate is

\[
\boxed{
\varepsilon_{\mathrm{white,matrix}}
=0.43643844034822693<1,
}
\]

and the exact scalar chi-square certificate is

\[
\boxed{
\varepsilon_{\mathrm{white,scalar}}
=0.3142366148262574<1.
}
\]

This resolves the known-temporal-law bottleneck exposed by Proposition 55. It does not resolve temporal-model uncertainty.

The immediate statistical frontier is therefore **robust innovation whitening under an uncertain temporal law**. A valid next theorem must keep the whitening advantage while allowing the true physical relaxation time to range over a finite-sample confidence set. It must not plug an estimated \(\tau\) into Proposition 56 and silently treat it as exact.

The immediate physical diagnostic is equally clear: after whitening, residual temporal structure should be tested directly. Persistent autocorrelation, time-varying innovation variance, heavy tails, multiple relaxation scales, oscillations, or temporal-spatial nonseparability are evidence that the exact Proposition 56 law is not an adequate description of the record.

The broader physics frontiers remain sensor-coordinate invariance, spatial coarse graining, richer temporal kernels, and intervention-sensitive identifiability.

The guiding question remains:

> **Which inferred structures belong to the underlying dynamical organization, and which are artifacts of measurement representation, model misspecification, or insufficient information?**

That question remains separate from any claim about consciousness.
'''
readme = readme[:frontier_start] + new_frontier + readme[frontier_end:]
write("README.md", readme)

index = read("docs/research_index.md")
for old, new in (
    ("| Propositions | **55** |", "| Propositions | **56** |"),
    ("| Reproducible experiments | **42, A-Z and AA-AP** |", "| Reproducible experiments | **43, A-Z and AA-AQ** |"),
    ("| Scientific result figures | **30** |", "| Scientific result figures | **31** |"),
    ("| Claim-level tests | **206** |", "| Claim-level tests | **214** |"),
    ("| Research-software version | **0.44.0** |", "| Research-software version | **0.45.0** |"),
):
    if index.count(old) != 1:
        raise RuntimeError(f"research index anchor not unique: {old}")
    index = index.replace(old, new, 1)
if "| Audit Proposition 56 |" not in index:
    start_anchor = "| Audit Proposition 53 | [Sampling-consistent physical relaxation time and irregular-grid Markov structure](proposition_53_physical_relaxation_time.md) |"
    if index.count(start_anchor) != 1:
        raise RuntimeError("research index audit anchor not unique")
    index = index.replace(
        start_anchor,
        start_anchor + "\n| Audit Proposition 56 | [Innovation-whitened target covariance](proposition_56_innovation_whitened_target_covariance.md) |",
        1,
    )

experiment_anchor = "# Experiment index\n"
p56_index_section = r'''## Layer F. Innovation-whitened target covariance, Proposition 56

Proposition 56 changes the order of target processing when the temporal covariance is known. The record is whitened first, the nuisance design is transformed by the same map, and nuisance projection is then performed in innovation coordinates.

The exact result is

\[
(N-q)\widehat\Sigma_{\mathrm{white}}
\sim
W_p(\Sigma,N-q).
\]

On Experiment AQ, the raw known-temporal-law radius `2.16714` becomes `0.43644` for the whitened matrix certificate and `0.31424` for the exact scalar chi-square certificate.

This layer is conditional on a correct target temporal covariance. The next theorem problem is robust whitening under temporal uncertainty.

[Proof](proposition_56_innovation_whitened_target_covariance.md) | [Experiment AQ data](innovation_whitened_target_covariance.json) | [Release 0.45.0](release_0_45.md)

'''
if "## Layer F. Innovation-whitened target covariance, Proposition 56" not in index:
    if index.count(experiment_anchor) != 1:
        raise RuntimeError("research index experiment anchor not unique")
    index = index.replace(experiment_anchor, p56_index_section + experiment_anchor, 1)

if "## Experiment AQ" not in index:
    index += r'''

## Experiment AQ

**Proposition 56.** Exact temporal whitening before nuisance projection restores an ordinary Wishart covariance law with `N-q` residual degrees of freedom on the declared Gaussian separable model. The AQ figure compares the raw known-temporal-law radius `2.16714`, the whitened matrix radius `0.43644`, and the exact scalar radius `0.31424`.

[Proof](proposition_56_innovation_whitened_target_covariance.md) | [JSON](innovation_whitened_target_covariance.json) | [figure](innovation_whitened_target_covariance.svg) | [script](../examples/innovation_whitened_target_covariance.py)
'''
write("docs/research_index.md", index)

append_once(
    "docs/assumption_ledger.md",
    "## Innovation-whitened target covariance, Proposition 56",
    r'''## Innovation-whitened target covariance, Proposition 56

| Assumption | Used for | If it fails |
| --- | --- | --- |
| The target temporal covariance used to construct the whitener is the true positive-definite temporal covariance | Exact Wishart reduction in Proposition 56 | The transformed residuals need not be temporally white and the exact Wishart law can fail |
| Temporal and spatial covariance are separable as \(R\otimes\Sigma\) | Independent Gaussian innovation rows after temporal whitening | Temporal whitening alone need not produce iid spatial residual rows |
| Target innovations are Gaussian | Exact Wishart and chi-square laws | The estimator may remain useful, but the exact finite-sample distributional certificate no longer follows |
| The nuisance mean lies in a fixed declared design \(H\) chosen independently of target noise | Exact annihilation after transforming \(H\) to \(WH\) | Residual deterministic structure or adaptive nuisance selection can invalidate the law |
| The nuisance design is transformed by the same whitener used on the data | Correct projection geometry | Projecting the untransformed nuisance design in whitened coordinates removes the wrong subspace |

**Required diagnostic:** inspect whitened residuals for remaining autocorrelation, time-varying variance, heavy tails, multiple timescales, oscillatory structure, and temporal-spatial nonseparability before using the exact Proposition 56 interpretation on a physical record.
''',
)

append_once(
    "docs/api_temporal_calibration.md",
    "## Proposition 56: innovation-whitened target covariance",
    r'''## Proposition 56: innovation-whitened target covariance

Public package-root imports:

```python
from observer_math import (
    GaussianWhitenedProjectedCovarianceBound,
    GaussianWhitenedScalarChiSquareBound,
    exponential_relaxation_whitened_projected_covariance,
    gaussian_whitened_projected_covariance_bound,
    gaussian_whitened_scalar_chi_square_bound,
    separable_gaussian_whitened_projected_covariance,
    whitened_nuisance_projector,
)
```

For a known temporal whitener `W` and fixed nuisance design `H`, use

```python
estimate = separable_gaussian_whitened_projected_covariance(
    samples,
    W,
    H,
)
```

For the Proposition 53 exponential physical-time model, use

```python
estimate = exponential_relaxation_whitened_projected_covariance(
    samples,
    sample_times,
    relaxation_time,
    H,
)
```

The matrix certificate uses the exact unit-weight Wishart law with `N-q` residual degrees of freedom. For scalar blocks, `gaussian_whitened_scalar_chi_square_bound` returns the exact chi-square interval.

The API assumes that the temporal law supplied to the whitener is correct. It does not treat an estimated relaxation time as exact.
''',
)

append_once(
    "docs/figure_reading_guide.md",
    "## Experiment AQ: innovation-whitened target covariance",
    r'''## Experiment AQ: innovation-whitened target covariance

**What the figure shows:** panel A compares three covariance certificates on the same target geometry. Panel B compares the raw projected temporal normalization with the `N-q` independent innovation residual degrees recovered after exact whitening. Panel C reports a seeded visibility study. Panel D shows the physical inference order: target record, exact whitening, transformed nuisance design, nuisance projection, Wishart residual covariance.

**Physical interpretation:** the temporal model is represented as a known linear filter driven by Gaussian innovations. Whitening applies the inverse filter. It does not create new data.

**What the figure does not show:** it does not establish that an estimated temporal law may be treated as exact, that every physical record is separable Gaussian, or that a covariance radius below one is a consciousness measure.
''',
)

append_once(
    "docs/research_overview.md",
    "## Proposition 56: exact temporal whitening changes the target information geometry",
    r'''## Proposition 56: exact temporal whitening changes the target information geometry

Proposition 55 showed that calibration was no longer the dominant bottleneck on the AP benchmark. Proposition 56 therefore changes the target estimator itself.

When the temporal covariance \(R\) is known, an exact whitener \(W\) with \(WRW^\mathsf T=I\) is applied before nuisance projection. The nuisance design becomes \(WH\). Projecting that transformed design leaves exactly \(N-q\) Gaussian innovation residual coordinates, producing an ordinary Wishart covariance law.

Experiment AQ moves the raw known-temporal-law radius from `2.16714` to `0.43644` for the matrix certificate and to `0.31424` for the exact scalar chi-square certificate. This crosses the perturbative threshold one on the controlled benchmark.

The result narrows the next research question: preserve as much of this whitening advantage as possible when the temporal law is known only through a finite-sample confidence set.
''',
)

append_once(
    "docs/reproducible_results.md",
    "## Experiment AQ: innovation-whitened target covariance",
    r'''## Experiment AQ: innovation-whitened target covariance

Run:

```bash
python examples/innovation_whitened_target_covariance.py
python examples/render_innovation_whitened_target_covariance.py
```

Committed assets:

- proof: `docs/proposition_56_innovation_whitened_target_covariance.md`
- data: `docs/innovation_whitened_target_covariance.json`
- figure: `docs/innovation_whitened_target_covariance.svg`
- experiment: `examples/innovation_whitened_target_covariance.py`
- renderer: `examples/render_innovation_whitened_target_covariance.py`

On the controlled AP/AQ target geometry, the raw known-temporal-law radius is `2.167136193997473`, the innovation-whitened matrix radius is `0.43643844034822693`, and the exact scalar chi-square radius is `0.3142366148262574`. The exact temporal covariance is treated as known in this experiment.
''',
)

history = read("docs/recent_release_history.md")
if not history.startswith("## 0.45.0"):
    new = '''## 0.45.0

Proposition 56 / Experiment AQ changes the target estimator by applying exact temporal whitening before nuisance projection. On the AP/AQ benchmark, the known-temporal-law covariance radius moves from `2.16714` to `0.43644` for the whitened matrix certificate and to `0.31424` for the exact scalar chi-square certificate. The release explicitly limits the theorem to a correct known target temporal covariance. See [release record](release_0_45.md).

'''
    write("docs/recent_release_history.md", new + history)

changelog = read("CHANGELOG.md")
if not changelog.startswith("## 0.45.0"):
    new = '''## 0.45.0 - 2026-09-08

- Added Proposition 56, which applies exact temporal whitening before nuisance projection and proves an ordinary Wishart law with `N-q` residual degrees of freedom.
- Added Experiment AQ and its machine-readable and visual record.
- Reduced the controlled raw known-temporal-law target radius from `2.16714` to `0.43644` for the matrix certificate and to `0.31424` for the exact scalar chi-square certificate.
- Added public Proposition 56 APIs, exact artifact reproducibility checks, Aitken generalized least-squares lineage, assumptions, proof documentation, and explicit model-mismatch diagnostics.
- Updated the intended release record to 56 propositions, 43 experiments, 31 scientific-result figures, and 214 claim-level tests.

'''
    write("CHANGELOG.md", new + changelog)
