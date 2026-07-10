"""Build and save Concrete Motivation content packages."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

from concrete_motivation.content_package_models import CONTENT_PACKAGE_FOLDER, ContentPackage, ContentPackageExport
from concrete_motivation.reels_script_writer import build_content_package
from concrete_motivation.slugify import slugify

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / CONTENT_PACKAGE_FOLDER


def _created_at_value(created_at: datetime | None = None) -> datetime:
    return (created_at or datetime.now().astimezone()).replace(microsecond=0)


def save_content_package(
    package: ContentPackage,
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
    *,
    created_at: datetime | None = None,
    label: str = "",
) -> ContentPackageExport:
    """Write a package as Markdown, JSON, and CSV."""
    created = _created_at_value(created_at)
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    parts = [created.strftime("%Y-%m-%d-%H%M%S"), slugify(package.topic)]
    if label.strip():
        parts.append(slugify(label))
    folder = root / "-".join(parts)
    folder.mkdir(parents=True, exist_ok=True)

    markdown_path = folder / "package.md"
    json_path = folder / "package.json"
    csv_path = folder / "package.csv"

    markdown_path.write_text(package.as_markdown(), encoding="utf-8")
    json_path.write_text(json.dumps(package.as_dict(), indent=2), encoding="utf-8")

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(package.as_csv_row().keys()))
        writer.writeheader()
        writer.writerow(package.as_csv_row())

    return ContentPackageExport(folder=folder, markdown_path=markdown_path, json_path=json_path, csv_path=csv_path)


def create_content_package(
    topic: str,
    audience: str = "",
    *,
    platform: str = "YouTube, Shorts, Instagram, Facebook, LinkedIn, Podcast",
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
    title_label: str = "",
    label: str = "",
    created_at: datetime | None = None,
) -> tuple[ContentPackage, ContentPackageExport]:
    """Build and save one offline content package."""
    package = build_content_package(topic, audience=audience, platform=platform, package_label=title_label)
    export = save_content_package(package, output_dir=output_dir, created_at=created_at, label=label)
    return package, export
