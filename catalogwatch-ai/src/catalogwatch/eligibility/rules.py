"""Eligibility computation and explainability."""
from __future__ import annotations

from typing import Dict, Any, Optional
import datetime


def years_since_release(release_year: Optional[int], current_year: Optional[int] = None) -> Optional[int]:
    if release_year is None:
        return None
    if current_year is None:
        current_year = datetime.date.today().year
    try:
        return int(current_year) - int(release_year)
    except Exception:
        return None


def classify_years(years: Optional[int], windows: Dict[str, Any]) -> Dict[str, Any]:
    """Classify a number of years into a window based on loaded windows config.

    windows: dict loaded from `configs/eligibility_windows.yml` with key `windows`.
    Returns a dict with label and the matching rule.
    """
    if years is None:
        return {"eligibility_window": "Unknown", "matched_rule": None}

    for rule in windows.get("windows", []):
        if rule["min_years"] <= years <= rule["max_years"]:
            return {"eligibility_window": rule["name"], "matched_rule": rule}

    return {"eligibility_window": "Unmatched", "matched_rule": None}


def explain_classification(release_year: Optional[int], current_year: Optional[int], windows: Dict[str, Any]) -> Dict[str, Any]:
    yrs = years_since_release(release_year, current_year)
    classification = classify_years(yrs, windows)
    return {"release_year": release_year, "years_since_release": yrs, **classification}
