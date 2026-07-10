"""Podcast guest outreach workflow for Concrete Motivation."""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from concrete_motivation.slugify import slugify


@dataclass(frozen=True, slots=True)
class PodcastGuestResult:
    theme: str
    audience: str
    created_paths: tuple[Path, ...]

    def as_markdown(self) -> str:
        files = "\n".join(f"- {path}" for path in self.created_paths)
        return (
            "# Podcast Guest Outreach Complete\n\n"
            f"**Theme:** {self.theme}\n\n"
            f"**Audience:** {self.audience}\n\n"
            "## Files Created\n"
            f"{files}"
        )


class PodcastGuestBot:
    """Create guest outreach, questions, and scoring assets."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parent.parent / "outputs" / "podcast_production" / "guest_outreach"

    def run(self, theme: str, audience: str = "leaders and creators") -> PodcastGuestResult:
        clean_theme = theme.strip() or "Built Under Pressure"
        clean_audience = audience.strip() or "leaders and creators"
        stamp = datetime.now().astimezone().replace(microsecond=0).strftime("%Y-%m-%d-%H%M%S")
        folder = self.root / f"{stamp}-{slugify(clean_theme)}"
        folder.mkdir(parents=True, exist_ok=True)

        files = {
            "00_podcast_guest_package.md": self._readme(clean_theme, clean_audience),
            "00_podcast_guest_package.json": json.dumps(self._package_dict(clean_theme, clean_audience), indent=2),
            "01_guest_list.csv": self._guest_list(clean_theme, clean_audience),
            "02_initial_message.md": self._guest_outreach(clean_theme, clean_audience),
            "03_follow_up_1.md": self._follow_up_one(clean_theme, clean_audience),
            "04_follow_up_2.md": self._follow_up_two(clean_theme, clean_audience),
            "05_interview_questions.md": self._interview_questions(clean_theme, clean_audience),
            "06_guest_scoring_system.md": self._guest_scoring_system(clean_theme, clean_audience),
            "07_crm_import_row.csv": self._crm_import_row(clean_theme, clean_audience),
            "README.md": self._readme(clean_theme, clean_audience),
        }
        paths: list[Path] = []
        for filename, body in files.items():
            path = folder / filename
            if filename.endswith(".json"):
                path.write_text(body + "\n", encoding="utf-8")
            else:
                path.write_text(body.strip() + "\n", encoding="utf-8")
            paths.append(path)
        return PodcastGuestResult(clean_theme, clean_audience, tuple(paths))

    def _readme(self, theme: str, audience: str) -> str:
        return f"""# Podcast Guest Package

## Theme
{theme}

## Audience
{audience}

## Purpose
Build a repeatable guest outreach system for Concrete Conversations.

## Files
- Markdown package
- JSON package
- Guest list CSV
- Initial message
- Follow-up 1
- Follow-up 2
- Interview questions
- Guest scoring system
- CRM import row format
"""

    def _package_dict(self, theme: str, audience: str) -> dict[str, str]:
        return {
            "theme": theme,
            "audience": audience,
            "initial_message": self._guest_outreach(theme, audience),
            "follow_up_1": self._follow_up_one(theme, audience),
            "follow_up_2": self._follow_up_two(theme, audience),
            "interview_questions": self._interview_questions(theme, audience),
            "guest_scoring_system": self._guest_scoring_system(theme, audience),
        }

    def _guest_list(self, theme: str, audience: str) -> str:
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=["guest_name", "organization", "email", "fit_score", "status", "next_action", "notes"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "guest_name": "Potential Guest 1",
                "organization": "Leaders Network",
                "email": "",
                "fit_score": 5,
                "status": "new",
                "next_action": "send invitation",
                "notes": f"{theme} for {audience}",
            }
        )
        writer.writerow(
            {
                "guest_name": "Potential Guest 2",
                "organization": "Creators Network",
                "email": "",
                "fit_score": 4,
                "status": "new",
                "next_action": "research guest angle",
                "notes": "",
            }
        )
        return buffer.getvalue()

    def _guest_outreach(self, theme: str, audience: str) -> str:
        return f"""# Guest Outreach

Subject: Invitation to join Concrete Conversations

Hello,

My name is Jaytee Miller, and I host Concrete Conversations.
I would love to invite you to join us for a conversation centered on {theme} for {audience}.

The show focuses on discipline, family, faith, leadership, resilience, and turning pressure into purpose.

Would you be open to a short interview?

Respectfully,
Jaytee Miller
Concrete Motivation
"""

    def _follow_up_one(self, theme: str, audience: str) -> str:
        return f"""# Follow-Up 1

Following up in case this invitation got buried.

The conversation would center on {theme} for {audience} and keep the tone practical and honest.

Would you like me to send a short outline?
"""

    def _follow_up_two(self, theme: str, audience: str) -> str:
        return f"""# Follow-Up 2

If this is not a fit right now, should I reconnect at a later date?

Respectfully,
Jaytee Miller
"""

    def _interview_questions(self, theme: str, audience: str) -> str:
        return f"""# Interview Questions

1. What pressure shaped your discipline the most?
2. Where did you learn to keep going when life got hard?
3. What does {theme} look like in real life for {audience}?
4. What habit keeps you grounded when motivation fades?
5. What advice would you give to somebody trying to build with consistency?
6. What role do faith and family play in your leadership?
7. What is one concrete action listeners can take this week?
"""

    def _guest_scoring_system(self, theme: str, audience: str) -> str:
        return f"""# Guest Scoring System

| Criterion | Score 1 | Score 3 | Score 5 |
|---|---|---|---|
| Relevance to {theme} | weak fit | acceptable fit | strong fit |
| Fit for {audience} | limited audience overlap | moderate overlap | direct overlap |
| Story strength | general story | some real evidence | strong lived experience |
| Clarity | unclear message | some clarity | clear and useful |
| Bookability | difficult to schedule | possible | easy and responsive |

## Decision Rule
Invite guests who score 20 or higher and have a clear, practical story.
"""

    def _crm_import_row(self, theme: str, audience: str) -> str:
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=["guest_name", "organization", "email", "stage", "next_follow_up_date", "source", "notes"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "guest_name": "Potential Guest 1",
                "organization": "Leaders Network",
                "stage": "New Lead",
                "source": "Podcast Guest Campaign",
                "notes": f"{theme} for {audience}",
            }
        )
        return buffer.getvalue()
