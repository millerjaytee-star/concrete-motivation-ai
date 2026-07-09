"""
Concrete Motivation AI Business OS
VP build: brand strategy, content engine, outreach engine, website copy, and weekly operating rhythm.
Run locally with: python3 brand_os/concrete_motivation_os.py
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated"

BRAND = {
    "name": "Concrete Motivation",
    "tagline": "Built under pressure. Proven through purpose.",
    "mission": "Help people turn adversity into achievement through discipline, leadership, accountability, and faith-driven action.",
    "vision": "Become a national motivational media, speaking, and development company serving schools, athletes, leaders, families, and communities.",
    "voice": ["real", "direct", "hopeful", "disciplined", "street-smart", "executive-level", "family-centered"],
    "pillars": [
        "Pressure builds purpose",
        "Discipline beats emotion",
        "Leadership starts at home",
        "The comeback is the brand",
        "Serve the masses with truth",
    ],
}

AUDIENCES = [
    "young men building identity and discipline",
    "student athletes preparing for life beyond the game",
    "parents and providers carrying pressure silently",
    "frontline leaders and managers growing into executives",
    "schools, youth programs, churches, and sports teams",
]

@dataclass
class ContentPiece:
    day: int
    platform: str
    title: str
    format: str
    hook: str
    call_to_action: str


def ensure_dirs() -> None:
    for folder in [OUT, OUT / "website", OUT / "podcast", OUT / "social", OUT / "outreach", OUT / "ops"]:
        folder.mkdir(parents=True, exist_ok=True)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def content_calendar(days: int = 30) -> list[ContentPiece]:
    platforms = ["YouTube Shorts", "TikTok", "Instagram Reels", "Facebook", "LinkedIn"]
    themes = [
        ("Built Under Pressure", "You are not behind. You are being built."),
        ("Discipline Over Feelings", "Your feelings are real, but your assignment is bigger."),
        ("Fatherhood & Leadership", "The people watching you need your consistency more than your excuses."),
        ("From Setback to Standard", "Do not let the worst chapter become the final title."),
        ("Concrete Conversations", "Real conversations create real change."),
    ]
    pieces: list[ContentPiece] = []
    for i in range(days):
        theme, hook = themes[i % len(themes)]
        platform = platforms[i % len(platforms)]
        pieces.append(ContentPiece(
            day=i + 1,
            platform=platform,
            title=f"{theme} #{i + 1}",
            format="30-60 sec vertical video" if platform != "LinkedIn" else "leadership post",
            hook=hook,
            call_to_action="Follow Concrete Motivation and share this with somebody who refuses to quit.",
        ))
    return pieces


def render_content_calendar(pieces: Iterable[ContentPiece]) -> str:
    lines = ["# Concrete Motivation 30-Day Content Calendar", "", "| Day | Platform | Title | Format | Hook | CTA |", "|---:|---|---|---|---|---|"]
    for p in pieces:
        lines.append(f"| {p.day} | {p.platform} | {p.title} | {p.format} | {p.hook} | {p.call_to_action} |")
    return "\n".join(lines)


def website_copy() -> str:
    return f"""
# Concrete Motivation Website Copy

## Hero
{BRAND['name']}
{BRAND['tagline']}

Pressure does not break everybody. Some people are built by it.
Concrete Motivation helps students, athletes, leaders, parents, and communities turn pain into purpose and purpose into action.

Primary CTA: Book Jaytee to Speak
Secondary CTA: Watch Concrete Conversations

## About
Concrete Motivation was built for people who had to become strong before life gave them permission. It is a motivational speaking, podcast, and media company created to serve people who are fighting through pressure, responsibility, grief, leadership, fatherhood, business, and the daily weight of becoming better.

We believe motivation is not just emotion. Motivation becomes real when it turns into discipline, systems, and service.

## Speaking Services
- School assemblies
- Student-athlete leadership talks
- Corporate leadership sessions
- Youth program workshops
- Community keynote events
- Faith and family-centered conversations

## Podcast
Concrete Conversations is where real life meets real leadership. Every episode gives the audience practical fuel: discipline, accountability, comeback stories, family, business, faith, and growth.

