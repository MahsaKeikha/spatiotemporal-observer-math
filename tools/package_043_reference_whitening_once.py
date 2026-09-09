from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


# Version metadata.
path = Path("pyproject.toml")
text = path.read_text(encoding="utf-8")
text = replace_once(text, 'version = "0.42.0"', 'version = "0.43.0"', "pyproject version")
path.write_text(text, encoding="utf-8")

path = Path("CITATION.cff")
text = path.read_text(encoding="utf-8")
text = replace_once(text, "version: 0.42.0", "version: 0.43.0", "citation version")
path.write_text(text, encoding="utf-8")

# Root public API.
path = Path("src/observer_math/__init__.py")
text = path.read_text(encoding="utf-8")
import_block = '''from .second_order_relaxation import (
    GaussianIrregularRelaxationSecondOrderOuterCover,
    GaussianReferenceWhitenedRelaxationTargetBound,
    gaussian_irregular_relaxation_log_likelihood_second_derivative,
    gaussian_irregular_relaxation_log_likelihood_second_derivative_bound,
    gaussian_irregular_relaxation_second_order_outer_cover,
    gaussian_reference_whitened_irregular_relaxation_target_matrix_chernoff_bound,
)
'''
if "GaussianReferenceWhitenedRelaxationTargetBound" not in text:
    text = replace_once(
        text,
        "from .search import Candidate, rank_subsystems\n",
        "from .search import Candidate, rank_subsystems\n" + import_block,
        "public API import block",
    )
    text = replace_once(
        text,
        '    "GaussianRelativeNearCompetitorScreen",\n',
        '    "GaussianIrregularRelaxationSecondOrderOuterCover",\n'
        '    "GaussianReferenceWhitenedRelaxationTargetBound",\n'
        '    "GaussianRelativeNearCompetitorScreen",\n',
        "public API class exports",
    )
    text = replace_once(
        text,
        '    "gaussian_irregular_relaxation_log_likelihood_lipschitz_bound",\n',
        '    "gaussian_irregular_relaxation_log_likelihood_lipschitz_bound",\n'
        '    "gaussian_irregular_relaxation_log_likelihood_second_derivative",\n'
        '    "gaussian_irregular_relaxation_log_likelihood_second_derivative_bound",\n'
        '    "gaussian_irregular_relaxation_second_order_outer_cover",\n',
        "public API irregular exports",
    )
    text = replace_once(
        text,
        '    "gaussian_relative_structural_null_near_competitor_screen",\n',
        '    "gaussian_reference_whitened_irregular_relaxation_target_matrix_chernoff_bound",\n'
        '    "gaussian_relative_structural_null_near_competitor_screen",\n',
        "public API whitening export",
    )
path.write_text(text, encoding="utf-8")

