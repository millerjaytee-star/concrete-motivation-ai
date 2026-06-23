"""Concrete Motivation brand profile loading for offline personalization."""

from dataclasses import dataclass
from pathlib import Path

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
            items.append(line.removeprefix("- ").strip())
    if not items:
        raise ValueError(f"Brand profile section is empty: {heading}.")
    return tuple(items)


def load_brand_profile(path: Path = PROFILE_PATH) -> BrandProfile:
    """Load Concrete Motivation personalization context from Markdown."""
    source_text = path.read_text(encoding="utf-8").strip()
    if not source_text:
        raise ValueError(f"Brand profile is empty: {path}")

    lines = [line.strip() for line in source_text.splitlines()]
    return BrandProfile(
        brand_name=_line_value(lines, "Brand name"),
        podcast_name=_line_value(lines, "Podcast name"),
        founder=_line_value(lines, "Founder"),
        voice=_line_value(lines, "Voice"),
        signature_message=_line_value(lines, "Signature message"),
        core_themes=_section_items(lines, "Core Themes"),
        primary_audience=_section_items(lines, "Primary Audience"),
        content_preferences=_section_items(lines, "Content Preferences"),
        avoid=_section_items(lines, "Avoid"),
        source_text=source_text,
    )
