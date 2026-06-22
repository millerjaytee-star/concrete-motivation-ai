from concrete_motivation.app import run


def scripted_app(*answers: str) -> str:
    responses = iter(answers)
    output: list[str] = []
    run(input_fn=lambda _prompt: next(responses), output_fn=output.append)
    return "\n".join(output)


def test_app_recovers_from_invalid_choice_and_empty_goal():
    output = scripted_app("not-a-number", "9", "1", "   ", "0")

    assert output.count("Please enter a number from 0 to 8.") == 2
    assert "Unable to run bot: Goal cannot be empty." in output
    assert output.endswith("Keep building. Goodbye.")


def test_app_runs_selected_bot_and_returns_to_menu():
    output = scripted_app("8", "renewing the mind after a setback", "0")

    assert "# Faith & Mindset Bot" in output
    assert "## Scripture-inspired principle" in output
    assert output.count("CONCRETE MOTIVATION AI COMMAND CENTER") == 2
