"""Interactive terminal interface for Concrete Motivation AI."""

from collections.abc import Callable

from .bot_registry import get_bot, grouped_bots, list_bots
from .bot_runner import BotRunner
from .crm_pipeline_manager import CRMPipelineManager
from .content_reels_factory import create_content_package
from .content_calendar import generate_weekly_calendar
from .executive_suite import ExecutiveSuite
from .forever_brand import ForeverBrandFactory
from .podcast_guest_bot import PodcastGuestBot
from .output_vault import OutputVault
from .school_outreach_bot import SchoolOutreachBot
from .sponsorship_bot import SponsorshipBot
from .youtube_publish_package import build_package, build_execute_command, save_package
from .system_check import run_system_check
from dashboard.metrics import build_dashboard_metrics

Input = Callable[[str], str]
Output = Callable[[str], None]

BANNER = """====================================
 CONCRETE MOTIVATION AI COMMAND CENTER
===================================="""


BOT_COUNT = len(list_bots())
RECENT_OUTPUTS_CHOICE = BOT_COUNT + 1
CALENDAR_CHOICE = BOT_COUNT + 2
EXECUTIVE_SUITE_CHOICE = BOT_COUNT + 3
FOREVER_BRAND_CHOICE = BOT_COUNT + 4
SYSTEM_CHECK_CHOICE = BOT_COUNT + 5
SCHOOL_OUTREACH_CHOICE = BOT_COUNT + 6
SPONSORSHIP_CHOICE = BOT_COUNT + 7
PODCAST_GUEST_CHOICE = BOT_COUNT + 8
CRM_PIPELINE_CHOICE = BOT_COUNT + 9
EXECUTIVE_DASHBOARD_CHOICE = BOT_COUNT + 10
CRM_DASHBOARD_CHOICE = BOT_COUNT + 11
SCHOOL_OUTREACH_CAMPAIGN_CHOICE = BOT_COUNT + 12
SPONSOR_CAMPAIGN_CHOICE = BOT_COUNT + 13
PODCAST_CAMPAIGN_CHOICE = BOT_COUNT + 14
CONTENT_PACKAGE_CHOICE = BOT_COUNT + 15
YOUTUBE_PACKAGE_CHOICE = BOT_COUNT + 16
YOUTUBE_DRY_RUN_CHOICE = BOT_COUNT + 17
MAX_CHOICE = YOUTUBE_DRY_RUN_CHOICE


def menu() -> str:
    group_blocks = []
    for group_name, bots in grouped_bots():
        lines = [f"[{group_name}]"]
        lines.extend(f"{bot.id}. {bot.name} - {bot.purpose}" for bot in bots)
        group_blocks.append("\n".join(lines))
    choices = "\n\n".join(group_blocks)
    return (
        f"{BANNER}\n\nChoose a bot or workflow:\n"
        f"{choices}\n"
        f"{RECENT_OUTPUTS_CHOICE}. View recent saved outputs\n"
        f"{CALENDAR_CHOICE}. Weekly Content Calendar Engine\n"
        f"{EXECUTIVE_SUITE_CHOICE}. Executive Team Full Brand Run\n"
        f"{FOREVER_BRAND_CHOICE}. Forever Brand Factory\n"
        f"{SYSTEM_CHECK_CHOICE}. System Check\n"
        f"{SCHOOL_OUTREACH_CHOICE}. School Outreach Workflow\n"
        f"{SPONSORSHIP_CHOICE}. Sponsor Outreach Workflow\n"
        f"{PODCAST_GUEST_CHOICE}. Podcast Guest Workflow\n"
        f"{CRM_PIPELINE_CHOICE}. CRM Pipeline Manager\n"
        f"{EXECUTIVE_DASHBOARD_CHOICE}. Executive Dashboard\n"
        f"{CRM_DASHBOARD_CHOICE}. CRM Dashboard\n"
        f"{SCHOOL_OUTREACH_CAMPAIGN_CHOICE}. School Outreach Campaign\n"
        f"{SPONSOR_CAMPAIGN_CHOICE}. Sponsor Campaign\n"
        f"{PODCAST_CAMPAIGN_CHOICE}. Podcast Guest Campaign\n"
        f"{CONTENT_PACKAGE_CHOICE}. Content/Reels Package\n"
        f"{YOUTUBE_PACKAGE_CHOICE}. YouTube Package\n"
        f"{YOUTUBE_DRY_RUN_CHOICE}. YouTube Upload Dry Run\n"
        "H. Help / recommended workflow\n"
        "0. Exit"
    )


