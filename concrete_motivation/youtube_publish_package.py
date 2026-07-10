"""Safe YouTube publishing package builder for Concrete Motivation.

This module prepares everything needed for a YouTube upload without performing
an upload by default. Publishing should only happen from a local Composio/YouTube
integration after explicit confirmation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
import re
from datetime import datetime


DEFAULT_TAGS = [
    "Concrete Motivation",
    "Jaytee Miller",
    "motivation",
    "discipline",
    "resilience",
    "faith",
    "leadership",
    "family",
    "mindset",
    "Concrete Conversations",
]


@dataclass(frozen=True)
class YouTubePublishPackage:
    topic: str
    title: str
    description: str
    tags: list[str] = field(default_factory=lambda: DEFAULT_TAGS.copy())
    visibility: str = "private"
    video_path: str = ""
    thumbnail_notes: str = ""
    shorts_plan: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, object]:
        return {
            "topic": self.topic,
            "title": self.title,
            "description": self.description,
            "tags": self.tags,
            "visibility": self.visibility,
            "video_path": self.video_path,
            "thumbnail_notes": self.thumbnail_notes,
            "shorts_plan": self.shorts_plan,
        }

    def as_markdown(self) -> str:
        tags = ", ".join(self.tags)
        shorts = "\n".join(f"- {item}" for item in self.shorts_plan)
        return f"""# YouTube Publishing Package

## Topic
{self.topic}

## Title
{self.title}

## Description
{self.description}

## Tags
{tags}

## Visibility
{self.visibility}

## Video Path
{self.video_path or '[Add local video path before upload]'}

## Thumbnail Notes
{self.thumbnail_notes}

## Shorts Plan
{shorts}
"""


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned[:80] or "youtube-package"


def build_package(topic: str, video_path: str = "", visibility: str = "private") -> YouTubePublishPackage:
    topic = topic.strip()
    if not topic:
        raise ValueError("topic cannot be empty")
    if visibility not in {"private", "unlisted", "public"}:
        raise ValueError("visibility must be private, unlisted, or public")

    title = f"Pressure Has a Purpose: {topic.title()}"
    description = (
        f"In this Concrete Motivation message, Jaytee Miller breaks down {topic} "
        "and gives practical steps to keep building through pressure.\n\n"
        "Concrete Motivation is about turning pressure into purpose through discipline, "
        "faith, leadership, family, and real action.\n\n"
        "Comment your one concrete commitment for this week. One brick at a time."
    )
    thumbnail_notes = "Bold face, strong contrast, text: PRESSURE BUILDS or ONE BRICK TODAY."
    shorts_plan = [
        "Hook Short: name the pressure in the first 3 seconds.",
        "Story Short: one honest moment from Jaytee's journey.",
        "Lesson Short: discipline after motivation fades.",
        "Faith/Family/Leadership Short: connect responsibility to purpose.",
        "Challenge Short: ask viewers for one concrete commitment.",
    ]
    return YouTubePublishPackage(
        topic=topic,
        title=title,
        description=description,
        video_path=video_path,
        visibility=visibility,
        thumbnail_notes=thumbnail_notes,
        shorts_plan=shorts_plan,
    )


def save_package(package: YouTubePublishPackage, output_dir: Path | str = "outputs/youtube_packages") -> Path:
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    base = f"{timestamp}-{slugify(package.topic)}"
    md_path = folder / f"{base}.md"
    json_path = folder / f"{base}.json"
    md_path.write_text(package.as_markdown(), encoding="utf-8")
    json_path.write_text(json.dumps(package.as_dict(), indent=2), encoding="utf-8")
    return md_path
