from pathlib import Path

for filename in (
    "CHANGELOG.md",
    "docs/api_temporal_calibration.md",
    "docs/reproducible_results.md",
    "docs/research_index.md",
):
    path = Path(filename)
    text = path.read_text(encoding="utf-8")
    count = text.count("\u2014")
    if count != 1:
        raise RuntimeError(f"{filename}: expected exactly one em dash, found {count}")
    path.write_text(text.replace("\u2014", ":"), encoding="utf-8")
