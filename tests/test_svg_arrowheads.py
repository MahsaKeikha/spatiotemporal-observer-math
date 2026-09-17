from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SVG_NS = "{http://www.w3.org/2000/svg}"


def _marker_figures() -> list[Path]:
    return [
        path
        for path in sorted(DOCS.glob("*.svg"))
        if "<marker" in path.read_text(encoding="utf-8")
    ]


def test_reader_facing_arrowheads_use_fixed_restrained_geometry() -> None:
    figures = _marker_figures()
    assert figures, "at least one reader-facing marker figure must exist"

    for figure in figures:
        root = ET.parse(figure).getroot()
        markers = list(root.iter(f"{SVG_NS}marker"))
        assert markers, f"{figure.name} declares marker text but no SVG marker element"

        for marker in markers:
            marker_id = marker.attrib.get("id", "<unnamed>")
            assert marker.attrib.get("markerUnits") == "userSpaceOnUse", (
                f"{figure.name} marker {marker_id} must not scale with stroke width"
            )
            assert float(marker.attrib["markerWidth"]) <= 10.0, (
                f"{figure.name} marker {marker_id} is too wide"
            )
            assert float(marker.attrib["markerHeight"]) <= 10.0, (
                f"{figure.name} marker {marker_id} is too tall"
            )


def test_no_reader_facing_svg_restores_stroke_scaled_arrowheads() -> None:
    for figure in _marker_figures():
        text = figure.read_text(encoding="utf-8")
        assert 'markerUnits="strokeWidth"' not in text, figure.name
