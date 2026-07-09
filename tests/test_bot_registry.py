from concrete_motivation.bot_registry import get_bot, grouped_bots, list_bots


def test_registry_contains_all_bots_in_menu_order():
    bots = list_bots()

    assert len(bots) == 15
    assert [bot.id for bot in bots] == list(range(1, 16))
    assert len({bot.slug for bot in bots}) == 15
    assert bots[0].name == "Brand Architect Bot"
    assert bots[-1].name == "Gmail Outreach Workflow"


def test_each_registered_prompt_exists_and_has_content():
    for bot in list_bots():
        assert bot.prompt_file.is_file()
        assert bot.prompt_file.read_text(encoding="utf-8").startswith("# ")


def test_grouped_bots_cover_every_bot_once():
    grouped = grouped_bots()
    grouped_ids = [bot.id for _group, bots in grouped for bot in bots]

    assert [group for group, _bots in grouped] == [
        "Brand and Content",
        "Growth and Revenue",
        "Operations and Workflows",
    ]
    assert sorted(grouped_ids) == [bot.id for bot in list_bots()]
    assert len(grouped_ids) == len(set(grouped_ids))


def test_get_bot_supports_number_and_slug():
    assert get_bot(2) is get_bot("motivational_speech")


def test_get_bot_rejects_unknown_identifier():
    try:
        get_bot(99)
    except ValueError as exc:
        assert "Unknown bot" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