def help_text() -> str:
    """Return a concise command center usage guide."""
    return """# Command Center Help

Recommended daily workflow:
1. Use CEO Bot to choose the priority.
2. Use Content Director Bot or Weekly Content Calendar Engine to turn it into publishable work.
3. Use Sales Outreach Bot, CRM Bot, or Gmail Outreach Workflow to move relationships forward.
4. Use School Outreach, Sponsor Outreach, Podcast Guest, and CRM Pipeline workflows to keep the pipeline moving.
5. Use the Executive Dashboard and CRM Dashboard to check the scoreboard before starting new work.
6. Save strong outputs to the vault, then edit them in Jaytee's final voice before posting or sending.

Strong goals are specific:
- Build a school speaking outreach campaign for high school athletes.
- Create a YouTube launch plan for discipline after setbacks.
- Draft a podcast episode with three clip moments and guest questions.
- Review the Executive Dashboard before starting new work.
- Use the CRM Dashboard to clear follow-ups before the day ends.

Use System Check before a serious work session or before pushing changes."""


def run(input_fn: Input = input, output_fn: Output = print, vault: OutputVault | None = None) -> None:
    """Run the menu loop until the user chooses Exit or sends EOF."""
    runner = BotRunner()
    output_vault = vault or OutputVault()
    output_vault.ensure_folders()
    output_fn(f"Provider: {runner.provider_name}")
    output_fn(menu())
    while True:
        try:
            raw_choice = input_fn(f"\nEnter your choice (0-{MAX_CHOICE}): ").strip()
        except (EOFError, KeyboardInterrupt):
            output_fn("\nKeep building. Goodbye.")
            return

        if raw_choice == "0":
            output_fn("Keep building. Goodbye.")
            return
        if raw_choice.lower() in {"h", "help", "?"}:
            output_fn(f"\n{help_text()}\n")
            output_fn(menu())
            continue
        if raw_choice == str(RECENT_OUTPUTS_CHOICE):
            recent = output_vault.recent_outputs()
            if recent:
                output_fn("Recent saved outputs:\n" + "\n".join(str(path) for path in recent))
            else:
                output_fn("No saved outputs yet.")
            output_fn(menu())
            continue
        if raw_choice == str(CALENDAR_CHOICE):
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
        if raw_choice == str(EXECUTIVE_SUITE_CHOICE):
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
        if raw_choice == str(FOREVER_BRAND_CHOICE):
            try:
                theme = input_fn("What is the forever brand theme? Press Enter for Built Under Pressure.\n> ")
                result = ForeverBrandFactory().run(theme)
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return
            except OSError as exc:
                output_fn(f"Unable to write forever brand files: {exc}")
                continue
            output_fn(f"\n{result.as_markdown()}\n")
            output_fn(menu())
            continue
        if raw_choice == str(SYSTEM_CHECK_CHOICE):
            result = run_system_check()
            output_fn(f"\n{result.as_markdown()}\n")
            output_fn(menu())
            continue
        if raw_choice == str(SCHOOL_OUTREACH_CHOICE):
            try:
                theme = input_fn("What school outreach theme should we build around?\n> ")
                audience = input_fn("Who should this speak to? Press Enter for high school athletes.\n> ")
                result = SchoolOutreachBot().run(theme, audience)
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return
            except OSError as exc:
                output_fn(f"Unable to write school outreach files: {exc}")
                continue
            output_fn(f"\n{result.as_markdown()}\n")
            output_fn(menu())
            continue
        if raw_choice == str(SPONSORSHIP_CHOICE):
            try:
                theme = input_fn("What sponsorship theme should we build around?\n> ")
                audience = input_fn("Who should this speak to? Press Enter for community partners and local brands.\n> ")
                result = SponsorshipBot().run(theme, audience)
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return
            except OSError as exc:
                output_fn(f"Unable to write sponsorship files: {exc}")
                continue
            output_fn(f"\n{result.as_markdown()}\n")
            output_fn(menu())
            continue
        if raw_choice == str(PODCAST_GUEST_CHOICE):
            try:
                theme = input_fn("What podcast guest theme should we build around?\n> ")
                audience = input_fn("Who should this speak to? Press Enter for leaders and creators.\n> ")
                result = PodcastGuestBot().run(theme, audience)
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return
            except OSError as exc:
                output_fn(f"Unable to write podcast guest files: {exc}")
                continue
            output_fn(f"\n{result.as_markdown()}\n")
            output_fn(menu())
            continue
        if raw_choice == str(CRM_PIPELINE_CHOICE):
            try:
                theme = input_fn("What CRM pipeline theme should we build around?\n> ")
                audience = input_fn("Who is this pipeline for? Press Enter for core leads.\n> ")
                result = CRMPipelineManager().run(theme, audience)
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return
            except OSError as exc:
                output_fn(f"Unable to write CRM pipeline files: {exc}")
                continue
            output_fn(f"\n{result.as_markdown()}\n")
            output_fn(menu())
            continue
        if raw_choice == str(EXECUTIVE_DASHBOARD_CHOICE):
            dashboard = build_dashboard_metrics()
            output_fn(f"\n{dashboard.as_markdown()}\n")
            output_fn(menu())
            continue
        if raw_choice == str(CRM_DASHBOARD_CHOICE):
            dashboard = CRMPipelineManager().dashboard_markdown()
            output_fn(f"\n{dashboard}\n")
            output_fn(menu())
            continue
        if raw_choice == str(SCHOOL_OUTREACH_CAMPAIGN_CHOICE):
            try:
                audience = input_fn("Who should this speak to? Press Enter for high school athletes.\n> ")
                region = input_fn("What region should we target? Press Enter to skip.\n> ")
                result = SchoolOutreachBot().run("Pressure Has a Purpose", audience, region)
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return
            except OSError as exc:
                output_fn(f"Unable to write school outreach files: {exc}")
                continue
            output_fn(f"\n{result.as_markdown()}\n")
            output_fn(menu())
            continue
        if raw_choice == str(SPONSOR_CAMPAIGN_CHOICE):
            try:
                segment = input_fn("What sponsor segment should we target? Press Enter for local gyms and barbershops.\n> ")
                audience = input_fn("Who should this speak to? Press Enter for community partners and local brands.\n> ")
                result = SponsorshipBot().run("Pressure Has a Purpose", audience, segment)
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return
            except OSError as exc:
                output_fn(f"Unable to write sponsorship files: {exc}")
                continue
            output_fn(f"\n{result.as_markdown()}\n")
            output_fn(menu())
            continue
        if raw_choice == str(PODCAST_CAMPAIGN_CHOICE):
            try:
                theme = input_fn("What podcast guest theme should we use? Press Enter for pressure to purpose.\n> ")
                audience = input_fn("Who should this speak to? Press Enter for leaders and creators.\n> ")
                result = PodcastGuestBot().run(theme or "pressure to purpose", audience)
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return
            except OSError as exc:
                output_fn(f"Unable to write podcast guest files: {exc}")
                continue
            output_fn(f"\n{result.as_markdown()}\n")
            output_fn(menu())
            continue
        if raw_choice == str(CONTENT_PACKAGE_CHOICE):
            try:
                topic = input_fn("What content theme should we package today?\n> ")
                audience = input_fn("Who is this for? Press Enter to skip.\n> ")
                package, export = create_content_package(topic, audience=audience)
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return
            except (OSError, ValueError) as exc:
                output_fn(f"Unable to write content package: {exc}")
                continue
            output_fn(f"\n{package.as_markdown()}\n")
            output_fn(f"Saved markdown: {export.markdown_path}")
            output_fn(menu())
            continue
        if raw_choice == str(YOUTUBE_PACKAGE_CHOICE):
            try:
                topic = input_fn("What YouTube topic should we package today?\n> ")
                video_path = input_fn("What local video path should be included?\n> ")
                visibility = input_fn("Visibility [private/unlisted/public]? Press Enter for private.\n> ").strip() or "private"
                package = build_package(topic, video_path=video_path, visibility=visibility)
                saved = save_package(package)
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return
            except (OSError, ValueError) as exc:
                output_fn(f"Unable to write YouTube package: {exc}")
                continue
            output_fn(f"\n{package.as_markdown()}\n")
            output_fn(f"Saved package: {saved}")
            output_fn(menu())
            continue
        if raw_choice == str(YOUTUBE_DRY_RUN_CHOICE):
            try:
                topic = input_fn("What YouTube topic should we preview?\n> ")
                video_path = input_fn("What local video path should be included?\n> ")
                visibility = input_fn("Visibility [private/unlisted/public]? Press Enter for private.\n> ").strip() or "private"
                package = build_package(topic, video_path=video_path, visibility=visibility)
                command = build_execute_command(package)
            except (EOFError, KeyboardInterrupt):
                output_fn("\nKeep building. Goodbye.")
                return
            except (OSError, ValueError, FileNotFoundError) as exc:
                output_fn(f"Unable to prepare YouTube dry run: {exc}")
                output_fn("Recovery command: composio link youtube")
                continue
            output_fn(f"\n{package.as_markdown()}\n")
            output_fn("Dry run command:")
            output_fn(" ".join(command))
            output_fn(menu())
            continue
        try:
            choice = int(raw_choice)
            bot = get_bot(choice)
        except (ValueError, TypeError):
            output_fn(f"Please enter a number from 0 to {MAX_CHOICE}.")
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
