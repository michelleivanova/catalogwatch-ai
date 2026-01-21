"""CSV ingestion utilities."""
from __future__ import annotations

import datetime
import pandas as pd
from typing import Dict, Any

from catalogwatch.ingest.schema import validate_columns


def load_csv(path: str) -> pd.DataFrame:
    """Load CSV and validate required columns.

    Args:
        path: path to CSV file

    Returns:
        DataFrame with raw columns
    """
    df = pd.read_csv(path)
    validate_columns(list(df.columns))
    return df


def canonicalize(df: pd.DataFrame, source: str = "csv") -> pd.DataFrame:
    """Return canonical form with ingestion metadata and normalized types.

    Adds `ingestion_metadata` column and ensures `release_year` is int when possible.
    """
    df = df.copy()
    # normalize release_year
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce").astype("Int64")
    df["ingestion_metadata"] = df.apply(
        lambda row: {"source": source, "loaded_at": datetime.datetime.utcnow().isoformat()}, axis=1
    )
    return df
