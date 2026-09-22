import pytest
from observer_math.data_split import (
    DataSplitLedger,add_certification_samples,add_design_samples,
    certification_sample_count,certification_effective_dof,lock_design,new_design_epoch,
)

def test_design_must_be_locked_before_certification():
    x=add_design_samples(DataSplitLedger(),20)
    with pytest.raises(ValueError):
        add_certification_samples(x,100,independent_of_design=True)

def test_independent_locked_stream_is_certifiable():
    x=lock_design(add_design_samples(DataSplitLedger(),20))
    x=add_certification_samples(x,100,independent_of_design=True)
    assert certification_sample_count(x)==100
    assert certification_effective_dof(x)==99

def test_reused_adaptive_data_fails_closed():
    x=lock_design(add_design_samples(DataSplitLedger(),20))
    x=add_certification_samples(x,100,independent_of_design=False)
    with pytest.raises(ValueError):
        certification_sample_count(x)

def test_new_design_epoch_invalidates_old_certificate_samples():
    x=lock_design(add_design_samples(DataSplitLedger(),20))
    x=add_certification_samples(x,100,independent_of_design=True)
    y=new_design_epoch(x)
    assert not y.design_locked and y.certification_samples==0
    with pytest.raises(ValueError):
        certification_sample_count(y)


def test_effective_dof_accounts_for_fitted_parameters():
    x=DataSplitLedger(design_samples=20,fitted_parameters=3)
    x=add_certification_samples(lock_design(x),100,independent_of_design=True)
    assert certification_effective_dof(x)==97
