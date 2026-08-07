"""Concrete Motivation brand profile loading for offline personalization."""

from dataclasses import dataclass
from pathlib import Path
import re

PROFILE_PATH = Path(__file__).resolve().parent.parent / "brand" / "concrete_motivation_profile.md"


@dataclass(frozen=True, slots=True)
class BrandProfile:
    """Brand context used to personalize offline bot responses."""

    brand_name: str
    podcast_name: str
    founder: str
    voice: str
    signature_message: str
    core_themes: tuple[str, ...]
    primary_audience: tuple[str, ...]
    content_preferences: tuple[str, ...]
    avoid: tuple[str, ...]
    source_text: str


def _line_value(lines: list[str], label: str) -> str:
    prefix = f"- {label}:"
    for line in lines:
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()
    raise ValueError(f"Brand profile is missing {label}.")


def _plain_markdown(value: str) -> str:
    """Remove the small amount of inline Markdown used by the profile."""
    return re.sub(r"[*_`]", "", value).strip()


def _first_line_value(lines: list[str], *labels: str) -> str:
    """Read the first available label across legacy and master-profile schemas."""
    for label in labels:
        try:
            return _plain_markdown(_line_value(lines, label))
        except ValueError:
            continue
    joined = ", ".join(labels)
    raise ValueError(f"Brand profile is missing all supported labels: {joined}.")


def _section_items(lines: list[str], heading: str) -> tuple[str, ...]:
    items: list[str] = []
    in_section = False
    for line in lines:
        if line == f"## {heading}":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.startswith("- "):
            items.append(_plain_markdown(line.removeprefix("- ").strip()))
        elif in_section and re.match(r"^\d+\. ", line):
            items.append(_plain_markdown(re.sub(r"^\d+\. ", "", line)))
    if not items:
        raise ValueError(f"Brand profile section is empty: {heading}.")
    return tuple(items)


def _first_section(lines: list[str], *headings: str) -> tuple[str, ...]:
    for heading in headings:
        try:
            return _section_items(lines, heading)
        except ValueError:
            continue
    joined = ", ".join(headings)
    raise ValueError(f"Brand profile is missing all supported sections: {joined}.")


def _canonical_terms(items: tuple[str, ...], terms: tuple[str, ...]) -> tuple[str, ...]:
    """Expose stable vocabulary while retaining the richer source descriptions."""
    lowered = " ".join(items).lower()
    present = tuple(term for term in terms if term in lowered)
    return present + tuple(item for item in items if item.lower() not in present)


def load_brand_profile(path: Path = PROFILE_PATH) -> BrandProfile:
    """Load Concrete Motivation personalization context from Markdown."""
    source_text = path.read_text(encoding="utf-8").strip()
    if not source_text:
        raise ValueError(f"Brand profile is empty: {path}")

    lines = [line.strip() for line in source_text.splitlines()]
    core_themes = _first_section(lines, "Core Themes", "Content pillars")
    audience = _first_section(lines, "Primary Audience", "Core audience")
    preferences = _first_section(lines, "Content Preferences", "Voice")
    avoid = _first_section(lines, "Avoid", "Non-negotiables")

    # Keep stable terms used by offline generation while accepting the richer
    # master profile introduced after the original compact profile schema.
    core_themes = _canonical_terms(
        core_themes,
        ("discipline", "leadership", "faith", "family", "athletics", "business"),
    )
    audience = _canonical_terms(
        audience,
        ("parents", "students", "athletes", "workers", "leaders", "entrepreneurs"),
    )
    avoid = _canonical_terms(
        avoid,
        ("generic motivational filler", "fake testimonials", "unsupported scripture quotations"),
    )

    return BrandProfile(
        brand_name=_first_line_value(lines, "Brand name", "Parent movement and company"),
        podcast_name=_first_line_value(lines, "Podcast name", "Trust and long-form media engine"),
        founder=_first_line_value(lines, "Founder"),
        voice=_first_line_value(lines, "Voice") if any(line.startswith("- Voice:") for line in lines) else "; ".join(preferences),
        signature_message=_first_line_value(lines, "Signature message", "Master phrase"),
        core_themes=core_themes,
        primary_audience=audience,
        content_preferences=preferences,
        avoid=avoid,
        source_text=source_text,
    )
