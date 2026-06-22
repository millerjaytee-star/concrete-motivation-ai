from dataclasses import replace

import pytest

from concrete_motivation.bot_registry import list_bots
from concrete_motivation.bot_runner import BotRunner


@pytest.mark.parametrize("bot", list_bots(), ids=lambda bot: bot.slug)
def test_every_bot_returns_its_required_sections(bot):
    response = BotRunner().run(bot, "build discipline after a setback")

    assert response.bot_name == bot.name
    assert response.goal == "build discipline after a setback"
    assert tuple(heading for heading, _ in response.sections) == bot.sections
    assert all(body.strip() for _, body in response.sections)
    assert "build discipline after a setback" in response.as_markdown().lower()


@pytest.mark.parametrize("goal", ["", "   ", "\n\t"])
def test_empty_goal_is_rejected(goal):
    with pytest.raises(ValueError, match="Goal cannot be empty"):
        BotRunner().run(list_bots()[0], goal)


def test_goal_whitespace_is_normalized():
    response = BotRunner().run(list_bots()[0], "  build   a brand\npeople trust ")

    assert response.goal == "build a brand people trust"


def test_missing_prompt_is_reported(tmp_path):
    bot = replace(list_bots()[0], prompt_file=tmp_path / "missing.md")

    with pytest.raises(FileNotFoundError, match="Prompt file not found"):
        BotRunner().run(bot, "create a message")
