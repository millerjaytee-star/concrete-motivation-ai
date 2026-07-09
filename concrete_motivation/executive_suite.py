"""Executive operating suite for Concrete Motivation."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from concrete_motivation.slugify import slugify


@dataclass(frozen=True, slots=True)
class ExecutiveSuiteResult:
    theme: str
    audience: str
    created_paths: tuple[Path, ...]

    def as_markdown(self) -> str:
        files = "\n".join(f"- {path}" for path in self.created_paths)
        return f"# Executive Suite Complete\n\n**Theme:** {self.theme}\n\n**Audience:** {self.audience}\n\n## Files Created\n{files}"


class ExecutiveSuite:
    """Create CEO, content, podcast, outreach, website, and analytics outputs."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parent.parent / "outputs" / "executive_suite"

    def run(self, theme: str, audience: str = "the masses") -> ExecutiveSuiteResult:
        theme = theme.strip() or "Built Under Pressure"
        audience = audience.strip() or "the masses"
        stamp = datetime.now().astimezone().replace(microsecond=0).strftime("%Y-%m-%d-%H%M%S")
        folder = self.root / f"{stamp}-{slugify(theme)}"
        folder.mkdir(parents=True, exist_ok=True)
        files = {
            "01_ceo_brief.md": self._ceo(theme, audience),
            "02_content_plan.md": self._content(theme, audience),
            "03_podcast_package.md": self._podcast(theme, audience),
            "04_outreach_campaign.md": self._outreach(theme),
            "05_website_actions.md": self._website(audience),
            "06_analytics_scorecard.md": self._analytics(theme),
        }
        paths = []
        for name, text in files.items():
            path = folder / name
            path.write_text(text.strip() + "\n", encoding="utf-8")
            paths.append(path)
        result = ExecutiveSuiteResult(theme, audience, tuple(paths))
        readme = folder / "README.md"
        readme.write_text(result.as_markdown() + "\n", encoding="utf-8")
        return ExecutiveSuiteResult(theme, audience, (readme, *paths))

    def _ceo(self, theme: str, audience: str) -> str:
        return f"""# CEO Brief

## Theme
{theme}

## Audience
{audience}

## Weekly Priorities
1. Publish 5 short videos.
2. Prepare 1 podcast episode and 1 trailer clip.
3. Send 20 outreach messages.
4. Improve 1 website section.
5. Track every lead, post, reply, and next action.

## Revenue Targets
- 3 community talks for proof and footage.
- 5 paid speaking conversations at $500-$1,500.
- 2 sponsor conversations for podcast or community content.

## Standard
Every action must build audience, proof, trust, or revenue.
"""

    def _content(self, theme: str, audience: str) -> str:
        return f"""# Content Plan

## Promise
Make {audience} feel seen, challenged, and ready to move.

## 5 Short Videos
1. You are not weak. You are under construction. Topic: {theme}.
2. Pressure becomes preparation when discipline leads.
3. The people depending on you need your consistency.
4. Do not let the worst chapter become the final title.
5. Concrete does not become strong without pressure.

## Captions
- Built under pressure. Proven through purpose.
- Discipline is motivation after the emotion leaves.
- Share this with somebody who refuses to quit.

## Hashtags
#ConcreteMotivation #BuiltUnderPressure #Motivation #Leadership #Discipline #Purpose
"""

    def _podcast(self, theme: str, audience: str) -> str:
        return f"""# Podcast Package

## Episode Title
{theme}: Built Under Pressure, Proven Through Purpose

## Episode Promise
Help {audience} turn pressure into discipline, discipline into leadership, and leadership into purpose.

## Segments
1. What pressure teaches.
2. Why motivation must become a system.
3. How family, leadership, faith, and discipline shape the comeback.
4. The Concrete Challenge for the week.

## Clip Lines
- Pressure built the foundation. Purpose keeps us standing.
- Motivation starts the fire. Discipline keeps the lights on.
- Your comeback needs a calendar, not just a wish.
"""

    def _outreach(self, theme: str) -> str:
        return f"""# Outreach Campaign

## Targets
Schools, youth programs, sports teams, community centers, podcast guests, local businesses, and sponsors.

## Email
Subject: Concrete Motivation Speaking Opportunity

Hello,

My name is Jaytee Miller, founder of Concrete Motivation and host of Concrete Conversations. I am reaching out to introduce a speaking experience built around {theme}, discipline, accountability, leadership, and resilience.

I would love to connect about bringing this message to your students, athletes, team, or community.

Thank you,
Jaytee Miller
Concrete Motivation
"""

    def _website(self, audience: str) -> str:
        return f"""# Website Actions

## Headline
Concrete Motivation: Built Under Pressure. Proven Through Purpose.

## Subheadline
Speaking, podcasting, and media for {audience} turning pressure into purpose through discipline, leadership, and action.

## Pages
Home, About, Speaking, Podcast, Contact.

## This Week
Add one proof section: mission, audience served, speaking topics, podcast clips, or contact form.
"""

    def _analytics(self, theme: str) -> str:
        return f"""# Analytics Scorecard

## Theme
{theme}

## Metrics
- Videos posted:
- Views:
- Likes:
- Comments:
- Shares:
- New followers:
- Outreach sent:
- Replies received:
- Meetings booked:
- Speaking leads:

## Review
Double down on what moves audience, trust, leads, or revenue.
"""
