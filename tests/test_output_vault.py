from datetime import datetime, timezone
import os

import pytest

from concrete_motivation.bot_registry import get_bot, list_bots
from concrete_motivation.bot_runner import BotRunner
from concrete_motivation.content_calendar import generate_weekly_calendar
from concrete_motivation.output_vault import BOT_OUTPUT_FOLDERS, CONTENT_CALENDAR_FOLDER, OutputVault
from concrete_motivation.slugify import slugify


@pytest.mark.parametrize(
    ("bot_slug", "folder"),
    sorted(BOT_OUTPUT_FOLDERS.items()),
)
def test_folder_selection_for_all_bots(bot_slug, folder, tmp_path):
    bot = get_bot(bot_slug)

    assert OutputVault(tmp_path).folder_for_bot(bot) == tmp_path / folder


def test_every_bot_has_an_output_folder_mapping():
    assert {bot.slug for bot in list_bots()} == set(BOT_OUTPUT_FOLDERS)


def test_slugify_creates_safe_filename_slugs():
    assert slugify("Starting From the Bottom!!!") == "starting-from-the-bottom"
    assert slugify("Faith & Family / Legacy", max_length=18) == "faith-family"
    assert slugify("!!!") == "output"


def test_markdown_saving_includes_metadata_and_full_output(tmp_path):
    bot = get_bot("motivational_speech")
    response = BotRunner().run(bot, "starting from bottom", "for fathers")
    created = datetime(2026, 6, 23, 12, 0, 0, tzinfo=timezone.utc)

    path = OutputVault(tmp_path).save_response(bot, response, created)
    text = path.read_text(encoding="utf-8")

    assert path.name == "2026-06-23-120000-motivational-speech-starting-from-bottom.md"
    assert path.parent == tmp_path / "speeches"
    assert text.startswith("---\n")
    assert "bot: Motivational Speech Bot" in text
    assert "goal: starting from bottom" in text
    assert "provider: offline" in text
    assert "fallback_used: false" in text
    assert "created_at: 2026-06-23T12:00:00+00:00" in text
    assert "# Motivational Speech Bot" in text
    assert "## Concrete Motivation Angle" in text


def test_recent_saved_outputs_are_newest_first(tmp_path):
    vault = OutputVault(tmp_path)
    bot = get_bot("brand_architect")
    response = BotRunner().run(bot, "build trust")
    older = vault.save_response(bot, response, datetime(2026, 6, 23, 10, 0, 0, tzinfo=timezone.utc))
    newer = vault.save_response(bot, response, datetime(2026, 6, 23, 11, 0, 0, tzinfo=timezone.utc))
    os.utime(older, (100, 100))
    os.utime(newer, (200, 200))

    assert vault.recent_outputs()[:2] == (newer, older)


def test_save_calendar_writes_to_content_calendar_folder(tmp_path):
    calendar = generate_weekly_calendar("discipline under pressure", "for fathers")
    created = datetime(2026, 6, 23, 12, 30, 0, tzinfo=timezone.utc)

    path = OutputVault(tmp_path).save_calendar(calendar, created)
    text = path.read_text(encoding="utf-8")

    assert path.parent == tmp_path / CONTENT_CALENDAR_FOLDER
    assert path.name == "2026-06-23-123000-content-calendar-discipline-under-pressure.md"
    assert "bot: Weekly Content Calendar Engine" in text
    assert "goal: discipline under pressure" in text
    assert "provider: offline" in text
    assert "fallback_used: false" in text
    assert "# Weekly Content Calendar Engine" in text
    assert "## Monday: Mindset Reel" in text


def test_recent_outputs_includes_saved_calendar_files(tmp_path):
    vault = OutputVault(tmp_path)
    calendar = generate_weekly_calendar("discipline")
    path = vault.save_calendar(calendar, datetime(2026, 6, 23, 12, 30, 0, tzinfo=timezone.utc))

    assert path in vault.recent_outputs()
