from concrete_motivation.content_calendar import generate_weekly_calendar


EXPECTED_DAYS = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)


def test_weekly_calendar_generates_seven_days():
    calendar = generate_weekly_calendar("discipline under pressure")

    assert len(calendar.days) == 7
    assert tuple(day.day for day in calendar.days) == EXPECTED_DAYS


def test_calendar_uses_required_content_types():
    calendar = generate_weekly_calendar("legacy")

    assert tuple(day.content_type for day in calendar.days) == (
        "Mindset Reel",
        "Podcast Clip",
        "Athlete/Youth Message",
        "Fatherhood/Faith/Leadership Post",
        "Concrete Conversations Episode Push",
        "Behind-the-Scenes / Story Post",
        "Reflection / Reset / Weekly Challenge",
    )


def test_calendar_days_include_required_fields():
    calendar = generate_weekly_calendar("starting from the bottom")

    for day in calendar.days:
        assert day.day
        assert day.content_type
        assert day.hook
        assert day.script_or_caption
        assert day.call_to_action
        assert day.recommended_platform
        assert day.repurpose_idea


def test_optional_detail_affects_calendar_output():
    calendar = generate_weekly_calendar(
        "family legacy",
        "for fathers on Instagram during football season",
    )
    output = calendar.as_markdown()

    assert "for fathers on Instagram during football season" in output
    assert "**Detail:** for fathers on Instagram during football season" in output


def test_empty_calendar_theme_is_rejected():
    try:
        generate_weekly_calendar("   ")
    except ValueError as exc:
        assert "Theme cannot be empty" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
