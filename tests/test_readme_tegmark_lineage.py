from pathlib import Path

README = Path("README.md")


def test_readme_preserves_two_paper_tegmark_lineage() -> None:
    text = README.read_text(encoding="utf-8")

    required = (
        "Consciousness as a State of Matter",
        "10.1016/j.chaos.2015.03.014",
        "arXiv:1401.1219",
        "Improved Measures of Integrated Information",
        "10.1371/journal.pcbi.1005123",
        "arXiv:1601.02626",
        "observer-factorization question",
        "factorization choices",
        "foundational intellectual lineage",
        "candidate subsystem boundary is allowed to change through time",
        "does not present the moving world-tube framework as a restatement of Tegmark's results",
        "Nothing here should be read as attributing those later results to Tegmark",
    )
    for token in required:
        assert token in text


def test_readme_keeps_tegmark_lineage_separate_from_consciousness_claims() -> None:
    text = README.read_text(encoding="utf-8")

    assert "either cited paper establishes that a recovered world-tube is conscious" in text
    assert "resolves the physical-to-experiential problem" in text
    assert "an inferred world-tube is conscious" in text
