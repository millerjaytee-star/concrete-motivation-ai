"""Build speaker booking revenue packages."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from concrete_motivation.slugify import slugify


SPEAKER_BOOKING_FOLDER = Path(__file__).resolve().parent.parent / "outputs" / "speaker_booking"


SEGMENT_NAMES = {
    "schools": "Schools",
    "churches": "Churches",
    "youth programs": "Youth Programs",
    "colleges": "Colleges",
    "corporate leadership teams": "Corporate Leadership Teams",
}


@dataclass(frozen=True, slots=True)
class SpeakerBookingPackage:
    segment: str
    theme: str
    speaking_topics: tuple[str, ...]
    price_menu: tuple[str, ...]
    proposal_outline: str
    outreach_email: str
    follow_up_sequence: str
    booking_cta: str
    payment_link_placeholder: str
    crm_import_row: str

    def as_markdown(self) -> str:
        topics = "\n".join(f"- {item}" for item in self.speaking_topics)
        pricing = "\n".join(f"- {item}" for item in self.price_menu)
        return f"""# Speaker Booking Package

## Segment
{self.segment}

## Theme
{self.theme}

## Speaking Topics
{topics}

## Price Menu
{pricing}

## Proposal Outline
{self.proposal_outline}

## Outreach Email
{self.outreach_email}

## Follow-Up Sequence
{self.follow_up_sequence}

## Booking CTA
{self.booking_cta}

## Payment / Deposit Link Placeholder
{self.payment_link_placeholder}

## CRM Import Row
{self.crm_import_row}
"""


@dataclass(frozen=True, slots=True)
class SpeakerBookingResult:
    segment: str
    theme: str
    created_paths: tuple[Path, ...]

    def as_markdown(self) -> str:
        files = "\n".join(f"- {path}" for path in self.created_paths)
        return (
            "# Speaker Booking Package Complete\n\n"
            f"**Segment:** {self.segment}\n\n"
            f"**Theme:** {self.theme}\n\n"
            "## Files Created\n"
            f"{files}"
        )


def _normalize_segment(segment: str) -> str:
    value = " ".join(segment.strip().lower().split())
    if value in SEGMENT_NAMES:
        return value
    if value.rstrip("s") in SEGMENT_NAMES:
        return value.rstrip("s")
    return value or "schools"


def build_speaker_booking_package(
    segment: str = "schools",
    theme: str = "Pressure Has a Purpose",
    *,
    offer: str = "Concrete Builders Membership",
) -> SpeakerBookingPackage:
    normalized = _normalize_segment(segment)
    segment_name = SEGMENT_NAMES.get(normalized, normalized.title())
    topics = (
        f"{theme}: building discipline under pressure",
        "How consistency changes outcomes",
        "Leadership when no one is cheering",
        "Family, faith, and follow-through",
    )
    price_menu = (
        "Keynote: [price placeholder]",
        "Workshop: [price placeholder]",
        "Half-day training: [price placeholder]",
        "Booking deposit: [payment link placeholder]",
    )
    proposal_outline = f"""1. Speaker introduction
2. Audience fit
3. Speaking topics
4. Logistics
5. Price menu placeholders
6. Payment/deposit placeholder
7. Next step
"""
    outreach_email = f"""Subject: Speaking opportunity for {segment_name}

Hello,

I am Jaytee Miller with Concrete Motivation. I help audiences turn pressure into discipline and purpose.

I would love to share a message built around {theme} with your {segment_name.lower()} audience.

Would you be open to a short conversation?
"""
    follow_up_sequence = """Follow-up 1: send a one-page outline and topic list.
Follow-up 2: confirm fit, audience needs, and date range.
Follow-up 3: close the loop with a booking CTA and payment placeholder.
"""
    booking_cta = "Reply to request a date, audience size, and speaking format."
    payment_link_placeholder = "[CONCRETE_MOTIVATION_BOOKING_PAYMENT_LINK]"
    from io import StringIO
    import csv

    buffer = StringIO()
    writer = csv.DictWriter(
        buffer,
        fieldnames=[
            "lead_name",
            "organization",
            "contact_name",
            "role",
            "email",
            "phone",
            "segment",
            "offer",
            "stage",
            "last_contact_date",
            "next_follow_up_date",
            "source",
            "notes",
            "outcome",
        ],
    )
    writer.writeheader()
    writer.writerow(
        {
            "lead_name": f"{segment_name} Booking Lead",
            "organization": segment_name,
            "contact_name": "",
            "role": "Decision maker",
            "email": "",
            "phone": "",
            "segment": normalized,
            "offer": offer,
            "stage": "New Lead",
            "last_contact_date": "",
            "next_follow_up_date": "",
            "source": "Speaker Booking Package",
            "notes": f"{theme} for {segment_name}",
            "outcome": "",
        }
    )
    crm_import_row = buffer.getvalue()
    return SpeakerBookingPackage(
        segment=segment_name,
        theme=theme,
        speaking_topics=topics,
        price_menu=price_menu,
        proposal_outline=proposal_outline,
        outreach_email=outreach_email,
        follow_up_sequence=follow_up_sequence,
        booking_cta=booking_cta,
        payment_link_placeholder=payment_link_placeholder,
        crm_import_row=crm_import_row,
    )


def save_speaker_booking_package(
    package: SpeakerBookingPackage,
    output_dir: Path | str = SPEAKER_BOOKING_FOLDER,
    *,
    created_at: datetime | None = None,
) -> SpeakerBookingResult:
    created = (created_at or datetime.now().astimezone()).replace(microsecond=0)
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    folder = root / f"{created.strftime('%Y-%m-%d-%H%M%S')}-{slugify(package.segment)}-{slugify(package.theme)}"
    folder.mkdir(parents=True, exist_ok=True)

    files = {
        "00_speaker_booking_package.md": package.as_markdown(),
        "01_speaking_topics.md": "\n".join(package.speaking_topics),
        "02_price_menu.md": "\n".join(package.price_menu),
        "03_proposal_outline.md": package.proposal_outline,
        "04_outreach_email.md": package.outreach_email,
        "05_follow_up_sequence.md": package.follow_up_sequence,
        "06_booking_cta.md": package.booking_cta,
        "07_payment_link_placeholder.md": package.payment_link_placeholder,
        "08_crm_import_row.csv": package.crm_import_row + "\n",
        "09_speaker_booking_package.json": json.dumps(
            {
                "segment": package.segment,
                "theme": package.theme,
                "speaking_topics": list(package.speaking_topics),
                "price_menu": list(package.price_menu),
                "proposal_outline": package.proposal_outline,
                "outreach_email": package.outreach_email,
                "follow_up_sequence": package.follow_up_sequence,
                "booking_cta": package.booking_cta,
                "payment_link_placeholder": package.payment_link_placeholder,
            },
            indent=2,
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
    return SpeakerBookingResult(package.segment, package.theme, tuple(created_paths))
