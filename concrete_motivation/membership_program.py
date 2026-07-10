"""Build the Concrete Builders Membership program assets."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from concrete_motivation.slugify import slugify


MEMBERSHIP_OUTPUT_FOLDER = Path(__file__).resolve().parent.parent / "outputs" / "membership"


@dataclass(frozen=True, slots=True)
class MembershipProgram:
    offer: str
    monthly_price: int
    annual_price: int
    premium_annual_price: int
    audience: str
    monthly_offer: str
    annual_offer: str
    faq: str
    terms_placeholder: str
    welcome_email: str
    renewal_email: str
    cancellation_save_email: str
    onboarding_checklist: str
    weekly_challenge_template: str

    def as_markdown(self) -> str:
        return f"""# Membership Program

## Offer
{self.offer}

## Monthly Price
${self.monthly_price}/month

## Annual Price
${self.annual_price}/year

## Premium Annual Price
${self.premium_annual_price}/year

## Audience
{self.audience}
"""

    def as_dict(self) -> dict[str, object]:
        return {
            "offer": self.offer,
            "monthly_price": self.monthly_price,
            "annual_price": self.annual_price,
            "premium_annual_price": self.premium_annual_price,
            "audience": self.audience,
            "monthly_offer": self.monthly_offer,
            "annual_offer": self.annual_offer,
            "faq": self.faq,
            "terms_placeholder": self.terms_placeholder,
            "welcome_email": self.welcome_email,
            "renewal_email": self.renewal_email,
            "cancellation_save_email": self.cancellation_save_email,
            "onboarding_checklist": self.onboarding_checklist,
            "weekly_challenge_template": self.weekly_challenge_template,
        }


@dataclass(frozen=True, slots=True)
class MembershipProgramResult:
    offer: str
    monthly_price: int
    annual_price: int
    premium_annual_price: int
    audience: str
    created_paths: tuple[Path, ...]

    def as_markdown(self) -> str:
        files = "\n".join(f"- {path}" for path in self.created_paths)
        return (
            "# Membership Program Complete\n\n"
            f"**Offer:** {self.offer}\n\n"
            f"**Monthly:** ${self.monthly_price}/month\n\n"
            f"**Annual:** ${self.annual_price}/year\n\n"
            f"**Premium Annual:** ${self.premium_annual_price}/year\n\n"
            f"**Audience:** {self.audience}\n\n"
            "## Files Created\n"
            f"{files}"
        )


def build_membership_program(
    offer: str = "Concrete Builders Membership",
    monthly_price: int = 40,
    annual_price: int = 400,
    premium_annual_price: int = 444,
    audience: str = "Concrete Motivation supporters",
) -> MembershipProgram:
    monthly_offer = f"""# Monthly Offer

## Offer
{offer}

## Price
${monthly_price}/month

## Included
- Weekly Concrete Motivation challenge
- Monthly live mindset and discipline session
- Private member newsletter
- Early access to speeches, YouTube videos, and podcast clips
- Downloadable worksheets and action plans
- Member-only accountability prompts
- Community shoutout opportunities
- Discount on live events, merch, and workshops
"""
    annual_offer = f"""# Annual Offer

## Offer
{offer}

## Price Options
- ${annual_price}/year launch annual plan
- ${premium_annual_price}/year premium annual plan

## Included
- Everything in the monthly membership
- Two months free compared to monthly pricing
- Founder member badge/status
- Annual member-only live call
- Priority Q&A submission
- Downloadable annual discipline workbook
- Early access to event tickets
- Special recognition as a founding Concrete Builder
"""
    faq = f"""# FAQ

## What is {offer}?
A practical membership for people who want discipline, accountability, encouragement, and weekly action.

## Who is it for?
Students, athletes, fathers, leaders, builders, and supporters who want a clear next step.

## Is this recurring?
Yes for the monthly option. Annual plans are billed once per year.

## How do payments work?
Use the configured external payment link. No card details are stored in this repository.
"""
    terms_placeholder = """# Terms Placeholder

This page is a placeholder for a future membership agreement, refund policy, and billing terms review.
Connect approved legal and payment providers before publishing the final policy language.
"""
    welcome_email = f"""# Welcome Email

Subject: Welcome to {offer}

