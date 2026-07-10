from concrete_motivation.app import run
from concrete_motivation.app import help_text, menu
from concrete_motivation.output_vault import OutputVault


def scripted_app(*answers: str, vault: OutputVault | None = None) -> str:
    responses = iter(answers)
    output: list[str] = []
    run(input_fn=lambda _prompt: next(responses), output_fn=output.append, vault=vault)
    return "\n".join(output)


def test_app_recovers_from_invalid_choice_and_empty_goal(tmp_path):
    output = scripted_app("not-a-number", "16", "1", "   ", "", "0", vault=OutputVault(tmp_path))

    assert "Please enter a number from 0 to 32." in output
    assert "No saved outputs yet." in output
    assert "Unable to run bot: Goal cannot be empty." in output
    assert output.endswith("Keep building. Goodbye.")


def test_menu_groups_bots_and_shows_help_choice():
    rendered = menu()

    assert "[Brand and Content]" in rendered
    assert "[Growth and Revenue]" in rendered
    assert "[Operations and Workflows]" in rendered
    assert "1. Brand Architect Bot - Define and protect the brand." in rendered
    assert "25. Executive Dashboard" in rendered
    assert "26. CRM Dashboard" in rendered
    assert "27. School Outreach Campaign" in rendered
    assert "28. Sponsor Campaign" in rendered
    assert "29. Podcast Guest Campaign" in rendered
    assert "30. Content/Reels Package" in rendered
    assert "31. YouTube Package" in rendered
    assert "32. YouTube Upload Dry Run" in rendered
    assert "H. Help / recommended workflow" in rendered


def test_app_help_returns_to_menu(tmp_path):
    output = scripted_app("h", "0", vault=OutputVault(tmp_path))

    assert "# Command Center Help" in output
    assert "Recommended daily workflow" in output
    assert output.count("CONCRETE MOTIVATION AI COMMAND CENTER") == 2


def test_help_text_names_recommended_growth_workflow():
    text = help_text()

    assert "CEO Bot" in text
    assert "Sales Outreach Bot" in text
    assert "System Check" in text
    assert "School Outreach" in text
    assert "CRM Pipeline" in text
    assert "Executive Dashboard" in text


def test_app_runs_selected_bot_and_returns_to_menu(tmp_path):
    vault = OutputVault(tmp_path)
    output = scripted_app("8", "renewing the mind after a setback", "", "n", "0", vault=vault)

    assert "Provider: offline" in output
    assert "# Faith & Mindset Bot" in output
    assert "## Scripture-inspired principle" in output
    assert "## Concrete Motivation Angle" in output
    assert "Output was not saved." in output
    assert output.count("CONCRETE MOTIVATION AI COMMAND CENTER") == 2


def test_ceo_bot_stages_priority_actions(tmp_path):
    vault = OutputVault(tmp_path)
    output = scripted_app(
        "9",
        "stage the next weekly move",
        "focus on YouTube, Gmail, website, CRM, and dashboard actions",
        "n",
        "0",
        vault=vault,
    )

    assert "# CEO Bot" in output
    assert "## YouTube stage" in output
    assert "## Gmail stage" in output
    assert "## Website stage" in output
    assert "## CRM stage" in output
    assert "## Dashboard stage" in output


def test_app_uses_optional_personalization_follow_up(tmp_path):
    output = scripted_app(
        "4",
        "daily discipline",
        "make it intense for Instagram reels",
        "n",
        "0",
        vault=OutputVault(tmp_path),
    )

    assert "# Social Media Content Bot" in output
    assert "make it intense for Instagram reels" in output


def test_app_save_prompt_defaults_to_yes(tmp_path):
    vault = OutputVault(tmp_path)
    output = scripted_app("2", "starting from bottom", "", "", "0", vault=vault)

    saved = list(tmp_path.rglob("*.md"))
    assert len(saved) == 1
    assert saved[0].parent.name == "speeches"
    assert "Saved to content vault:" in output


def test_app_can_skip_save(tmp_path):
    vault = OutputVault(tmp_path)
    output = scripted_app("3", "fatherhood and pressure", "", "n", "0", vault=vault)

    assert not list(tmp_path.rglob("*.md"))
    assert "Output was not saved." in output


def test_app_lists_recent_saved_outputs(tmp_path):
    vault = OutputVault(tmp_path)
    output = scripted_app("1", "build trust", "", "", "16", "0", vault=vault)

    assert "Recent saved outputs:" in output
    assert "brand_architect" not in output
    assert "brand-architect-build-trust.md" in output


def test_app_generates_calendar_and_defaults_save_to_yes(tmp_path):
    vault = OutputVault(tmp_path)
    output = scripted_app(
        "17",
        "discipline under pressure",
        "for fathers on Instagram",
        "",
        "0",
        vault=vault,
    )

    saved = list(tmp_path.rglob("*.md"))
    assert len(saved) == 1
    assert saved[0].parent.name == "content_calendars"
    assert "# Weekly Content Calendar Engine" in output
    assert "## Sunday: Reflection / Reset / Weekly Challenge" in output
    assert "for fathers on Instagram" in output
    assert "Saved to content vault:" in output


def test_app_calendar_skip_save(tmp_path):
    vault = OutputVault(tmp_path)
    output = scripted_app("17", "legacy", "", "n", "0", vault=vault)

    assert "# Weekly Content Calendar Engine" in output
    assert not list(tmp_path.rglob("*.md"))
    assert "Output was not saved." in output
