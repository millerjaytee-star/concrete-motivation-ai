"""Helpers for the YouTube upload verification workflow."""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from concrete_motivation.youtube_publish_package import (
    DEFAULT_TAGS,
    YOUTUBE_DEFAULT_CATEGORY_ID,
    YOUTUBE_UPLOAD_TOOL,
    YouTubePublishPackage,
    build_execute_command,
)

DEFAULT_TEST_VIDEO = Path("generated_videos/01_built_under_pressure.mp4")
DEFAULT_TEST_TITLE = "Built Under Pressure"
DEFAULT_TEST_DESCRIPTION = "Test upload from Concrete Motivation AI Operating System."
DEFAULT_TEST_VISIBILITY = "private"
CONNECT_COMMAND = "composio link youtube"


@dataclass(frozen=True, slots=True)
class VerificationResult:
    upload_status: str
    video_id: str
    video_url: str
    channel_name: str
    upload_output: str
    channel_output: str

    def as_markdown(self) -> str:
        return (
            "# YouTube Upload Verification\n\n"
            f"## Upload Status\n{self.upload_status}\n\n"
            f"## Video ID\n{self.video_id or 'unavailable'}\n\n"
            f"## Video URL\n{self.video_url or 'unavailable'}\n\n"
            f"## Channel Name\n{self.channel_name or 'unavailable'}\n"
        )


def build_verification_package(video_path: str | Path = DEFAULT_TEST_VIDEO) -> YouTubePublishPackage:
    path = Path(video_path)
    return YouTubePublishPackage(
        topic=DEFAULT_TEST_TITLE,
        title=DEFAULT_TEST_TITLE,
        description=DEFAULT_TEST_DESCRIPTION,
        tags=DEFAULT_TAGS.copy(),
        visibility=DEFAULT_TEST_VISIBILITY,
        video_path=str(path),
        thumbnail_notes="Verification upload: plain title card and high-contrast branding.",
        shorts_plan=["Verification upload only; no Shorts generated."],
    )


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, capture_output=True, text=True)


def ensure_project_initialized(root: Path) -> Path | None:
    project_file = root / ".composio" / "project.json"
    return project_file if project_file.is_file() else None


def extract_json_objects(text: str) -> list[Any]:
    documents: list[Any] = []
    decoder = json.JSONDecoder()
    for match in re.finditer(r"[\{\[]", text):
        try:
            value, _end = decoder.raw_decode(text[match.start() :])
        except json.JSONDecodeError:
            continue
        documents.append(value)
    return documents


def find_first_value(payload: Any, keys: tuple[str, ...]) -> str:
    if isinstance(payload, dict):
        for key in keys:
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        for value in payload.values():
            found = find_first_value(value, keys)
            if found:
                return found
    elif isinstance(payload, list):
        for item in payload:
            found = find_first_value(item, keys)
            if found:
                return found
    return ""


def extract_video_id(text: str) -> str:
    documents = extract_json_objects(text)
    for document in documents:
        found = find_first_value(document, ("videoId", "video_id", "id"))
        if found:
            return found
    match = re.search(r"(?:videoId|video_id|id)[:=]\s*([A-Za-z0-9_-]{6,})", text)
    if match:
        return match.group(1)
    return ""


def extract_channel_name(text: str) -> str:
    documents = extract_json_objects(text)
    for document in documents:
        found = find_first_value(
            document,
            (
                "channelTitle",
                "channel_name",
                "channelName",
                "title",
                "name",
            ),
        )
        if found:
            return found
    return ""


def extract_video_url(text: str, video_id: str) -> str:
    if video_id:
        return f"https://www.youtube.com/watch?v={video_id}"
    documents = extract_json_objects(text)
    for document in documents:
        found = find_first_value(document, ("videoUrl", "url", "webpage_url", "webUrl"))
        if found and ("youtube.com/watch" in found or "youtu.be/" in found):
            return found
    return ""


def build_upload_result(upload_text: str, channel_text: str) -> VerificationResult:
    video_id = extract_video_id(upload_text)
    video_url = extract_video_url(upload_text, video_id)
    channel_name = extract_channel_name(channel_text) or extract_channel_name(upload_text)
    status = "SUCCESS" if video_id else "FAILED"
    return VerificationResult(
        upload_status=status,
        video_id=video_id,
        video_url=video_url,
        channel_name=channel_name,
        upload_output=upload_text,
        channel_output=channel_text,
    )


def build_upload_command(package: YouTubePublishPackage) -> list[str]:
    if package.visibility != "private":
        package = YouTubePublishPackage(
            topic=package.topic,
            title=package.title,
            description=package.description,
            tags=package.tags,
            visibility="private",
            video_path=package.video_path,
            thumbnail_notes=package.thumbnail_notes,
            shorts_plan=package.shorts_plan,
        )
    return build_execute_command(package, category_id=YOUTUBE_DEFAULT_CATEGORY_ID)


def build_channel_lookup_command() -> list[str]:
    return [
        "composio",
        "execute",
        "YOUTUBE_LIST_CHANNELS",
        "-d",
        json.dumps({"mine": True, "part": "snippet", "maxResults": 1}),
    ]
