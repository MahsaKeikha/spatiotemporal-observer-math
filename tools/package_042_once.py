"""One-shot branch packaging helper for release 0.42.0; removed before merge."""

from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def patch_public_api() -> None:
    path = Path("src/observer_math/__init__.py")
    text = path.read_text(encoding="utf-8")
    import_block = """from .irregular_relaxation_evalue import (
    GaussianIrregularRelaxationEValueGrid,
    GaussianIrregularRelaxationEValueModel,
    GaussianIrregularRelaxationEValueOuterCover,
    GaussianIrregularRelaxationTargetBound,
    gaussian_irregular_relaxation_evalue_grid,
    gaussian_irregular_relaxation_evalue_model,
    gaussian_irregular_relaxation_evalue_outer_cover,
    gaussian_irregular_relaxation_log_evalue,
    gaussian_irregular_relaxation_log_likelihood_kernel,
    gaussian_irregular_relaxation_log_likelihood_lipschitz_bound,
    gaussian_irregular_relaxation_target_matrix_chernoff_bound,
)
"""
    if "GaussianIrregularRelaxationEValueModel" not in text:
        text = replace_once(
            text,
            "from .identifiability import (\n",
            import_block + "from .identifiability import (\n",
            "init import insertion",
        )
        text = replace_once(
            text,
            '    "GaussianIncrementCorrelationInterval",\n',
            '    "GaussianIncrementCorrelationInterval",\n'
            '    "GaussianIrregularRelaxationEValueGrid",\n'
            '    "GaussianIrregularRelaxationEValueModel",\n'
            '    "GaussianIrregularRelaxationEValueOuterCover",\n'
            '    "GaussianIrregularRelaxationTargetBound",\n',
            "init class exports",
        )
        text = replace_once(
            text,
            '    "gaussian_factor_aware_near_competitor_screen",\n',
            '    "gaussian_factor_aware_near_competitor_screen",\n'
            '    "gaussian_irregular_relaxation_evalue_grid",\n'
            '    "gaussian_irregular_relaxation_evalue_model",\n'
            '    "gaussian_irregular_relaxation_evalue_outer_cover",\n'
            '    "gaussian_irregular_relaxation_log_evalue",\n'
            '    "gaussian_irregular_relaxation_log_likelihood_kernel",\n'
            '    "gaussian_irregular_relaxation_log_likelihood_lipschitz_bound",\n'
            '    "gaussian_irregular_relaxation_target_matrix_chernoff_bound",\n',
            "init function exports",
        )
    path.write_text(text, encoding="utf-8")


