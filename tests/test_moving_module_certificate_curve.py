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
