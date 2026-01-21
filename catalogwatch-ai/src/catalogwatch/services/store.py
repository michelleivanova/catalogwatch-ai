"""Simple file-based store abstraction for Phase 1."""
from __future__ import annotations

import os
import pandas as pd
from typing import Any


def ensure_data_dir(path: str = "data/ingested") -> None:
    os.makedirs(path, exist_ok=True)


def write_parquet(df: pd.DataFrame, name: str, path: str = "data/ingested") -> str:
    ensure_data_dir(path)
    out = os.path.join(path, f"{name}.parquet")
    df.to_parquet(out, index=False)
    return out


def read_parquet(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)
