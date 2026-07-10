"""The central registry for all Concrete Motivation specialists."""

from pathlib import Path

from .models import Bot

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"


def _bot(
    bot_id: int,
    slug: str,
    name: str,
    purpose: str,
    sections: tuple[str, ...],
) -> Bot:
    return Bot(bot_id, slug, name, purpose, PROMPT_DIR / f"{slug}.md", sections)


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
    _bot(9, "ceo_bot", "CEO Bot", "Coordinate the launch operating system across content, revenue, and operations.",
         ("Executive decision", "Launch scoreboard", "System alignment", "Risk controls", "Next 72 hours")),
)

_BOTS_BY_ID = {bot.id: bot for bot in BOTS}
_BOTS_BY_SLUG = {bot.slug: bot for bot in BOTS}


def list_bots() -> tuple[Bot, ...]:
    """Return all bots in menu order."""
    return BOTS


def get_bot(identifier: int | str) -> Bot:
    """Find a bot by menu number or slug."""
    bot = _BOTS_BY_ID.get(identifier) if isinstance(identifier, int) else _BOTS_BY_SLUG.get(identifier)
    if bot is None:
        raise ValueError(f"Unknown bot: {identifier}")
    return bot
