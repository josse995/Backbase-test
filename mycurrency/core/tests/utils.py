from mycurrency.core.models import Currency, CurrencyExchangeRate


def sample_currency_eur(**params):
    """Create a sample Currency and return it"""
    return Currency.objects.create(code="EUR", name="Euro", symbol="€")


def sample_currency_usd(**params):
    """Create a sample Currency and return it"""
    return Currency.objects.create(code="USD", name="United States Dollar", symbol="$")


def sample_currency_exchange_rates(valuation_date, rate_value, **params):
    """Create a sample currency exchange and return it"""
    source_currencies = Currency.objects.filter(code="EUR")
    if not source_currencies:
        source_currency = sample_currency_eur()
    else:
        source_currency = source_currencies.first()

    exchanged_currencies = Currency.objects.filter(code="USD")
    if not exchanged_currencies:
        exchanged_currency = sample_currency_usd()
    else:
        exchanged_currency = exchanged_currencies.first()

    defaults = {
        "source_currency": source_currency,
        "exchanged_currency": exchanged_currency,
        "valuation_date": valuation_date,
        "rate_value": rate_value,
        "provider": "test_provider",
    }
    defaults.update(params)
    return CurrencyExchangeRate.objects.create(**defaults)
