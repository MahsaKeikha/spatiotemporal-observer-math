import numpy as np
from observer_math.certificate_sensitivity import burden_sensitivity,counterfactual_tightening
LOCAL=np.array([[.7,.8,.75],[.72,.78,.77],[.74,.8,.76]])
TRANS=np.array([[.8,.75],[.79,.76]])
KW=dict(covariance_relative_error=.01,leader_local_factors=LOCAL,
        leader_transport_factors=TRANS,competitor_local_factors=LOCAL,
        competitor_transport_factors=TRANS,subset_size=3,ambient_size=7,
        transport_weight=.35)

def test_burden_fractions_partition_total():
    x=burden_sensitivity(**KW)
    assert np.isclose(x.local_fraction+x.transport_fraction,1.)
    assert np.isclose(x.local_burden+x.transport_burden,x.baseline_burden)

def test_equal_fraction_tightening_gain_matches_target_burden():
    x=burden_sensitivity(**KW)
    y=counterfactual_tightening(empirical_margin=1.,tightening_fraction=.25,**KW)
    assert np.isclose(y["local_gain"],.25*x.local_burden)
    assert np.isclose(y["transport_gain"],.25*x.transport_burden)


def test_primitive_factor_pressure_partitions_pre_score_error():
    from observer_math.certificate_sensitivity import primitive_factor_pressure
    x=primitive_factor_pressure(covariance_relative_error=.01,
        leader_local_factors=LOCAL,leader_transport_factors=TRANS,
        competitor_local_factors=LOCAL,competitor_transport_factors=TRANS,
        subset_size=3,ambient_size=7)
    assert x["valid"]
    assert np.isclose(sum(x["fractions"].values()),1.)
    assert np.isclose(sum(x["pressure"].values()),x["total_primitive_pressure"])
