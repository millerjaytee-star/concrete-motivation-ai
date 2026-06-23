from concrete_motivation.brand_profile import load_brand_profile


def test_brand_profile_loads_successfully():
    profile = load_brand_profile()

    assert profile.brand_name == "Concrete Motivation"
    assert profile.podcast_name == "Concrete Conversations"
    assert profile.founder == "Jaytee Miller"
    assert "discipline" in profile.core_themes
    assert "athletes" in profile.primary_audience
    assert "generic motivational fluff" in profile.avoid
