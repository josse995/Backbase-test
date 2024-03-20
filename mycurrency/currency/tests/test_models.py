from django.test import TestCase

from mycurrency.currency.models import CurrencyExchangeRate, Currency
from mycurrency.currency.tests.utils import sample_currency_usd, sample_currency_eur


class ModelTests(TestCase):

    def test_currency_str(self):
        currency = sample_currency_usd()
        self.assertEqual(str(currency), "USD - United States Dollar")

    def test_currency_exchange_rate_str(self):
        source_currency = sample_currency_usd()
        exchanged_currency = sample_currency_eur()
        currency_exchange_rate = CurrencyExchangeRate.objects.create(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            valuation_date="2024-01-01",
            rate_value=10.5,
            provider="test_provider",
        )
        self.assertEqual(
            str(currency_exchange_rate),
            "USD - EUR - 2024-01-01 - TEST_PROVIDER",
        )
