from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one occurrence, found {count}: {old!r}")
    write(path, text.replace(old, new, 1))


def append_once(path: str, marker: str, addition: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + addition.rstrip() + "\n")


# Version metadata.
replace_once("pyproject.toml", 'version = "0.43.0"', 'version = "0.44.0"')
replace_once("CITATION.cff", "version: 0.43.0", "version: 0.44.0")

# Public API imports.
replace_once(
    "src/observer_math/__init__.py",
    "from .recovery import (\n",
    "from .quadratic_relaxation_target import (\n"
    "    GaussianIrregularRelaxationQuadraticTargetBound,\n"
    "    gaussian_irregular_relaxation_quadratic_target_bound,\n"
    ")\n"
    "from .recovery import (\n",
)
replace_once(
    "src/observer_math/__init__.py",
    "    structured_residual_class_path_recovery_bound,\n)\nfrom .sampling import (\n",
    "    structured_residual_class_path_recovery_bound,\n"
    ")\n"
    "from .relaxation_curvature import (\n"
    "    GaussianIrregularRelaxationQuadraticOuterCover,\n"
    "    gaussian_irregular_relaxation_log_evalue_derivative,\n"
    "    gaussian_irregular_relaxation_log_evalue_second_derivative_bound,\n"
    "    gaussian_irregular_relaxation_quadratic_outer_cover,\n"
    ")\n"
    "from .sampling import (\n",
)
init_path = "src/observer_math/__init__.py"
init_text = read(init_path)
exports = [
    "GaussianIrregularRelaxationQuadraticOuterCover",
    "GaussianIrregularRelaxationQuadraticTargetBound",
    "gaussian_irregular_relaxation_log_evalue_derivative",
    "gaussian_irregular_relaxation_log_evalue_second_derivative_bound",
    "gaussian_irregular_relaxation_quadratic_outer_cover",
    "gaussian_irregular_relaxation_quadratic_target_bound",
]
for name in exports:
    if f'"{name}"' in init_text:
        raise RuntimeError(f"{init_path}: export already present: {name}")
closing = init_text.rfind("]\n")
if closing < 0:
    raise RuntimeError("could not find __all__ closing bracket")
insert = "".join(f'    "{name}",\n' for name in exports)
init_text = init_text[:closing] + insert + init_text[closing:]
write(init_path, init_text)

# Extend the existing artifact test without adding another test function.
artifact_path = "tests/test_quadratic_relaxation_calibration_artifact.py"
artifact = read(artifact_path)
old_artifact = "    record = json.loads(JSON_PATH.read_text(encoding=\"utf-8\"))\n    assert module.render(record) == svg_text\n"
new_artifact = (
    "    record = json.loads(JSON_PATH.read_text(encoding=\"utf-8\"))\n"
    "    assert module.render(record) == svg_text\n\n"
    "    import observer_math\n\n"
    "    assert callable(observer_math.gaussian_irregular_relaxation_quadratic_outer_cover)\n"
    "    assert callable(observer_math.gaussian_irregular_relaxation_quadratic_target_bound)\n"
)
if artifact.count(old_artifact) != 1:
    raise RuntimeError("artifact test anchor changed")
write(artifact_path, artifact.replace(old_artifact, new_artifact, 1))

# README release record.
replace_once("README.md", "version-0.43.0-2563eb", "version-0.44.0-2563eb")
replace_once("README.md", "| Research record | 0.43.0 state |", "| Research record | 0.44.0 state |")
replace_once("README.md", "| Proved statements | **54 propositions** |", "| Proved statements | **55 propositions** |")
replace_once("README.md", "| Reproducible studies | **41 experiments, A-Z and AA-AO** |", "| Reproducible studies | **42 experiments, A-Z and AA-AP** |")
replace_once("README.md", "| Scientific result figures | **29 figures** |", "| Scientific result figures | **30 figures** |")
replace_once("README.md", "| Claim-level tests | **200 tests** |", "| Claim-level tests | **206 tests** |")
replace_once("README.md", "| Research-software version | **0.43.0** |", "| Research-software version | **0.44.0** |")
replace_once("README.md", "not included in the 29 scientific-result figure count", "not included in the 30 scientific-result figure count")
replace_once("README.md", "# 5. Complete theorem roadmap, Proposition 1 to Proposition 54", "# 5. Complete theorem roadmap, Proposition 1 to Proposition 55")

