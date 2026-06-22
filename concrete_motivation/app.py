"""Interactive terminal interface for Concrete Motivation AI."""

from collections.abc import Callable

from .bot_registry import get_bot, list_bots
from .bot_runner import BotRunner

Input = Callable[[str], str]
Output = Callable[[str], None]

BANNER = """====================================
 CONCRETE MOTIVATION AI COMMAND CENTER
===================================="""


def menu() -> str:
    choices = "\n".join(f"{bot.id}. {bot.name}" for bot in list_bots())
    return f"{BANNER}\n\nChoose a bot:\n{choices}\n0. Exit"


def run(input_fn: Input = input, output_fn: Output = print) -> None:
    """Run the menu loop until the user chooses Exit or sends EOF."""
    runner = BotRunner()
    output_fn(menu())
    while True:
        try:
            raw_choice = input_fn("\nEnter your choice (0-8): ").strip()
        except (EOFError, KeyboardInterrupt):
            output_fn("\nKeep building. Goodbye.")
            return

        if raw_choice == "0":
            output_fn("Keep building. Goodbye.")
            return
        try:
            choice = int(raw_choice)
            bot = get_bot(choice)
        except (ValueError, TypeError):
            output_fn("Please enter a number from 0 to 8.")
            continue

        try:
            goal = input_fn("What do you want this bot to create today?\n> ")
            response = runner.run(bot, goal)
        except ValueError as exc:
            output_fn(f"Unable to run bot: {exc}")
            continue
        except (EOFError, KeyboardInterrupt):
            output_fn("\nKeep building. Goodbye.")
            return
        except OSError as exc:
            output_fn(f"Unable to load the bot resources: {exc}")
            continue

        output_fn(f"\n{response.as_markdown()}\n")
        output_fn(menu())
