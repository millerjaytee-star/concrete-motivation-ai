"""The central registry for all Concrete Motivation specialists."""

from pathlib import Path

from .models import Bot

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"


def _prompt_path(slug: str) -> Path:
    path = PROMPT_DIR / f"{slug}.md"
    if path.is_dir():
        return path / "PROMPT.md"
    return path


def _bot(
    bot_id: int,
    slug: str,
    name: str,
    purpose: str,
    sections: tuple[str, ...],
) -> Bot:
    return Bot(bot_id, slug, name, purpose, _prompt_path(slug), sections)


BOTS: tuple[Bot, ...] = (
    _bot(1, "brand_architect", "Brand Architect Bot", "Define and protect the brand.",
         ("Brand message", "Audience", "Tone", "Offer idea", "Next action")),
    _bot(2, "motivational_speech", "Motivational Speech Bot", "Create original, high-energy speeches.",
         ("Title", "Opening hook", "Main speech", "Crowd engagement lines", "Closing call-to-action")),
    _bot(3, "concrete_conversations_podcast", "Concrete Conversations Podcast Bot", "Build purposeful podcast episodes.",
         ("Episode title", "Episode promise", "Intro", "Segments", "Guest questions", "Clip moments", "Outro")),
    _bot(4, "social_media_content", "Social Media Content Bot", "Turn ideas into platform-ready content.",
         ("Hooks", "Short-form script", "Caption", "Hashtags", "Repurpose ideas")),
    _bot(5, "athlete_outreach", "Athlete Outreach Bot", "Open doors with athletes and sports leaders.",
         ("Target audience", "Message angle", "DM/email draft", "Follow-up message", "Offer")),
    _bot(6, "business_growth", "Business Growth Bot", "Build practical revenue and partnership plans.",
         ("Opportunity", "Offer/package", "Pricing idea", "Sales action", "Partnership angle")),
    _bot(7, "operations", "Operations Bot", "Turn ideas into accountable execution.",
         ("Weekly priorities", "Task checklist", "SOP idea", "Owner", "Deadline suggestions")),
    _bot(8, "faith_mindset", "Faith & Mindset Bot", "Create spiritually grounded mindset content.",
         ("Theme", "Reflection", "Scripture-inspired principle", "Practical action", "Closing affirmation")),
    _bot(9, "ceo", "CEO Bot", "Set executive priorities, standards, and decisions.",
         ("Executive decision", "Top priorities", "Scoreboard", "Risks", "Next command")),
    _bot(10, "content_director", "Content Director Bot", "Plan campaigns across every brand channel.",
         ("Campaign thesis", "Channel plan", "Content pillars", "Production queue", "Publishing rhythm")),
    _bot(11, "podcast_producer", "Podcast Producer Bot", "Produce Concrete Conversations episodes end to end.",
         ("Episode concept", "Run of show", "Guest prep", "Clip plan", "Production checklist")),
    _bot(12, "sales_outreach", "Sales Outreach Bot", "Create sales messaging for speaking, sponsors, and partners.",
         ("Target segment", "Offer angle", "Email draft", "Call script", "Follow-up plan")),
    _bot(13, "youtube_growth", "YouTube Growth Bot", "Grow the YouTube channel with searchable, repeatable video systems.",
         ("Video opportunity", "Title and thumbnail angles", "Retention plan", "Shorts plan", "Next upload actions")),
    _bot(14, "crm", "CRM Bot", "Organize leads, pipeline stages, and next actions.",
         ("Pipeline snapshot", "Lead segments", "Next actions", "Follow-up schedule", "Data fields")),
    _bot(15, "gmail_outreach", "Gmail Outreach Workflow", "Draft Gmail-ready outreach workflows and follow-ups.",
         ("Workflow goal", "Search or lead list", "Message sequence", "Tracking rules", "Daily execution checklist")),
)

_BOTS_BY_ID = {bot.id: bot for bot in BOTS}
_BOTS_BY_SLUG = {bot.slug: bot for bot in BOTS}

BOT_GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "Brand and Content",
        (
            "brand_architect",
            "motivational_speech",
            "concrete_conversations_podcast",
            "social_media_content",
            "faith_mindset",
        ),
    ),
    (
        "Growth and Revenue",
        (
            "athlete_outreach",
            "business_growth",
            "sales_outreach",
            "youtube_growth",
        ),
    ),
    (
        "Operations and Workflows",
        (
            "operations",
            "ceo",
            "content_director",
            "podcast_producer",
            "crm",
            "gmail_outreach",
        ),
    ),
)


def list_bots() -> tuple[Bot, ...]:
    """Return all bots in menu order."""
    return BOTS


def grouped_bots() -> tuple[tuple[str, tuple[Bot, ...]], ...]:
    """Return bots grouped for command center display."""
    groups: list[tuple[str, tuple[Bot, ...]]] = []
    for label, slugs in BOT_GROUPS:
        groups.append((label, tuple(get_bot(slug) for slug in slugs)))
    return tuple(groups)


def get_bot(identifier: int | str) -> Bot:
    """Find a bot by menu number or slug."""
    bot = _BOTS_BY_ID.get(identifier) if isinstance(identifier, int) else _BOTS_BY_SLUG.get(identifier)
    if bot is None:
        raise ValueError(f"Unknown bot: {identifier}")
    return bot
