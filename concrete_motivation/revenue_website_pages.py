"""Create payment-link-ready website revenue pages."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from concrete_motivation.payment_link_manager import PaymentLinkManager


WEBSITE_CONTENT_DIR = Path(__file__).resolve().parent.parent / "website_content"


@dataclass(frozen=True, slots=True)
class RevenueWebsitePagesResult:
    created_paths: tuple[Path, ...]

    def as_markdown(self) -> str:
        files = "\n".join(f"- {path}" for path in self.created_paths)
        return f"# Revenue Website Pages Complete\n\n## Files Created\n{files}"


def _page(
    headline: str,
    problem: str,
    promise: str,
    offer: str,
    who_it_is_for: str,
    benefits: tuple[str, ...],
    cta_button_text: str,
    payment_link_placeholder: str,
    booking_contact_fallback: str,
) -> str:
    benefits_lines = "\n".join(f"- {item}" for item in benefits)
    return f"""# {headline}

## Problem
{problem}

## Promise
{promise}

## Offer
{offer}

## Who It Is For
{who_it_is_for}

## Benefits
{benefits_lines}

## CTA Button Text
{cta_button_text}

## Payment Link Placeholder
{payment_link_placeholder}

## Booking / Contact Fallback
{booking_contact_fallback}
"""


def build_revenue_website_pages(
    offer: str = "Concrete Builders Membership",
    monthly_price: int = 40,
    annual_price: int = 400,
    premium_annual_price: int = 444,
    payment_manager: PaymentLinkManager | None = None,
) -> dict[str, str]:
    manager = payment_manager or PaymentLinkManager()
    links = manager.load()
    monthly_link = links["monthly_payment_link"]
    annual_link = links["annual_payment_link"]
    booking_link = links["booking_payment_link"]
    sponsor_link = links["sponsor_payment_link"]
    membership = _page(
        headline="Concrete Builders Membership",
        problem="Supporters need a weekly system that turns motivation into disciplined action.",
        promise="We help members keep building through weekly challenges, live sessions, and accountability.",
        offer=f"${monthly_price}/month, ${annual_price}/year launch annual plan, or ${premium_annual_price}/year premium annual plan.",
        who_it_is_for="Students, athletes, fathers, leaders, builders, and supporters who want a practical rhythm.",
        benefits=(
            "Weekly Concrete Motivation challenge",
            "Monthly live mindset and discipline session",
            "Private member newsletter",
            "Early access to speeches, videos, and podcast clips",
            "Worksheets and action plans",
            "Member-only accountability prompts",
        ),
        cta_button_text="Join Concrete Builders Membership",
        payment_link_placeholder=f"Monthly: {monthly_link}\nAnnual: {annual_link}",
        booking_contact_fallback="If the payment link is not active yet, use the contact form or email millerjaytee@gmail.com.",
    )
    speaking = _page(
        headline="Book Jaytee to Speak",
        problem="Schools, churches, companies, and youth programs need honest leadership messages that lead to action.",
        promise="Every talk is built to leave the room with a clear next move, not just emotion.",
        offer="Keynotes, workshops, team talks, leadership sessions, and live conversations.",
        who_it_is_for="Schools, churches, youth organizations, colleges, and corporate leadership teams.",
        benefits=(
            "Pressure-to-purpose message",
            "Interactive delivery",
            "Audience-specific takeaway",
            "Follow-up challenge",
            "Booking-ready logistics",
        ),
        cta_button_text="Request a Speaking Date",
        payment_link_placeholder=f"Booking deposit link: {booking_link}",
        booking_contact_fallback="Use the booking form or email millerjaytee@gmail.com to start the conversation.",
    )
    sponsors = _page(
        headline="Sponsor Concrete Motivation",
        problem="Brands want a values-led way to reach a disciplined, growth-minded audience.",
        promise="We provide partnership opportunities that support the mission and the community.",
        offer="Sponsor packages for podcast, video, community, and membership support.",
        who_it_is_for="Local businesses, youth development organizations, brands, and community partners.",
        benefits=(
            "Aligned audience reach",
            "Story-driven placement",
            "Community visibility",
            "Podcast and video association",
            "Repeat exposure options",
        ),
        cta_button_text="Explore Sponsorship",
        payment_link_placeholder=f"Sponsor payment link: {sponsor_link}",
        booking_contact_fallback="If the sponsor link is unavailable, use the booking form or email millerjaytee@gmail.com.",
    )
    book = _page(
        headline="Book Jaytee Miller",
        problem="Audiences need a speaker who can connect pain, discipline, leadership, and purpose without fake hype.",
        promise="Jaytee brings a direct, practical, faith-aware message that moves people to action.",
        offer="Speaking, workshops, live podcast conversations, and leadership sessions.",
        who_it_is_for="Schools, churches, youth programs, colleges, and leadership teams.",
        benefits=(
            "Clear message",
            "Audience-first examples",
            "Practical challenge",
            "Booking-ready call to action",
            "Follow-up support",
        ),
        cta_button_text="Book Jaytee Now",
        payment_link_placeholder=f"Booking deposit link: {booking_link}",
        booking_contact_fallback="Use the booking form or email millerjaytee@gmail.com.",
    )
    payment_links = f"""# Payment Links

## Problem
We need a safe place to show payment options without storing secrets in the repo.

## Promise
Payment links are loaded from environment variables or the ignored local config file.

## Offer
- Monthly membership link
- Annual membership link
- Booking deposit link
- Sponsor payment link

## Who It Is For
The internal team preparing payment-link-ready website pages.

## Benefits
- No card numbers stored here
- Clear placeholders when links are missing
- Easy update path for approved providers

## CTA Button Text
Review Payment Link Status

## Payment Link Placeholder
Monthly: {monthly_link}
Annual: {annual_link}
Booking: {booking_link}
Sponsor: {sponsor_link}

## Booking / Contact Fallback
Use the booking form or email millerjaytee@gmail.com if a link is not yet configured.
"""
    return {
        "membership.md": membership,
        "speaking.md": speaking,
        "sponsors.md": sponsors,
        "book_jaytee.md": book,
        "payment_links.md": payment_links,
    }


def save_revenue_website_pages(
    output_dir: Path | str = WEBSITE_CONTENT_DIR,
    *,
    offer: str = "Concrete Builders Membership",
    monthly_price: int = 40,
    annual_price: int = 400,
    premium_annual_price: int = 444,
    payment_manager: PaymentLinkManager | None = None,
    created_at: datetime | None = None,
) -> RevenueWebsitePagesResult:
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    pages = build_revenue_website_pages(
        offer=offer,
        monthly_price=monthly_price,
        annual_price=annual_price,
        premium_annual_price=premium_annual_price,
        payment_manager=payment_manager,
    )
    created_paths = []
    for filename, body in pages.items():
        path = root / filename
        path.write_text(body.strip() + "\n", encoding="utf-8")
        created_paths.append(path)
    return RevenueWebsitePagesResult(tuple(created_paths))

