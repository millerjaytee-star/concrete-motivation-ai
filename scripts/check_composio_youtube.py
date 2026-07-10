#!/usr/bin/env python3
"""Check local Composio readiness for YouTube publishing.

This script is safe: it does not upload, modify, or delete anything.
It only runs local Composio CLI discovery commands and prints what it finds.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass


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


def main() -> int:
    print_section("Concrete Motivation YouTube Publishing Readiness Check")

    if not shutil.which("composio"):
        print("Composio CLI was not found on PATH.")
        print("Fix: install/login to Composio, then rerun this script.")
        return 1

    checks = [
        ("Composio version/help", ("composio", "--help")),
        ("Connected accounts", ("composio", "connections", "list")),
        ("Developer connected accounts", ("composio", "dev", "connected-accounts", "list")),
        ("Tool/action discovery", ("composio", "tools", "list")),
        ("Action discovery", ("composio", "actions", "list")),
    ]

    combined = []
    for title, command in checks:
        print_section(title)
        result = run_command(*command)
        print_result(result)
        combined.append(result.text.lower())

    searchable = "\n".join(combined)
    print_section("YouTube Result")
    youtube_found = "youtube" in searchable
    upload_found = any(word in searchable for word in ("upload", "video", "publish")) and youtube_found

    if youtube_found:
        print("YouTube appears somewhere in the local Composio output.")
    else:
        print("YouTube was not found in the visible local Composio output.")
        print("Next step: run `composio dev init`, then connect/enable YouTube in Composio.")

    if upload_found:
        print("A likely YouTube publishing/upload capability appears to be available.")
        print("Next step: build the confirmed uploader around the exact action name shown above.")
    else:
        print("No confirmed YouTube upload/publish action was detected from these CLI checks.")
        print("Next step: paste this full output into Codex/ChatGPT so the exact CLI path can be wired up.")

    return 0 if youtube_found else 2


if __name__ == "__main__":
    raise SystemExit(main())
