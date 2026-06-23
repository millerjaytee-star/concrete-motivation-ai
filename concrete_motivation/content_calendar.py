"""Weekly content calendar generation for Concrete Motivation."""

from __future__ import annotations

from dataclasses import dataclass


CALENDAR_NAME = "Weekly Content Calendar Engine"


@dataclass(frozen=True, slots=True)
class CalendarDay:
    """One day in a weekly content calendar."""

    day: str
    content_type: str
    hook: str
    script_or_caption: str
    call_to_action: str
    recommended_platform: str
    repurpose_idea: str


@dataclass(frozen=True, slots=True)
class WeeklyContentCalendar:
    """A structured 7-day content calendar."""

    theme: str
    detail: str
    days: tuple[CalendarDay, ...]
    provider_name: str = "offline"
    fallback_used: bool = False

    def as_markdown(self) -> str:
        """Render the calendar as Markdown for the terminal and vault."""
        blocks = [
            f"# {CALENDAR_NAME}",
            f"**Theme:** {self.theme}",
        ]
        if self.detail:
            blocks.append(f"**Detail:** {self.detail}")
        for day in self.days:
            blocks.append(
                "\n".join(
                    (
                        f"## {day.day}: {day.content_type}",
                        f"**Day:** {day.day}",
                        f"**Content type:** {day.content_type}",
                        f"**Hook:** {day.hook}",
                        f"**Short script or caption:** {day.script_or_caption}",
                        f"**Call to action:** {day.call_to_action}",
                        f"**Recommended platform:** {day.recommended_platform}",
                        f"**Repurpose idea:** {day.repurpose_idea}",
                    )
                )
            )
        return "\n\n".join(blocks)


def generate_weekly_calendar(theme: str, detail: str = "") -> WeeklyContentCalendar:
    """Generate a Concrete Motivation 7-day execution calendar."""
    clean_theme = " ".join(theme.split())
    if not clean_theme:
        raise ValueError("Theme cannot be empty.")
    clean_detail = " ".join(detail.split())
    detail_clause = f" Tie it to this context: {clean_detail}." if clean_detail else ""
    audience_line = clean_detail or "athletes, fathers, leaders, and people rebuilding under pressure"

    days = (
        CalendarDay(
            "Monday",
            "Mindset Reel",
            f"You do not wait for pressure to leave before you build discipline around {clean_theme}.",
            f"Open with the weight people are carrying, name the Concrete Motivation truth, then give one disciplined action connected to {clean_theme}.{detail_clause}",
            "Comment with the one promise you will keep before the day ends.",
            "Instagram Reels, TikTok, YouTube Shorts",
            "Turn the strongest line into a quote card and use the action step as a Story poll.",
        ),
        CalendarDay(
            "Tuesday",
            "Podcast Clip",
            f"The real conversation about {clean_theme} starts where the highlight reel stops.",
            f"Pull a 45-60 second Concrete Conversations-style clip about the honest tension behind {clean_theme}, then land it with practical movement for this audience or context: {audience_line}.",
            "Send this clip to someone who needs a real conversation, not empty hype.",
            "Instagram Reels, YouTube Shorts, Facebook",
            "Use the clip transcript as a carousel and a podcast newsletter teaser.",
        ),
        CalendarDay(
            "Wednesday",
            "Athlete/Youth Message",
            f"Talent does not carry you when {clean_theme} starts testing your habits.",
            f"Speak directly to young competitors: pressure is not punishment, it is a place to practice discipline, leadership, and execution.{detail_clause}",
            "Share this with a teammate, student, or young person who needs the next right step.",
            "Instagram, TikTok, team group chats",
            "Adapt the message into a coach email, locker-room note, and seven-day challenge.",
        ),
        CalendarDay(
            "Thursday",
            "Fatherhood/Faith/Leadership Post",
            f"Legacy is built when you keep showing up for {clean_theme} with faith and action.",
            f"Write a grounded caption about family, leadership, and the responsibility to build while life is still heavy. Keep it faith-aware, not forced.{detail_clause}",
            "Save this and choose one leadership action your family can feel this week.",
            "Instagram, Facebook, LinkedIn",
            "Read the caption as a voiceover and turn the key lesson into a text message for a men's group.",
        ),
        CalendarDay(
            "Friday",
            "Concrete Conversations Episode Push",
            f"This week's Concrete Conversations question: what is {clean_theme} trying to teach you?",
            f"Promote an episode, episode idea, or long-form conversation around the week's theme. Promise honesty, practical wisdom, and one action listeners can use immediately.",
            "Subscribe, listen, and send the episode to one person rebuilding in real time.",
            "Podcast feed, YouTube, Instagram Stories",
            "Cut three clips: the truth, the lesson, and the next action.",
        ),
        CalendarDay(
            "Saturday",
            "Behind-the-Scenes / Story Post",
            f"The work behind {clean_theme} is not always loud, but it still counts.",
            f"Show the real build: notes, training, family time, preparation, outreach, or recovery. Connect the ordinary work to Concrete Motivation discipline.{detail_clause}",
            "Reply with what you are building quietly this weekend.",
            "Instagram Stories, Facebook Stories, TikTok",
            "Save the behind-the-scenes moment for a weekly recap reel.",
        ),
        CalendarDay(
            "Sunday",
            "Reflection / Reset / Weekly Challenge",
            f"Before the next week starts, reset your foundation around {clean_theme}.",
            f"Reflect on the week, name the lesson, and give a simple challenge: one promise, one person to serve, one action to execute before Monday night.{detail_clause}",
            "Write your one promise for the week and keep it before motivation gets loud again.",
            "Instagram, Facebook, email list",
            "Turn the challenge into a printable checklist, Story template, and Monday reminder.",
        ),
    )
    return WeeklyContentCalendar(clean_theme, clean_detail, days)
