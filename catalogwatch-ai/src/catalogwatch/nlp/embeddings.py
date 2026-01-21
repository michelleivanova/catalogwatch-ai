"""Embeddings placeholder and interface.

Phase 1: returns a zero vector. Interface is ready to be swapped with a real model.
"""
from __future__ import annotations

import numpy as np
from typing import Iterable


def text_to_vector(text: str, dim: int = 384) -> np.ndarray:
    """Return a placeholder vector for `text`. Replace with model inference later."""
    return np.zeros(dim, dtype=float)


def batch_text_to_vectors(texts: Iterable[str], dim: int = 384):
    return np.vstack([text_to_vector(t, dim=dim) for t in texts])
