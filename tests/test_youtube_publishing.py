import json
import sys
from pathlib import Path
from subprocess import CompletedProcess

from concrete_motivation.youtube_publish_package import (
    YOUTUBE_DEFAULT_CATEGORY_ID,
    YOUTUBE_UPLOAD_TOOL,
    build_execute_command,
    build_package,
)
from scripts.check_composio_youtube import load_cached_youtube_actions
from scripts import youtube_upload_confirmed, youtube_upload_dry_run


def test_build_execute_command_uses_exact_youtube_upload_slug(tmp_path):
    video = tmp_path / "clip.mp4"
    video.write_bytes(b"fake video bytes")

    package = build_package("discipline under pressure", video_path=str(video))
    command = build_execute_command(package)

    assert command[:3] == ["composio", "execute", YOUTUBE_UPLOAD_TOOL]
    assert command[3:5] == ["--file", str(video)]
    payload = json.loads(command[-1])
    assert payload["privacyStatus"] == "private"
    assert payload["categoryId"] == YOUTUBE_DEFAULT_CATEGORY_ID
    assert payload["title"].startswith("Pressure Has a Purpose:")


def test_dry_run_script_prints_command_without_uploading(monkeypatch, tmp_path, capsys):
    video = tmp_path / "dry-run.mp4"
    video.write_bytes(b"fake video bytes")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "youtube_upload_dry_run.py",
            "discipline under pressure",
            "--video-path",
            str(video),
        ],
    )

    assert youtube_upload_dry_run.main() == 0
    output = capsys.readouterr().out
    assert YOUTUBE_UPLOAD_TOOL in output
    assert "Dry run command:" in output
    assert "Saved package:" in output


def test_confirmed_script_requires_exact_confirmation(monkeypatch, tmp_path, capsys):
    video = tmp_path / "confirmed.mp4"
    video.write_bytes(b"fake video bytes")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "youtube_upload_confirmed.py",
            "discipline under pressure",
            "--video-path",
            str(video),
        ],
    )
    monkeypatch.setattr("builtins.input", lambda _prompt="": "nope")

    assert youtube_upload_confirmed.main() == 1
    output = capsys.readouterr().out
    assert "Upload cancelled." in output


def test_confirmed_script_runs_composio_command_with_private_default(monkeypatch, tmp_path, capsys):
    video = tmp_path / "publish.mp4"
    video.write_bytes(b"fake video bytes")
    recorded: dict[str, list[str]] = {}

    def fake_run(command, check=False, capture_output=False, text=False):
        recorded["command"] = list(command)
        return CompletedProcess(command, 0, stdout="uploaded", stderr="")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "youtube_upload_confirmed.py",
            "discipline under pressure",
            "--video-path",
            str(video),
        ],
    )
    monkeypatch.setattr("builtins.input", lambda _prompt="": "UPLOAD TO YOUTUBE")
    monkeypatch.setattr("subprocess.run", fake_run)

    assert youtube_upload_confirmed.main() == 0
    output = capsys.readouterr().out

    assert recorded["command"][:3] == ["composio", "execute", YOUTUBE_UPLOAD_TOOL]
    assert "--file" in recorded["command"]
    assert "private" in output
    assert "Executing:" in output


def test_composio_checker_finds_cached_youtube_upload_action():
    actions = load_cached_youtube_actions()

    assert YOUTUBE_UPLOAD_TOOL in actions
