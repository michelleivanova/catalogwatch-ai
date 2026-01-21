"""Schema and basic validation for CSV ingestion."""
from typing import List


REQUIRED_COLUMNS: List[str] = [
    "catalog_id",
    "artist_name",
    "track_title",
    "release_year",
    "rights_holder",
    "territory",
    "ownership_notes",
]


def validate_columns(columns: List[str]) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
