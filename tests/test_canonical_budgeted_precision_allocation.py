from examples.canonical_budgeted_precision_allocation import block_id


def test_bj_block_ids_are_stable_and_auditable():
    assert block_id(2, 34) == "t2:c34"
