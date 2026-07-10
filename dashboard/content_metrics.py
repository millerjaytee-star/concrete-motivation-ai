"""Content metrics for the Concrete Motivation executive dashboard."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ContentMetrics:
    total_content_packages: int
    total_reels_created: int
    total_shorts_created: int
    youtube_packages: int
    last_generated_content: Path | None

    def as_rows(self) -> tuple[tuple[str, str], ...]:
        last_generated = str(self.last_generated_content) if self.last_generated_content else "None"
        return (
            ("Total content packages", str(self.total_content_packages)),
            ("Total reels created", str(self.total_reels_created)),
            ("Total shorts created", str(self.total_shorts_created)),
            ("YouTube packages created", str(self.youtube_packages)),
            ("Last generated content package", last_generated),
        )

    def weekly_scoreboard_rows(self) -> tuple[tuple[str, str], ...]:
        return (
            ("Content packages ready", str(self.total_content_packages)),
            ("Reels queued", str(self.total_reels_created)),
            ("Shorts queued", str(self.total_shorts_created)),
            ("YouTube packages ready", str(self.youtube_packages)),
        )


def _package_dirs(root: Path, folder_name: str) -> list[Path]:
    folder = root / folder_name
    if not folder.exists():
        return []
    return sorted(
        [path for path in folder.iterdir() if path.is_dir() and (path / "package.md").is_file()],
        key=lambda path: path.name,
    )


def _package_files(root: Path, folder_name: str) -> list[Path]:
    folder = root / folder_name
    if not folder.exists():
        return []
    return sorted([path for path in folder.glob("*.md") if path.is_file()], key=lambda path: path.name)


def build_content_metrics(root: Path | str | None = None) -> ContentMetrics:
    base = Path(root) if root is not None else Path(__file__).resolve().parent.parent
    content_packages = _package_dirs(base, "outputs/content_packages")
    youtube_packages = _package_files(base, "outputs/youtube_packages")
    all_candidates = [path / "package.md" for path in content_packages] + youtube_packages
    last_generated = max(all_candidates, key=lambda path: path.stat().st_mtime) if all_candidates else None

    return ContentMetrics(
        total_content_packages=len(content_packages),
        total_reels_created=sum(1 for path in content_packages if "reel-" in path.name),
        total_shorts_created=sum(1 for path in content_packages if "day-" in path.name),
        youtube_packages=len(youtube_packages),
        last_generated_content=last_generated,
    )
