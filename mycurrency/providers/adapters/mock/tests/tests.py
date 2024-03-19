import json
import random

from datetime import datetime
from unittest import TestCase

from mycurrency.core.models import CurrencyExchangeRate, Currency
from mycurrency.core.tests.utils import sample_currency_eur, sample_currency_usd
from mycurrency.providers.adapters.mock.mock_provider import MockProvider


class MockProviderTestCase(TestCase):

    def setUp(self):
        Currency.objects.all().delete()
        CurrencyExchangeRate.objects.all().delete()

    def test_get_exchange_rate(self):
        mock_provider = MockProvider()

        source_currency = "EUR"
        exchanged_currency = "USD"
        valuation_date = datetime(2024, 1, 1).strftime("%Y-%m-%d")
        json_string = mock_provider.get_exchange_rate_date(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            valuation_date=valuation_date,
        )

        currency_exchanged_rate_map = json.loads(json_string)
        self.assertEqual(
            currency_exchanged_rate_map["source_currency_code"], source_currency
        )
        self.assertEqual(
            currency_exchanged_rate_map["exchanged_currency_code"], exchanged_currency
        )
        self.assertEqual(currency_exchanged_rate_map["valuation_date"], valuation_date)

    def test_load_from_response(self):
        mock_provider = MockProvider()

        source_currency = sample_currency_eur()
        exchanged_currency = sample_currency_usd()
        valuation_date = datetime(2024, 1, 1).strftime("%Y-%m-%d")
        data = {
            "source_currency_code": source_currency.code,
            "exchanged_currency_code": exchanged_currency.code,
            "rate_value": round(random.uniform(0, 10), 4),
            "valuation_date": valuation_date,
        }

        mock_provider.load_from_response(json.dumps(data))

        currency_exchanged_rates = CurrencyExchangeRate.objects.all()
        currency_exchange_rate = currency_exchanged_rates[0]
        self.assertEqual(
            currency_exchange_rate.source_currency.code, source_currency.code
        )
        self.assertEqual(
            currency_exchange_rate.exchanged_currency.code, exchanged_currency.code
        )
        self.assertEqual(
            currency_exchange_rate.valuation_date.strftime("%Y-%m-%d"), valuation_date
        )
