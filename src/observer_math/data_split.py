"""Independent design/certification split for adaptive measurement.

Adaptive actions may be selected from a design stream. A fixed-design Wishart
certificate is emitted only from a separately designated certification stream.
This module records that separation explicitly; it does not claim validity for
adaptively reused certification observations.
"""
from __future__ import annotations
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class DataSplitLedger:
    design_samples: int=0
    certification_samples: int=0
    design_locked: bool=False
    certification_independent: bool=True

    def __post_init__(self):
        if self.design_samples<0 or self.certification_samples<0:
            raise ValueError("sample counts must be nonnegative")

def add_design_samples(x:DataSplitLedger,count:int)->DataSplitLedger:
    if count<=0: raise ValueError("count must be positive")
    if x.design_locked:
        raise ValueError("design is locked; start a new design epoch to adapt again")
    return replace(x,design_samples=x.design_samples+count)

def lock_design(x:DataSplitLedger)->DataSplitLedger:
    return replace(x,design_locked=True)

def add_certification_samples(x:DataSplitLedger,count:int,*,independent_of_design:bool
                              )->DataSplitLedger:
    if count<=0: raise ValueError("count must be positive")
    if not x.design_locked:
        raise ValueError("lock the measurement design before certification sampling")
    return replace(x,certification_samples=x.certification_samples+count,
                   certification_independent=(
                       x.certification_independent and bool(independent_of_design)))

def certification_sample_count(x:DataSplitLedger)->int:
    if not x.design_locked or not x.certification_independent:
        raise ValueError("fixed-design certificate requires a locked design and independent certification stream")
    if x.certification_samples<2:
        raise ValueError("at least two certification samples are required")
    return x.certification_samples

def new_design_epoch(x:DataSplitLedger)->DataSplitLedger:
    """Changing design invalidates the fixed-design certification stream."""
    return DataSplitLedger(design_samples=x.design_samples,
                           certification_samples=0,
                           design_locked=False,
                           certification_independent=True)
