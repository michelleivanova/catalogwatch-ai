from catalogwatch.eligibility.rules import years_since_release, classify_years, explain_classification
from catalogwatch.eligibility.config import load_windows


def test_years_and_windows():
    windows = load_windows("configs/eligibility_windows.yml")

    assert years_since_release(2000, current_year=2025) == 25
    res = classify_years(25, windows)
    assert res["eligibility_window"] == "Early Watch"

    assert classify_years(31, windows)["eligibility_window"] == "Mid Window"
    assert classify_years(36, windows)["eligibility_window"] == "Imminent"
    assert classify_years(40, windows)["eligibility_window"] == "Post Eligibility"

    # explain returns years and window
    expl = explain_classification(1995, 2025, windows)
    assert expl["years_since_release"] == 30
    assert expl["eligibility_window"] == "Early Watch"
