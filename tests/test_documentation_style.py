import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


_MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
_EXTERNAL_SCHEMES = {"http", "https", "mailto", "doi"}


def _documentation_files(root: Path) -> list[Path]:
    return [
        root / "README.md",
        root / "CHANGELOG.md",
        root / "CONTRIBUTING.md",
        *sorted((root / "docs").rglob("*.md")),
    ]


def _local_target_path(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if not target or target.startswith("#"):
        return None

    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]

    parsed = urlsplit(target)
    if parsed.scheme.lower() in _EXTERNAL_SCHEMES or parsed.netloc:
        return None

    path_text = unquote(parsed.path)
    if not path_text:
        return None

    return (source.parent / path_text).resolve()


def test_documentation_style_and_local_links():
    """Keep public prose style and repository-local navigation consistent."""
    root = Path(__file__).resolve().parents[1]
    markdown_files = _documentation_files(root)

    punctuation_violations = []
    missing_targets = []

    for path in markdown_files:
        if not path.exists():
            continue

        text = path.read_text(encoding="utf-8")
        em_count = text.count("\u2014")
        en_count = text.count("\u2013")
        if em_count or en_count:
            punctuation_violations.append(
                f"{path.relative_to(root)}: em_dash={em_count}, en_dash={en_count}"
            )

        for match in _MARKDOWN_LINK.finditer(text):
            raw_target = match.group(1)
            target_path = _local_target_path(path, raw_target)
            if target_path is None:
                continue
            if not target_path.exists():
                missing_targets.append(
                    f"{path.relative_to(root)} -> {raw_target}"
                )

    assert not punctuation_violations, (
        "Documentation must use ordinary punctuation instead of en or em dashes:\n"
        + "\n".join(punctuation_violations)
    )
    assert not missing_targets, (
        "Documentation contains missing repository-local link or image targets:\n"
        + "\n".join(missing_targets)
    )
