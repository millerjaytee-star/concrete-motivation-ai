from __future__ import annotations

import json
import sys

from concrete_motivation.payment_link_manager import PaymentLinkManager
from scripts import create_payment_link_config, show_payment_link_status


def test_payment_link_manager_reads_local_config(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    local = config_dir / "payment_links.local.json"
    local.write_text(
        json.dumps(
            {
                "monthly_payment_link": "https://pay.concretemotivation.test/monthly",
                "annual_payment_link": "https://pay.concretemotivation.test/annual",
                "booking_payment_link": "https://pay.concretemotivation.test/booking",
                "sponsor_payment_link": "https://pay.concretemotivation.test/sponsor",
            }
        ),
        encoding="utf-8",
    )

    manager = PaymentLinkManager(config_path=local, example_path=config_dir / "payment_links.example.json")
    status = manager.status()

    assert status.configured_count == 4
    assert "Configured links: 4/4" in status.as_markdown()


def test_payment_link_scripts_create_and_show_status(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "create_payment_link_config.py",
            "--config-dir",
            str(tmp_path / "config"),
        ],
    )
    assert create_payment_link_config.main() == 0

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "show_payment_link_status.py",
            "--config-dir",
            str(tmp_path / "config"),
        ],
    )
    assert show_payment_link_status.main() == 0

    output = capsys.readouterr().out
    assert "Payment Link Status" in output
    assert "Configured links: 0/4" in output
