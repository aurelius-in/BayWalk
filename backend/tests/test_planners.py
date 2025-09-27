from planners.coverage import compute_coverage
def test_coverage_stub():
    c = compute_coverage({"anchors":[]},{"coverage_pct":0.9})
    assert 0 <= c["pct"] <= 1
