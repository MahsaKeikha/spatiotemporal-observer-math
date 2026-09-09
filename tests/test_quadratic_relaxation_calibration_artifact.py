import importlib.util
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "quadratic_relaxation_calibration.json"
SVG_PATH = ROOT / "docs" / "quadratic_relaxation_calibration.svg"
RENDERER_PATH = ROOT / "examples" / "render_quadratic_relaxation_calibration.py"


def test_experiment_ap_svg_is_valid_and_reproducible():
    svg_text = SVG_PATH.read_text(encoding="utf-8")
    root = ET.fromstring(svg_text)
    assert root.tag.endswith("svg")

    spec = importlib.util.spec_from_file_location("render_experiment_ap", RENDERER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    record = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert module.render(record) == svg_text

    import observer_math

    assert callable(observer_math.gaussian_irregular_relaxation_quadratic_outer_cover)
    assert callable(observer_math.gaussian_irregular_relaxation_quadratic_target_bound)
