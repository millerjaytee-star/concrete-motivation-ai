"""Build the Concrete Motivation Revenue Commander package."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from concrete_motivation.gmail_sales_stager import build_gmail_sales_sequence
from concrete_motivation.membership_program import build_membership_program
from concrete_motivation.payment_link_manager import PaymentLinkManager
from concrete_motivation.revenue_website_pages import build_revenue_website_pages
from concrete_motivation.speaker_booking_engine import build_speaker_booking_package
from concrete_motivation.social_sales_campaign import build_social_sales_campaign
from concrete_motivation.slugify import slugify


REVENUE_COMMANDER_FOLDER = Path(__file__).resolve().parent.parent / "outputs" / "revenue_commander"


@dataclass(frozen=True, slots=True)
class RevenueCommanderResult:
    theme: str
    monthly_price: int
    annual_price: int
    premium_annual_price: int
    created_paths: tuple[Path, ...]

    def as_markdown(self) -> str:
        files = "\n".join(f"- {path}" for path in self.created_paths)
        return (
            "# Revenue Commander Complete\n\n"
            f"**Theme:** {self.theme}\n\n"
            f"**Monthly:** ${self.monthly_price}/month\n\n"
            f"**Annual:** ${self.annual_price}/year\n\n"
            f"**Premium Annual:** ${self.premium_annual_price}/year\n\n"
            "## Files Created\n"
            f"{files}\n\n"
            "## Weekly Revenue Scoreboard\n"
            "See `08_weekly_revenue_scoreboard.md` for readiness, payment-link status, and the next command."
        )


class RevenueCommander:
    """Generate one revenue action package without sending or charging anything."""

    def __init__(self, root: Path | None = None, payment_manager: PaymentLinkManager | None = None) -> None:
        self.root = root or REVENUE_COMMANDER_FOLDER
        self.payment_manager = payment_manager or PaymentLinkManager()

    def run(
        self,
        theme: str = "Concrete Builders Membership",
        monthly_price: int = 40,
        annual_price: int = 400,
        premium_annual_price: int = 444,
    ) -> RevenueCommanderResult:
        clean_theme = theme.strip() or "Concrete Builders Membership"
        self.root.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().astimezone().replace(microsecond=0).strftime("%Y-%m-%d-%H%M%S")
        folder = self.root / f"{stamp}-{slugify(clean_theme)}"
        folder.mkdir(parents=True, exist_ok=True)

        membership = build_membership_program(
            offer=clean_theme,
            monthly_price=monthly_price,
            annual_price=annual_price,
            premium_annual_price=premium_annual_price,
            audience="Concrete Motivation supporters",
        )
        payment_status = self.payment_manager.status()
        website_pages = build_revenue_website_pages(
            offer=clean_theme,
            monthly_price=monthly_price,
            annual_price=annual_price,
            premium_annual_price=premium_annual_price,
            payment_manager=self.payment_manager,
        )
        social_campaign = build_social_sales_campaign(clean_theme, days=14, audience="membership prospects and booking leads")
        gmail_sequence = build_gmail_sales_sequence(clean_theme, audience="membership prospects and booking leads")
        speaker_package = build_speaker_booking_package(segment="schools", theme=clean_theme)

        files = {
            "00_revenue_decision.md": self._decision(clean_theme, payment_status.configured_count, payment_status.total_count),
            "01_offer_stack.md": self._offer_stack(clean_theme, membership),
            "02_membership_plan.md": self._membership_plan(membership),
            "03_payment_link_map.json": json.dumps(
                {
                    "theme": clean_theme,
                    "links": [
                        {
                            "label": record.label,
                            "env_var": record.env_var,
                            "source": record.source,
                            "value": record.display_value,
                            "configured": record.configured,
                        }
                        for record in payment_status.records
                    ],
                },
                indent=2,
            ),
            "04_website_sales_pages.md": self._website_sales_pages(website_pages),
            "05_social_sales_campaign.md": self._social_sales_campaign(social_campaign),
            "06_gmail_sales_sequence.md": self._gmail_sales_sequence(gmail_sequence),
            "07_crm_revenue_actions.csv": self._crm_actions(clean_theme),
            "08_weekly_revenue_scoreboard.md": self._weekly_scoreboard(
                clean_theme,
                payment_status.configured_count,
                payment_status.total_count,
                membership,
                social_campaign,
                gmail_sequence,
                speaker_package,
            ),
        }
        created_paths: list[Path] = []
        for filename, body in files.items():
            path = folder / filename
            if filename.endswith(".json"):
                path.write_text(body + "\n", encoding="utf-8")
            elif filename.endswith(".csv"):
                path.write_text(body, encoding="utf-8")
            else:
                path.write_text(body.strip() + "\n", encoding="utf-8")
            created_paths.append(path)
        return RevenueCommanderResult(clean_theme, monthly_price, annual_price, premium_annual_price, tuple(created_paths))

    def _decision(self, theme: str, configured_links: int, total_links: int) -> str:
        return f"""# Revenue Decision