def patch_readme() -> None:
    path = Path("README.md")
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "version-0.41.1-2563eb",
        "version-0.42.0-2563eb",
        "README badge",
    )
    text = replace_once(
        text,
        "| Research record | 0.41.1 state |",
        "| Research record | 0.42.0 state |",
        "README state header",
    )
    text = replace_once(
        text,
        "| Reproducible studies | **39 experiments, A-Z and AA-AM** |",
        "| Reproducible studies | **40 experiments, A-Z and AA-AN** |",
        "README experiment count",
    )
    text = replace_once(
        text,
        "| Scientific result figures | **27 figures** |",
        "| Scientific result figures | **28 figures** |",
        "README figure count",
    )
    text = replace_once(
        text,
        "| Claim-level tests | **188 tests** |",
        "| Claim-level tests | **195 tests** |",
        "README test count",
    )
    text = replace_once(
        text,
        "| Research-software version | **0.41.1** |",
        "| Research-software version | **0.42.0** |",
        "README version count",
    )

    phase_table = """| Sampling consistency | Irregular-grid Markov factorization |
| --- | --- |
| [![Experiment AM: physical relaxation time](docs/physical_relaxation_sampling.svg)](docs/proposition_53_physical_relaxation_time.md) | [![Proposition 53: irregular-grid Markov factorization](docs/physical_relaxation_markov.svg)](docs/proposition_53_physical_relaxation_time.md) |
"""
    phase_new = phase_table + """
[![Experiment AN: finite-sample irregular-time tau calibration](docs/irregular_relaxation_evalue_calibration.svg)](docs/proposition_53b_irregular_tau_evalue.md)

**Proposition 53B / Experiment AN:** the same physical-time parameter is now calibrated directly from an irregular record with a finite-sample continuum e-value. The visible likelihood-compatible region is approximately `[0.69155, 0.84455] s`, while the certified outer cover is `[0.495625, 1.1065625] s`. The difference is an explicit tightness gap, not a coverage failure.
"""
    text = replace_once(text, phase_table, phase_new, "README Phase IX figure")

    layer_old = """## Layer E. Sampling-consistent physical representation, Proposition 53

| Proposition | Mathematical question | Physical question |
| ---: | --- | --- |
| 53 | Can the exponential temporal family be parameterized by a physical relaxation time and factorized exactly on arbitrary increasing timestamps? | Does the inferred timescale survive sampling changes, and does the same physical model retain a local transition law under irregular or missing observations? |

[Full Proposition 53 proof](docs/proposition_53_physical_relaxation_time.md).
"""
    layer_new = """## Layer E. Sampling-consistent physical representation and inference, Proposition 53

| Proposition | Mathematical question | Physical question |
| ---: | --- | --- |
| 53A | Can the exponential temporal family be parameterized by a physical relaxation time and factorized exactly on arbitrary increasing timestamps? | Does the inferred timescale survive sampling changes, and does the same physical model retain a local transition law under irregular or missing observations? |
| 53B | Can the physical relaxation time itself be calibrated with finite-sample coverage directly on irregular timestamps? | Which physical timescales remain compatible with an irregular calibration record, independent of the target experiment's sampling schedule? |

[Proposition 53A proof](docs/proposition_53_physical_relaxation_time.md) | [Proposition 53B proof](docs/proposition_53b_irregular_tau_evalue.md).
"""
    text = replace_once(text, layer_old, layer_new, "README Layer E")

    section_old = """# 6. Latest physical result, Proposition 53 and Experiment AM

| Sampling invariance | Exact irregular-grid local structure |
| --- | --- |
| [![Experiment AM](docs/physical_relaxation_sampling.svg)](docs/proposition_53_physical_relaxation_time.md) | [![Proposition 53 Markov factorization](docs/physical_relaxation_markov.svg)](docs/proposition_53_physical_relaxation_time.md) |
"""
    section_new = """# 6. Latest physical-statistical result, Proposition 53B and Experiment AN

[![Experiment AN](docs/irregular_relaxation_evalue_calibration.svg)](docs/proposition_53b_irregular_tau_evalue.md)

Proposition 53 now has two linked stages: **53A** establishes sampling-consistent physical time and exact irregular-grid Markov structure; **53B** uses that structure to calibrate the physical relaxation time directly with a finite-sample continuum e-value.

| Sampling invariance | Exact irregular-grid local structure |
| --- | --- |
| [![Experiment AM](docs/physical_relaxation_sampling.svg)](docs/proposition_53_physical_relaxation_time.md) | [![Proposition 53 Markov factorization](docs/physical_relaxation_markov.svg)](docs/proposition_53_physical_relaxation_time.md) |
"""
    text = replace_once(text, section_old, section_new, "README latest section")

    am_links = """[Full proof](docs/proposition_53_physical_relaxation_time.md) | [0.41.1 research record](docs/release_0_41_1.md) | [Machine-readable results](docs/physical_relaxation_sampling.json) | [Experiment script](examples/physical_relaxation_sampling.py) | [Sampling renderer](examples/render_physical_relaxation_sampling.py) | [Markov renderer](examples/render_physical_relaxation_markov.py) | [Claim-level tests](tests/test_physical_relaxation.py)
"""
    an_block = am_links + """
### Proposition 53B: finite-sample physical-time calibration

For Experiment AN, the true value is `tau = 0.78 s`. At 97.5% calibration confidence the continuum e-value diagnostic accepts approximately `[0.69155, 0.84455] s` on a 2001-point visibility grid. A deterministic cell-local derivative certificate safely retains `[0.495625, 1.1065625] s`, with 115 of 160 cells retained and 45 excluded.

Changing seconds to milliseconds changes the checked log e-values by at most `2.05e-12`, confirming that the inference geometry is about physical time rather than the numerical unit used to write it.

The retained family composes with Proposition 49 on a different independent 120-sample target timestamp grid. With calibration and target covariance confidence both `0.975`, the combined confidence is `0.950625`.

The current target relative covariance radius is **`3.1554895445 > 1`**. This is an important limitation: the finite-sample calibration theorem is valid, but the current deterministic cover is still too conservative for downstream inverse-covariance perturbation theorems that require `epsilon < 1`. Tightening that cover is the next proof target.

[Proposition 53B proof](docs/proposition_53b_irregular_tau_evalue.md) | [0.42.0 research record](docs/release_0_42.md) | [Experiment AN JSON](docs/irregular_relaxation_evalue_calibration.json) | [Experiment AN script](examples/irregular_relaxation_evalue_calibration.py) | [AN renderer](examples/render_irregular_relaxation_evalue.py) | [53B theorem tests](tests/test_irregular_relaxation_evalue.py)
"""
    text = replace_once(text, am_links, an_block, "README AN detail")
    text = replace_once(
        text,
        "- representing a single exponential temporal model by a physical relaxation time;\n",
        "- representing a single exponential temporal model by a physical relaxation time;\n"
        "- calibrating that physical relaxation time directly on irregular timestamps with finite-sample continuum coverage;\n"
        "- certifying a finite outer cover of the retained physical-time family and propagating it to an independent target grid;\n",
        "README establishes bullets",
    )
    text = replace_once(
        text,
        "| Release 0.41.1 audit | [0.41.1 Research Record](docs/release_0_41_1.md) |",
        "| Release 0.42.0 audit | [0.42.0 Research Record](docs/release_0_42.md) |\n"
        "| Previous 0.41.1 audit | [0.41.1 Research Record](docs/release_0_41_1.md) |",
        "README release links",
    )
    path.write_text(text, encoding="utf-8")


