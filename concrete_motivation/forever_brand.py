"""Forever Brand Factory for Concrete Motivation.

Creates a complete repeatable launch package for website, podcast, social media,
outreach, CRM tracking, YouTube, and operating cadence. This is offline-safe and
keeps the company moving even before every platform API is connected.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from concrete_motivation.slugify import slugify


PLATFORMS = ("YouTube", "Instagram", "TikTok", "Facebook", "LinkedIn", "Gmail", "Website")


@dataclass(frozen=True, slots=True)
class ForeverBrandResult:
    theme: str
    created_paths: tuple[Path, ...]

    def as_markdown(self) -> str:
        files = "\n".join(f"- {path}" for path in self.created_paths)
        return f"# Forever Brand Factory Complete\n\n**Theme:** {self.theme}\n\n## Files Created\n{files}"


class ForeverBrandFactory:
    """Generate the full Concrete Motivation brand operating kit."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parent.parent / "outputs" / "forever_brand"

    def run(self, theme: str = "Built Under Pressure") -> ForeverBrandResult:
        theme = theme.strip() or "Built Under Pressure"
        stamp = datetime.now().astimezone().replace(microsecond=0).strftime("%Y-%m-%d-%H%M%S")
        folder = self.root / f"{stamp}-{slugify(theme)}"
        folder.mkdir(parents=True, exist_ok=True)

        files = {
            "00_START_HERE.md": self._start_here(theme),
            "01_platform_access_map.md": self._platform_access(),
            "02_social_bios_and_handles.md": self._bios(),
            "03_30_day_never_ending_content_calendar.md": self._calendar(theme),
            "04_first_10_video_scripts.md": self._scripts(theme),
            "05_podcast_launch_package.md": self._podcast(theme),
            "06_website_final_copy.md": self._website(),
            "07_gmail_outreach_agenda.md": self._gmail(theme),
            "08_crm_lead_tracker.csv": self._crm_csv(),
            "09_weekly_operating_system.md": self._weekly_os(),
            "10_quality_control_checklist.md": self._quality(),
        }
        paths: list[Path] = []
        for filename, body in files.items():
            path = folder / filename
            path.write_text(body.strip() + "\n", encoding="utf-8")
            paths.append(path)
        result = ForeverBrandResult(theme, tuple(paths))
        readme = folder / "README.md"
        readme.write_text(result.as_markdown() + "\n", encoding="utf-8")
        return ForeverBrandResult(theme, (readme, *paths))

    def _start_here(self, theme: str) -> str:
        return f"""# Concrete Motivation Forever Brand Factory

## Theme
{theme}

## Brand Mission
Concrete Motivation exists to help people turn adversity into achievement through discipline, leadership, accountability, faith, family, and action.

## Brand Promise
Built under pressure. Proven through purpose.

## What This Package Does
This folder gives you the launch material for the website, podcast, social platforms, Gmail outreach, CRM tracking, and weekly operating rhythm.

## Execution Order
1. Lock handles and bios.
2. Publish website pages.
3. Record the first 10 videos.
4. Launch the podcast trailer and Episode 1.
5. Send outreach every weekday.
6. Track every lead in the CRM.
7. Review analytics every Sunday.
"""

    def _platform_access(self) -> str:
        rows = "\n".join(f"| {p} | Create or confirm account | Use same brand name, image, bio, and link | Owner: Jaytee |" for p in PLATFORMS)
        return f"""# Platform Access Map

| Platform | Access Needed | Setup Standard | Owner |
|---|---|---|---|
{rows}

## Important
This code creates the assets and operating system. Account creation, password ownership, and final posting approvals must stay with you inside each platform.

## Recommended Handle Order
1. concretemotivation
2. concrete.motivation
3. officialconcretemotivation
4. concretemotivationofficial

## Link-in-bio Stack
- Website home page
- Book speaking page
- YouTube channel
- Podcast page
- Contact email
"""

    def _bios(self) -> str:
        return """# Social Bios and Profile Setup

## Main Bio
Built under pressure. Proven through purpose. Motivation, leadership, discipline, family, faith, and comeback stories.

## Short Bio
Pressure builds purpose. Concrete Motivation.

## YouTube Description
Concrete Motivation is a motivational speaking, podcast, and media brand built for people turning pressure into purpose. Hosted by Jaytee Miller, Concrete Conversations brings real stories, leadership lessons, discipline, fatherhood, faith, business, and comeback fuel to people who refuse to quit.

## TikTok / Instagram Bio
Built under pressure. Proven through purpose. Discipline. Leadership. Comebacks.

## Facebook Page Description
Concrete Motivation helps students, leaders, athletes, parents, and communities turn adversity into achievement through practical motivation, discipline, and purpose.

## LinkedIn About
Concrete Motivation is a leadership and motivational speaking brand focused on pressure, discipline, accountability, resilience, and purpose. Through speaking, podcasting, media, and outreach, the brand serves schools, teams, youth programs, businesses, and communities.
"""

    def _calendar(self, theme: str) -> str:
        platforms = ["YouTube Short", "TikTok", "Instagram Reel", "Facebook Post", "LinkedIn Post"]
        hooks = [
            "You are not weak. You are under construction.",
            "Pressure is not the enemy when purpose is the outcome.",
            "Discipline is what motivation looks like after the feeling leaves.",
            "Your comeback needs a calendar, not just a wish.",
            "Concrete does not become strong without pressure.",
        ]
        lines = ["# 30-Day Content Calendar", "", "| Day | Platform | Topic | Hook | CTA |", "|---:|---|---|---|---|"]
        for day in range(1, 31):
            platform = platforms[(day - 1) % len(platforms)]
            hook = hooks[(day - 1) % len(hooks)]
            lines.append(f"| {day} | {platform} | {theme} #{day} | {hook} | Follow Concrete Motivation and share this with somebody who refuses to quit. |")
        return "\n".join(lines)

    def _scripts(self, theme: str) -> str:
        scripts = []
        for n in range(1, 11):
            scripts.append(f"""## Video {n}: {theme}

Hook: You are not behind. You are being built.

Script: Some seasons do not feel like progress because they feel heavy. But concrete gets stronger through pressure, not comfort. The goal is not to avoid pressure. The goal is to become the kind of person who can carry purpose through it. Today, do one disciplined thing that your future self will thank you for.

CTA: Follow Concrete Motivation for discipline, leadership, and comeback fuel.
""")
        return "# First 10 Video Scripts\n\n" + "\n".join(scripts)

    def _podcast(self, theme: str) -> str:
        return f"""# Podcast Launch Package

## Show Name
Concrete Conversations

## Trailer Title
Welcome to Concrete Conversations

## Episode 1 Title
{theme}: The Movement Behind Concrete Motivation

## Trailer Script
This is Concrete Conversations, the home for real stories, real leadership, and real comeback fuel. Concrete Motivation was built for people carrying pressure but still choosing purpose. We talk discipline, family, faith, leadership, business, adversity, and the work it takes to build something strong.

## Episode 1 Flow
1. Welcome and mission.
2. Why Concrete Motivation exists.
3. What pressure taught Jaytee about leadership, family, and purpose.
4. Why discipline matters more than temporary motivation.
5. Who this movement is built to serve.
6. The weekly Concrete Challenge.

## Concrete Challenge
For the next seven days, choose one area where you keep making excuses. Replace the excuse with one measurable action every day.
"""

    def _website(self) -> str:
        return """# Website Final Copy

## Home Hero
Concrete Motivation
Built under pressure. Proven through purpose.

## Home Subheadline
Motivational speaking, podcasting, and media for people turning adversity into achievement through discipline, leadership, accountability, faith, and action.

## Pages
- Home
- About
- Speaking
- Podcast
- Contact

## Speaking Page
Book Jaytee Miller for schools, sports teams, youth programs, churches, companies, and community events.

## Speaking Topics
- Built Under Pressure
- Discipline Over Emotion
- Leadership Starts at Home
- Student-Athlete Purpose
- Turning Setbacks Into Standards
- Family, Faith, and Accountability

## Contact CTA
Bring Concrete Motivation to your school, team, company, church, or community.
"""

    def _gmail(self, theme: str) -> str:
        return f"""# Gmail Outreach Agenda

## Daily Activity
- 10 school or youth program emails
- 5 podcast guest invitations
- 3 sponsor introductions
- 5 follow-ups
- Log every action in the CRM

## School Email
Subject: Concrete Motivation Speaking Opportunity

Hello,

My name is Jaytee Miller, founder of Concrete Motivation and host of Concrete Conversations. I am reaching out to introduce a speaking experience built around {theme}, discipline, accountability, leadership, and resilience.

Concrete Motivation is designed for students and young leaders who need a real message that meets them where they are while pushing them toward who they can become.

I would love to connect about bringing this message to your students, athletes, or youth community.

Thank you,
Jaytee Miller
Concrete Motivation

## Podcast Guest Email
Subject: Invitation to Join Concrete Conversations

Hello,

I would be honored to invite you to be a guest on Concrete Conversations, a podcast focused on leadership, resilience, discipline, family, faith, and turning adversity into achievement.

Would you be open to a short conversation about joining an upcoming episode?

Respectfully,
Jaytee Miller
Concrete Motivation
"""

    def _crm_csv(self) -> str:
        return "lead_type,name,organization,email,platform,status,last_contact,next_action,notes\nschool,,,,,new,,,\nyouth_program,,,,,new,,,\npodcast_guest,,,,,new,,,\nsponsor,,,,,new,,,\nchurch,,,,,new,,,\nsports_team,,,,,new,,,"

    def _weekly_os(self) -> str:
        return """# Weekly Operating System

## Monday CEO Day
Set theme, revenue goals, outreach target, and content focus.

## Tuesday Content Day
Record 5 short videos and draft captions.

## Wednesday Outreach Day
Send school, guest, sponsor, and community emails.

## Thursday Podcast Day
Record or outline episode, cut clips, prepare YouTube assets.

## Friday Website and Partnerships Day
Improve website proof, contact partners, review replies.

## Saturday Story Day
Capture behind-the-scenes content and real-life leadership moments.

## Sunday Review Day
Review analytics, update CRM, plan next week.
"""

    def _quality(self) -> str:
        return """# Quality Control Checklist

## Brand Check
- Message is clear.
- Tone is real, disciplined, hopeful, and strong.
- CTA is included.
- No typos.
- No fake claims.
- No copyrighted music or images without permission.

## Platform Check
- Correct handle.
- Correct bio.
- Correct link.
- Correct profile image.
- Post fits platform format.

## Business Check
- Lead tracked.
- Follow-up date set.
- Content saved.
- Analytics reviewed.
- Next action assigned.
"""
