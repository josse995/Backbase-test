import random

from datetime import datetime
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from mycurrency.core.api.serializers import CurrencyExchangeRateSerializer
from mycurrency.core.models import CurrencyExchangeRate
from mycurrency.core.tests.utils import (
    sample_currency_eur,
    sample_currency_exchange_rates,
)
from mycurrency.providers.services import date_ranges_in_days


class PublicCurrencyRatesTestCase(APITestCase):
    """Test unauthenticated currency rates"""

    def setUp(self) -> None:
        self.url = reverse("currency_rates:currency-rates")

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedCurrencyRatesTestCase(APITestCase):
    """Test authenticated currency rates"""

    def setUp(self) -> None:
        self.url = reverse("currency_rates:currency-rates")
        self.user = get_user_model().objects.create_user("test@test.com", "test")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_missing_parameter_source_currency(self):
        """Test that request without source_currency return 400."""
        params = {
            "date_from": "2024-01-01",
            "date_to": "2024-01-01",
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Parameter 'source_currency' is required.")

    def test_missing_parameter_date_from(self):
        """Test that request without date_from returns 400."""
        currency = sample_currency_eur()
        params = {"date_to": "2024-01-01", "source_currency": currency.code}
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Parameter 'date_from' is required.")

    def test_missing_parameter_date_to(self):
        """Test that request without date_to returns 400."""
        currency = sample_currency_eur()
        params = {"date_from": "2024-01-01", "source_currency": currency.code}
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Parameter 'date_to' is required.")

    def test_parameter_source_currency_incorrect(self):
        """Test that given source currency returns 400."""
        params = {
            "date_from": "2024-01-01",
            "date_to": "2024-01-01",
            "source_currency": "AAA",
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Incorrect source currency 'AAA'")

    def test_parameter_date_from_wrong_format(self):
        """Test that given date_from returns 400."""
        currency = sample_currency_eur()
        params = {
            "date_from": "a",
            "date_to": "2024-01-01",
            "source_currency": currency.code,
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["error"], "Invalid date format for parameter 'date_from'"
        )

    def test_parameter_date_to_wrong_format(self):
        """Test that given date_to returns 400."""
        currency = sample_currency_eur()
        params = {
            "date_from": "2024-01-01",
            "date_to": "a",
            "source_currency": currency.code,
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["error"], "Invalid date format for parameter 'date_to'"
        )

    def test_parameters_date_from_greater_than_date_to(self):
        """Test response error when date_from is greater than date_to date."""
        currency = sample_currency_eur()
        params = {
            "date_from": "2024-01-01",
            "date_to": "2023-01-01",
            "source_currency": currency.code,
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["error"],
            "Parameter 'date_from' must be greater than parameter 'date_to'",
        )

    def test_retrieve_currency_rates(self):
        """Test retrieving currency rates"""

        date_from_str = "2024-01-01"
        date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
        date_to_str = "2024-01-10"
        date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date()
        dates = list(date_ranges_in_days(date_from, date_to))
        for interation_date in dates:
            rate_value = round(random.uniform(0, 10), 4)
            sample_currency_exchange_rates(interation_date, rate_value)

        params = {
            "date_from": date_from_str,
            "date_to": date_to_str,
            "source_currency": "EUR",
        }
        res = self.client.get(self.url, params)

        currency_rates = CurrencyExchangeRate.objects.all()
        serializer = CurrencyExchangeRateSerializer(currency_rates, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
