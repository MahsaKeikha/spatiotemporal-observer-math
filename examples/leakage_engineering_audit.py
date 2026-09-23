"""Experiment AU: engineering leakage-dimension design audit."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.leakage_geometry import leakage_measurement_geometry

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "leakage_engineering_audit.json"


def _log_mgf(d: int, x: np.ndarray, *, upper: bool) -> np.ndarray:
    if upper:
        log_chi, sign = -0.5*d*np.log1p(-2*x), -x
    else:
        log_chi, sign = -0.5*d*np.log1p(2*x), x
    bracket = log_chi if d == 1 else np.logaddexp(np.log(float(d-1)), log_chi)-np.log(float(d))
    return sign + bracket


def radius(d: int, blocks: int, r: int, confidence: float = 0.975, grid: int = 1024) -> float:
    lp = float(np.log(2.0*blocks*d/(1.0-confidence)))
    xu=np.geomspace(1e-8,0.499999,grid)
    xl=np.geomspace(1e-8,1e3,grid)
    u=(lp+r*_log_mgf(d,xu,upper=True))/xu/r
    l=(lp+r*_log_mgf(d,xl,upper=False))/xl/r
    return float(max(np.min(u), min(1.0,float(np.min(l)))))


def entry(d: int, blocks: int) -> int:
    lo, hi=2,4
    while radius(d,blocks,hi)>=1.0: hi*=2
    while lo<hi:
        mid=(lo+hi)//2
        if radius(d,blocks,mid)<1.0: hi=mid
        else: lo=mid+1
    return lo


def build_record() -> dict[str, object]:
    n,s,blocks,r=7,3,175,118
    rows=[]
    for retained in range(n-s+1):
        g=leakage_measurement_geometry(n,s,screened_environment_size=retained)
        d=g.screened_block_dimension
        rows.append({
            "retained_environment_coordinates": retained,
            "covariance_dimension": d,
            "radius_at_118_residual_degrees": radius(d,blocks,r),
            "first_residual_degrees_below_one": entry(d,blocks),
            "exact_without_additional_structure": retained == n-s,
        })
    return {
        "experiment":"AU",
        "title":"Engineering leakage-dimension design audit",
        "benchmark":{"node_count":n,"subset_size":s,"environment_size":n-s,"simultaneous_blocks":blocks,"residual_degrees":r},
        "design_sweep":rows,
        "interpretation":"Rows with fewer than four retained environment coordinates are engineering what-if designs, not valid replacements for the original leakage quantity unless an independently justified conditional-screening certificate makes the omitted coordinates irrelevant.",
    }


def main() -> None:
    record=build_record()
    OUTPUT.write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(record,indent=2))


if __name__=="__main__":
    main()
