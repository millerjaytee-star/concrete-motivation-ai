from concrete_motivation.providers import OfflineProvider, OpenAIProvider, create_provider, provider_name_from_env


def test_provider_factory_defaults_to_offline():
    provider = create_provider({})

    assert isinstance(provider, OfflineProvider)
    assert provider.name == "offline"


def test_provider_factory_selects_openai_when_configured():
    provider = create_provider({"CONCRETE_AI_PROVIDER": "openai", "OPENAI_API_KEY": "test-key"})

    assert isinstance(provider, OpenAIProvider)
    assert provider.name == "openai"


def test_missing_api_key_does_not_crash_app_provider_selection():
    provider = create_provider({"CONCRETE_AI_PROVIDER": "openai"})

    assert isinstance(provider, OfflineProvider)
    assert provider.name == "offline"


def test_unknown_provider_defaults_to_offline():
    assert provider_name_from_env({"CONCRETE_AI_PROVIDER": "not-real"}) == "offline"
