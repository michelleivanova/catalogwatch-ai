"""Explainability helpers for Phase 1 deterministic scoring.

Provides per-feature contribution breakdown consistent with `scoring.simple_score`.
"""
from __future__ import annotations

from typing import Dict, Any


WEIGHTS = {
    "eligibility": 0.6,
    "ownership_clarity": 0.3,
    "exclusive_penalty": 0.1,
}


def compute_contributions(features: Dict[str, Any]) -> Dict[str, float]:
    """Compute per-feature contributions and total score.

    This mirrors the logic in `scoring.simple_score` to keep explanations aligned.
    Returns a dict with per-component contributions and a `total` field.
    """
    years = features.get("years_since_release", -1)
    if years < 0:
        eligibility = 0.0
    else:
        eligibility = min(1.0, years / 40.0)

    ownership_clarity = 1.0
    if features.get("ambiguous"):
        ownership_clarity -= 0.5
    if features.get("artist_owned"):
        ownership_clarity += 0.2

    exclusive_penalty = -0.2 if features.get("has_exclusive_license") else 0.0

    contrib_elig = WEIGHTS["eligibility"] * eligibility
    contrib_owner = WEIGHTS["ownership_clarity"] * ownership_clarity
    contrib_excl = WEIGHTS["exclusive_penalty"] * exclusive_penalty

    total = contrib_elig + contrib_owner + contrib_excl
    total = max(0.0, min(1.0, total))

    return {
        "eligibility_value": eligibility,
        "eligibility_contribution": contrib_elig,
        "ownership_clarity_value": ownership_clarity,
        "ownership_contribution": contrib_owner,
        "exclusive_penalty_value": exclusive_penalty,
        "exclusive_contribution": contrib_excl,
        "total": total,
    }
