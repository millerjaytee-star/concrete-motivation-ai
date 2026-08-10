#!/usr/bin/env python3
"""Concrete Motivation YouTube full-revamp runner via Composio.

This script is intentionally conservative:
- audits first
- never uploads/deletes videos
- never changes visibility of existing videos
- only updates channel metadata, creates/updates named playlists, and creates channel sections
- requires an explicit confirmation phrase for mutations

Composio tool slugs are current as of the 2026-07-21 YouTube toolkit:
YOUTUBE_UPDATE_CHANNEL, YOUTUBE_LIST_USER_PLAYLISTS, YOUTUBE_CREATE_PLAYLIST,
YOUTUBE_UPDATE_PLAYLIST, YOUTUBE_LIST_CHANNEL_SECTIONS, YOUTUBE_CREATE_CHANNEL_SECTION.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "youtube_launch" / "YOUTUBE_REVAMP_MANIFEST_2026.json"
CONFIRM_PHRASE = "REVAMP CONCRETE MOTIVATION"


@dataclass
class Result:
    returncode: int
    stdout: str
    stderr: str

    @property
    def text(self) -> str:
        return "\n".join(x for x in (self.stdout.strip(), self.stderr.strip()) if x)


def run(*args: str, timeout: int = 90) -> Result:
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
        return Result(p.returncode, p.stdout, p.stderr)
    except FileNotFoundError:
        return Result(127, "", f"Command not found: {args[0]}")
    except subprocess.TimeoutExpired:
        return Result(124, "", f"Timed out after {timeout}s")


def parse_json_loose(text: str) -> Any:
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.startswith("{") or line.startswith("["):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return None


def composio_execute(tool: str, payload: dict[str, Any] | None = None) -> Result:
    payload = payload or {}
    # Existing repo installations used this syntax; keep it first for compatibility.
    legacy = run("composio", "execute", tool, "-d", json.dumps(payload))
    if legacy.returncode == 0:
        return legacy
    # Universal CLI syntax used by current Composio docs.
    modern = run("composio", "tools", "execute", tool, "-d", json.dumps(payload))
    return modern if modern.returncode == 0 else legacy


def extract_items(raw: Any) -> list[dict[str, Any]]:
    if raw is None:
        return []
    if isinstance(raw, list):
        return [x for x in raw if isinstance(x, dict)]
    if not isinstance(raw, dict):
        return []
    for key in ("items", "playlists", "sections", "data", "result", "response"):
        value = raw.get(key)
        if isinstance(value, list):
            return [x for x in value if isinstance(x, dict)]
        if isinstance(value, dict):
            nested = extract_items(value)
            if nested:
                return nested
    return []


def get_title(item: dict[str, Any]) -> str:
    snippet = item.get("snippet") if isinstance(item.get("snippet"), dict) else {}
    return str(item.get("title") or snippet.get("title") or "").strip()


def get_id(item: dict[str, Any]) -> str:
    return str(item.get("id") or item.get("playlistId") or item.get("channelSectionId") or "").strip()


def check_environment() -> None:
    if not shutil.which("composio"):
        raise SystemExit("Composio CLI is not on PATH. Install/login first, then rerun.")
    connection = run("composio", "connected-accounts", "list", "--toolkits", "youtube")
    if connection.returncode != 0:
        connection = run("composio", "connections", "list", "--toolkit", "youtube")
    if connection.returncode != 0 or "youtube" not in connection.text.lower():
        raise SystemExit("YouTube is not visibly connected in Composio. Run: composio link youtube")


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("channel", {}).get("handle") != "@concretemotivation444":
        raise SystemExit("Refusing to run: manifest handle is not @concretemotivation444")
    return data


def audit(manifest: dict[str, Any]) -> dict[str, Any]:
    playlists_result = composio_execute("YOUTUBE_LIST_USER_PLAYLISTS", {"maxResults": 50, "part": "snippet,status"})
    playlists_raw = parse_json_loose(playlists_result.stdout)
    playlists = extract_items(playlists_raw)

    sections_result = composio_execute("YOUTUBE_LIST_CHANNEL_SECTIONS", {"part": "snippet,contentDetails", "mine": True})
    sections_raw = parse_json_loose(sections_result.stdout)
    sections = extract_items(sections_raw)

    existing_playlists = {get_title(x): get_id(x) for x in playlists if get_title(x)}
    desired_titles = [p["title"] for p in manifest["playlists"]]
    report = {
        "youtube_connected": playlists_result.returncode == 0,
        "existing_playlists": existing_playlists,
        "missing_playlists": [t for t in desired_titles if t not in existing_playlists],
        "channel_sections_found": len(sections),
        "channel_handle": manifest["channel"]["handle"],
    }
    return report


def update_channel(manifest: dict[str, Any]) -> None:
    channel = manifest["channel"]
    candidates = [
        {
            "description": channel["description"],
            "keywords": ",".join(channel["keywords"]),
        },
        {
            "snippet": {"description": channel["description"]},
            "brandingSettings": {"channel": {"keywords": ",".join(channel["keywords"])}}
        },
    ]
    errors: list[str] = []
    for payload in candidates:
        result = composio_execute("YOUTUBE_UPDATE_CHANNEL", payload)
        if result.returncode == 0:
            print("✓ Channel description/keywords updated")
            return
        errors.append(result.text[-1000:])
    raise RuntimeError("Could not update channel metadata with available schema.\n" + "\n---\n".join(errors))


def ensure_playlists(manifest: dict[str, Any]) -> dict[str, str]:
    current = composio_execute("YOUTUBE_LIST_USER_PLAYLISTS", {"maxResults": 50, "part": "snippet,status"})
    items = extract_items(parse_json_loose(current.stdout))
    ids = {get_title(x): get_id(x) for x in items if get_title(x) and get_id(x)}

    for playlist in manifest["playlists"]:
        title = playlist["title"]
        payload = {
            "title": title,
            "description": playlist["description"],
            "privacyStatus": playlist.get("privacyStatus", "public"),
        }
        if title in ids:
            update_payload = dict(payload)
            update_payload["playlistId"] = ids[title]
            update_payload["id"] = ids[title]
            result = composio_execute("YOUTUBE_UPDATE_PLAYLIST", update_payload)
            if result.returncode == 0:
                print(f"✓ Playlist refreshed: {title}")
            else:
                print(f"! Could not refresh existing playlist {title}; leaving it untouched")
            continue

        created = composio_execute("YOUTUBE_CREATE_PLAYLIST", payload)
        if created.returncode != 0:
            raise RuntimeError(f"Could not create playlist {title}: {created.text}")
        raw = parse_json_loose(created.stdout)
        created_items = extract_items(raw)
        new_id = ""
        if isinstance(raw, dict):
            new_id = get_id(raw)
        if not new_id and created_items:
            new_id = get_id(created_items[0])
        if new_id:
            ids[title] = new_id
        print(f"✓ Playlist created: {title}")

    # Re-list so IDs are canonical even if create responses were wrapped.
    current = composio_execute("YOUTUBE_LIST_USER_PLAYLISTS", {"maxResults": 50, "part": "snippet,status"})
    items = extract_items(parse_json_loose(current.stdout))
    return {get_title(x): get_id(x) for x in items if get_title(x) and get_id(x)}


def ensure_sections(manifest: dict[str, Any], playlist_ids: dict[str, str]) -> None:
    desired = [x for x in manifest["home_sections"] if x in playlist_ids]
    if not desired:
        print("! No playlist-backed channel sections could be created")
        return

    existing = composio_execute("YOUTUBE_LIST_CHANNEL_SECTIONS", {"part": "snippet,contentDetails", "mine": True})
    existing_items = extract_items(parse_json_loose(existing.stdout))
    existing_titles = {get_title(x) for x in existing_items}

    position = 0
    for title in desired:
        if title in existing_titles:
            position += 1
            continue
        payloads = [
            {"type": "singlePlaylist", "title": title, "position": position, "playlistId": playlist_ids[title]},
            {"snippet": {"type": "singlePlaylist", "title": title, "position": position}, "contentDetails": {"playlists": [playlist_ids[title]]}},
        ]
        done = False
        for payload in payloads:
            result = composio_execute("YOUTUBE_CREATE_CHANNEL_SECTION", payload)
            if result.returncode == 0:
                print(f"✓ Home section created: {title}")
                done = True
                break
        if not done:
            print(f"! Could not create channel section automatically: {title}")
        position += 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--apply", action="store_true", help="Apply metadata/playlists/channel sections")
    parser.add_argument("--yes", action="store_true", help="Skip interactive phrase only in a trusted local session")
    args = parser.parse_args()

    check_environment()
    manifest = load_manifest(args.manifest)
    report = audit(manifest)
    print(json.dumps(report, indent=2))

    if not args.apply:
        print("\nAUDIT ONLY. No YouTube changes were made.")
        print("Run with --apply to perform the revamp.")
        return 0

    if not args.yes:
        typed = input(f"Type exactly '{CONFIRM_PHRASE}' to continue: ").strip()
        if typed != CONFIRM_PHRASE:
            print("Cancelled. No mutations performed.")
            return 2

    update_channel(manifest)
    playlist_ids = ensure_playlists(manifest)
    ensure_sections(manifest, playlist_ids)

    print("\nREVAMP APPLY COMPLETE")
    print("Channel metadata, playlist architecture, and supported playlist-backed Home sections were processed.")
    print("Banner/profile image, trailer assignment, external links, and thumbnail files still require YouTube Studio or a supported media-upload action.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
