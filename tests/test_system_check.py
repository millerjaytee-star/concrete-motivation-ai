from concrete_motivation.system_check import run_system_check


def test_system_check_passes_core_checks_and_reports_warnings():
    result = run_system_check()
    rendered = result.as_markdown()

    assert result.ok is True
    assert "Registered bots: 15" in rendered
    assert "Every bot has an output vault mapping." in rendered
    assert "Output folder ok: outputs/gmail_outreach" in rendered
    assert "Output folder ok: outputs/revenue_commander" in rendered
    assert "## Warnings" in rendered
    assert result.warnings
    assert any("Generated MP4 files" in warning for warning in result.warnings)