# Add AP to the visible Phase IX history.
replace_once(
    "README.md",
    "[![Experiment AO: two-scale certified relaxation cover](docs/two_scale_irregular_tau_cover.svg)](docs/proposition_54_two_scale_irregular_tau_cover.md)\n\n**Proposition 54 / Experiment AO:**",
    "[![Experiment AO: two-scale certified relaxation cover](docs/two_scale_irregular_tau_cover.svg)](docs/proposition_54_two_scale_irregular_tau_cover.md)\n\n"
    "[![Experiment AP: quadratic finite-sample relaxation calibration](docs/quadratic_relaxation_calibration.svg)](docs/proposition_55_quadratic_relaxation_calibration.md)\n\n"
    "**Proposition 55 / Experiment AP:** the observed local likelihood slope and a rigorous cell-local curvature bound contract the 160-cell certified tau width from `0.61094 s` to `0.16469 s`, about `73.0%`, without spending additional probability budget. The target radius improves to `2.41488`. A known-tau oracle calculation still gives `2.16725 > 1`, showing that calibration uncertainty is no longer the dominant bottleneck on this target configuration.\n\n"
    "**Proposition 54 / Experiment AO:**",
)

# Add theorem layer G.
replace_once(
    "README.md",
    "[Proposition 54 proof](docs/proposition_54_two_scale_irregular_tau_cover.md).\n\n---\n\n# 6.",
    "[Proposition 54 proof](docs/proposition_54_two_scale_irregular_tau_cover.md).\n\n"
    "## Layer G. Local likelihood curvature, Proposition 55\n\n"
    "| Proposition | Mathematical question | Physical question |\n"
    "| ---: | --- | --- |\n"
    "| 55 | Can exact local likelihood slope and a certified second derivative replace a first-order worst case when enclosing the physical relaxation-time confidence set? | How sharply does the observed irregular calibration record constrain nearby physical timescales, and where does calibration stop being the dominant source of target uncertainty? |\n\n"
    "[Proposition 55 proof](docs/proposition_55_quadratic_relaxation_calibration.md).\n\n---\n\n# 6.",
)

# Insert a dedicated latest P55 result before the older P52 section.
replace_once(
    "README.md",
    "---\n\n# 8. Latest statistical certification result, Proposition 52 and Experiment AL",
    "---\n\n# 8. Latest calibration-curvature result, Proposition 55 and Experiment AP\n\n"
    "[![Experiment AP](docs/quadratic_relaxation_calibration.svg)](docs/proposition_55_quadratic_relaxation_calibration.md)\n\n"
    "Proposition 55 replaces the first-order calibration-cell envelope by an exact observed-data log-evalue slope plus a rigorous cell-local second-order remainder. On the Experiment AP benchmark, the certified 160-cell physical-time width contracts from `0.6109375 s` to `0.1646875 s` while preserving the same finite-sample calibration confidence.\n\n"
    "The end-to-end radius improves from `3.1554895445` in Proposition 53B and `2.5720746948` in Proposition 54 to `2.4148799294`. The most important diagnostic is the known-tau oracle radius:\n\n"
    "\\[\n"
    "\\boxed{\n"
    "\\varepsilon_{\\mathrm{oracle}}=2.167246895150515>1\n"
    "}\n"
    "\\]\n\n"
    "Thus further calibration tightening alone cannot make this target configuration enter the `epsilon < 1` perturbative regime. The next target is the covariance concentration layer itself.\n\n"
    "[Full Proposition 55 proof](docs/proposition_55_quadratic_relaxation_calibration.md) | [0.44.0 research record](docs/release_0_44.md) | [Experiment AP JSON](docs/quadratic_relaxation_calibration.json) | [Experiment AP script](examples/quadratic_relaxation_calibration.py) | [AP renderer](examples/render_quadratic_relaxation_calibration.py)\n\n"
    "---\n\n# 8. Latest statistical certification result, Proposition 52 and Experiment AL",
)

