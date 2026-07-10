#!/usr/bin/env python3
"""Check local Composio readiness for YouTube publishing."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CommandResult:
    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    @property
    def text(self) -> str:
        return "\n".join(part for part in (self.stdout.strip(), self.stderr.strip()) if part)


def run_command(*command: str) -> CommandResult:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError:
        return CommandResult(command, 127, "", f"Command not found: {command[0]}")
    except subprocess.TimeoutExpired:
        return CommandResult(command, 124, "", "Command timed out after 30 seconds")

    return CommandResult(command, completed.returncode, completed.stdout, completed.stderr)


def print_section(title: str) -> None:
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def print_result(result: CommandResult) -> None:
    print(f"$ {' '.join(result.command)}")
    print(f"exit_code={result.returncode}")
    if result.text:
        print(result.text)
    else:
        print("(no output)")


def load_cached_youtube_actions() -> list[str]:
    cache_dir = Path.home() / ".composio" / "tool_definitions"
    return sorted(path.stem for path in cache_dir.glob("YOUTUBE*.json"))


def main() -> int:
    print_section("Concrete Motivation YouTube Publishing Readiness Check")

    if not shutil.which("composio"):
        print("Composio CLI was not found on PATH.")
        print("Fix: install/login to Composio, then rerun this script.")
        return 1

    checks = [
        ("Composio version/help", ("composio", "--help")),
        ("Toolkit connection list", ("composio", "connections", "list", "--toolkit", "youtube")),
        ("Developer connected accounts", ("composio", "dev", "connected-accounts", "list")),
        ("YouTube toolkit tools", ("composio", "tools", "list", "youtube", "--limit", "50")),
        ("YouTube upload tool schema", ("composio", "execute", "YOUTUBE_MULTIPART_UPLOAD_VIDEO", "--get-schema", "--skip-checks")),
    ]

    combined = []
    for title, command in checks:
        print_section(title)
        result = run_command(*command)
        print_result(result)
        combined.append(result.text.lower())

    print_section("Cached YouTube Actions")
    cached_actions = load_cached_youtube_actions()
    if cached_actions:
        for slug in cached_actions:
            print(slug)
    else:
        print("(no cached YouTube tool definitions found)")

    searchable = "\n".join(combined)
    print_section("YouTube Result")
    youtube_found = "youtube" in searchable or bool(cached_actions)
    upload_found = "YOUTUBE_MULTIPART_UPLOAD_VIDEO" in cached_actions
    connected_confirmed = "active" in searchable and "youtube" in searchable

    if youtube_found:
        print("YouTube toolkit definitions are available locally.")
    else:
        print("YouTube was not found in the visible local Composio output.")
        print("Next step: run `composio dev init`, then connect/enable YouTube in Composio.")

    if upload_found:
        print("Upload/publish action confirmed: YOUTUBE_MULTIPART_UPLOAD_VIDEO")
        print("Use this exact Composio command shape when uploading:")
        print("composio execute YOUTUBE_MULTIPART_UPLOAD_VIDEO --file <video-path> -d '<payload-json>'")
    else:
        print("No confirmed YouTube upload/publish action was detected from the cached tool list.")
        print("Next step: inspect ~/.composio/tool_definitions or rerun Composio sync after login.")

    if connected_confirmed:
        print("YouTube appears connected in the available CLI output.")
    else:
        print("YouTube connection was not confirmed from this environment.")
        print("Exact connect command: composio link youtube")

    return 0 if youtube_found else 2


if __name__ == "__main__":
    raise SystemExit(main())
