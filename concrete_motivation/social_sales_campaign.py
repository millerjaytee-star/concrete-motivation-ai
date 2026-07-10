"""Build a 14-day social sales campaign for membership and bookings."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from concrete_motivation.slugify import slugify


SOCIAL_SALES_OUTPUT_FOLDER = Path(__file__).resolve().parent.parent / "outputs" / "social_sales"


@dataclass(frozen=True, slots=True)
class SocialSalesCampaign:
    offer: str
    days: int
    audience: str
    instagram_captions: tuple[str, ...]
    facebook_posts: tuple[str, ...]
    linkedin_posts: tuple[str, ...]
    reel_scripts: tuple[str, ...]
    youtube_community_posts: tuple[str, ...]
    newsletter_angles: tuple[str, ...]
    cta_calendar: tuple[tuple[int, str, str], ...]

    def as_markdown(self) -> str:
        return f"""# Social Sales Campaign

## Offer
{self.offer}

## Days
{self.days}

## Audience
{self.audience}
"""


@dataclass(frozen=True, slots=True)
class SocialSalesCampaignResult:
    offer: str
    days: int
    audience: str
    created_paths: tuple[Path, ...]

    def as_markdown(self) -> str:
        files = "\n".join(f"- {path}" for path in self.created_paths)
        return (
            "# Social Sales Campaign Complete\n\n"
            f"**Offer:** {self.offer}\n\n"
            f"**Days:** {self.days}\n\n"
            f"**Audience:** {self.audience}\n\n"
            "## Files Created\n"
            f"{files}"
        )


def _series(prefix: str, offer: str, days: int, audience: str, cta: str) -> tuple[str, ...]:
    entries = []
    for day in range(1, days + 1):
        entries.append(
            f"Day {day}: {prefix} for {offer}. Speak to {audience}. CTA: {cta}."
        )
    return tuple(entries)


def build_social_sales_campaign(
    offer: str = "Concrete Builders Membership",
    days: int = 14,
    audience: str = "Concrete Motivation supporters",
) -> SocialSalesCampaign:
    instagram = _series("Instagram caption", offer, days, audience, "Join the membership or book Jaytee")
    facebook = _series("Facebook post", offer, days, audience, "Join the membership or book Jaytee")
    linkedin = _series("LinkedIn post", offer, days, audience, "Explore the membership or speaker booking")
    reels = _series("Short Reel script", offer, days, audience, "Join the membership today")
    community = _series("YouTube Community post", offer, days, audience, "Join the membership or request booking")
    newsletter_angles = tuple(
        f"Newsletter angle {day}: why {offer} helps {audience} stay disciplined and accountable."
        for day in range(1, 8)
    )
    cta_calendar = tuple(
        (
            day,
            "membership" if day % 2 else "booking",
            f"Day {day} CTA: {'Join the membership' if day % 2 else 'Book Jaytee'}",
        )
        for day in range(1, days + 1)
    )
    return SocialSalesCampaign(
        offer=offer,
        days=days,
        audience=audience,
        instagram_captions=instagram,
        facebook_posts=facebook,
        linkedin_posts=linkedin,
        reel_scripts=reels,
        youtube_community_posts=community,
        newsletter_angles=newsletter_angles,
        cta_calendar=cta_calendar,
    )


def save_social_sales_campaign(
    campaign: SocialSalesCampaign,
    output_dir: Path | str = SOCIAL_SALES_OUTPUT_FOLDER,
    *,
    created_at: datetime | None = None,
) -> SocialSalesCampaignResult:
    created = (created_at or datetime.now().astimezone()).replace(microsecond=0)
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    folder = root / f"{created.strftime('%Y-%m-%d-%H%M%S')}-{slugify(campaign.offer)}"
    folder.mkdir(parents=True, exist_ok=True)

    files = {
        "00_social_sales_campaign.md": campaign.as_markdown(),
        "01_instagram_captions.md": "\n\n".join(campaign.instagram_captions),
        "02_facebook_posts.md": "\n\n".join(campaign.facebook_posts),
        "03_linkedin_posts.md": "\n\n".join(campaign.linkedin_posts),
        "04_reel_scripts.md": "\n\n".join(campaign.reel_scripts),
        "05_youtube_community_posts.md": "\n\n".join(campaign.youtube_community_posts),
        "06_newsletter_angles.md": "\n\n".join(campaign.newsletter_angles),
        "07_cta_calendar.csv": _cta_csv(campaign),
        "08_social_sales_campaign.json": json.dumps(
            {
                "offer": campaign.offer,
                "days": campaign.days,
                "audience": campaign.audience,
                "instagram_captions": list(campaign.instagram_captions),
                "facebook_posts": list(campaign.facebook_posts),
                "linkedin_posts": list(campaign.linkedin_posts),
                "reel_scripts": list(campaign.reel_scripts),
                "youtube_community_posts": list(campaign.youtube_community_posts),
                "newsletter_angles": list(campaign.newsletter_angles),
                "cta_calendar": [
                    {"day": day, "channel": channel, "cta": cta}
                    for day, channel, cta in campaign.cta_calendar
                ],
            },
            indent=2,
        ),
    }
    created_paths: list[Path] = []
    for filename, body in files.items():
        path = folder / filename
        if filename.endswith(".json"):
            path.write_text(body + "\n", encoding="utf-8")
        else:
            path.write_text(body.strip() + "\n", encoding="utf-8")
        created_paths.append(path)
    return SocialSalesCampaignResult(campaign.offer, campaign.days, campaign.audience, tuple(created_paths))


def _cta_csv(campaign: SocialSalesCampaign) -> str:
    from io import StringIO

    handle = StringIO()
    writer = csv.DictWriter(handle, fieldnames=["day", "channel", "cta"])
    writer.writeheader()
    for day, channel, cta in campaign.cta_calendar:
        writer.writerow({"day": day, "channel": channel, "cta": cta})
    return handle.getvalue()

