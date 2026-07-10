"""Sponsorship outreach workflow for Concrete Motivation."""

from __future__ import annotations

import json
import csv
import io
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from concrete_motivation.slugify import slugify


@dataclass(frozen=True, slots=True)
class SponsorshipResult:
    theme: str
    audience: str
    created_paths: tuple[Path, ...]

    def as_markdown(self) -> str:
        files = "\n".join(f"- {path}" for path in self.created_paths)
        return (
            "# Sponsorship Outreach Complete\n\n"
            f"**Theme:** {self.theme}\n\n"
            f"**Audience:** {self.audience}\n\n"
            "## Files Created\n"
            f"{files}"
        )


class SponsorshipBot:
    """Create sponsor prospect and outreach assets."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parent.parent / "outputs" / "sales_outreach" / "sponsorship"

    def run(self, theme: str, audience: str = "community partners and local brands", segment: str = "") -> SponsorshipResult:
        clean_theme = theme.strip() or "Built Under Pressure"
        clean_audience = audience.strip() or "community partners and local brands"
        clean_segment = segment.strip()
        stamp = datetime.now().astimezone().replace(microsecond=0).strftime("%Y-%m-%d-%H%M%S")
        folder_name = f"{stamp}-{slugify(clean_theme)}"
        if clean_segment:
            folder_name = f"{folder_name}-{slugify(clean_segment)}"
        folder = self.root / folder_name
        folder.mkdir(parents=True, exist_ok=True)

        files = {
            "00_sponsor_campaign.md": self._readme(clean_theme, clean_audience, clean_segment),
            "00_sponsor_campaign.json": json.dumps(self._package_dict(clean_theme, clean_audience, clean_segment), indent=2),
            "01_sponsor_prospect_list_template.csv": self._prospect_template(clean_theme, clean_audience, clean_segment),
            "02_initial_message.md": self._sponsor_email(clean_theme, clean_audience, clean_segment),
            "03_follow_up_1.md": self._follow_up_one(clean_theme, clean_audience, clean_segment),
            "04_follow_up_2.md": self._follow_up_two(clean_theme, clean_audience, clean_segment),
            "05_proposal_outline.md": self._proposal_outline(clean_theme, clean_audience, clean_segment),
            "06_crm_import_row.csv": self._crm_import_row(clean_theme, clean_audience, clean_segment),
            "README.md": self._readme(clean_theme, clean_audience, clean_segment),
        }
        paths: list[Path] = []
        for filename, body in files.items():
            path = folder / filename
            if filename.endswith(".json"):
                path.write_text(body + "\n", encoding="utf-8")
            else:
                path.write_text(body.strip() + "\n", encoding="utf-8")
            paths.append(path)
        return SponsorshipResult(clean_theme, clean_audience, tuple(paths))

    def _package_dict(self, theme: str, audience: str, segment: str) -> dict[str, str]:
        return {
            "theme": theme,
            "audience": audience,
            "segment": segment,
            "initial_message": self._sponsor_email(theme, audience, segment),
            "follow_up_1": self._follow_up_one(theme, audience, segment),
            "follow_up_2": self._follow_up_two(theme, audience, segment),
            "proposal_outline": self._proposal_outline(theme, audience, segment),
        }

    def _readme(self, theme: str, audience: str, segment: str = "") -> str:
        return f"""# Sponsorship Outreach Package

## Theme
{theme}

## Audience
{audience}

## Segment
{segment or "n/a"}

## Purpose
Build sponsor conversations around aligned community impact, content reach, and brand trust.

## Files
- Markdown package
- JSON package
- Sponsor prospect CSV
- Initial message
- Follow-up 1
- Follow-up 2
- Proposal outline
- CRM import row format
"""

    def _prospect_template(self, theme: str, audience: str, segment: str = "") -> str:
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=[
                "company_name",
                "contact_name",
                "contact_role",
                "email",
                "category",
                "fit_score",
                "stage",
                "next_action",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "company_name": segment or "Local Business",
                "contact_name": "Owner",
                "contact_role": "decision maker",
                "email": "",
                "category": "local_business",
                "fit_score": 5,
                "stage": "new",
                "next_action": "research fit",
                "notes": f"{theme} for {audience} {segment}".strip(),
            }
        )
        writer.writerow(
            {
                "company_name": segment or "Community Partner",
                "contact_name": "Contact",
                "contact_role": "decision maker",
                "email": "",
                "category": "community_partner",
                "fit_score": 4,
                "stage": "new",
                "next_action": "find contact",
            }
        )
        writer.writerow(
            {
                "company_name": segment or "Brand Partner",
                "contact_name": "Contact",
                "contact_role": "decision maker",
                "email": "",
                "category": "brand_partner",
                "fit_score": 4,
                "stage": "new",
                "next_action": "send intro",
            }
        )
        return buffer.getvalue()

    def _sponsor_email(self, theme: str, audience: str, segment: str = "") -> str:
        return f"""# Sponsor Outreach Email

Subject: Partnership opportunity with Concrete Motivation{f" for {segment}" if segment else ""}

Hello,

My name is Jaytee Miller, founder of Concrete Motivation.
I am reaching out with a sponsorship opportunity centered on {theme} for {audience}{f" and {segment}" if segment else ""}.

Concrete Motivation creates disciplined, faith-aware, family-aware content and live speaking experiences that connect with people who care about growth, leadership, and consistency.

I would love to send a short outline and explore whether there is a fit for your brand.

Respectfully,
Jaytee Miller
Concrete Motivation
"""

    def _follow_up_one(self, theme: str, audience: str, segment: str = "") -> str:
        return f"""# Follow-Up 1

Following up in case this note got buried.

I can send a one-page outline showing how {theme} can be positioned for {audience}{f" and {segment}" if segment else ""}.

Would a brief conversation next week be useful?
"""

    def _follow_up_two(self, theme: str, audience: str, segment: str = "") -> str:
        return f"""# Follow-Up 2

If this is not the right time, should I reconnect later this month or next quarter?

I appreciate your time and consideration.
"""

    def _proposal_outline(self, theme: str, audience: str, segment: str = "") -> str:
        return f"""# Sponsorship Proposal Outline

## 1. Who We Are
Concrete Motivation is a leadership and motivation brand built to turn pressure into purpose.

## 2. Why This Matters
{theme} resonates with {audience}{f" and {segment}" if segment else ""} and creates a message that is honest, memorable, and actionable.

## 3. Audience Value
- Students
- Athletes
- Fathers
- Leaders under pressure

## 4. Sponsor Value
- Brand alignment
- Community trust
- Content visibility
- Event and media exposure

## 5. Next Step
Book a short call and determine if there is a fit for a sponsored conversation, event, or content partnership.
"""

    def _crm_import_row(self, theme: str, audience: str, segment: str = "") -> str:
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=[
                "company_name",
                "contact_name",
                "contact_role",
                "email",
                "segment",
                "stage",
                "next_follow_up_date",
                "source",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "company_name": segment or "Local Business",
                "contact_name": "Owner",
                "contact_role": "decision maker",
                "segment": segment or "local",
                "stage": "New Lead",
                "source": "Sponsor Campaign",
                "notes": f"{theme} for {audience} {segment}".strip(),
            }
        )
        return buffer.getvalue()
