import json
from pathlib import Path

import pytest

from concrete_motivation.launch_system import (
    FORBIDDEN_DEFAULT_ACTIONS,
    PRIVATE_ONLY_VISIBILITY,
    SYSTEMS,
    verify_launch_system,
)
from scripts import test_youtube_upload


ROOT = Path(__file__).resolve().parent.parent


def test_launch_system_covers_every_required_system():
    report = verify_launch_system(ROOT)
    check_names = {check.name for check in report.checks}

    assert set(SYSTEMS) == check_names
    assert report.overall_status in {"ready", "manual_action_required"}
    assert report.upload_policy["youtube_visibility"] == PRIVATE_ONLY_VISIBILITY
    assert set(FORBIDDEN_DEFAULT_ACTIONS).issubset(set(report.upload_policy["blocked_actions"]))


def test_launch_report_serializes_for_dashboard_or_cli():
    report = verify_launch_system(ROOT)
    data = json.loads(report.as_json())

    assert data["upload_policy"]["upload_limit"] == "one video per explicit verification run"
    assert "Championship Launch Verification" in report.as_markdown()
    assert any(check["name"] == "YouTube" for check in data["checks"])


def test_launch_artifacts_exist_and_do_not_store_secrets():
    required = (
        ROOT / "docs" / "CHAMPIONSHIP_LAUNCH_SYSTEM.md",
        ROOT / "docs" / "YOUTUBE_PUBLISHING_VERIFICATION.md",
        ROOT / "crm" / "lead_pipeline_template.csv",
        ROOT / "dashboard" / "launch_dashboard.html",
        ROOT / "social_handoff" / "launch_handoff.md",
    )

    for path in required:
        text = path.read_text(encoding="utf-8")
        assert text.strip()
        assert "sk-" not in text
        assert "API_KEY=" not in text
        assert "ya29." not in text


def test_youtube_upload_harness_is_private_and_single_video_only(tmp_path):
    video = tmp_path / "generated_videos" / "01_built_under_pressure.mp4"
    video.parent.mkdir()
    video.write_bytes(b"not a real video, just a path validation fixture")

    original = test_youtube_upload.VIDEO_PATH
    test_youtube_upload.VIDEO_PATH = Path("generated_videos/01_built_under_pressure.mp4")
    try:
        old_cwd = Path.cwd()
        try:
            import os

            os.chdir(tmp_path)
            test_youtube_upload.validate_single_private_upload(test_youtube_upload.VIDEO_PATH, "private")
            payload = test_youtube_upload.build_payload(test_youtube_upload.VIDEO_PATH)
        finally:
            os.chdir(old_cwd)
    finally:
        test_youtube_upload.VIDEO_PATH = original

    assert payload["title"] == "Built Under Pressure"
    assert payload["visibility"] == "private"
    assert payload["privacy_status"] == "private"


def test_youtube_upload_harness_rejects_public_visibility(tmp_path):
    video = tmp_path / "generated_videos" / "01_built_under_pressure.mp4"
    video.parent.mkdir()
    video.write_bytes(b"fixture")

    original = test_youtube_upload.VIDEO_PATH
    test_youtube_upload.VIDEO_PATH = Path("generated_videos/01_built_under_pressure.mp4")
    try:
        old_cwd = Path.cwd()
        try:
            import os

            os.chdir(tmp_path)
            with pytest.raises(ValueError, match="PRIVATE"):
                test_youtube_upload.validate_single_private_upload(test_youtube_upload.VIDEO_PATH, "public")
        finally:
            os.chdir(old_cwd)
    finally:
        test_youtube_upload.VIDEO_PATH = original
