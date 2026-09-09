import importlib.util
import json
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs" / "innovation_whitened_target_covariance.json"
SVG = ROOT / "docs" / "innovation_whitened_target_covariance.svg"
RENDERER = ROOT / "examples" / "render_innovation_whitened_target_covariance.py"


def _load_renderer():
    spec = importlib.util.spec_from_file_location("render_aq", RENDERER)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load Experiment AQ renderer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_experiment_aq_svg_is_valid_and_reproducible_from_committed_json() -> None:
    ET.parse(SVG)
    record = json.loads(DATA.read_text(encoding="utf-8"))
    rendered = _load_renderer().render(record)
    assert rendered == SVG.read_text(encoding="utf-8")
