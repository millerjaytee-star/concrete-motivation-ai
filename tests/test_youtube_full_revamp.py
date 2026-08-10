from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "youtube_launch" / "YOUTUBE_REVAMP_MANIFEST_2026.json"
SCRIPT = ROOT / "scripts" / "youtube_full_revamp.py"


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_manifest_targets_correct_channel():
    data = load_manifest()
    assert data["channel"]["name"] == "Concrete Motivation"
    assert data["channel"]["handle"] == "@concretemotivation444"


def test_manifest_contains_master_phrase_and_brand_rules():
    data = load_manifest()
    description = data["channel"]["description"]
    assert "BUILD FROM PRESSURE." in description
    assert "LEAD WITH PURPOSE." in description
    assert "MOVE WITH DISCIPLINE." in description
    assert data["visual_rules"]["use_real_photos_only"] is True
    assert data["visual_rules"]["preserve_faces_and_body_structure"] is True


def test_required_playlists_exist_and_are_unique():
    data = load_manifest()
    titles = [x["title"] for x in data["playlists"]]
    assert len(titles) == len(set(titles))
    for required in (
        "START HERE — CONCRETE MOTIVATION",
        "CONCRETE CONVERSATIONS",
        "BUILD FROM PRESSURE",
        "DISCIPLINE OVER FEELINGS",
        "LEAD WITH PURPOSE",
        "FAITH, FAMILY & LEGACY",
        "REAL LIFE. REAL TALK.",
        "MINDSET & PERSONAL GROWTH",
        "CONCRETE NATION",
    ):
        assert required in titles


def test_script_has_explicit_confirmation_and_no_destructive_video_actions():
    source = SCRIPT.read_text(encoding="utf-8")
    assert "REVAMP CONCRETE MOTIVATION" in source
    assert "YOUTUBE_DELETE_VIDEO" not in source
    assert "YOUTUBE_MULTIPART_UPLOAD_VIDEO" not in source
    assert "YOUTUBE_UPDATE_VIDEO" not in source
    assert "privacy of existing videos" not in source.lower()


def test_script_uses_current_composio_youtube_tool_slugs():
    source = SCRIPT.read_text(encoding="utf-8")
    for slug in (
        "YOUTUBE_UPDATE_CHANNEL",
        "YOUTUBE_LIST_USER_PLAYLISTS",
        "YOUTUBE_CREATE_PLAYLIST",
        "YOUTUBE_UPDATE_PLAYLIST",
        "YOUTUBE_LIST_CHANNEL_SECTIONS",
        "YOUTUBE_CREATE_CHANNEL_SECTION",
    ):
        assert slug in source
