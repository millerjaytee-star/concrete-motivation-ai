"""Legacy compatibility wrapper for the Concrete Motivation bot team."""

from __future__ import annotations

from concrete_motivation.app import run as run_command_center
from concrete_motivation.bot_registry import get_bot, list_bots
from concrete_motivation.bot_runner import BotRunner


def run() -> None:
    """Launch the current Concrete Motivation command center."""
    run_command_center()


def run_bot(identifier: int | str, goal: str, personalization_detail: str = ""):
    """Run one registered bot from older scripts that imported Core.division_manager."""
    bot = get_bot(identifier)
    return BotRunner().run(bot, goal, personalization_detail)


__all__ = ["get_bot", "list_bots", "run", "run_bot"]


if __name__ == "__main__":
    run()
