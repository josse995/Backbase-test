from mycurrency.providers.adapters.fixer.fixer_provider import FixerProvider
from mycurrency.providers.adapters.mock.mock_provider import MockProvider

AVAILABLE_PROVIDERS = {"mock": MockProvider(), "fixer": FixerProvider()}
