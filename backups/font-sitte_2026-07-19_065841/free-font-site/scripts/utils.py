"""Shared utilities for font catalog aggregation."""

from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = DATA_DIR / "output"

CATEGORY_MAP = {
    "sans serif": "sans-serif",
    "sans-serif": "sans-serif",
    "serif": "serif",
    "slab serif": "slab-serif",
    "slab-serif": "slab-serif",
    "monospace": "monospace",
    "display": "display",
    "handwriting": "handwriting",
    "script": "script",
    "decorative": "decorative",
    "symbol": "symbol",
    "blackletter": "display",
    "nerd font": "monospace",
}

LICENSE_COMMERCIAL_OK = {
    "ofl",
    "sil open font license",
    "sil open font license 1.1",
    "apache",
    "apache-2.0",
    "apache license 2.0",
    "apache 2.0",
    "ufl",
    "ubuntu font license",
    "mit",
    "bsd",
    "cc0",
    "public domain",
    "gpl",
    "gpl-3.0",
    "open font license",
}


def as_tag_list(tags: Any) -> list[str]:
    if tags is None:
        return []
    if isinstance(tags, list):
        return [str(t) for t in tags if t]
    if isinstance(tags, str):
        return [tags] if tags else []
    return [str(tags)]


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def normalize_category(raw: str | None) -> str:
    if not raw:
        return "other"
    key = raw.strip().lower()
    return CATEGORY_MAP.get(key, "other")


def normalize_license(raw: str | None) -> str:
    if not raw:
        return "Unknown"
    text = raw.strip()
    upper = text.upper()
    if "OFL" in upper or "OPEN FONT" in upper:
        return "OFL"
    if "APACHE" in upper:
        return "Apache-2.0"
    if "UBUNTU" in upper or upper == "UFL":
        return "UFL"
    if "MIT" in upper:
        return "MIT"
    if "CC0" in upper or "PUBLIC DOMAIN" in upper:
        return "CC0"
    if "GPL" in upper:
        return "GPL"
    return text


def is_commercial_ok(license_type: str, license_raw: str = "") -> bool:
    combined = f"{license_type} {license_raw}".lower()
    if any(bad in combined for bad in ("personal use only", "demo", "trial")):
        return False
    return any(ok in combined for ok in LICENSE_COMMERCIAL_OK)


def parse_google_variant_key(key: str) -> tuple[int, str]:
    """Parse Google Fonts variant keys like 400, 400i, regular, italic."""
    key = key.replace("regular", "400").replace("italic", "i")
    style = "italic" if key.endswith("i") else "normal"
    weight_str = key.rstrip("i")
    try:
        weight = int(weight_str)
    except ValueError:
        weight = 400
    return weight, style


def variant_label(weight: int, style: str) -> str:
    names = {100: "Thin", 200: "ExtraLight", 300: "Light", 400: "Regular",
             500: "Medium", 600: "SemiBold", 700: "Bold", 800: "ExtraBold", 900: "Black"}
    base = names.get(weight, str(weight))
    if style == "italic":
        return f"{base} Italic"
    return base


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_csv_rows(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    import csv

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
