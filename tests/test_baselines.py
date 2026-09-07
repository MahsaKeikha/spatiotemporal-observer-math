import numpy as np

from observer_math import best_fixed_boundary, independent_local_path


def test_local_and_fixed_baselines_answer_different_questions():
    candidates = ((0,), (1,))
    local = np.array([[0.9, 0.1], [0.2, 0.8], [0.7, 0.3]])

    local_path = independent_local_path(local, candidates)
    fixed_path = best_fixed_boundary(local, candidates)

    assert local_path.candidate_indices == (0, 1, 0)
    assert fixed_path.candidate_indices == (0, 0, 0)
