from concrete_motivation.bot_registry import get_bot, list_bots


def test_registry_contains_all_eight_bots_in_menu_order():
    bots = list_bots()

    assert len(bots) == 8
    assert [bot.id for bot in bots] == list(range(1, 9))
    assert len({bot.slug for bot in bots}) == 8
    assert bots[0].name == "Brand Architect Bot"
    assert bots[-1].name == "Faith & Mindset Bot"


def test_each_registered_prompt_exists_and_has_content():
    for bot in list_bots():
        assert bot.prompt_file.is_file()
        assert bot.prompt_file.read_text(encoding="utf-8").startswith("# ")


def test_get_bot_supports_number_and_slug():
    assert get_bot(2) is get_bot("motivational_speech")


def test_get_bot_rejects_unknown_identifier():
    try:
        get_bot(99)
    except ValueError as exc:
        assert "Unknown bot" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
