"""Resolve and configure an ffmpeg binary for local video export."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from shutil import which


@dataclass(frozen=True, slots=True)
class FFmpegStatus:
    requested: str | None
    resolved: Path | None
    source: str

    @property
    def available(self) -> bool:
        return self.resolved is not None and self.resolved.is_file()

    def as_markdown(self) -> str:
        resolved = str(self.resolved) if self.resolved else "None"
        return f"""# FFmpeg Status

## Requested
{self.requested or "None"}

## Resolved
{resolved}

## Source
{self.source}

## Available
{'yes' if self.available else 'no'}
"""


def _candidate_paths(value: str) -> tuple[Path, ...]:
    path = Path(value).expanduser()
    if path.is_file():
        return (path,)
    candidates = [
        path,
        path / "ffmpeg",
        path / "bin" / "ffmpeg",
        path / "build-test" / "bin" / "ffmpeg",
    ]
    return tuple(candidates)


def bundled_imageio_ffmpeg_binary() -> Path | None:
    try:
        import imageio_ffmpeg
    except Exception:
        return None

    binaries_dir = Path(imageio_ffmpeg.__file__).resolve().parent / "binaries"
    if not binaries_dir.is_dir():
        return None
    for candidate in sorted(binaries_dir.iterdir()):
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate
    return None


def resolve_ffmpeg_binary(preferred: str | Path | None = None) -> Path:
    requested = str(preferred or os.getenv("CONCRETE_MOTIVATION_FFMPEG_BIN", "")).strip()
    if requested:
        for candidate in _candidate_paths(requested):
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return candidate

    try:
        bundled = bundled_imageio_ffmpeg_binary()
        if bundled and bundled.is_file():
            return bundled
    except Exception:
        pass

    fallback = Path("/usr/bin/ffmpeg")
    if fallback.is_file() and os.access(fallback, os.X_OK):
        return fallback
    system = which("ffmpeg")
    if system:
        return Path(system)
    return Path(requested or "ffmpeg")


def ffmpeg_status(preferred: str | Path | None = None) -> FFmpegStatus:
    requested = str(preferred or os.getenv("CONCRETE_MOTIVATION_FFMPEG_BIN", "")).strip() or None
    resolved = resolve_ffmpeg_binary(preferred)
    if requested and resolved.as_posix() == requested:
        source = "requested"
    elif "imageio_ffmpeg" in resolved.as_posix():
        source = "imageio-ffmpeg bundle"
    else:
        source = "system or fallback"
    return FFmpegStatus(requested=requested, resolved=resolved if resolved.is_file() else None, source=source)


def configure_imageio_ffmpeg(preferred: str | Path | None = None) -> Path:
    resolved = resolve_ffmpeg_binary(preferred)
    if resolved.is_file():
        os.environ["IMAGEIO_FFMPEG_EXE"] = str(resolved)
    return resolved


def ffmpeg_supports_encoder(binary: str | Path, encoder: str = "libx264") -> bool:
    path = Path(binary)
    if not path.is_file():
        return False
    try:
        completed = subprocess.run(
            [str(path), "-hide_banner", "-encoders"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return False
    if completed.returncode not in (0, 1):
        return False
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    return encoder in output