## Contact CTA
Bring Concrete Motivation to your school, team, company, church, or community program.
Email: concrete motivation booking inbox
"""


def podcast_pack() -> str:
    return """
# Concrete Conversations Podcast Starter Pack

## Show Promise
Real conversations for people building purpose under pressure.

## Episode 1 Title
Built Under Pressure: The Story Behind Concrete Motivation

## Cold Open
Some people meet pressure and fold. Some people meet pressure and finally discover what they are made of. This is Concrete Motivation, and this is not just a podcast. This is a foundation for every person who refuses to quit.

## Episode Flow
1. Welcome and mission
2. Why the word concrete matters
3. Personal leadership, family, adversity, and purpose
4. The difference between temporary motivation and built discipline
5. Message to young men, parents, leaders, and dreamers
6. Weekly challenge
7. Call to action

## Weekly Challenge
Pick one area of your life where you keep making excuses. For the next seven days, replace the excuse with one measurable action.

## Closing Line
Pressure built the foundation. Purpose keeps us standing. This is Concrete Motivation.
"""


def outreach_templates() -> str:
    return """
# Outreach Email Agenda and Templates

## Daily Gmail Agenda
- 10 school/youth program outreach emails
- 5 podcast guest invitations
- 5 sponsor/partner introductions
- 3 follow-ups from previous contacts
- Log every contact in the CRM sheet or leads folder

## School / Youth Program Email
Subject: Concrete Motivation Speaking Opportunity for Your Students

Hello,

My name is Jaytee Miller, founder of Concrete Motivation and host of Concrete Conversations. I am reaching out to introduce a motivational speaking experience built to help students turn pressure into purpose through discipline, accountability, leadership, and resilience.

Concrete Motivation is designed for students who need a real voice, practical tools, and a message that meets them where they are while pushing them toward who they can become.

I would love to connect and discuss how Concrete Motivation could support your students, athletes, or youth community.

Thank you,
Jaytee Miller
Concrete Motivation

## Podcast Guest Email
Subject: Invitation to Join Concrete Conversations

Hello,

I would be honored to invite you to be a guest on Concrete Conversations, a podcast focused on leadership, resilience, discipline, family, faith, and turning adversity into achievement.

Your story and perspective would bring real value to an audience that is committed to growth, purpose, and building something strong from life’s pressure.

Would you be open to a short conversation about joining an upcoming episode?

Respectfully,
Jaytee Miller
Concrete Motivation
"""


def operating_rhythm() -> str:
    return """
# Concrete Motivation Weekly Operating Rhythm

## Monday: CEO Day
- Review brand goals
- Pick weekly theme
- Confirm speaking/outreach targets
- Track revenue opportunities

## Tuesday: Content Production
- Record 5 short videos
- Draft 2 LinkedIn/Facebook posts
- Create 1 podcast outline

## Wednesday: Outreach
- Send school/youth program emails
- Send guest invitations
- Follow up with leads

## Thursday: YouTube and Podcast
- Record or edit long-form content
- Cut 5 short clips
- Write title, description, tags, and captions

## Friday: Community and Partnerships
- Engage with comments
- DM potential partners
- Review analytics

## Saturday: Brand Storytelling
- Film behind-the-scenes content
- Capture family, discipline, leadership, and real-life moments

## Sunday: Reset
- Weekly reflection
- Plan next theme
- Prepare Monday CEO brief
"""


def main() -> None:
    ensure_dirs()
    pieces = content_calendar(30)
    write(OUT / "BRAND_OS.json", json.dumps(BRAND, indent=2))
    write(OUT / "social" / "30_day_content_calendar.md", render_content_calendar(pieces))
    write(OUT / "website" / "homepage_copy.md", website_copy())
    write(OUT / "podcast" / "podcast_starter_pack.md", podcast_pack())
    write(OUT / "outreach" / "email_agenda_and_templates.md", outreach_templates())
    write(OUT / "ops" / "weekly_operating_rhythm.md", operating_rhythm())
    print("Concrete Motivation AI Business OS generated successfully.")
    print(f"Files created in: {OUT}")


if __name__ == "__main__":
    main()
