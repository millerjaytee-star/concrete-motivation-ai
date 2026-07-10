"""Data models for Concrete Motivation content packages and batches."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


CONTENT_PACKAGE_FOLDER = "content_packages"


@dataclass(frozen=True, slots=True)
class ContentPackage:
    """A single publish-ready content package."""

    topic: str
    audience: str
    core_message: str
    platform: str
    youtube_concept: str
    long_form_youtube_title: str
    long_form_youtube_outline: tuple[str, ...]
    youtube_description: str
    youtube_tags: tuple[str, ...]
    thumbnail_text: str
    reel_60_second_script: str
    short_30_second_script: str
    hook_15_second_script: str
    instagram_caption: str
    facebook_caption: str
    linkedin_post: str
    podcast_segment: str
    call_to_action: str
    repurpose_plan: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-friendly representation."""
        return {
            "topic": self.topic,
            "audience": self.audience,
            "core_message": self.core_message,
            "platform": self.platform,
            "youtube_concept": self.youtube_concept,
            "long_form_youtube_title": self.long_form_youtube_title,
            "long_form_youtube_outline": list(self.long_form_youtube_outline),
            "youtube_description": self.youtube_description,
            "youtube_tags": list(self.youtube_tags),
            "thumbnail_text": self.thumbnail_text,
            "reel_60_second_script": self.reel_60_second_script,
            "short_30_second_script": self.short_30_second_script,
            "hook_15_second_script": self.hook_15_second_script,
            "instagram_caption": self.instagram_caption,
            "facebook_caption": self.facebook_caption,
            "linkedin_post": self.linkedin_post,
            "podcast_segment": self.podcast_segment,
            "call_to_action": self.call_to_action,
            "repurpose_plan": list(self.repurpose_plan),
        }

    def as_markdown(self) -> str:
        """Render the package for human review."""
        outline = "\n".join(f"- {item}" for item in self.long_form_youtube_outline)
        tags = ", ".join(self.youtube_tags)
        repurpose = "\n".join(f"- {item}" for item in self.repurpose_plan)
        return f"""# Concrete Motivation Content Package

## Topic
{self.topic}

## Audience
{self.audience}

## Core Message
{self.core_message}

## Platform
{self.platform}

## YouTube Concept
{self.youtube_concept}

## Long-Form YouTube Title
{self.long_form_youtube_title}

## Long-Form YouTube Outline
{outline}

## YouTube Description
{self.youtube_description}

## YouTube Tags
{tags}

## Thumbnail Notes
{self.thumbnail_text}

## 60-Second Reel Script
{self.reel_60_second_script}

## 30-Second Short Script
{self.short_30_second_script}

## 15-Second Hook
{self.hook_15_second_script}

## Instagram Caption
{self.instagram_caption}

## Facebook Caption
{self.facebook_caption}

## LinkedIn Post
{self.linkedin_post}

## Podcast Segment
{self.podcast_segment}

## Call To Action
{self.call_to_action}

## Repurpose Plan
{repurpose}
"""

    def as_csv_row(self) -> dict[str, str]:
        """Return a single row for CRM or tracker exports."""
        return {
            "topic": self.topic,
            "audience": self.audience,
            "core_message": self.core_message,
            "platform": self.platform,
            "youtube_concept": self.youtube_concept,
            "long_form_youtube_title": self.long_form_youtube_title,
            "long_form_youtube_outline": " | ".join(self.long_form_youtube_outline),
            "youtube_description": self.youtube_description,
            "youtube_tags": ", ".join(self.youtube_tags),
            "thumbnail_text": self.thumbnail_text,
            "reel_60_second_script": self.reel_60_second_script,
            "short_30_second_script": self.short_30_second_script,
            "hook_15_second_script": self.hook_15_second_script,
            "instagram_caption": self.instagram_caption,
            "facebook_caption": self.facebook_caption,
            "linkedin_post": self.linkedin_post,
            "podcast_segment": self.podcast_segment,
            "call_to_action": self.call_to_action,
            "repurpose_plan": " | ".join(self.repurpose_plan),
        }


@dataclass(frozen=True, slots=True)
class ContentPackageExport:
    """Files written for one content package."""

    folder: Path
    markdown_path: Path
    json_path: Path
    csv_path: Path


@dataclass(frozen=True, slots=True)
class ContentBatchResult:
    """A batch of related content packages."""

    label: str
    packages: tuple[ContentPackage, ...]
    exports: tuple[ContentPackageExport, ...] = field(default_factory=tuple)

    def as_markdown(self) -> str:
        """Summarize the batch for the terminal."""
        lines = [f"# Content Batch: {self.label}", f"**Packages:** {len(self.packages)}"]
        for index, package in enumerate(self.packages, start=1):
            lines.append(
                "\n".join(
                    (
                        f"## {index}. {package.topic}",
                        f"**Audience:** {package.audience}",
                        f"**Title:** {package.long_form_youtube_title}",
                        f"**CTA:** {package.call_to_action}",
                    )
                )
            )
        return "\n\n".join(lines)