# README public record and front-page visual.
path = Path("README.md")
text = path.read_text(encoding="utf-8")
text = replace_once(text, "version-0.42.0-2563eb", "version-0.43.0-2563eb", "README badge")
old_record = '''| Research record | 0.42.0 state |
| --- | ---: |
| Proved statements | **53 propositions** |
| Reproducible studies | **40 experiments, A-Z and AA-AN** |
| Scientific result figures | **28 figures** |
| Claim-level tests | **195 tests** |
| CI matrix | **Python 3.10, 3.11, 3.12** |
| Research-software version | **0.42.0** |

The physics pipeline is an explanatory diagram and is not included in the 28 scientific-result figure count.'''
new_record = '''| Research record | 0.43.0 state |
| --- | ---: |
| Proved statements | **54 propositions** |
| Reproducible studies | **41 experiments, A-Z and AA-AO** |
| Scientific result figures | **29 figures** |
| Claim-level tests | **202 tests** |
| CI matrix | **Python 3.10, 3.11, 3.12** |
| Research-software version | **0.43.0** |

The physics pipeline is an explanatory diagram and is not included in the 29 scientific-result figure count.'''
text = replace_once(text, old_record, new_record, "README research record")
phase_anchor = '''[![Experiment AN: finite-sample irregular-time tau calibration](docs/irregular_relaxation_evalue_calibration.svg)](docs/proposition_53b_irregular_tau_evalue.md)

**Proposition 53B / Experiment AN:** the same physical-time parameter is now calibrated directly from an irregular record with a finite-sample continuum e-value. The visible likelihood-compatible region is approximately `[0.69155, 0.84455] s`, while the certified outer cover is `[0.495625, 1.1065625] s`. The difference is an explicit tightness gap, not a coverage failure.'''
phase_new = phase_anchor + '''

[![Experiment AO: second-order reference whitening](docs/second_order_reference_whitening.svg)](docs/proposition_54_second_order_reference_whitening.md)

**Proposition 54 / Experiment AO:** second-order calibration geometry contracts the retained physical-time cover to `[0.686875, 0.8515625] s`. A calibration-derived reference whitener then transforms the independent target temporal family close to identity. On the same controlled target geometry as Experiment AN, the certified relative covariance radius moves from `3.1554895445` to **`0.6899552436 < 1`** at combined confidence `0.950625`.'''
text = replace_once(text, phase_anchor, phase_new, "README AO visual")
text = replace_once(
    text,
    "# 5. Complete theorem roadmap, Proposition 1 to Proposition 53",
    "# 5. Complete theorem roadmap, Proposition 1 to Proposition 54",
    "README roadmap title",
)
text = replace_once(
    text,
    "## Layer E. Sampling-consistent physical representation and inference, Proposition 53",
    "## Layer E. Sampling-consistent physical representation and inference, Propositions 53 to 54",
    "README layer E title",
)
row = "| 53B | Can the physical relaxation time itself be calibrated with finite-sample coverage directly on irregular timestamps? | Which physical timescales remain compatible with an irregular calibration record, independent of the target experiment's sampling schedule? |"
row_new = row + "\n| 54 | Can second-order calibration geometry and a calibration-derived exact reference whitener preserve finite-sample target certification under strong temporal dependence? | Can physical-time uncertainty be propagated through irregular-time whitening strongly enough to recover a subunit covariance regime? |"
text = replace_once(text, row, row_new, "README P54 roadmap row")
text = replace_once(
    text,
    "[Proposition 53A proof](docs/proposition_53_physical_relaxation_time.md) | [Proposition 53B proof](docs/proposition_53b_irregular_tau_evalue.md).",
    "[Proposition 53A proof](docs/proposition_53_physical_relaxation_time.md) | [Proposition 53B proof](docs/proposition_53b_irregular_tau_evalue.md) | [Proposition 54 proof](docs/proposition_54_second_order_reference_whitening.md).",
    "README proof links",
)
old_latest = "# 6. Latest physical-statistical result, Proposition 53B and Experiment AN\n\n[![Experiment AN](docs/irregular_relaxation_evalue_calibration.svg)](docs/proposition_53b_irregular_tau_evalue.md)"
new_latest = '''# 6. Latest physical-statistical result, Proposition 54 and Experiment AO

[![Experiment AO](docs/second_order_reference_whitening.svg)](docs/proposition_54_second_order_reference_whitening.md)

Proposition 54 keeps Proposition 53B's finite-sample physical-time calibration event and sharpens its deterministic geometry. The second-order outer cover retains 31 of 160 cells, with certified extremes `[0.686875, 0.8515625] s`. A reference relaxation time `0.76921875 s` is chosen from calibration alone, and the exact Proposition 53A irregular-time whitener is fixed before the independent target record is used.

On the Experiment AO target geometry, the transformed temporal family has certified operator radius `0.0084958644`. The final Proposition 49 relative covariance radius is

\\[
\\boxed{0.6899552435608669<1}
\\]

at combined confidence `0.950625`. The exact whitening identity is satisfied numerically to about `1.9e-15`. A dense visibility check reaches about 50.7 percent of the temporal operator certificate and 99.996 percent of the normalization certificate.

This is the first result in the physical-time branch that closes the specific above-one covariance-certification bottleneck exposed by Experiment AN. It does so by propagating calibrated uncertainty through exact model-based temporal whitening, not by treating correlated raw samples as independent.

[Full Proposition 54 proof](docs/proposition_54_second_order_reference_whitening.md) | [0.43.0 research record](docs/release_0_43_0.md) | [Experiment AO JSON](docs/second_order_reference_whitening.json) | [Experiment AO script](examples/second_order_reference_whitening.py) | [AO renderer](examples/render_second_order_reference_whitening.py) | [Claim-level tests](tests/test_second_order_relaxation.py)

### Previous physical-time result: Proposition 53B and Experiment AN

[![Experiment AN](docs/irregular_relaxation_evalue_calibration.svg)](docs/proposition_53b_irregular_tau_evalue.md)'''
text = replace_once(text, old_latest, new_latest, "README latest result")
path.write_text(text, encoding="utf-8")

