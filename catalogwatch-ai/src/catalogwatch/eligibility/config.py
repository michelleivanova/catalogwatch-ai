"""Load eligibility window configuration."""
from __future__ import annotations

import yaml
from typing import Dict, Any


def load_windows(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    return cfg