def append_supporting_docs() -> None:
    additions = {
        "docs/research_index.md": """

## Proposition 53B and Experiment AN — finite-sample physical tau calibration

Proposition 53B uses the exact irregular-grid innovation likelihood from Proposition 53A to construct a finite-sample continuum e-value confidence set for physical relaxation time `tau`. Experiment AN records the 97.5% calibration result, its certified cell-local outer cover, seconds/milliseconds invariance, and independent target composition. See [the proof](proposition_53b_irregular_tau_evalue.md), [the figure](irregular_relaxation_evalue_calibration.svg), and [the machine-readable record](irregular_relaxation_evalue_calibration.json).
""",
        "docs/reproducible_results.md": """

## Experiment AN — finite-sample irregular-time relaxation calibration

The deterministic Experiment AN script calibrates `tau = 0.78 s` from 96 independent Gaussian channels on 32 irregular timestamps. The 2001-point diagnostic accepted span is `[0.69155, 0.84455] s`; the certified 160-cell outer cover retains `[0.495625, 1.1065625] s`. Seconds-versus-milliseconds log-e-value discrepancy is at most `2.05e-12`. The independent target composition has confidence `0.950625` and target covariance relative-error radius `3.1554895445`, which is valid but above the downstream `epsilon < 1` regime. See `irregular_relaxation_evalue_calibration.json` and `irregular_relaxation_evalue_calibration.svg`.
""",
        "docs/api_temporal_calibration.md": """

## Physical-time irregular calibration API — Proposition 53B

The `observer_math.irregular_relaxation_evalue` module exposes exact irregular-time likelihood, continuum e-value evaluation, cell-local certified outer covers, and independent target-family composition. The principal public symbols are `GaussianIrregularRelaxationEValueModel`, `GaussianIrregularRelaxationEValueGrid`, `GaussianIrregularRelaxationEValueOuterCover`, `GaussianIrregularRelaxationTargetBound`, `gaussian_irregular_relaxation_evalue_model`, `gaussian_irregular_relaxation_log_evalue`, `gaussian_irregular_relaxation_evalue_grid`, `gaussian_irregular_relaxation_evalue_outer_cover`, and `gaussian_irregular_relaxation_target_matrix_chernoff_bound`. They are also exported from the package root in release 0.42.0.
""",
        "docs/assumption_ledger.md": """

## Proposition 53B calibration assumptions

The finite-sample irregular-time `tau` confidence set assumes independent calibration channels, Gaussianity, known zero mean, unit marginal variance, one common stationary exponential relaxation time, a predeclared positive `tau` interval, and a mixture numerator fixed before inspecting the calibration record. Target composition additionally assumes calibration and target records are independent and inherits Proposition 49's target covariance assumptions. The current theorem does not cover unknown calibration means, non-Gaussian innovations, multiple relaxation times, oscillatory kernels, or adaptive mixture selection from the same calibration data.
""",
    }
    for filename, addition in additions.items():
        path = Path(filename)
        if not path.exists():
            continue
        body = path.read_text(encoding="utf-8")
        if "Proposition 53B" not in body and "Experiment AN" not in body:
            path.write_text(body.rstrip() + addition, encoding="utf-8")

    changelog = Path("CHANGELOG.md")
    if changelog.exists():
        body = changelog.read_text(encoding="utf-8")
        if "## 0.42.0" not in body:
            heading_end = body.find("\n", body.find("#")) + 1
            entry = """

## 0.42.0 — 2026-09-08

- Add Proposition 53B: exact irregular-time innovation likelihood and finite-sample continuum e-value inference for physical relaxation time.
- Add cell-local certified outer covers and independent target composition through Proposition 49.
- Add Experiment AN, machine-readable results, deterministic SVG, proof record, and claim-level artifact checks.
- Report the current target covariance radius `3.1554895445 > 1` explicitly as the next tightness frontier.
"""
            body = body[:heading_end] + entry + body[heading_end:]
            changelog.write_text(body, encoding="utf-8")

    recent = Path("docs/recent_release_history.md")
    if recent.exists():
        body = recent.read_text(encoding="utf-8")
        if "0.42.0" not in body:
            body = body.rstrip() + """

## 0.42.0

Proposition 53B adds direct finite-sample inference for physical relaxation time on irregular timestamps. Experiment AN records continuum e-value calibration, a certified finite outer cover, time-unit invariance, and independent target composition. The release intentionally exposes the remaining tightness gap: target covariance radius `3.1554895445 > 1`. See [the 0.42.0 research record](release_0_42.md).
"""
            recent.write_text(body, encoding="utf-8")


if __name__ == "__main__":
    patch_public_api()
    patch_readme()
    append_supporting_docs()
