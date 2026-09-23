from examples.design_policy_comparison import main


def test_bh_targeted_policy_finds_binding_block_and_beats_naive_selection(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docs").mkdir()
    result = main()
    assert result["targeted"]["block"] == "B0"
    assert result["targeted"]["required_radius"] == 0.1
    assert result["targeted"]["robust_evidence"] >= result["threshold"]
    assert result["largest_uncertainty_first"]["block"] == "B1"
    assert not result["largest_uncertainty_first"]["achieved"]
    assert result["targeted"]["normalized_effort"] < result["uniform_25_percent_radius"]["normalized_total_effort"]
