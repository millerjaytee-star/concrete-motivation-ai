"""Deterministic copy writer for Concrete Motivation content packages."""

from __future__ import annotations

from dataclasses import replace

from concrete_motivation.content_package_models import ContentPackage
from concrete_motivation.slugify import slugify

DEFAULT_PLATFORM = "YouTube, Shorts, Instagram, Facebook, LinkedIn, Podcast"
DEFAULT_AUDIENCE = "high school and college students, athletes, fathers, and leaders under pressure"
DEFAULT_TAGS = (
    "Concrete Motivation",
    "discipline",
    "consistency",
    "faith",
    "leadership",
    "family",
    "resilience",
    "mindset",
    "pressure",
    "motivation",
)
REEL_ANGLES = (
    "Start Small",
    "Win the Morning",
    "Choose Discipline",
    "Faith Under Pressure",
    "One More Rep",
    "Lead Quietly",
)


def _clean(value: str) -> str:
    return " ".join(value.split()).strip()


def _audience_line(audience: str) -> str:
    clean_audience = _clean(audience)
    return clean_audience or DEFAULT_AUDIENCE


def _topic_title(topic: str) -> str:
    return _clean(topic).title()


def build_content_package(
    topic: str,
    audience: str = "",
    platform: str = DEFAULT_PLATFORM,
    *,
    package_label: str = "",
) -> ContentPackage:
    """Build a complete offline content package from one theme."""
    clean_topic = _clean(topic)
    if not clean_topic:
        raise ValueError("topic cannot be empty")

    clean_audience = _audience_line(audience)
    clean_platform = _clean(platform) or DEFAULT_PLATFORM
    title_topic = _topic_title(clean_topic)
    story_anchor = (
        "This comes from Jaytee Miller's real story: losing multiple siblings, "
        "pushing through adversity, serving as a district leader, raising six children, "
        "and building Concrete Motivation without quitting."
    )
    concept = (
        f"{title_topic} for {clean_audience}. "
        f"{story_anchor} The message is discipline after motivation fades."
    )
    core_message = (
        f"Pressure is not permission to quit. For {clean_audience}, the win is choosing "
        f"discipline, consistency, and faith one decision at a time while {clean_topic} stays heavy."
    )
    title_suffix = package_label.title() if package_label else title_topic
    long_form_title = f"Pressure Has a Purpose: {title_suffix}"
    outline = (
        f"Open with the pressure point: {clean_topic}.",
        "Tell the personal story: loss, adversity, family responsibility, leadership, and the Concrete Motivation build.",
        "State the lesson: discipline is what remains after emotion leaves.",
        "Give one practical action step the audience can use today.",
        "Close with a faith-aware call to keep building one brick at a time.",
    )
    youtube_description = (
        f"In this Concrete Motivation concept, Jaytee Miller speaks directly to {clean_audience} "
        f"about {clean_topic}.\n\n"
        f"{story_anchor}\n\n"
        "This is not fake hype. It is a call to stay disciplined, stay consistent, stay faithful, "
        "and keep building when life gets hard.\n\n"
        "Comment your one concrete commitment for the week. One brick at a time."
    )
    thumbnail_text = "PRESSURE HAS A PURPOSE"
    reel_script = (
        f"Open strong: {clean_topic} is not here to break you. It is here to expose what needs discipline.\n"
        f"Say the truth: {story_anchor}\n"
        "Move the room: when motivation fades, discipline has to speak louder.\n"
        "Give the action step: choose one habit, one promise, and one hard thing to finish today.\n"
        "Close: build through it. Pressure has a purpose."
    )
    short_script = (
        f"Pressure shows you what you trust. If you are {clean_audience}, do not wait for easy.\n"
        "Keep the promise. Stay disciplined. Keep moving.\n"
        "One brick at a time, you become the person pressure was trying to build."
    )
    hook = (
        f"Pressure is not the enemy. It is the test.\n"
        f"If you are {clean_audience}, listen to this before you quit."
    )
    instagram_caption = (
        f"Pressure has a purpose.\n\n"
        f"{story_anchor}\n\n"
        "For everybody carrying more than they talk about: keep your head up, keep your word, "
        "and keep building one brick at a time.\n\n"
        "#ConcreteMotivation #Discipline #Faith #Consistency #Leadership #Family"
    )
    facebook_caption = (
        f"Pressure has a purpose, especially for {clean_audience} who are trying to build through hard seasons.\n\n"
        f"{story_anchor}\n\n"
        "The answer is not quitting. The answer is discipline, consistency, faith, and one concrete step today.\n"
        "Build through it."
    )
    linkedin_post = (
        f"Pressure has a purpose.\n\n"
        f"{story_anchor}\n\n"
        f"For {clean_audience}, the leadership lesson is simple: consistency beats emotion, "
        "discipline beats delay, and faith keeps the mission steady when the pressure gets loud.\n\n"
        "The next step is not complicated. Decide what matters. Execute one promise. Repeat tomorrow."
    )
    podcast_segment = (
        f"Podcast segment idea: a grounded conversation about {clean_topic}, framed around what pressure "
        "teaches when nobody is clapping.\n"
        "Pull the story of loss, responsibility, leadership, and the Concrete Motivation build into a 3 to 5 minute segment.\n"
        "End with a practical challenge: name one habit that proves you are still in the fight."
    )
    call_to_action = "Comment your concrete commitment, save the package for review, and build one brick today."
    repurpose_plan = (
        "Turn the hook into a 15-second Short.",
        "Cut the reel into a 30-second version for Shorts and Reels.",
        "Use the LinkedIn post as a leadership post for professionals and parents.",
        "Turn the podcast segment into a teaser clip and captioned quote card.",
        "Repurpose the YouTube title and thumbnail notes for the next upload queue.",
    )
    return ContentPackage(
        topic=clean_topic,
        audience=clean_audience,
        core_message=core_message,
        platform=clean_platform,
        youtube_concept=concept,
        long_form_youtube_title=long_form_title,
        long_form_youtube_outline=outline,
        youtube_description=youtube_description,
        youtube_tags=DEFAULT_TAGS,
        thumbnail_text=thumbnail_text,
        reel_60_second_script=reel_script,
        short_30_second_script=short_script,
        hook_15_second_script=hook,
        instagram_caption=instagram_caption,
        facebook_caption=facebook_caption,
        linkedin_post=linkedin_post,
        podcast_segment=podcast_segment,
        call_to_action=call_to_action,
        repurpose_plan=repurpose_plan,
    )


def build_reels_topic(theme: str, index: int) -> str:
    clean_theme = _clean(theme)
    if not clean_theme:
        raise ValueError("theme cannot be empty")
    angle = REEL_ANGLES[(index - 1) % len(REEL_ANGLES)]
    return f"{clean_theme}: {angle}"


def build_day_topic(theme: str, day_number: int) -> str:
    clean_theme = _clean(theme)
    if not clean_theme:
        raise ValueError("theme cannot be empty")
    return f"Day {day_number}: {clean_theme}"


def with_package_label(package: ContentPackage, label: str) -> ContentPackage:
    """Return a package with the title adjusted for a batch label."""
    clean_label = _clean(label)
    if not clean_label:
        return package
    return replace(package, long_form_youtube_title=f"{package.long_form_youtube_title} ({clean_label.title()})")


def package_slug(topic: str) -> str:
    return slugify(topic)
