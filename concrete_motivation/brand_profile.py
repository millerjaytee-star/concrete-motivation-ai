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


def _first_line_value(lines: list[str], *labels: str) -> str:
    for label in labels:
        try:
            return _clean_markdown(_line_value(lines, label))
        except ValueError:
            continue
    raise ValueError(f"Brand profile is missing all supported labels: {', '.join(labels)}.")


def _clean_markdown(value: str) -> str:
    return value.replace("**", "").strip()


def _section_items(lines: list[str], heading: str) -> tuple[str, ...]:
    items: list[str] = []
    in_section = False
    for line in lines:
        if line == f"## {heading}":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            match = re.match(r"(?:- |\d+\. )(.*)", line)
            if match:
                items.append(_clean_markdown(match.group(1)))
    if not items:
        raise ValueError(f"Brand profile section is empty: {heading}.")
    return tuple(items)


def _first_section(lines: list[str], *headings: str) -> tuple[str, ...]:
    for heading in headings:
        try:
            return _section_items(lines, heading)
        except ValueError:
            continue
    raise ValueError(f"Brand profile is missing all supported sections: {', '.join(headings)}.")


def load_brand_profile(path: Path = PROFILE_PATH) -> BrandProfile:
    """Load Concrete Motivation personalization context from Markdown."""
    source_text = path.read_text(encoding="utf-8").strip()
    if not source_text:
        raise ValueError(f"Brand profile is empty: {path}")

    lines = [line.strip() for line in source_text.splitlines()]
    return BrandProfile(
        brand_name=_first_line_value(lines, "Brand name", "Parent movement and company"),
        podcast_name=_first_line_value(lines, "Podcast name", "Trust and long-form media engine"),
        founder=_first_line_value(lines, "Founder"),
        voice="; ".join(_first_section(lines, "Voice")),
        signature_message=_first_line_value(lines, "Signature message", "Master phrase"),
        core_themes=_first_section(lines, "Core Themes", "Content pillars"),
        primary_audience=_first_section(lines, "Primary Audience", "Core audience"),
        content_preferences=_first_section(lines, "Content Preferences", "Language patterns"),
        avoid=_first_section(lines, "Avoid", "Non-negotiables"),
        source_text=source_text,
    )
