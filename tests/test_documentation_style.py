from pathlib import Path


def test_documentation_avoids_en_and_em_dashes():
    """Keep repository prose consistent with the project's human writing style."""
    root = Path(__file__).resolve().parents[1]
    markdown_files = [
        root / "README.md",
        root / "CHANGELOG.md",
        root / "CONTRIBUTING.md",
        *sorted((root / "docs").rglob("*.md")),
    ]
    violations = []
    for path in markdown_files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        em_count = text.count("\u2014")
        en_count = text.count("\u2013")
        if em_count or en_count:
            violations.append(
                f"{path.relative_to(root)}: em_dash={em_count}, en_dash={en_count}"
            )

    assert not violations, (
        "Documentation must use ordinary punctuation instead of en or em dashes:\n"
        + "\n".join(violations)
    )