# Append concise audit sections to repository ledgers.
sections = {
    "docs/research_index.md": '''\n\n## Proposition 54 and Experiment AO: second-order physical-time reference whitening\n\nProposition 54 sharpens the Proposition 53B continuum tau cover with a second-order interpolation remainder, then fixes the exact Proposition 53A irregular-time whitener at a calibration-derived reference tau. The independent target nuisance design is transformed by the same whitener and Proposition 49 is applied to a certified near-identity temporal family.\n\nExperiment AO retains 31 of 160 tau cells, uses reference tau `0.76921875 s`, and achieves relative target covariance radius `0.6899552435608669 < 1` at combined confidence `0.950625`.\n\nProof: [Proposition 54](proposition_54_second_order_reference_whitening.md). Machine-readable record: [Experiment AO JSON](second_order_reference_whitening.json).\n''',
    "docs/assumption_ledger.md": '''\n\n## Proposition 54: second-order physical-time reference whitening\n\nAdditional obligations beyond Proposition 53B are: the target record is independent of calibration; the target nuisance design is fixed before target-data inspection; the separable Gaussian target model uses the same exponential relaxation family; the calibration-derived reference tau is chosen without target data; and the projected normalization stays positive over the certified transformed temporal family. The theorem is conditional on these assumptions and does not establish that a real system follows one exponential timescale.\n''',
    "docs/api_temporal_calibration.md": '''\n\n## Proposition 54 public API\n\n`GaussianIrregularRelaxationSecondOrderOuterCover` records the curvature-certified tau cells. `gaussian_irregular_relaxation_log_likelihood_second_derivative` evaluates the exact calibration likelihood curvature, while `gaussian_irregular_relaxation_log_likelihood_second_derivative_bound` certifies it on a subinterval. `gaussian_irregular_relaxation_second_order_outer_cover` constructs the finite continuum outer cover. `GaussianReferenceWhitenedRelaxationTargetBound` and `gaussian_reference_whitened_irregular_relaxation_target_matrix_chernoff_bound` propagate the retained physical-time family through a calibration-derived Proposition 53A reference whitener and then into Proposition 49.\n''',
    "docs/reproducible_results.md": '''\n\n## Experiment AO: second-order physical-time reference whitening\n\nThe same controlled calibration and target geometry as Experiment AN is reused. The second-order tau cover retains 31 of 160 cells with certified extremes `[0.686875, 0.8515625] s`. The calibration-derived reference whitener gives a transformed temporal covering radius `0.008495864441166266`, normalization radius `0.46699818384400943`, and final target relative covariance radius `0.6899552435608669 < 1` at combined confidence `0.950625`. The committed JSON and deterministic SVG are `second_order_reference_whitening.json` and `second_order_reference_whitening.svg`.\n''',
    "docs/recent_release_history.md": '''\n\n## 0.43.0\n\nProposition 54 and Experiment AO add second-order continuum certification and calibration-derived reference whitening for irregular physical time. The release closes the controlled above-one target covariance bottleneck from Experiment AN, reaching `0.6899552435608669 < 1` at combined confidence `0.950625`. See [release 0.43.0](release_0_43_0.md).\n''',
    "CHANGELOG.md": '''\n\n## 0.43.0\n\n- add Proposition 54 second-order physical-time continuum certification;\n- add calibration-derived exact irregular-time reference whitening for independent target covariance certification;\n- add Experiment AO, machine-readable results, deterministic SVG, proof, tests, public API, and release record;\n- on the controlled Experiment AN target geometry, reduce the certified relative covariance radius from `3.1554895445` to `0.6899552436 < 1` at combined confidence `0.950625`.\n''',
}
for filename, section in sections.items():
    path = Path(filename)
    text = path.read_text(encoding="utf-8")
    marker = section.strip().splitlines()[0]
    if marker not in text:
        path.write_text(text.rstrip() + section + "\n", encoding="utf-8")
