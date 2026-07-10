"""Revenue metrics for the Concrete Motivation executive dashboard."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from concrete_motivation.payment_link_manager import PaymentLinkManager


@dataclass(frozen=True, slots=True)
class RevenueMetrics:
    membership_packages_created: int
    configured_payment_links: int
    total_payment_links: int
    revenue_campaign_packages: int
    speaker_booking_packages: int
    sponsor_packages: int
    membership_launch_readiness_score: int
    next_revenue_command: str

    def as_rows(self) -> tuple[tuple[str, str], ...]:
        return (
            ("Membership packages created", str(self.membership_packages_created)),
            (
                "Configured payment links",
                f"{self.configured_payment_links}/{self.total_payment_links}",
            ),
            ("Revenue campaign packages", str(self.revenue_campaign_packages)),
            ("Speaker booking packages", str(self.speaker_booking_packages)),
            ("Sponsor packages", str(self.sponsor_packages)),
            ("Membership launch readiness score", f"{self.membership_launch_readiness_score}/100"),
            ("Next revenue command", self.next_revenue_command),
        )


def _count_package_folders(root: Path, folder_name: str) -> int:
    folder = root / folder_name
    if not folder.exists():
        return 0
    return sum(1 for path in folder.iterdir() if path.is_dir())


def build_revenue_metrics(root: Path | str | None = None) -> RevenueMetrics:
    base = Path(root) if root is not None else Path(__file__).resolve().parent.parent
    outputs = base / "outputs"
    membership = _count_package_folders(outputs, "membership")
    revenue_commander = _count_package_folders(outputs, "revenue_commander")
    social_sales = _count_package_folders(outputs, "social_sales")
    speaker_booking = _count_package_folders(outputs, "speaker_booking")
    sponsor = _count_package_folders(outputs / "sales_outreach", "sponsorship")

    payment_status = PaymentLinkManager().status()
    configured_links = payment_status.configured_count
    total_links = payment_status.total_count

    readiness = 0
    readiness += 20 if membership else 0
    readiness += 20 if configured_links == total_links else 0
    readiness += 20 if revenue_commander or social_sales else 0
    readiness += 20 if speaker_booking else 0
    readiness += 20 if sponsor else 0

    if membership == 0:
        next_command = "Run create_membership_program.py"
    elif configured_links < total_links:
        next_command = "Run create_payment_link_config.py and connect payment links"
    elif revenue_commander == 0 and social_sales == 0:
        next_command = "Run create_social_sales_campaign.py"
    elif speaker_booking == 0:
        next_command = "Run create_speaker_booking_package.py"
    elif sponsor == 0:
        next_command = "Review sponsor outreach and package the offer"
    else:
        next_command = "Review the CEO dashboard and stage the next revenue push"

    return RevenueMetrics(
        membership_packages_created=membership,
        configured_payment_links=configured_links,
        total_payment_links=total_links,
        revenue_campaign_packages=revenue_commander + social_sales,
        speaker_booking_packages=speaker_booking,
        sponsor_packages=sponsor,
        membership_launch_readiness_score=readiness,
        next_revenue_command=next_command,
    )

