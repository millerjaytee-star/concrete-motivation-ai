from __future__ import annotations

import csv
import sys

from concrete_motivation.crm_pipeline_manager import CRMPipelineManager
from concrete_motivation.podcast_guest_bot import PodcastGuestBot
from concrete_motivation.school_outreach_bot import SchoolOutreachBot
from concrete_motivation.sponsorship_bot import SponsorshipBot
from scripts import add_crm_lead, create_crm_pipeline, create_podcast_guest_campaign, create_school_outreach_campaign, create_sponsor_campaign, show_crm_dashboard


def test_school_outreach_bot_writes_expected_assets(tmp_path):
    result = SchoolOutreachBot(root=tmp_path).run("discipline after pressure", "high school athletes", "DMV")

    assert len(result.created_paths) == 9
    lead_csv = next(path for path in result.created_paths if path.name.endswith(".csv"))
    rows = list(csv.DictReader(lead_csv.read_text(encoding="utf-8").splitlines()))
    assert rows[0]["status"] == "new"
    assert "Speaking opportunity" in next(path for path in result.created_paths if path.name == "02_initial_message.md").read_text(encoding="utf-8")
    assert "follow-up" in next(path for path in result.created_paths if path.name == "03_follow_up_1.md").read_text(encoding="utf-8").lower()
    assert "06_crm_import_row.csv" in {path.name for path in result.created_paths}


def test_sponsorship_bot_writes_expected_assets(tmp_path):
    result = SponsorshipBot(root=tmp_path).run("pressure has a purpose", "local brands", "local gyms and barbershops")

    assert len(result.created_paths) == 9
    prospect = next(path for path in result.created_paths if path.name.endswith(".csv"))
    assert "company_name" in prospect.read_text(encoding="utf-8")
    assert "Partnership opportunity" in next(path for path in result.created_paths if path.name == "02_initial_message.md").read_text(encoding="utf-8")
    assert "Sponsor" in next(path for path in result.created_paths if path.name == "05_proposal_outline.md").read_text(encoding="utf-8")


def test_podcast_guest_bot_writes_expected_assets(tmp_path):
    result = PodcastGuestBot(root=tmp_path).run("pressure builds discipline", "leaders and creators")

    assert len(result.created_paths) == 10
    questions = next(path for path in result.created_paths if path.name == "05_interview_questions.md").read_text(encoding="utf-8")
    scoring = next(path for path in result.created_paths if path.name == "06_guest_scoring_system.md").read_text(encoding="utf-8")
    assert "Interview Questions" in questions
    assert "Guest Scoring System" in scoring
    assert "Invite guests who score 20 or higher" in scoring


def test_crm_pipeline_manager_writes_stage_tracking_and_exports(tmp_path):
    result = CRMPipelineManager(root=tmp_path).run("discipline after pressure", "high school athletes")

    assert len(result.created_paths) == 6
    overview = next(path for path in result.created_paths if path.name == "00_crm_pipeline_overview.md")
    assert "CRM Pipeline Overview" in overview.read_text(encoding="utf-8")
    follow_up_csv = next(path for path in result.created_paths if path.name == "02_follow_up_dates.csv")
    export_csv = next(path for path in result.created_paths if path.name == "04_csv_export.csv")
    dashboard = next(path for path in result.created_paths if path.name == "03_pipeline_dashboard.md")
    assert follow_up_csv.read_text(encoding="utf-8").startswith("lead_name,stage,follow_up_date")
    header = export_csv.read_text(encoding="utf-8").splitlines()[0]
    assert header == (
        "lead_name,organization,contact_name,role,email,phone,segment,offer,stage,"
        "last_contact_date,next_follow_up_date,source,notes,outcome"
    )
    assert "Pipeline Dashboard" in dashboard.read_text(encoding="utf-8")


def test_crm_pipeline_script_initializes_master_csv(monkeypatch, tmp_path, capsys):
    csv_path = tmp_path / "outputs" / "crm" / "concrete_motivation_pipeline.csv"
    out_dir = tmp_path / "outputs" / "crm" / "pipeline_manager"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "create_crm_pipeline.py",
            "--csv-path",
            str(csv_path),
            "--output-dir",
            str(out_dir),
        ],
    )

    assert create_crm_pipeline.main() == 0
    output = capsys.readouterr().out
    assert csv_path.is_file()
    assert "Saved master CSV:" in output


def test_crm_lead_script_appends_to_master_csv(monkeypatch, tmp_path, capsys):
    csv_path = tmp_path / "outputs" / "crm" / "concrete_motivation_pipeline.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.write_text(
        "lead_name,organization,contact_name,role,email,phone,segment,offer,stage,last_contact_date,next_follow_up_date,source,notes,outcome\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "add_crm_lead.py",
            "--lead-name",
            "Lead 1",
            "--organization",
            "School A",
            "--csv-path",
            str(csv_path),
        ],
    )

    assert add_crm_lead.main() == 0
    output = capsys.readouterr().out
    assert "Added lead" in output


def test_campaign_scripts_import_and_run(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "create_school_outreach_campaign.py",
            "--audience",
            "high school athletes",
            "--region",
            "DMV",
            "--output-dir",
            str(tmp_path / "school"),
        ],
    )
    assert create_school_outreach_campaign.main() == 0

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "create_sponsor_campaign.py",
            "--segment",
            "local gyms and barbershops",
            "--output-dir",
            str(tmp_path / "sponsor"),
        ],
    )
    assert create_sponsor_campaign.main() == 0

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "create_podcast_guest_campaign.py",
            "--theme",
            "pressure to purpose",
            "--output-dir",
            str(tmp_path / "podcast"),
        ],
    )
    assert create_podcast_guest_campaign.main() == 0

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "show_crm_dashboard.py",
            "--csv-path",
            str(tmp_path / "outputs" / "crm" / "concrete_motivation_pipeline.csv"),
        ],
    )
    assert show_crm_dashboard.main() == 0

    output = capsys.readouterr().out
    assert "School Outreach Complete" in output
    assert "Sponsorship Outreach Complete" in output
    assert "Podcast Guest Outreach Complete" in output
    assert "CRM Dashboard" in output
