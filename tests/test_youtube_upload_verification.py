from __future__ import annotations

import sys
from subprocess import CompletedProcess

from concrete_motivation.youtube_upload_verification import (
    DEFAULT_TEST_DESCRIPTION,
    DEFAULT_TEST_TITLE,
    DEFAULT_TEST_VISIBILITY,
    build_upload_result,
    build_verification_package,
)
from scripts import test_youtube_upload


def test_verification_package_uses_required_title_description_and_visibility(tmp_path):
    video = tmp_path / "01_built_under_pressure.mp4"
    video.write_bytes(b"fake video bytes")

    package = build_verification_package(video)

    assert package.title == DEFAULT_TEST_TITLE
    assert package.description == DEFAULT_TEST_DESCRIPTION
    assert package.visibility == DEFAULT_TEST_VISIBILITY
    assert package.video_path == str(video)


def test_build_upload_result_parses_video_id_url_and_channel_name():
    upload_text = """
    {
      "videoId": "abc123XYZ",
      "url": "https://www.youtube.com/watch?v=abc123XYZ",
      "channelTitle": "Concrete Motivation"
    }
    """
    channel_text = """
    {
      "items": [
        {
          "snippet": {
            "title": "Concrete Motivation Channel"
          }
        }
      ]
    }
    """

    result = build_upload_result(upload_text, channel_text)

    assert result.upload_status == "SUCCESS"
    assert result.video_id == "abc123XYZ"
    assert result.video_url == "https://www.youtube.com/watch?v=abc123XYZ"
    assert result.channel_name == "Concrete Motivation Channel"


def test_test_youtube_upload_script_reports_private_single_video_flow(monkeypatch, tmp_path, capsys):
    video = tmp_path / "01_built_under_pressure.mp4"
    video.write_bytes(b"fake video bytes")
    calls: list[list[str]] = []

    def fake_run(command):
        calls.append(list(command))
        if command[:3] == ["composio", "connections", "list"]:
            return CompletedProcess(command, 0, stdout="youtube: ACTIVE", stderr="")
        if command[:3] == ["composio", "execute", "YOUTUBE_MULTIPART_UPLOAD_VIDEO"]:
            return CompletedProcess(
                command,
                0,
                stdout='{"videoId":"abc123XYZ","channelTitle":"Concrete Motivation"}',
                stderr="",
            )
        if command[:3] == ["composio", "execute", "YOUTUBE_LIST_CHANNELS"]:
            return CompletedProcess(
                command,
                0,
                stdout='{"items":[{"snippet":{"title":"Concrete Motivation Channel"}}]}',
                stderr="",
            )
        raise AssertionError(f"Unexpected command: {command}")

    monkeypatch.setattr(test_youtube_upload, "run_command", fake_run)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "test_youtube_upload.py",
            "--video-path",
            str(video),
        ],
    )

    assert test_youtube_upload.main() == 0
    output = capsys.readouterr().out

    assert any("YOUTUBE_MULTIPART_UPLOAD_VIDEO" in " ".join(command) for command in calls)
    assert "Built Under Pressure" in output
    assert "PRIVATE" not in output  # script reports lowercase private from package markdown
    assert "SUCCESS" in output
    assert "abc123XYZ" in output
    assert "Concrete Motivation Channel" in output
