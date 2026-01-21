"""Lightweight rule-based parser for ownership notes."""
from __future__ import annotations

import re
from typing import Dict, Any, List


KEYWORDS = {
    "reversion": [r"revert", r"reversion", r"reverted"],
    "exclusive_license": [r"exclusive license", r"exclusive rights", r"sole license", r"exclusive"],
    "artist_owned": [r"artist-owned", r"artist owned", r"artist-owned masters", r"self-released", r"self released", r"self-released"],
    "ambiguous": [r"ambiguous", r"legacy contract", r"legacy", r"disputed", r"unclear"],
}


def _find_matches(text: str, patterns: List[str]) -> List[str]:
    found: List[str] = []
    for p in patterns:
        if re.search(p, text, flags=re.IGNORECASE):
            found.append(p)
    return found


def parse_ownership_notes(text: str) -> Dict[str, Any]:
    """Extract signals from ownership notes using keyword matching.

    Returns a dict with booleans, evidence list, and a simple confidence proxy.
    """
    if not text or not isinstance(text, str):
        return {"signals": {}, "evidence": [], "confidence": 0.0}

    signals = {}
    evidence = []

    for signal, patterns in KEYWORDS.items():
        matches = _find_matches(text, patterns)
        signals[signal] = bool(matches)
        if matches:
            evidence.extend(matches)

    # small heuristic for confidence: proportion of signal categories matched
    nonzero = sum(1 for v in signals.values() if v)
    confidence = min(1.0, nonzero / max(1, len(KEYWORDS)))

    return {"signals": signals, "evidence": evidence, "confidence": confidence}
