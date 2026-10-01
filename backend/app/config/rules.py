from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml

ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = ROOT / "config" / "rules.yaml"


def load_rules() -> List[Dict[str, Any]]:
    with RULES_PATH.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}
    return raw.get("rules", [])
