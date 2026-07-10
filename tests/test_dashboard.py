from __future__ import annotations

import csv
import sys
from pathlib import Path

from dashboard.ceo_dashboard import main as dashboard_main
from dashboard.content_metrics import build_content_metrics
from dashboard.crm_metrics import build_crm_metrics
from dashboard.metrics import build_dashboard_metrics
from dashboard.revenue_metrics import build_revenue_metrics


def _write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def test_content_metrics_count_existing_artifacts(tmp_path):
    content_root = tmp_path / "outputs" / "content_packages"
    youtube_root = tmp_path / "outputs" / "youtube_packages"

    for folder in (
        content_root / "2026-01-01-alpha",
        content_root / "2026-01-02-bravo-reel-01",
        content_root / "2026-01-03-charlie-day-01",
    ):
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "package.md").write_text(folder.name, encoding="utf-8")

    youtube_root.mkdir(parents=True, exist_ok=True)
    first = youtube_root / "2026-01-01-alpha.md"
    second = youtube_root / "2026-01-04-beta.md"
    first.write_text("alpha", encoding="utf-8")
    second.write_text("beta", encoding="utf-8")
    first.touch()
    second.touch()

    metrics = build_content_metrics(tmp_path)

    assert metrics.total_content_packages == 3
    assert metrics.total_reels_created == 1
    assert metrics.total_shorts_created == 1
    assert metrics.youtube_packages == 2
    assert metrics.last_generated_content == second


def test_crm_metrics_count_workflow_artifacts(tmp_path):
    school = tmp_path / "outputs" / "outreach_messages" / "school_outreach" / "package-1"
    sponsor = tmp_path / "outputs" / "sales_outreach" / "sponsorship" / "package-1"
    podcast = tmp_path / "outputs" / "podcast_production" / "guest_outreach" / "package-1"
    crm_master = tmp_path / "outputs" / "crm" / "concrete_motivation_pipeline.csv"

    _write_csv(
        school / "01_lead_template.csv",
        ["school_name", "contact_name", "role", "email", "phone", "city", "state", "fit_score", "status", "next_action", "notes"],
        [
            {"role": "athletic_director", "status": "new", "next_action": "send intro email", "notes": "a"},
            {"role": "principal", "status": "new", "next_action": "research school priorities", "notes": "b"},
        ],
    )
    _write_csv(
        sponsor / "01_sponsor_prospect_list_template.csv",
        ["company_name", "contact_name", "contact_role", "email", "category", "fit_score", "stage", "next_action", "notes"],
        [
            {"category": "local_business", "fit_score": "0", "stage": "new", "next_action": "research fit"},
            {"category": "brand_partner", "fit_score": "0", "stage": "new", "next_action": "send intro"},
            {"category": "community_partner", "fit_score": "0", "stage": "new", "next_action": "find contact"},
        ],
    )
    podcast.mkdir(parents=True, exist_ok=True)
    _write_csv(
        podcast / "01_guest_list.csv",
        ["guest_name", "organization", "email", "fit_score", "status", "next_action", "notes"],
        [
            {"guest_name": "Potential Guest 1", "organization": "Leaders Network", "fit_score": "5", "status": "new", "next_action": "send invitation", "notes": ""},
            {"guest_name": "Potential Guest 2", "organization": "Creators Network", "fit_score": "4", "status": "new", "next_action": "research guest angle", "notes": ""},
        ],
    )
    _write_csv(
        crm_master,
        ["lead_name", "organization", "contact_name", "role", "email", "phone", "segment", "offer", "stage", "last_contact_date", "next_follow_up_date", "source", "notes", "outcome"],
        [
            {"lead_name": "Lead 1", "organization": "School A", "role": "Athletic Director", "segment": "school", "offer": "Speaking Session", "stage": "New Lead", "source": "CRM Pipeline Manager", "notes": ""},
            {"lead_name": "Lead 2", "organization": "Sponsor B", "role": "Owner", "segment": "sponsor", "offer": "Sponsorship", "stage": "Contacted", "source": "CRM Pipeline Manager", "notes": ""},
            {"lead_name": "Lead 3", "organization": "Podcast C", "role": "Host", "segment": "podcast_guest", "offer": "Guest Interview", "stage": "Follow-Up Due", "source": "CRM Pipeline Manager", "notes": ""},
        ],
    )

    metrics = build_crm_metrics(tmp_path)

    assert metrics.school_outreach_contacts == 2
    assert metrics.sponsor_contacts == 3
    assert metrics.podcast_guests == 2
    assert metrics.pending_follow_ups == 3


