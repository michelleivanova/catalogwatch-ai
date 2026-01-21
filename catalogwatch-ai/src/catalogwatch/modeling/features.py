"""Feature engineering utilities."""
from __future__ import annotations

from typing import Dict, Any
import numpy as np


def feature_from_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Create a small feature dict from a canonical record.

    Fields produced are small and interpretable for Phase 1.
    """
    years = record.get("years_since_release")
    signals = record.get("ownership_signals", {})

    features = {
        "years_since_release": years if years is not None else -1,
        "has_reversion": 1 if signals.get("reversion") else 0,
        "has_exclusive_license": 1 if signals.get("exclusive_license") else 0,
        "artist_owned": 1 if signals.get("artist_owned") else 0,
        "ambiguous": 1 if signals.get("ambiguous") else 0,
    }

    # ownership embedding placeholder (could be large) - for now small zeros
    features["ownership_embedding"] = np.zeros(8, dtype=float)
    return features
