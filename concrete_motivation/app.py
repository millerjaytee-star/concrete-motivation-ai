"""Interactive terminal interface for Concrete Motivation AI."""

from collections.abc import Callable

from .bot_registry import get_bot, list_bots
from .bot_runner import BotRunner
from .content_calendar import generate_weekly_calendar
from .executive_suite import ExecutiveSuite
from .output_vault import OutputVault

Input = Callable[[str], str]
Output = Callable[[str], None]

BANNER = """====================================
 CONCRETE MOTIVATION AI COMMAND CENTER
===================================="""


def menu() -> str:
    choices = "\n".join(f"{bot.id}. {bot.name}" for bot in list_bots())
    return f"{BANNER}\n\nChoose a bot:\n{choices}\n9. View recent saved outputs\n10. Weekly Content Calendar Engine\n11. Executive Team Full Brand Run\n0. Exit"


def run(input_fn: Input = input, output_fn: Output = print, vault: OutputVault | None = None) -> None:
    """Run the menu loop until the user chooses Exit or sends EOF."""
    runner = BotRunner()
    output_vault = vault or OutputVault()
    output_vault.ensure_folders()
    output_fn(f"Provider: {runner.provider_name}")
    output_fn(menu())
    while True:
        try:
            raw_choice = input_fn("\nEnter your choice (0-11): ").strip()
        except (EOFError, KeyboardInterrupt):
            output_fn("\nKeep building. Goodbye.")
            return

        if raw_choice == "0":
            output_fn("Keep building. Goodbye.")
            return
        if raw_choice == "9":
            recent = output_vault.recent_outputs()
            if recent:
                output_fn("Recent saved outputs:\n" + "\n".join(str(path) for path in recent))
            else:
                output_fn("No saved outputs yet.")
            output_fn(menu())
            continue
        if raw_choice == "10":
            try:
                theme = input_fn("What is the main theme for this week?\n> ")
                detail = input_fn("Any audience, platform, event, or business goal to include? Press Enter to skip.\n> ")
                calendar = generate_weekly_calendar(theme, detail)
            except ValueError as exc:
                output_fn(f"Unable to create calendar: {exc}")
                continue
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return

            output_fn(f"\n{calendar.as_markdown()}\n")
            try:
                save_choice = input_fn("Save this output to the content vault? [Y/n] ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return
            if save_choice in {"", "y", "yes"}:
                saved_path = output_vault.save_calendar(calendar)
                output_fn(f"Saved to content vault: {saved_path}")
            else:
                output_fn("Output was not saved.")
            output_fn(menu())
            continue
        if raw_choice == "11":
            try:
                theme = input_fn("What is the executive theme for this brand run?\n> ")
                audience = input_fn("Who are we serving with this run? Press Enter for 'the masses'.\n> ")
                result = ExecutiveSuite().run(theme, audience)
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return
            except OSError as exc:
                output_fn(f"Unable to write executive suite files: {exc}")
                continue
            output_fn(f"\n{result.as_markdown()}\n")
            output_fn(menu())
            continue
        try:
            choice = int(raw_choice)
            bot = get_bot(choice)
        except (ValueError, TypeError):
            output_fn("Please enter a number from 0 to 11.")
            continue

        try:
            goal = input_fn("What do you want this bot to create today?\n> ")
            personalization_detail = input_fn(
                "Any specific audience, tone, or personal detail to include? Press Enter to skip.\n> "
            )
            response = runner.run(bot, goal, personalization_detail)
        except ValueError as exc:
            output_fn(f"Unable to run bot: {exc}")
            continue
        except (EOFError, KeyboardInterrupt):
            output_fn("\nKeep building. Goodbye.")
            return
        except OSError as exc:
            output_fn(f"Unable to load the bot resources: {exc}")
            continue

        if response.fallback_used:
            output_fn("OpenAI generation was unavailable, so offline mode was used for this response.")
        output_fn(f"\n{response.as_markdown()}\n")
        try:
            save_choice = input_fn("Save this output to the content vault? [Y/n] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            output_fn("\nKeep building. Goodbye.")
            return
        if save_choice in {"", "y", "yes"}:
            saved_path = output_vault.save_response(bot, response)
            output_fn(f"Saved to content vault: {saved_path}")
        else:
            output_fn("Output was not saved.")
        output_fn(menu())
