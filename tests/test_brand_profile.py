from concrete_motivation.brand_profile import load_brand_profile


def test_brand_profile_loads_successfully():
    profile = load_brand_profile()

    assert profile.brand_name == "Concrete Motivation"
    assert profile.podcast_name == "Concrete Conversations"
    assert profile.founder == "Jaytee Miller"
    assert any("Discipline" in theme for theme in profile.core_themes)
    assert any("Athletes" in audience for audience in profile.primary_audience)
    assert "No empty hype" in profile.avoid
