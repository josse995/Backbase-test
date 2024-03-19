import json
import random

from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

import pytest
import requests

from mycurrency.core.models import Currency, CurrencyExchangeRate
from mycurrency.core.tests.utils import sample_currency_eur, sample_currency_usd
from mycurrency.providers.adapters.fixer.fixer_provider import FixerProvider


@pytest.mark.django_db
class FixerTests(TestCase):

    def setUp(self):
        Currency.objects.all().delete()
        CurrencyExchangeRate.objects.all().delete()

    @patch("mycurrency.providers.adapters.fixer.fixer_provider.requests.get")
    def test_get_exchange_rate_date_success(self, mock_requests_get):
        mock_response = """{
          "success": true,
          "timestamp": 1710547199,
          "historical": true,
          "base": "EUR",
          "date": "2024-03-17",
          "rates": {
            "USD": 1.089858
          }
        }"""
        mock_requests_get.return_value.json.return_value = mock_response
        mock_requests_get.return_value.raise_for_status.return_value = None

        fixer_provider = FixerProvider()
        result = fixer_provider.get_exchange_rate_date("EUR", "USD", "2024-03-17")

        self.assertEqual(result, mock_response)

    @patch("mycurrency.providers.adapters.fixer.fixer_provider.requests.get")
    def test_get_exchange_rate_date_failure(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.RequestException(
            "Simulated error"
        )
        fixer_provider = FixerProvider()
        result = fixer_provider.get_exchange_rate_date("EUR", "USD", "2024-03-17")

        self.assertIsNone(result)

    def test_load_from_response(self):
        fixer_provider = FixerProvider()

        source_currency = sample_currency_eur()
        exchanged_currency = sample_currency_usd()
        valuation_date = datetime(2024, 1, 1).strftime("%Y-%m-%d")
        data = {
            "success": True,
            "timestamp": 1710547199,
            "historical": True,
            "base": source_currency.code,
            "date": valuation_date,
            "rates": {
                exchanged_currency.code: round(random.uniform(0, 10), 4),
            },
        }

        fixer_provider.load_from_response(json.dumps(data))

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
