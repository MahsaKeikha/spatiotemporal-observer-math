import re
import xml.etree.ElementTree as ET
from pathlib import Path


SVG_NS = {"svg": "http://www.w3.org/2000/svg"}
FONT_SIZE = {
    "box-title": 22.0,
    "body": 17.0,
    "math": 19.0,
}
HORIZONTAL_PADDING = 24.0
VERTICAL_PADDING = 28.0
ARROWHEAD_GAP = 12.0
WIDTH_FACTOR = 0.62


def _number(value: str) -> float:
    return float(value)


def _block_geometry(group: ET.Element) -> tuple[float, float, float, float]:
    return (
        _number(group.attrib["data-x"]),
        _number(group.attrib["data-y"]),
        _number(group.attrib["data-width"]),
        _number(group.attrib["data-height"]),
    )


def _estimated_text_width(text: str, font_size: float) -> float:
    return len(text) * font_size * WIDTH_FACTOR


def test_recoverable_geometry_text_stays_inside_declared_blocks():
    root = Path(__file__).resolve().parents[1]
    figure = root / "docs" / "recoverable_geometry_pipeline.svg"
    svg = ET.parse(figure).getroot()

    blocks = svg.findall(".//svg:g[@data-qa-block='true']", SVG_NS)
    assert len(blocks) == 5

    for block in blocks:
        x, y, width, height = _block_geometry(block)
        rect = block.find("svg:rect", SVG_NS)
        assert rect is not None
        assert _number(rect.attrib["x"]) == x
        assert _number(rect.attrib["y"]) == y
        assert _number(rect.attrib["width"]) == width
        assert _number(rect.attrib["height"]) == height

        texts = block.findall("svg:text", SVG_NS)
        assert texts
        for label in texts:
            label_text = "".join(label.itertext()).strip()
            label_x = _number(label.attrib["x"])
            label_y = _number(label.attrib["y"])
            css_class = label.attrib.get("class", "")
            assert css_class in FONT_SIZE
            assert label.attrib.get("text-anchor") == "middle"

            safe_width = width - 2.0 * HORIZONTAL_PADDING
            estimated_width = _estimated_text_width(
                label_text,
                FONT_SIZE[css_class],
            )
            assert estimated_width <= safe_width, (
                f"{block.attrib['id']} text may overflow horizontally: "
                f"{label_text!r}"
            )
            assert x + HORIZONTAL_PADDING <= label_x <= x + width - HORIZONTAL_PADDING
            assert y + VERTICAL_PADDING <= label_y <= y + height - VERTICAL_PADDING


def test_recoverable_geometry_connectors_attach_to_block_boundaries():
    root = Path(__file__).resolve().parents[1]
    figure = root / "docs" / "recoverable_geometry_pipeline.svg"
    svg = ET.parse(figure).getroot()

    blocks = {
        block.attrib["id"]: _block_geometry(block)
        for block in svg.findall(".//svg:g[@data-qa-block='true']", SVG_NS)
    }
    connectors = svg.findall(".//svg:path[@data-from][@data-to]", SVG_NS)
    assert len(connectors) == 4

    path_pattern = re.compile(
        r"^M(?P<x1>[0-9.]+) (?P<y1>[0-9.]+) H(?P<x2>[0-9.]+)$"
    )
    for connector in connectors:
        source = blocks[connector.attrib["data-from"]]
        target = blocks[connector.attrib["data-to"]]
        match = path_pattern.fullmatch(connector.attrib["d"])
        assert match is not None

        x1 = _number(match.group("x1"))
        y1 = _number(match.group("y1"))
        x2 = _number(match.group("x2"))
        source_x, source_y, source_width, source_height = source
        target_x, target_y, _, target_height = target

        assert x1 == source_x + source_width
        assert y1 == source_y + source_height / 2.0
        assert y1 == target_y + target_height / 2.0
        assert x2 == target_x - ARROWHEAD_GAP
        assert x2 > x1


def test_recoverable_geometry_figure_uses_no_forbidden_dash_characters():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "recoverable_geometry_pipeline.svg").read_text(
        encoding="utf-8"
    )
    assert "\u2013" not in text
    assert "\u2014" not in text
