from __future__ import annotations

import csv
import sys

from concrete_motivation.social_sales_campaign import build_social_sales_campaign, save_social_sales_campaign
from scripts import create_social_sales_campaign


def test_social_sales_campaign_builds_14_day_assets(tmp_path):
    campaign = build_social_sales_campaign("Concrete Builders Membership", days=14, audience="students and fathers")
    result = save_social_sales_campaign(campaign, output_dir=tmp_path)

    assert len(result.created_paths) == 9
    names = {path.name for path in result.created_paths}
    assert "01_instagram_captions.md" in names
    assert "07_cta_calendar.csv" in names
    rows = list(csv.DictReader(result.created_paths[7].read_text(encoding="utf-8").splitlines()))
    assert len(rows) == 14


def test_social_sales_campaign_script_runs(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "create_social_sales_campaign.py",
            "--offer",
            "Concrete Builders Membership",
            "--days",
            "14",
            "--output-dir",
            str(tmp_path),
        ],
    )

    assert create_social_sales_campaign.main() == 0
    output = capsys.readouterr().out
    assert "Social Sales Campaign Complete" in output
