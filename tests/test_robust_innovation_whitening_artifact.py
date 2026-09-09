import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "robust_innovation_whitened_target.json"
SVG_PATH = ROOT / "docs" / "robust_innovation_whitened_target.svg"


def _record() -> dict[str, object]:
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_experiment_ar_machine_readable_checkpoint() -> None:
    record = _record()
    calibration = record["calibration_input"]
    target = record["target_model"]
    certificate = record["uniform_target_certificate"]

    assert record["experiment"] == "AR"
    assert np.isclose(calibration["retained_lower_seconds"], 0.686875)
    assert np.isclose(calibration["retained_upper_seconds"], 0.8515625)
    assert np.isclose(target["working_relaxation_time_seconds"], 0.76921875)
    assert target["residual_degrees_of_freedom"] == 118
    assert np.isclose(target["combined_calibration_target_confidence"], 0.950625)
    assert np.isclose(certificate["covariance_relative_error"], 0.8677117534900387)
    assert certificate["crosses_relative_radius_one"] is True


def test_experiment_ar_records_the_expected_improvement() -> None:
    comparison = _record()["comparison"]

    assert comparison["proposition_55_raw_time_calibrated_radius"] > 2.0
    assert comparison["proposition_56_exact_tau_innovation_radius"] < 0.45
    assert comparison["proposition_57_uncertain_tau_innovation_radius"] < 1.0
    assert np.isclose(
        comparison["reduction_from_raw_time_calibrated_fraction"],
        0.6406812020281043,
    )


def test_experiment_ar_svg_contains_the_claim_level_labels() -> None:
    svg = SVG_PATH.read_text(encoding="utf-8")

    assert "Experiment AR" in svg
    assert "0.86771" in svg
    assert "0.950625" in svg
    assert "64.1%" in svg
    assert "Pointwise radii are diagnostics only" in svg
