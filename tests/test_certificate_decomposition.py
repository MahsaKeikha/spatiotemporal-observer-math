import numpy as np
from observer_math.certificate_decomposition import (
    pair_certificate_decomposition,path_radius_decomposition)
from observer_math.active_measurement import complete_path_radius_from_relative_covariance
LOCAL=np.array([[.7,.8,.75],[.72,.78,.77],[.74,.8,.76]])
TRANS=np.array([[.8,.75],[.79,.76]])

def test_decomposition_reconstructs_complete_path_radius():
    d=.01
    x=path_radius_decomposition(covariance_relative_error=d,local_factors=LOCAL,
        transport_factors=TRANS,subset_size=3,ambient_size=7,transport_weight=.35)
    direct=complete_path_radius_from_relative_covariance(
        np.full(3,d),np.full(2,d),LOCAL,TRANS,
        subset_size=3,ambient_size=7,transport_weight=.35)
    assert np.isclose(x["local_total"]+x["transport_weighted_total"],direct)

def test_pair_total_is_sum_of_local_and_transport_burdens():
    x=pair_certificate_decomposition(covariance_relative_error=.01,
        leader_local_factors=LOCAL,leader_transport_factors=TRANS,
        competitor_local_factors=LOCAL,competitor_transport_factors=TRANS,
        subset_size=3,ambient_size=7,transport_weight=.35)
    assert np.isclose(x["pair_total_burden"],
                      x["pair_local_burden"]+x["pair_transport_burden"])
    assert all(v>=0 for side in ("leader","competitor")
               for v in x[side]["factor_error_sums"].values())