Welcome to Concrete Builders Membership.

You are here because you want discipline, consistency, faith, and real support.

Your first action this week:
1. Read the weekly challenge.
2. Pick one habit.
3. Report back with your progress.

CTA: Open your member dashboard or payment confirmation page.
"""
    renewal_email = f"""# Renewal / Nurture Email

Subject: Keep building with us

You have already started the work.

Renewing keeps the weekly challenge, live sessions, and accountability going.

CTA: Review your renewal link and keep your seat in Concrete Builders Membership.
"""
    cancellation_save_email = f"""# Cancellation Save Email

Subject: Before you go

If the timing is wrong, consider moving to the annual plan or pausing with a clear return date.

CTA: Review the annual offer or reply with the reason you are leaving so we can improve the program.
"""
    onboarding_checklist = f"""# Member Onboarding Checklist

1. Confirm the payment link.
2. Welcome the member by email.
3. Share the weekly challenge.
4. Add the member to the CRM.
5. Send the first accountability prompt.
6. Point the member to the archive and live session schedule.
"""
    weekly_challenge_template = f"""# Weekly Challenge Template

## Week
<week number>

## Theme
<theme>

## Action
1. Choose one discipline habit.
2. Complete it daily for seven days.
3. Report one win and one obstacle.

## CTA
Join {offer} and stay in the work.
"""
    return MembershipProgram(
        offer=offer,
        monthly_price=monthly_price,
        annual_price=annual_price,
        premium_annual_price=premium_annual_price,
        audience=audience,
        monthly_offer=monthly_offer,
        annual_offer=annual_offer,
        faq=faq,
        terms_placeholder=terms_placeholder,
        welcome_email=welcome_email,
        renewal_email=renewal_email,
        cancellation_save_email=cancellation_save_email,
        onboarding_checklist=onboarding_checklist,
        weekly_challenge_template=weekly_challenge_template,
    )


def save_membership_program(
    program: MembershipProgram,
    output_dir: Path | str = MEMBERSHIP_OUTPUT_FOLDER,
    *,
    created_at: datetime | None = None,
) -> MembershipProgramResult:
    created = (created_at or datetime.now().astimezone()).replace(microsecond=0)
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    folder = root / f"{created.strftime('%Y-%m-%d-%H%M%S')}-{slugify(program.offer)}"
    folder.mkdir(parents=True, exist_ok=True)

    files = {
        "00_membership_sales_page.md": f"""# Membership Sales Page

## Headline
{program.offer}

## Problem
People need a practical place to stay accountable and keep building when motivation fades.

## Promise
We turn discipline into a weekly system people can actually follow.

## Offer
{program.monthly_price}/month, ${program.annual_price}/year, or ${program.premium_annual_price}/year.

## Who It Is For
{program.audience}

## Benefits
- Weekly challenge
- Live session
- Newsletter
- Early access
- Worksheets
- Accountability prompts

## CTA Button Text
Join Concrete Builders Membership

## Payment Link Placeholder
Monthly: [CONCRETE_MOTIVATION_MONTHLY_PAYMENT_LINK]
Annual: [CONCRETE_MOTIVATION_ANNUAL_PAYMENT_LINK]

## Booking / Contact Fallback
Use the booking form or email millerjaytee@gmail.com if payment links are not yet connected.
""",
        "01_monthly_offer.md": program.monthly_offer,
        "02_annual_offer.md": program.annual_offer,
        "03_faq.md": program.faq,
        "04_terms_placeholder.md": program.terms_placeholder,
        "05_welcome_email.md": program.welcome_email,
        "06_renewal_nurture_email.md": program.renewal_email,
        "07_cancellation_save_email.md": program.cancellation_save_email,
        "08_member_onboarding_checklist.md": program.onboarding_checklist,
        "09_weekly_challenge_template.md": program.weekly_challenge_template,
    }
    paths: list[Path] = []
    for filename, body in files.items():
        path = folder / filename
        path.write_text(body.strip() + "\n", encoding="utf-8")
        paths.append(path)
    return MembershipProgramResult(
        program.offer,
        program.monthly_price,
        program.annual_price,
        program.premium_annual_price,
        program.audience,
        tuple(paths),
    )
