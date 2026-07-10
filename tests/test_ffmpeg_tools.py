from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

from concrete_motivation.ffmpeg_tools import configure_imageio_ffmpeg, ffmpeg_status, resolve_ffmpeg_binary
from scripts import check_ffmpeg


def _make_executable(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IEXEC)
    return path


def test_resolve_ffmpeg_binary_prefers_direct_file(tmp_path, monkeypatch):
    binary = _make_executable(tmp_path / "ffmpeg", "#!/bin/sh\necho ffmpeg\n")
    monkeypatch.setenv("CONCRETE_MOTIVATION_FFMPEG_BIN", "")

    resolved = resolve_ffmpeg_binary(binary)

    assert resolved == binary


def test_resolve_ffmpeg_binary_finds_binary_inside_directory(tmp_path, monkeypatch):
    binary_dir = tmp_path / "build-test" / "bin"
    binary_dir.mkdir(parents=True)
    binary = _make_executable(binary_dir / "ffmpeg", "#!/bin/sh\necho ffmpeg\n")
    monkeypatch.delenv("CONCRETE_MOTIVATION_FFMPEG_BIN", raising=False)

    resolved = resolve_ffmpeg_binary(tmp_path)

    assert resolved == binary


def test_configure_imageio_ffmpeg_sets_environment_variable(tmp_path, monkeypatch):
    binary = _make_executable(tmp_path / "ffmpeg", "#!/bin/sh\necho ffmpeg\n")
    monkeypatch.delenv("IMAGEIO_FFMPEG_EXE", raising=False)

    resolved = configure_imageio_ffmpeg(binary)

    assert resolved == binary
    assert os.environ["IMAGEIO_FFMPEG_EXE"] == str(binary)


def test_check_ffmpeg_reports_selected_binary(monkeypatch, tmp_path, capsys):
    binary = _make_executable(
        tmp_path / "ffmpeg",
        "#!/bin/sh\n"
        "if [ \"$1\" = \"-version\" ]; then\n"
        "  echo 'ffmpeg version 1.2.3'\n"
        "else\n"
        "  echo 'ffmpeg'\n"
        "fi\n",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "check_ffmpeg.py",
            "--ffmpeg-bin",
            str(binary),
        ],
    )

    assert check_ffmpeg.main() == 0
    output = capsys.readouterr().out

    assert "FFmpeg Status" in output
    assert str(binary) in output
    assert "ffmpeg version 1.2.3" in output