# Renumber later README sections after inserting P55.
for old, new in (
    ("# 8. Latest statistical certification result", "# 9. Latest statistical certification result"),
    ("# 9. What covariance means physically", "# 10. What covariance means physically"),
    ("# 10. Identifiability before interpretation", "# 11. Identifiability before interpretation"),
    ("# 11. What this repository establishes", "# 12. What this repository establishes"),
    ("# 12. How to read the repository", "# 13. How to read the repository"),
    ("# 13. Reproducibility standard", "# 14. Reproducibility standard"),
    ("# 13. Current frontier", "# 15. Current frontier"),
    ("# 14. Citation, bibliography, and conceptual source", "# 16. Citation, bibliography, and conceptual source"),
):
    replace_once("README.md", old, new)
replace_once("README.md", "| Propositions 44 to 53 |", "| Propositions 44 to 55 |")
replace_once(
    "README.md",
    "| Release 0.42.0 audit | [0.42.0 Research Record](docs/release_0_42.md) |",
    "| Release 0.44.0 audit | [0.44.0 Research Record](docs/release_0_44.md) |\n"
    "| Release 0.43.0 audit | [0.43.0 Research Record](docs/release_0_43.md) |\n"
    "| Release 0.42.0 audit | [0.42.0 Research Record](docs/release_0_42.md) |",
)

# Replace stale frontier with the bottleneck actually identified by P55.
readme = read("README.md")
start = readme.index("# 15. Current frontier\n")
end = readme.index("---\n\n# 16. Citation, bibliography, and conceptual source", start)
frontier = """# 15. Current frontier

Propositions 53B through 55 now separate three questions that were previously entangled: finite-sample calibration of a physical relaxation time, numerical compression of the retained temporal family, and local likelihood geometry.

Experiment AP shows that the calibration layer can now be made much tighter. At 160 cells the certified relaxation-time width contracts by about `73.0%` relative to the first-order enclosure.

The known-tau oracle calculation changes the research priority. Even when temporal-parameter uncertainty is removed completely, the current target covariance theorem gives

\\[
\\boxed{
\\varepsilon_{\\mathrm{oracle}}=2.167246895150515>1.
}
\\]

For this benchmark, additional calibration sharpening alone cannot cross the perturbative threshold one.

The immediate statistical frontier is therefore the **target covariance concentration problem** itself. Candidate directions include a sharper design-specific matrix concentration theorem, a concentration argument that exploits the exact irregular-grid innovation whitening more directly, and explicit target-information requirements showing how sample duration, timestamp geometry, block dimension, and nuisance rank control the attainable radius.

The broader physics frontiers remain model falsification beyond one exponential timescale, sensor-coordinate invariance, spatial coarse graining, and intervention-sensitive identifiability.

The guiding question remains:

> **Which inferred structures belong to the underlying dynamical organization, and which are artifacts of measurement representation or insufficient information?**

That question remains separate from any claim about consciousness.

"""
write("README.md", readme[:start] + frontier + readme[end:])

# Research overview current record and a new P54-P55 section.
replace_once(
    "docs/research_overview.md",
    "The 0.41.0 research record contains 53 propositions, 39 reproducible experiments, 26 scientific result figures, and 183 claim-level tests.",
    "The 0.44.0 research record targets 55 propositions, 42 reproducible experiments, 30 scientific result figures, and 206 claim-level tests. These counts become verified after the exact release candidate is merged and the resulting `main` workflow succeeds.",
)
replace_once(
    "docs/research_overview.md",
    "---\n\n# What the project now establishes",
    "## Propositions 54 and 55: separate calibration resolution, then use local curvature\n\n"
    "[![Experiment AO](two_scale_irregular_tau_cover.svg)](proposition_54_two_scale_irregular_tau_cover.md)\n\n"
    "[![Experiment AP](quadratic_relaxation_calibration.svg)](proposition_55_quadratic_relaxation_calibration.md)\n\n"
    "Proposition 54 separates the fine grid needed to certify the continuum calibration set from the smaller target covariance cover. Proposition 55 then uses the exact observed-data e-value slope and a rigorous local curvature bound to tighten the calibration enclosure itself.\n\n"
    "At 160 calibration cells, the certified physical-time width falls from `0.6109375 s` to `0.1646875 s`. The target covariance radius improves to `2.4148799294`.\n\n"
    "The known-tau oracle radius is still `2.1672468952 > 1`. This identifies the next bottleneck: target covariance concentration rather than calibration uncertainty.\n\n"
    "---\n\n# What the project now establishes",
)
append_once(
    "docs/research_overview.md",
    "Proposition 55 oracle bottleneck",
    "## Proposition 55 oracle bottleneck\n\n"
    "Experiment AP includes a known-tau diagnostic that removes temporal calibration uncertainty completely. The current target concentration theorem still gives relative radius `2.1672468952 > 1`. This is a negative but actionable result: further calibration refinement alone cannot solve this target benchmark. The next theorem should attack the target concentration layer or derive explicit information requirements for entering the `epsilon < 1` regime.",
)

