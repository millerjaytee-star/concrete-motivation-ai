"""Filename-safe slug helpers."""

from __future__ import annotations

import re
import unicodedata


def slugify(value: str, max_length: int = 60) -> str:
    """Convert text into a lowercase, hyphenated, filename-safe slug."""
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if max_length > 0 and len(slug) > max_length:
        shortened = slug[:max_length].strip("-")
        if "-" in shortened:
            shortened = shortened.rsplit("-", 1)[0] or shortened
        slug = shortened
    return slug or "output"
