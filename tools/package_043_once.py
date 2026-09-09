"""One-shot release 0.43.0 packaging helper. Remove before merge."""

from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


# Public API.
path = Path("src/observer_math/__init__.py")
text = path.read_text(encoding="utf-8")
if "GaussianIrregularRelaxationTwoScaleTargetBound" not in text:
    import_block = '''from .two_scale_relaxation_cover import (
    GaussianIrregularRelaxationTwoScaleTargetBound,
    GaussianOptimizedIrregularRelaxationTwoScaleTargetBound,
    gaussian_irregular_relaxation_two_scale_target_bound,
    gaussian_optimized_irregular_relaxation_two_scale_target_bound,
)
'''
    text = replace_once(
        text,
        "from .uniform_matrix_chernoff import (\n",
        import_block + "from .uniform_matrix_chernoff import (\n",
        "public import",
    )
    text = replace_once(
        text,
        '    "GaussianIncrementCorrelationInterval",\n',
        '    "GaussianIncrementCorrelationInterval",\n'
        '    "GaussianIrregularRelaxationTwoScaleTargetBound",\n'
        '    "GaussianOptimizedIrregularRelaxationTwoScaleTargetBound",\n',
        "public class exports",
    )
    text = replace_once(
        text,
        '    "gaussian_irregular_relaxation_target_matrix_chernoff_bound",\n',
        '    "gaussian_irregular_relaxation_target_matrix_chernoff_bound",\n'
        '    "gaussian_irregular_relaxation_two_scale_target_bound",\n'
        '    "gaussian_optimized_irregular_relaxation_two_scale_target_bound",\n',
        "public function exports",
    )
path.write_text(text, encoding="utf-8")


# Front page.
path = Path("README.md")
text = path.read_text(encoding="utf-8")
text = replace_once(text, "version-0.42.0-2563eb", "version-0.43.0-2563eb", "README badge")
text = replace_once(text, "| Research record | 0.42.0 state |", "| Research record | 0.43.0 state |", "README record header")
text = replace_once(text, "| Proved statements | **53 propositions** |", "| Proved statements | **54 propositions** |", "README proposition count")
text = replace_once(text, "| Reproducible studies | **40 experiments, A-Z and AA-AN** |", "| Reproducible studies | **41 experiments, A-Z and AA-AO** |", "README experiment count")
text = replace_once(text, "| Scientific result figures | **28 figures** |", "| Scientific result figures | **29 figures** |", "README figure count")
text = replace_once(text, "| Claim-level tests | **195 tests** |", "| Claim-level tests | **200 tests** |", "README test count")
text = replace_once(text, "| Research-software version | **0.42.0** |", "| Research-software version | **0.43.0** |", "README version row")
text = replace_once(text, "not included in the 28 scientific-result figure count", "not included in the 29 scientific-result figure count", "README figure note")
text = replace_once(text, "# 5. Complete theorem roadmap, Proposition 1 to Proposition 53", "# 5. Complete theorem roadmap, Proposition 1 to Proposition 54", "README theorem heading")

an_anchor = "[![Experiment AN: finite-sample irregular-time tau calibration](docs/irregular_relaxation_evalue_calibration.svg)](docs/proposition_53b_irregular_tau_evalue.md)\n"
ao_block = an_anchor + '''
[![Experiment AO: two-scale certified relaxation cover](docs/two_scale_irregular_tau_cover.svg)](docs/proposition_54_two_scale_irregular_tau_cover.md)

**Proposition 54 / Experiment AO:** calibration certification and target temporal-cover resolution are now separated. Refining the calibration certificate from 160 to 2560 cells shrinks the certified tau width from `0.61094 s` to `0.21217 s`. On the exact Experiment AN target problem, the final relative covariance radius falls from `3.15549` to `2.57207`, an `18.49%` reduction. The radius remains above one, so the next bottleneck is the local temporal operator/likelihood envelope rather than cover-cardinality coupling.
'''
text = replace_once(text, an_anchor, ao_block, "README AO figure insertion")

layer_anchor = "[Proposition 53A proof](docs/proposition_53_physical_relaxation_time.md) | [Proposition 53B proof](docs/proposition_53b_irregular_tau_evalue.md).\n"
layer_new = layer_anchor + '''

## Layer F. Two-scale physical-time uncertainty propagation, Proposition 54

| Proposition | Mathematical question | Physical question |
| ---: | --- | --- |
| 54 | Can calibration certification resolution be separated from target temporal-cover resolution without losing finite-sample validity? | Can a physical timescale be certified finely while propagating only a compressed family into an independent target experiment? |

[Proposition 54 proof](docs/proposition_54_two_scale_irregular_tau_cover.md).
'''
text = replace_once(text, layer_anchor, layer_new, "README layer 54 insertion")

