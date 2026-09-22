"""Independent design/certification provenance for adaptive measurement.

The ledger records a caller-declared provenance assertion; it does not prove
statistical independence. Certification is parameterized by effective
innovation degrees of freedom r=N-q, not raw observation count.
"""
from __future__ import annotations
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class DataSplitLedger:
    design_samples: int=0
    certification_samples: int=0
    fitted_parameters: int=1
    design_locked: bool=False
    certification_independent: bool=True
    provenance_asserted: bool=False
    def __post_init__(self):
        if self.design_samples<0 or self.certification_samples<0 or self.fitted_parameters<0:
            raise ValueError("counts must be nonnegative")

def add_design_samples(x:DataSplitLedger,count:int)->DataSplitLedger:
    if count<=0: raise ValueError("count must be positive")
    if x.design_locked: raise ValueError("design is locked; start a new design epoch to adapt again")
    return replace(x,design_samples=x.design_samples+count)

def lock_design(x:DataSplitLedger)->DataSplitLedger:
    return replace(x,design_locked=True)

def add_certification_samples(x:DataSplitLedger,count:int,*,independent_of_design:bool
                              )->DataSplitLedger:
    if count<=0: raise ValueError("count must be positive")
    if not x.design_locked: raise ValueError("lock the measurement design before certification sampling")
    asserted=bool(independent_of_design)
    return replace(x,certification_samples=x.certification_samples+count,
        certification_independent=x.certification_independent and asserted,
        provenance_asserted=x.provenance_asserted or asserted)

def certification_effective_dof(x:DataSplitLedger)->int:
    if not x.design_locked or not x.certification_independent or not x.provenance_asserted:
        raise ValueError("certificate requires locked design and asserted independent certification provenance")
    r=x.certification_samples-x.fitted_parameters
    if r<2: raise ValueError("effective certification degrees of freedom must be at least two")
    return r

def certification_sample_count(x:DataSplitLedger)->int:
    """Backward-compatible raw count accessor after validating provenance."""
    certification_effective_dof(x)
    return x.certification_samples

def new_design_epoch(x:DataSplitLedger)->DataSplitLedger:
    return DataSplitLedger(design_samples=x.design_samples,
        certification_samples=0,fitted_parameters=x.fitted_parameters,
        design_locked=False,certification_independent=True,provenance_asserted=False)
