"""Scoring and a neural-ready scaffold."""
from __future__ import annotations

from typing import Dict, Any
import numpy as np


def simple_score(features: Dict[str, Any]) -> float:
    """Deterministic composite score (0..1) for Phase 1 demo.

    Weights are illustrative and fixed; later this becomes a trainable model.
    """
    years = features.get("years_since_release", -1)
    # eligibility proximity: map years to [0,1] with a soft cap
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

    score = 0.6 * eligibility + 0.3 * ownership_clarity + 0.1 * exclusive_penalty
    # clamp
    return float(max(0.0, min(1.0, score)))


class NNScorer:
    """Placeholder NN scorer with fit/predict API. Not implemented for Phase 1.

    This class provides a simple API that's easy to replace with a PyTorch/Keras model.
    """

    def __init__(self):
        self.is_trained = False

    def fit(self, X, y):
        # no-op for Phase 1; would train a small feed-forward net later
        self.is_trained = True

    def predict(self, X):
        # Accepts array-like features and returns placeholder scores
        return [0.0 for _ in range(len(X))]