section_anchor = "# 7. Latest statistical certification result, Proposition 52 and Experiment AL"
section54 = '''# 7. Latest tightening result, Proposition 54 and Experiment AO

[![Experiment AO](docs/two_scale_irregular_tau_cover.svg)](docs/proposition_54_two_scale_irregular_tau_cover.md)

Proposition 54 decouples the fine partition used to certify the continuum physical-time confidence set from the smaller target temporal cover used by Proposition 49.

On Experiment AO, the Proposition 53B baseline radius `3.1554895445` falls to `2.5720746948`, a reduction of approximately `18.49%`, at the same combined confidence `0.950625`.

The result is deliberately not presented as closing the downstream perturbation problem: `2.57207 > 1`. Instead it shows that target-cover cardinality was only part of the looseness. The next proof target is a sharper local curvature or operator certificate.

[Full Proposition 54 proof](docs/proposition_54_two_scale_irregular_tau_cover.md) | [0.43.0 research record](docs/release_0_43.md) | [Experiment AO JSON](docs/two_scale_irregular_tau_cover.json) | [Experiment AO script](examples/two_scale_irregular_tau_cover.py)

---

# 8. Latest statistical certification result, Proposition 52 and Experiment AL'''
text = replace_once(text, section_anchor, section54, "README latest result insertion")
# Shift the remaining top-level numbered headings after the inserted section.
for old, new in [
    ("# 8. What covariance means physically", "# 9. What covariance means physically"),
    ("# 9. Identifiability before interpretation", "# 10. Identifiability before interpretation"),
    ("# 10. What this repository establishes", "# 11. What this repository establishes"),
    ("# 11. How to read the repository", "# 12. How to read the repository"),
    ("# 12. Reproducibility standard", "# 13. Reproducibility standard"),
]:
    if old in text:
        text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")


# Research index.
path = Path("docs/research_index.md")
text = path.read_text(encoding="utf-8")
if "Proposition 54" not in text:
    text += '''

## Proposition 54: two-scale certified irregular-time relaxation cover

**Question.** Can the numerical resolution needed to certify the calibration confidence set be separated from the number of temporal representatives carried into the target covariance theorem?

**Result.** Yes. A fine Proposition 53B outer cover is enclosed by its retained physical-time interval, then a second target grid covers that interval with operator radius `L h / 2` and normalization radius `q L h / 2`. Target cover size may be selected using calibration-derived geometry and declared target design information without inspecting target observations.

**Experiment AO.** On the Experiment AN problem, the target covariance radius decreases from `3.1554895445` to `2.5720746948`, an `18.49%` reduction, but remains above one.

[Proof](proposition_54_two_scale_irregular_tau_cover.md) | [Machine record](two_scale_irregular_tau_cover.json)
'''
path.write_text(text, encoding="utf-8")


# Temporal API documentation.
path = Path("docs/api_temporal_calibration.md")
text = path.read_text(encoding="utf-8")
if "gaussian_irregular_relaxation_two_scale_target_bound" not in text:
    text += '''

## Proposition 54 two-scale irregular relaxation cover

Public functions:

- `gaussian_irregular_relaxation_two_scale_target_bound`
- `gaussian_optimized_irregular_relaxation_two_scale_target_bound`

Public result types:

- `GaussianIrregularRelaxationTwoScaleTargetBound`
- `GaussianOptimizedIrregularRelaxationTwoScaleTargetBound`

The first function certifies a fine calibration outer cover and then covers its retained physical-time interval with a separately chosen target grid. The second selects the target grid size from a declared candidate set using calibration-derived geometry and target design information only. No target observations are used for that selection.
'''
path.write_text(text, encoding="utf-8")


# Reproducible results.
path = Path("docs/reproducible_results.md")
text = path.read_text(encoding="utf-8")
if "Experiment AO" not in text:
    text += '''

## Experiment AO: two-scale certified irregular-time relaxation cover

Experiment AO reuses the Experiment AN physical-time problem and separates calibration certification resolution from target temporal-cover resolution.

At 1280 calibration cells and selected target cover size `K=65`, the final relative covariance radius is `2.572074694777741`, compared with the Proposition 53B baseline `3.155489544511118`. This is an `18.49%` reduction. The value remains above one.

[Proof](proposition_54_two_scale_irregular_tau_cover.md) | [JSON](two_scale_irregular_tau_cover.json) | [Figure](two_scale_irregular_tau_cover.svg)
'''
path.write_text(text, encoding="utf-8")


# Changelog.
path = Path("CHANGELOG.md")
text = path.read_text(encoding="utf-8")
if "## 0.43.0" not in text:
    text = '''## 0.43.0 - 2026-09-08

- Added Proposition 54, a two-scale certified physical relaxation-time cover that separates calibration-cell resolution from target temporal-cover resolution.
- Added Experiment AO and its machine-readable/visual record.
- Reduced the Experiment AN target covariance radius from `3.15549` to `2.57207` while retaining combined confidence `0.950625`; the release explicitly records that the radius remains above one.
- Added public Proposition 54 API functions and result types.

''' + text
path.write_text(text, encoding="utf-8")


# Recent release history.
path = Path("docs/recent_release_history.md")
if path.exists():
    text = path.read_text(encoding="utf-8")
    if "0.43.0" not in text:
        text = '''## 0.43.0

Proposition 54 / Experiment AO separates fine irregular-time calibration certification from target temporal-cover resolution. The exact AN benchmark radius decreases from `3.15549` to `2.57207` but remains above the perturbative threshold one. See [release record](release_0_43.md).

''' + text
    path.write_text(text, encoding="utf-8")
