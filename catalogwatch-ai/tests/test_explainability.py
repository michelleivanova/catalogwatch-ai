from catalogwatch.modeling.features import feature_from_record
from catalogwatch.modeling.explainability import compute_contributions


def test_explainability_contributions():
    # craft a record with known fields
    record = {
        "years_since_release": 30,
        "ownership_signals": {"reversion": True, "exclusive_license": False, "artist_owned": False, "ambiguous": False},
    }
    feats = feature_from_record(record)
    expl = compute_contributions(feats)

    # Eligibility: years 30 -> eligibility value = 30/40 = 0.75
    assert abs(expl["eligibility_value"] - 0.75) < 1e-6
    # total should be between 0 and 1
    assert 0.0 <= expl["total"] <= 1.0