# Research index: fix stale headline and append P55 navigation.
index_path = "docs/research_index.md"
index = read(index_path)
for old, new in (
    ("| Propositions | **53** |", "| Propositions | **55** |"),
    ("| Reproducible experiments | **39, A-Z and AA-AM** |", "| Reproducible experiments | **42, A-Z and AA-AP** |"),
    ("| Scientific result figures | **27** |", "| Scientific result figures | **30** |"),
    ("| Claim-level tests | **188** |", "| Claim-level tests | **206** |"),
    ("| Research-software version | **0.41.1** |", "| Research-software version | **0.44.0** |"),
):
    if index.count(old) != 1:
        raise RuntimeError(f"research index anchor changed: {old}")
    index = index.replace(old, new, 1)
write(index_path, index)
append_once(
    index_path,
    "## Proposition 55 and Experiment AP",
    "## Proposition 55 and Experiment AP\n\n"
    "**Mathematical question.** Can exact local slope and certified likelihood curvature replace a first-order worst case when enclosing the Proposition 53B continuum confidence set?\n\n"
    "**Physical question.** How sharply does the observed irregular calibration record constrain nearby physical relaxation times, and when does calibration stop being the dominant source of uncertainty?\n\n"
    "At 160 calibration cells, the first-order width `0.6109375 s` contracts to `0.1646875 s`. The target covariance radius improves to `2.4148799294`, while the known-tau oracle radius remains `2.1672468952 > 1`.\n\n"
    "[Proof](proposition_55_quadratic_relaxation_calibration.md) | [Figure](quadratic_relaxation_calibration.svg) | [JSON](quadratic_relaxation_calibration.json) | [Release record](release_0_44.md)",
)

# API documentation.
append_once(
    "docs/api_temporal_calibration.md",
    "## Proposition 55: quadratic relaxation calibration",
    "## Proposition 55: quadratic relaxation calibration\n\n"
    "Public package-root imports:\n\n"
    "```python\n"
    "from observer_math import (\n"
    "    GaussianIrregularRelaxationQuadraticOuterCover,\n"
    "    GaussianIrregularRelaxationQuadraticTargetBound,\n"
    "    gaussian_irregular_relaxation_log_evalue_derivative,\n"
    "    gaussian_irregular_relaxation_log_evalue_second_derivative_bound,\n"
    "    gaussian_irregular_relaxation_quadratic_outer_cover,\n"
    "    gaussian_irregular_relaxation_quadratic_target_bound,\n"
    ")\n"
    "```\n\n"
    "The quadratic outer cover is a deterministic enclosure of the already valid Proposition 53B continuum e-value set. It uses the exact observed-data derivative at each cell center and a rigorous cell-local second-derivative bound. It does not consume an additional probability budget.\n\n"
    "The quadratic target helper composes the retained interval with the existing target covariance machinery. Experiment AP shows that this improves the target radius but does not remove the known-tau oracle floor of the current concentration theorem.",
)

