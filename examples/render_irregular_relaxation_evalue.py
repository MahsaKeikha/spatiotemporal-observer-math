"""Render the committed Experiment AN record as a deterministic SVG."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs" / "irregular_relaxation_evalue_calibration.json"
OUTPUT = ROOT / "docs" / "irregular_relaxation_evalue_calibration.svg"
WIDTH = 1440
HEIGHT = 960


def _text(x: float, y: float, value: str, size: int = 18, weight: int = 400, fill: str = "#162033") -> str:
    value = html.escape(value)
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">{value}</text>'
    )


def _rect(x: float, y: float, w: float, h: float, fill: str, stroke: str = "#d8e0ea", radius: int = 18) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    )


def _line(x1: float, y1: float, x2: float, y2: float, stroke: str, width: float = 2.0, dash: str | None = None) -> str:
    dashed = "" if dash is None else f' stroke-dasharray="{dash}"'
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{width:.1f}" stroke-linecap="round"{dashed}/>'
    )


def _circle(x: float, y: float, r: float, fill: str) -> str:
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}"/>'


def _polyline(points: list[tuple[float, float]], stroke: str, width: float = 3.0) -> str:
    encoded = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return (
        f'<polyline points="{encoded}" fill="none" stroke="{stroke}" '
        f'stroke-width="{width:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def _map(value: float, low: float, high: float, start: float, end: float) -> float:
    return start + (value - low) * (end - start) / (high - low)


def render(record: dict[str, object]) -> str:
    model = record["model"]
    continuum = record["continuum_evalue"]
    cover = record["certified_outer_cover"]
    target = record["independent_target_composition"]
    scaling = record["calibration_information_scaling"]
    units = record["time_unit_invariance"]

    true_tau = float(model["true_relaxation_time_seconds"])
    tau_low, tau_high = [float(v) for v in model["declared_interval_seconds"]]
    diagnostic_low = float(continuum["diagnostic_accepted_lower_seconds"])
    diagnostic_high = float(continuum["diagnostic_accepted_upper_seconds"])
    retained_low = float(cover["retained_lower_seconds"])
    retained_high = float(cover["retained_upper_seconds"])

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="#f7f9fc"/>',
        _text(60, 62, "Experiment AN: finite-sample calibration of physical tau on irregular time", 31, 700),
        _text(60, 98, "Exact innovation likelihood + continuum e-value + certified finite outer cover", 19, 400, "#526277"),
        _rect(60, 122, 1320, 66, "#eaf2ff", "#b9d1f6"),
        _text(88, 164, f"true tau = {true_tau:.2f} s", 24, 700, "#1d4ed8"),
        _text(310, 164, f"96 calibration channels x {int(model['calibration_sample_count'])} irregular samples", 19, 500),
        _text(870, 164, "finite-sample confidence = 97.5%", 19, 700, "#0f766e"),
    ]

    panel_w, panel_h = 635, 315
    left_x, right_x = 60, 745
    top_y, bottom_y = 220, 560

    parts.extend([
        _rect(left_x, top_y, panel_w, panel_h, "white"),
        _text(left_x + 24, top_y + 38, "A. Continuum confidence geometry in physical seconds", 21, 700),
        _text(left_x + 24, top_y + 66, "The diagnostic grid visualizes the set; the theorem is continuum-valued.", 15, 400, "#526277"),
    ])
    x0, x1, axis_y = left_x + 62, left_x + panel_w - 35, top_y + 252
    parts.append(_line(x0, axis_y, x1, axis_y, "#8da0b6", 2))
    for value in (0.4, 0.6, 0.8, 1.0, 1.2):
        x = _map(value, tau_low, tau_high, x0, x1)
        parts.extend([_line(x, axis_y - 7, x, axis_y + 7, "#8da0b6", 1.5), _text(x - 15, axis_y + 29, f"{value:.1f}", 13)])
    y_declared, y_cert, y_diag = top_y + 112, top_y + 158, top_y + 204
    for label, y in (("declared", y_declared), ("certified", y_cert), ("diagnostic", y_diag)):
        parts.append(_text(left_x + 24, y + 6, label, 14, 700))
    bar_x0 = left_x + 120
    parts.append(_rect(bar_x0, y_declared - 12, x1 - bar_x0, 22, "#edf1f6", "#c7d0dc", 6))
    cert_start, cert_end = _map(retained_low, tau_low, tau_high, x0, x1), _map(retained_high, tau_low, tau_high, x0, x1)
    diag_start, diag_end = _map(diagnostic_low, tau_low, tau_high, x0, x1), _map(diagnostic_high, tau_low, tau_high, x0, x1)
    parts.extend([
        _rect(cert_start, y_cert - 12, cert_end - cert_start, 22, "#cfe0ff", "#77a5ee", 6),
        _rect(diag_start, y_diag - 12, diag_end - diag_start, 22, "#bfe9dc", "#49a98a", 6),
    ])
    true_x = _map(true_tau, tau_low, tau_high, x0, x1)
    parts.extend([
        _line(true_x, top_y + 92, true_x, axis_y - 12, "#7c3aed", 2.5, "5 5"),
        _text(true_x + 7, top_y + 100, "true tau", 13, 700, "#7c3aed"),
        _text(left_x + 325, top_y + 301, f"visible accepted: {diagnostic_low:.5f}-{diagnostic_high:.5f} s", 13, 600, "#0f766e"),
    ])

    retained, excluded, total = int(cover["retained_cell_count"]), int(cover["excluded_cell_count"]), int(cover["cell_count"])
    parts.extend([
        _rect(right_x, top_y, panel_w, panel_h, "white"),
        _text(right_x + 24, top_y + 38, "B. Deterministic outer-cover certificate", 21, 700),
        _text(right_x + 24, top_y + 66, "A cell is removed only when its entire tau interval is provably rejected.", 15, 400, "#526277"),
    ])
    bar_left, bar_right, bar_y = right_x + 48, right_x + panel_w - 48, top_y + 128
    split = bar_left + (bar_right - bar_left) * retained / total
    parts.extend([
        _rect(bar_left, bar_y, split - bar_left, 34, "#cfe0ff", "#77a5ee", 7),
        _rect(split, bar_y, bar_right - split, 34, "#fde2dd", "#e58c79", 7),
        _text(bar_left, bar_y + 62, f"retained {retained}/{total}", 16, 700, "#1d4ed8"),
        _text(split + 10, bar_y + 62, f"excluded {excluded}/{total}", 16, 700, "#b54733"),
        _text(right_x + 48, top_y + 226, f"certified span: {retained_low:.6f}-{retained_high:.6f} s", 17, 700),
        _text(right_x + 48, top_y + 256, f"cell radius: {float(cover['cell_radius_seconds']):.8f} s", 15),
        _text(right_x + 48, top_y + 284, f"true log e-value: {float(continuum['true_tau_log_evalue']):.4f}", 15, 700, "#0f766e"),
        _text(right_x + 325, top_y + 284, f"threshold: {float(continuum['log_evalue_threshold']):.4f}", 15, 700, "#b54733"),
    ])

    parts.extend([
        _rect(left_x, bottom_y, panel_w, panel_h, "white"),
        _text(left_x + 24, bottom_y + 38, "C. More independent channels sharpen the visible likelihood set", 21, 700),
        _text(left_x + 24, bottom_y + 66, "Certified width can remain conservative because it uses worst-case cell derivatives.", 15, 400, "#526277"),
    ])
    px0, px1, py0, py1 = left_x + 72, left_x + panel_w - 34, bottom_y + 262, bottom_y + 105
    parts.extend([_line(px0, py0, px1, py0, "#8da0b6", 1.5), _line(px0, py0, px0, py1, "#8da0b6", 1.5)])
    diagnostic_points, certified_points = [], []
    for row in scaling:
        channels = int(row["channel_count"])
        diagnostic_width = float(row["diagnostic_accepted_width_seconds"])
        certified_width = float(row["certified_retained_upper_seconds"]) - float(row["certified_retained_lower_seconds"])
        x = _map(channels, 24, 192, px0, px1)
        diagnostic_points.append((x, _map(diagnostic_width, 0.0, 0.75, py0, py1)))
        certified_points.append((x, _map(certified_width, 0.0, 0.75, py0, py1)))
        parts.append(_text(x - 12, py0 + 23, str(channels), 13))
    parts.extend([_polyline(diagnostic_points, "#0f9d78", 3.5), _polyline(certified_points, "#7aa2e3", 3.0)])
    for x, y in diagnostic_points:
        parts.append(_circle(x, y, 6, "#0f9d78"))
    for x, y in certified_points:
        parts.append(_circle(x, y, 5, "#7aa2e3"))
    parts.extend([
        _text(px0 - 50, py1 + 6, "0.75", 13), _text(px0 - 50, py0 + 5, "0.00", 13),
        _text(px0 + 175, py0 + 48, "independent calibration channels", 14),
        _line(left_x + 350, bottom_y + 92, left_x + 380, bottom_y + 92, "#0f9d78", 3.5),
        _text(left_x + 388, bottom_y + 98, "diagnostic width", 13),
        _line(left_x + 350, bottom_y + 116, left_x + 380, bottom_y + 116, "#7aa2e3", 3),
        _text(left_x + 388, bottom_y + 122, "certified width", 13),
    ])

    parts.extend([
        _rect(right_x, bottom_y, panel_w, panel_h, "white"),
        _text(right_x + 24, bottom_y + 38, "D. Independent target composition: valid but not yet tight", 21, 700),
        _text(right_x + 24, bottom_y + 68, f"combined confidence = {100.0 * float(target['combined_confidence']):.4f}%", 18, 700, "#0f766e"),
        _text(right_x + 24, bottom_y + 104, f"target temporal representatives: {int(target['retained_temporal_cover_point_count'])}", 15),
        _text(right_x + 24, bottom_y + 134, f"eigenvalue cover radius: {float(target['target_eigenvalue_covering_radius']):.4f}", 15),
        _text(right_x + 24, bottom_y + 164, f"normalization cover radius: {float(target['target_normalization_covering_radius']):.4f}", 15),
        _text(right_x + 24, bottom_y + 194, f"projected degrees lower bound: {float(target['target_projected_degrees_of_freedom_lower_bound']):.2f}", 15),
        _rect(right_x + 24, bottom_y + 218, panel_w - 48, 54, "#fff3cd", "#e6b84c", 10),
        _text(right_x + 42, bottom_y + 251, f"target relative covariance radius = {float(target['target_covariance_relative_error']):.4f} > 1", 18, 700, "#8a5b00"),
        _text(right_x + 24, bottom_y + 301, f"seconds vs milliseconds max |delta log e| = {float(units['max_abs_log_evalue_error_seconds_vs_milliseconds']):.2e}", 14, 600, "#526277"),
        _text(60, 925, "Interpretation: Proposition 53B closes finite-sample irregular-time tau calibration; the next problem is tightening the certified cover enough for downstream epsilon < 1.", 16, 600, "#39485a"),
        "</svg>",
    ])
    return "\n".join(parts) + "\n"


def main() -> None:
    record = json.loads(INPUT.read_text(encoding="utf-8"))
    OUTPUT.write_text(render(record), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
