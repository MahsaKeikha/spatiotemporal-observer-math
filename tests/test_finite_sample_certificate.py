import numpy as np
from observer_math.finite_sample_certificate import (
    finite_sample_pair_certificate,first_certifying_sample_count,wishart_path_radius,
)

LOCAL=np.array([[.7,.8,.75],[.72,.78,.77],[.74,.8,.76]])
TRANS=np.array([[.8,.75],[.79,.76]])

def args():
    return dict(block_dimension=10,block_count=20,confidence=.95,
                leader_action=2.,competitor_action=1.,
                leader_local_factors=LOCAL,leader_transport_factors=TRANS,
                competitor_local_factors=LOCAL,competitor_transport_factors=TRANS,
                subset_size=3,ambient_size=7,transport_weight=.35)

def test_wishart_radius_decreases_with_sample_count():
    d1,r1=wishart_path_radius(sample_count=200,block_dimension=10,block_count=20,
        confidence=.95,local_factors=LOCAL,transport_factors=TRANS,
        subset_size=3,ambient_size=7,transport_weight=.35)
    d2,r2=wishart_path_radius(sample_count=2000,block_dimension=10,block_count=20,
        confidence=.95,local_factors=LOCAL,transport_factors=TRANS,
        subset_size=3,ambient_size=7,transport_weight=.35)
    assert d2<d1
    assert r2<=r1

def test_pair_certificate_uses_margin_minus_both_path_radii():
    x=finite_sample_pair_certificate(sample_count=5000,**args())
    assert np.isclose(x.robust_separation,x.empirical_margin-x.leader_radius-x.competitor_radius)

def test_first_certifying_sample_is_minimal_when_found():
    found=first_certifying_sample_count(minimum=100,maximum=20000,**args())
    if found is not None and found.sample_count>100:
        prev=finite_sample_pair_certificate(sample_count=found.sample_count-1,**args())
        assert not prev.certified
