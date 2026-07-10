"""Stage Gmail membership sales drafts without sending email."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from concrete_motivation.slugify import slugify


GMAIL_STAGING_FOLDER = Path(__file__).resolve().parent.parent / "outputs" / "gmail_staging" / "membership"


@dataclass(frozen=True, slots=True)
class GmailDraft:
    name: str
    subject: str
    body: str
    cta: str
    label: str
    crm_stage: str
    follow_up_date: str

    def as_markdown(self) -> str:
        return f"""# {self.name}

## Subject
{self.subject}

## Body
{self.body}

## CTA
{self.cta}

## Suggested Gmail Label
{self.label}

## CRM Stage
{self.crm_stage}

## Follow-Up Date
{self.follow_up_date}
"""


@dataclass(frozen=True, slots=True)
class GmailSalesSequence:
    offer: str
    audience: str
    drafts: tuple[GmailDraft, ...]

    def as_markdown(self) -> str:
        blocks = [f"# Gmail Sales Sequence\n\n**Offer:** {self.offer}\n\n**Audience:** {self.audience}"]
        blocks.extend(draft.as_markdown() for draft in self.drafts)
        return "\n\n".join(blocks)


@dataclass(frozen=True, slots=True)
class GmailSalesSequenceResult:
    offer: str
    audience: str
    created_paths: tuple[Path, ...]

    def as_markdown(self) -> str:
        files = "\n".join(f"- {path}" for path in self.created_paths)
        return (
            "# Gmail Membership Sequence Complete\n\n"
            f"**Offer:** {self.offer}\n\n"
            f"**Audience:** {self.audience}\n\n"
            "## Files Created\n"
            f"{files}"
        )


def build_gmail_sales_sequence(
    offer: str = "Concrete Builders Membership",
    audience: str = "Concrete Motivation supporters",
    *,
    created_at: datetime | None = None,
) -> GmailSalesSequence:
    now = created_at or datetime.now().astimezone()
    offsets = [0, 1, 3, 5, 7, 10, 14]
    names = [
        "Launch Email",
        "Story Email",
        "Benefits Email",
        "Objection Email",
        "Annual Plan Email",
        "Last-Call Email",
        "Welcome Email",
    ]
    subjects = [
        f"Join {offer}",
        "Why this membership exists",
        f"How {offer} helps you stay on track",
        "What if I am too busy?",
        "A better annual option",
        "Last call to join the first wave",
        f"Welcome to {offer}",
    ]
    bodies = [
        f"{offer} is the weekly rhythm for people who want discipline, accountability, and real support.",
        "This started because pressure does not disappear just because motivation does.",
        "The membership gives weekly challenge, live support, newsletters, and accountability prompts.",
        "Busy people still need a system. The membership is built to fit a real life.",
        "The annual plan is the better value for members who want to stay connected all year.",
        "This is the last reminder before the launch group closes.",
        "Here is how to get started, read the challenge, and take the first action.",
    ]
    ctas = [
        "Join the membership using the approved payment link.",
        "Reply if you want the backstory or a quick overview.",
        "Review the member benefits and join now.",
        "Choose the option that fits your season.",
        "Upgrade to the annual plan for the best value.",
        "Join now before the launch window closes.",
        "Open your welcome resources and start the weekly challenge.",
    ]
    labels = [
        "CM/Membership Launch",
        "CM/Membership Story",
        "CM/Membership Benefits",
        "CM/Membership Objection",
        "CM/Membership Annual",
        "CM/Membership Last Call",
        "CM/Membership Welcome",
    ]
    stages = [
        "New Lead",
        "Contacted",
        "Follow-Up Due",
        "Follow-Up Due",
        "Proposal Sent",
        "Follow-Up Due",
        "Booked/Paid",
    ]
    drafts = []
    for index, name in enumerate(names):
        draft_date = (now + timedelta(days=offsets[index])).date().isoformat()
        drafts.append(
            GmailDraft(
                name=name,
                subject=subjects[index],
                body=bodies[index],
                cta=ctas[index],
                label=labels[index],
                crm_stage=stages[index],
                follow_up_date=draft_date,
            )
        )
    return GmailSalesSequence(offer=offer, audience=audience, drafts=tuple(drafts))


def save_gmail_sales_sequence(
    sequence: GmailSalesSequence,
    output_dir: Path | str = GMAIL_STAGING_FOLDER,
    *,
    created_at: datetime | None = None,
) -> GmailSalesSequenceResult:
    created = (created_at or datetime.now().astimezone()).replace(microsecond=0)
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    folder = root / f"{created.strftime('%Y-%m-%d-%H%M%S')}-{slugify(sequence.offer)}"
    folder.mkdir(parents=True, exist_ok=True)
    created_paths: list[Path] = []
    for index, draft in enumerate(sequence.drafts, start=1):
        path = folder / f"{index:02d}_{slugify(draft.name)}.md"
        path.write_text(draft.as_markdown().strip() + "\n", encoding="utf-8")
        created_paths.append(path)
    return GmailSalesSequenceResult(sequence.offer, sequence.audience, tuple(created_paths))

