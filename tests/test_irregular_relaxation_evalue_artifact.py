import importlib.util
import json
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "examples" / "render_irregular_relaxation_evalue.py"
RECORD = ROOT / "docs" / "irregular_relaxation_evalue_calibration.json"
FIGURE = ROOT / "docs" / "irregular_relaxation_evalue_calibration.svg"


def _load_renderer():
    spec = importlib.util.spec_from_file_location("render_irregular_relaxation_evalue", RENDERER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_experiment_an_svg_is_valid_and_reproducible_from_committed_json():
    renderer = _load_renderer()
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    rendered = renderer.render(record)
    committed = FIGURE.read_text(encoding="utf-8")

    assert rendered == committed
    ET.fromstring(committed)
