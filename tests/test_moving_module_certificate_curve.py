import numpy as np
from examples.moving_module_certificate_curve import analytical_scores,extract,path_action

def test_analytical_factor_shapes_and_ranges():
    planted,candidates,local,lf,transport,tf=analytical_scores()
    assert local.shape==(len(planted),len(candidates))
    assert lf.shape==(*local.shape,3)
    assert tf.shape==(len(planted)-1,len(candidates),len(candidates),2)
    assert np.all((lf>=0)&(lf<=1))
    assert np.all((tf>=0)&(tf<=1))

def test_path_factor_extraction_matches_horizon():
    planted,candidates,local,lf,transport,tf=analytical_scores()
    value,ids=path_action(planted,candidates,local,transport)
    a,b=extract(ids,lf,tf)
    assert np.isfinite(value)
    assert a.shape==(len(planted),3)
    assert b.shape==(len(planted)-1,2)


def test_factor_products_reproduce_scores():
    planted,candidates,local,lf,transport,tf=analytical_scores()
    np.testing.assert_allclose(np.prod(lf,axis=2)**(1/3),local,rtol=1e-12,atol=1e-12)
    np.testing.assert_allclose(np.sqrt(np.prod(tf,axis=3)),transport,rtol=1e-12,atol=1e-12)


def test_critical_radius_pipeline_uses_analytical_factors():
    from observer_math.finite_sample_certificate import (
        critical_relative_covariance_radius,minimum_wishart_sample_count_for_radius,
        finite_sample_pair_certificate)
    planted,candidates,local,lf,transport,tf=analytical_scores()
    from examples.worldtube_active_measurement_bridge import top_two_worldtubes_dp
    leader,a1,runner,a2=top_two_worldtubes_dp(
        local,candidates,transport,transport_weight=TRANSPORT_WEIGHT,
        continuity_weight=CONTINUITY_WEIGHT)
    A1,i1=path_action(leader,candidates,local,transport)
    A2,i2=path_action(runner,candidates,local,transport)
    l1,t1=extract(i1,lf,tf); l2,t2=extract(i2,lf,tf)
    ambient=max(max(c) for c in candidates)+1; subset=len(candidates[0])
    d=critical_relative_covariance_radius(
        leader_action=A1,competitor_action=A2,leader_local_factors=l1,
        leader_transport_factors=t1,competitor_local_factors=l2,
        competitor_transport_factors=t2,subset_size=subset,ambient_size=ambient,
        transport_weight=TRANSPORT_WEIGHT)
    n=minimum_wishart_sample_count_for_radius(
        target_radius=d,block_dimension=ambient+subset,
        block_count=len(local)*len(candidates),confidence=CONFIDENCE)
    assert d>0 and n>=2
    at=finite_sample_pair_certificate(
        sample_count=n,block_dimension=ambient+subset,
        block_count=len(local)*len(candidates),confidence=CONFIDENCE,
        leader_action=A1,competitor_action=A2,leader_local_factors=l1,
        leader_transport_factors=t1,competitor_local_factors=l2,
        competitor_transport_factors=t2,subset_size=subset,ambient_size=ambient,
        transport_weight=TRANSPORT_WEIGHT)
    assert at.covariance_radius<=d
