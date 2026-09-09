import importlib.util
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import observer_math as public_api


def test_proposition_54_public_api_and_experiment_ao_figure_are_reproducible():
    root = Path(__file__).resolve().parents[1]

    assert public_api.GaussianIrregularRelaxationSecondOrderOuterCover is not None
    assert public_api.GaussianReferenceWhitenedRelaxationTargetBound is not None
    assert callable(public_api.gaussian_irregular_relaxation_log_likelihood_second_derivative)
    assert callable(public_api.gaussian_irregular_relaxation_log_likelihood_second_derivative_bound)
    assert callable(public_api.gaussian_irregular_relaxation_second_order_outer_cover)
    assert callable(
        public_api.gaussian_reference_whitened_irregular_relaxation_target_matrix_chernoff_bound
    )

    renderer_path = root / "examples" / "render_second_order_reference_whitening.py"
    spec = importlib.util.spec_from_file_location("render_second_order_reference_whitening", renderer_path)
    assert spec is not None and spec.loader is not None
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)

    record = json.loads(
        (root / "docs" / "second_order_reference_whitening.json").read_text(encoding="utf-8")
    )
    committed_svg = (root / "docs" / "second_order_reference_whitening.svg").read_text(
        encoding="utf-8"
    )
    assert renderer.render(record) == committed_svg
    ET.fromstring(committed_svg)