# Assumption ledger.
append_once(
    "docs/assumption_ledger.md",
    "## Proposition 55: quadratic physical-time calibration",
    "## Proposition 55: quadratic physical-time calibration\n\n"
    "**Assumptions.** The Proposition 53B calibration model remains in force: independent standardized Gaussian calibration channels, one stationary exponential physical relaxation time, strictly increasing timestamps, a mixture density fixed before calibration observations, and a declared finite relaxation-time interval. The target composition additionally requires an independent target record, fixed declared target timestamps, and a fixed nuisance design.\n\n"
    "**What the curvature theorem certifies.** The analytic first derivative and deterministic second-derivative bound give a valid quadratic lower enclosure of the observed continuum log e-value on every calibration cell. A cell is excluded only when the complete cell is proved rejected.\n\n"
    "**Failure modes.** Multi-timescale relaxation, oscillation, nonstationarity, heavy-tailed innovations, dependent calibration channels, or calibration-target mismatch can invalidate the physical model even when the mathematical cell certificate is computed correctly.\n\n"
    "**Oracle diagnostic.** The known-tau target calculation is not an implementable inference procedure. It is used only to identify whether temporal-parameter uncertainty is still the dominant source of the target theorem radius.",
)

# Figure guide, inserted before the generic future-figure checklist.
replace_once(
    "docs/figure_reading_guide.md",
    "---\n\n# How to read any future figure",
    "---\n\n# Proposition 55, Experiment AP\n\n"
    "Figure: `quadratic_relaxation_calibration.svg`\n\n"
    "**Panel A** compares certified physical-time width under the first-order and quadratic calibration enclosures. The shrinking orange curve means the deterministic representation of the same finite-sample confidence set is tighter. It does not mean the physical process changed.\n\n"
    "**Panel B** shows the declared interval, the first-order retained interval, the quadratic retained interval, and the controlled true relaxation time. The interval is a confidence enclosure for a model parameter measured in seconds.\n\n"
    "**Panel C** compares downstream target covariance theorem radii. The line at one is a mathematical perturbation threshold, not a physical phase transition.\n\n"
    "**Panel D** highlights the key negative diagnostic: even exact knowledge of tau leaves the current target theorem at radius about `2.167`. Therefore calibration uncertainty is no longer the dominant bottleneck on this benchmark.\n\n"
    "The figure does not measure energy, consciousness, integration, or physical organization directly.\n\n"
    "---\n\n# How to read any future figure",
)

# Release history and changelog.
replace_once(
    "docs/recent_release_history.md",
    "## 0.43.0\n",
    "## 0.44.0\n\n"
    "Proposition 55 / Experiment AP replaces the first-order calibration enclosure by an exact local log-evalue slope plus a rigorous cell-local curvature certificate. At 160 cells the certified tau width contracts by about `73.0%`, and the target radius improves to `2.41488`. A known-tau oracle radius of `2.16725 > 1` shows that target covariance concentration, not calibration uncertainty, is now the dominant bottleneck. See [release record](release_0_44.md).\n\n"
    "## 0.43.0\n",
)
changelog = read("CHANGELOG.md")
marker = "# Changelog\n"
if marker not in changelog:
    raise RuntimeError("CHANGELOG heading missing")
entry = (
    "# Changelog\n\n"
    "## 0.44.0\n\n"
    "- Added Proposition 55, a quadratic finite-sample outer cover for irregular-time physical relaxation calibration using exact local log-evalue slope and a rigorous cell-local curvature bound.\n"
    "- Added Experiment AP and a deterministic visible SVG comparing first-order versus quadratic calibration, the target-radius ladder, and the known-tau oracle floor.\n"
    "- Added a known-tau diagnostic showing the current target concentration theorem remains at relative radius `2.1672468952 > 1`, so calibration refinement alone cannot close this benchmark.\n"
    "- Added public API exports, proof documentation, assumptions, figure interpretation, machine-readable results, and exact figure reproducibility testing.\n"
    "- Updated the intended release record to 55 propositions, 42 experiments, 30 scientific-result figures, and 206 claim-level tests.\n"
)
if "## 0.44.0" in changelog:
    raise RuntimeError("0.44.0 already present in changelog")
write("CHANGELOG.md", changelog.replace(marker, entry, 1))