## Theme
{theme}

## Decision
Keep the revenue stack simple: membership first, payment links second, website pages third, social sales fourth, Gmail follow-up fifth.

## Payment Link Status
Configured: {configured_links}/{total_links}

## Next Command
If any link is missing, stage the placeholder and update the ignored local config before promoting the page.
"""

    def _offer_stack(self, theme: str, membership) -> str:
        return f"""# Offer Stack

## Primary Offer
{membership.offer}

## Membership
Monthly: ${membership.monthly_price}/month
Annual: ${membership.annual_price}/year
Premium Annual: ${membership.premium_annual_price}/year

## Booking
Speaker booking packages are staged separately so the team can sell talks without mixing them with membership checkout.

## Sponsor Layer
Sponsor packages stay available for community businesses and aligned brands.

## Message
{theme} should lead with discipline, accountability, and a clear next action.
"""

    def _membership_plan(self, membership) -> str:
        return f"""# Membership Plan

## Offer
{membership.offer}

## Monthly Offer
{membership.monthly_offer}

## Annual Offer
{membership.annual_offer}

## FAQ
{membership.faq}

## Onboarding
{membership.onboarding_checklist}
"""

    def _website_sales_pages(self, pages: dict[str, str]) -> str:
        order = ("membership.md", "speaking.md", "sponsors.md", "book_jaytee.md", "payment_links.md")
        lines = [f"## {name}\n{pages[name].splitlines()[0]}" for name in order]
        return "# Website Sales Pages\n\n" + "\n\n".join(lines)

    def _social_sales_campaign(self, campaign) -> str:
        first = campaign.instagram_captions[0] if campaign.instagram_captions else ""
        return f"""# Social Sales Campaign

## Offer
{campaign.offer}

## Days
{campaign.days}

## First Instagram Caption
{first}

## CTA Rhythm
{campaign.cta_calendar[0][2] if campaign.cta_calendar else "Join the membership or book Jaytee"}
"""

    def _gmail_sales_sequence(self, sequence) -> str:
        drafts = "\n".join(f"- {draft.name}: {draft.subject}" for draft in sequence.drafts)
        return f"""# Gmail Sales Sequence

## Offer
{sequence.offer}

## Drafts
{drafts}
"""

    def _crm_actions(self, theme: str) -> str:
        from io import StringIO

        buffer = StringIO()
        handle = csv.DictWriter(
            buffer,
            fieldnames=["lead_name", "organization", "segment", "offer", "stage", "next_follow_up_date", "source", "notes"],
        )
        handle.writeheader()
        handle.writerow(
            {
                "lead_name": "Membership Lead 1",
                "organization": "Community Supporter",
                "segment": "membership",
                "offer": theme,
                "stage": "New Lead",
                "next_follow_up_date": "",
                "source": "Revenue Commander",
                "notes": "Join membership launch sequence",
            }
        )
        handle.writerow(
            {
                "lead_name": "Speaker Lead 1",
                "organization": "School Network",
                "segment": "speaker booking",
                "offer": theme,
                "stage": "Contacted",
                "next_follow_up_date": "",
                "source": "Revenue Commander",
                "notes": "Review booking opportunity",
            }
        )
        return buffer.getvalue()

    def _weekly_scoreboard(
        self,
        theme: str,
        configured_links: int,
        total_links: int,
        membership,
        social_campaign,
        gmail_sequence,
        speaker_package,
    ) -> str:
        readiness = 0
        readiness += 20 if membership.offer else 0
        readiness += 20 if configured_links == total_links else 0
        readiness += 20 if social_campaign.days >= 14 else 0
        readiness += 20 if gmail_sequence.drafts else 0
        readiness += 20 if speaker_package.segment else 0
        next_command = (
            "Create payment links"
            if configured_links < total_links
            else "Publish the membership page and stage the first outreach block"
        )
        return f"""# Weekly Revenue Scoreboard

## Theme
{theme}

## Readiness Score
{readiness}/100

## Membership Packages Created
1

## Configured Payment Links
{configured_links}/{total_links}

## Revenue Campaign Packages
1

## Speaker Booking Packages
1

## Sponsor Packages
1

## Membership Launch Readiness Score
{readiness}

## Next Revenue Command
{next_command}
"""