def test_revenue_metrics_count_workflow_artifacts(monkeypatch, tmp_path):
    monkeypatch.setenv("CONCRETE_MOTIVATION_MONTHLY_PAYMENT_LINK", "https://pay.concretemotivation.test/monthly")
    monkeypatch.setenv("CONCRETE_MOTIVATION_ANNUAL_PAYMENT_LINK", "https://pay.concretemotivation.test/annual")
    monkeypatch.setenv("CONCRETE_MOTIVATION_BOOKING_PAYMENT_LINK", "https://pay.concretemotivation.test/booking")
    monkeypatch.setenv("CONCRETE_MOTIVATION_SPONSOR_PAYMENT_LINK", "https://pay.concretemotivation.test/sponsor")

    for folder in (
        tmp_path / "outputs" / "membership" / "2026-01-01-alpha",
        tmp_path / "outputs" / "revenue_commander" / "2026-01-02-bravo",
        tmp_path / "outputs" / "social_sales" / "2026-01-03-charlie",
        tmp_path / "outputs" / "speaker_booking" / "2026-01-04-delta",
        tmp_path / "outputs" / "sales_outreach" / "sponsorship" / "2026-01-05-echo",
    ):
        folder.mkdir(parents=True, exist_ok=True)

    metrics = build_revenue_metrics(tmp_path)

    assert metrics.membership_packages_created == 1
    assert metrics.configured_payment_links == 4
    assert metrics.revenue_campaign_packages == 2
    assert metrics.speaker_booking_packages == 1
    assert metrics.sponsor_packages == 1
    assert metrics.membership_launch_readiness_score == 100
    assert metrics.next_revenue_command == "Review the CEO dashboard and stage the next revenue push"


def test_dashboard_script_writes_report(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("CONCRETE_MOTIVATION_MONTHLY_PAYMENT_LINK", "https://pay.concretemotivation.test/monthly")
    monkeypatch.setenv("CONCRETE_MOTIVATION_ANNUAL_PAYMENT_LINK", "https://pay.concretemotivation.test/annual")
    monkeypatch.setenv("CONCRETE_MOTIVATION_BOOKING_PAYMENT_LINK", "https://pay.concretemotivation.test/booking")
    monkeypatch.setenv("CONCRETE_MOTIVATION_SPONSOR_PAYMENT_LINK", "https://pay.concretemotivation.test/sponsor")
    for folder in (
        tmp_path / "outputs" / "membership" / "2026-01-01-alpha",
        tmp_path / "outputs" / "revenue_commander" / "2026-01-02-bravo",
        tmp_path / "outputs" / "social_sales" / "2026-01-03-charlie",
        tmp_path / "outputs" / "speaker_booking" / "2026-01-04-delta",
        tmp_path / "outputs" / "sales_outreach" / "sponsorship" / "2026-01-05-echo",
    ):
        folder.mkdir(parents=True, exist_ok=True)

    dashboard_path = tmp_path / "ceo_dashboard.md"
    metrics = build_dashboard_metrics(tmp_path)
    monkeypatch.setattr("dashboard.ceo_dashboard.build_dashboard_metrics", lambda _root: metrics)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ceo_dashboard.py",
            "--output",
            str(dashboard_path),
        ],
    )

    assert dashboard_main() == 0
    output = capsys.readouterr().out

    assert dashboard_path.is_file()
    assert "# Concrete Motivation Executive Dashboard" in dashboard_path.read_text(encoding="utf-8")
    assert "Total content packages" in output
    assert "Membership packages created" in output
    assert "Weekly Scoreboard" in output
    assert "Next revenue command" in output
    assert "Saved dashboard:" in output
