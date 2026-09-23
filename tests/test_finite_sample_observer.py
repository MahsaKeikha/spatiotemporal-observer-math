import numpy as np
from observer_math.finite_sample_observer import (
    finite_sample_observer_step,first_joint_certificate,sample_count_trajectory,
)
LOCAL=np.array([[.7,.8,.75],[.72,.78,.77],[.74,.8,.76]])
TRANS=np.array([[.8,.75],[.79,.76]])
KW=dict(block_dimension=10,block_count=20,confidence=.95,
        leader_action=2.,competitor_action=1.,
        leader_local_factors=LOCAL,leader_transport_factors=TRANS,
        competitor_local_factors=LOCAL,competitor_transport_factors=TRANS,
        subset_size=3,ambient_size=7,transport_weight=.35)

def test_sample_count_drives_structural_separation():
    xs=sample_count_trajectory([200,2000,20000],log_evidence=10.,
        evidence_threshold=4.,available_kl=[1.],assumptions_valid=True,
        certificate_kwargs=KW)
    assert xs[2].covariance_radius < xs[1].covariance_radius < xs[0].covariance_radius
    assert xs[2].robust_separation >= xs[1].robust_separation >= xs[0].robust_separation

def test_evidence_gate_still_blocks_structurally_certified_state():
    x=finite_sample_observer_step(sample_count=20000,log_evidence=0.,
        evidence_threshold=4.,available_kl=[1.],assumptions_valid=True,
        certificate_kwargs=KW)
    if x.certified_structurally:
        assert x.decision=="MEASURE_MORE"
        assert x.evidence_deficit>0

def test_invalid_assumptions_override_finite_sample_certificate():
    x=finite_sample_observer_step(sample_count=20000,log_evidence=10.,
        evidence_threshold=4.,available_kl=[1.],assumptions_valid=False,
        certificate_kwargs=KW)
    assert x.decision=="ABSTAIN_INVALID_ASSUMPTIONS"

def test_first_joint_certificate_is_first_certify_on_grid():
    grid=[200,500,1000,2000,5000,10000,20000]
    x=first_joint_certificate(grid,log_evidence=10.,evidence_threshold=4.,
        available_kl=[1.],assumptions_valid=True,certificate_kwargs=KW)
    if x is not None:
        earlier=[s for s in sample_count_trajectory(grid,log_evidence=10.,
            evidence_threshold=4.,available_kl=[1.],assumptions_valid=True,
            certificate_kwargs=KW) if s.sample_count<x.sample_count]
        assert all(s.decision!="CERTIFY" for s in earlier)
