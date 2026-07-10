"""Batch execution helpers for Concrete Motivation content packages."""

from __future__ import annotations

from pathlib import Path

from concrete_motivation.content_package_models import ContentBatchResult, ContentPackage, ContentPackageExport
from concrete_motivation.content_reels_factory import create_content_package
from concrete_motivation.reels_script_writer import build_day_topic, build_reels_topic


def create_reels_batch(
    theme: str,
    count: int,
    audience: str = "",
    *,
    output_dir: Path | str,
) -> ContentBatchResult:
    """Create and save a batch of reel-focused content packages."""
    if count < 1:
        raise ValueError("count must be at least 1")
    packages: list[ContentPackage] = []
    exports: list[ContentPackageExport] = []
    for index in range(1, count + 1):
        topic = build_reels_topic(theme, index)
        package, export = create_content_package(
            topic,
            audience=audience,
            output_dir=output_dir,
            title_label=f"Reel {index}",
            label=f"reel-{index:02d}",
        )
        packages.append(package)
        exports.append(export)
    return ContentBatchResult(label=f"{theme} reels batch", packages=tuple(packages), exports=tuple(exports))


def create_30_day_content_batch(
    theme: str,
    audience: str = "",
    *,
    output_dir: Path | str,
) -> ContentBatchResult:
    """Create and save a 30-day content batch."""
    packages: list[ContentPackage] = []
    exports: list[ContentPackageExport] = []
    for day in range(1, 31):
        topic = build_day_topic(theme, day)
        package, export = create_content_package(
            topic,
            audience=audience,
            output_dir=output_dir,
            title_label=f"Day {day}",
            label=f"day-{day:02d}",
        )
        packages.append(package)
        exports.append(export)
    return ContentBatchResult(label=f"30-day {theme} batch", packages=tuple(packages), exports=tuple(exports))
