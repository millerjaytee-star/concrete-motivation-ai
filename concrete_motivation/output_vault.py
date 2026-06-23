"""Local Markdown output vault for generated bot responses."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from concrete_motivation.content_calendar import CALENDAR_NAME, WeeklyContentCalendar
from concrete_motivation.models import Bot, BotResponse
from concrete_motivation.slugify import slugify

VAULT_DIR = Path(__file__).resolve().parent.parent / "outputs"
CONTENT_CALENDAR_FOLDER = "content_calendars"

BOT_OUTPUT_FOLDERS: dict[str, str] = {
    "brand_architect": "brand",
    "motivational_speech": "speeches",
    "concrete_conversations_podcast": "podcast_episodes",
    "social_media_content": "social_posts",
    "athlete_outreach": "outreach_messages",
    "business_growth": "business_growth",
    "operations": "operations",
    "faith_mindset": "faith_mindset",
}


@dataclass(frozen=True, slots=True)
class OutputVault:
    """Save and list local Markdown assets."""

    root: Path = VAULT_DIR

    def ensure_folders(self) -> None:
        """Create every content vault folder when missing."""
        for folder_name in (*BOT_OUTPUT_FOLDERS.values(), CONTENT_CALENDAR_FOLDER):
            (self.root / folder_name).mkdir(parents=True, exist_ok=True)

    def folder_for_bot(self, bot: Bot) -> Path:
        """Return the destination folder for a bot."""
        try:
            folder_name = BOT_OUTPUT_FOLDERS[bot.slug]
        except KeyError as exc:
            raise ValueError(f"No output folder configured for {bot.name}.") from exc
        return self.root / folder_name

    def filename_for(self, bot: Bot, goal: str, created_at: datetime) -> str:
        """Build the safe Markdown filename for a response."""
        timestamp = created_at.strftime("%Y-%m-%d-%H%M%S")
        bot_slug = slugify(bot.slug)
        goal_slug = slugify(goal)
        return f"{timestamp}-{bot_slug}-{goal_slug}.md"

    def save_response(
        self,
        bot: Bot,
        response: BotResponse,
        created_at: datetime | None = None,
    ) -> Path:
        """Save a bot response with metadata and return the written path."""
        created = (created_at or datetime.now().astimezone()).replace(microsecond=0)
        folder = self.folder_for_bot(bot)
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / self.filename_for(bot, response.goal, created)
        metadata = "\n".join(
            (
                "---",
                f"bot: {response.bot_name}",
                f"goal: {response.goal}",
                f"provider: {response.provider_name}",
                f"fallback_used: {str(response.fallback_used).lower()}",
                f"created_at: {created.isoformat()}",
                "---",
            )
        )
        path.write_text(f"{metadata}\n\n{response.as_markdown()}\n", encoding="utf-8")
        return path

    def save_calendar(
        self,
        calendar: WeeklyContentCalendar,
        created_at: datetime | None = None,
    ) -> Path:
        """Save a weekly content calendar with metadata and return the written path."""
        created = (created_at or datetime.now().astimezone()).replace(microsecond=0)
        folder = self.root / CONTENT_CALENDAR_FOLDER
        folder.mkdir(parents=True, exist_ok=True)
        timestamp = created.strftime("%Y-%m-%d-%H%M%S")
        path = folder / f"{timestamp}-content-calendar-{slugify(calendar.theme)}.md"
        metadata = "\n".join(
            (
                "---",
                f"bot: {CALENDAR_NAME}",
                f"goal: {calendar.theme}",
                f"provider: {calendar.provider_name}",
                f"fallback_used: {str(calendar.fallback_used).lower()}",
                f"created_at: {created.isoformat()}",
                "---",
            )
        )
        path.write_text(f"{metadata}\n\n{calendar.as_markdown()}\n", encoding="utf-8")
        return path

    def recent_outputs(self, limit: int = 10) -> tuple[Path, ...]:
        """Return recently saved Markdown files, newest first."""
        if not self.root.exists():
            return ()
        files = [path for path in self.root.rglob("*.md") if path.is_file()]
        files.sort(key=lambda path: (path.stat().st_mtime, str(path)), reverse=True)
        return tuple(files[:limit])
