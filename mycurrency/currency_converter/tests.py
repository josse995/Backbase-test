import random

from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from mycurrency.core.models import CurrencyExchangeRate
from mycurrency.core.tests.utils import (
    sample_currency_eur,
    sample_currency_exchange_rates,
)
from mycurrency.currency_converter.serializers import GetCurrencyConverterSerializer


class PublicCurrencyConverterTestCase(APITestCase):
    """Test unauthenticated currency converter"""

    def setUp(self) -> None:
        self.url = reverse("currency_converter:currency-converter")

    def test_auth_required(self) -> None:
        """Test that authentication is required"""
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedCurrencyConverterTestCase(APITestCase):
    """Test authenticated currency converter"""

    def setUp(self) -> None:
        self.url = reverse("currency_converter:currency-converter")
        self.user = get_user_model().objects.create_user("test@test.com", "test")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_missing_parameter_source_currency(self):
        """Test that request without source_currency return 400."""
        params = {"exchanged_currency": "EUR", "amount": 100}
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Parameter 'source_currency' is required.")

    def test_missing_parameter_exchanged_currency(self):
        """Test that request without exchanged_currency return 400."""
        currency = sample_currency_eur()
        params = {"source_currency": currency.code, "amount": 100}
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["error"], "Parameter 'exchanged_currency' is required."
        )

    def test_missing_parameter_amount(self):
        """Test that request without amount return 400."""
        currency = sample_currency_eur()
        params = {
            "source_currency": currency.code,
            "exchanged_currency": currency.code,
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Parameter 'amount' is required.")

    def test_parameter_source_currency_incorrect(self):
        """Test that given source currency returns 400."""
        currency = sample_currency_eur()
        params = {
            "source_currency": "AAA",
            "exchanged_currency": currency.code,
            "amount": 100,
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Incorrect source currency 'AAA'")

    def test_parameter_exchanged_currency_incorrect(self):
        """Test that given exchanged currency returns 400."""
        currency = sample_currency_eur()
        params = {
            "source_currency": currency.code,
            "exchanged_currency": "AAA",
            "amount": 100,
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Incorrect exchange currency 'AAA'")

    def test_parameter_amount_not_a_number(self):
        """Test that given amount returns 400."""
        currency = sample_currency_eur()
        params = {
            "source_currency": currency.code,
            "exchanged_currency": "EUR",
            "amount": "a",
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["error"],
            "Parameter 'amount' must be a positive number greater than 0",
        )

    def test_parameter_amount_negative(self):
        """Test that given negative amount returns 400."""
        currency = sample_currency_eur()
        params = {
            "source_currency": currency.code,
            "exchanged_currency": "EUR",
            "amount": -100,
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["error"],
            "Parameter 'amount' must be a positive number greater than 0",
        )

    def test_retrieve_currency_converter(self):
        """Test that retrieved amount is correct with a specific currency exchange rate."""
        amount = 100
        today_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        rate_value = round(random.uniform(0, 10), 4)
        sample_currency_exchange_rates(today_date, rate_value)
        params = {
            "source_currency": "EUR",
            "exchanged_currency": "USD",
            "amount": amount,
        }
        res = self.client.get(self.url, params)
        currency_rates = CurrencyExchangeRate.objects.all()
        serializer = GetCurrencyConverterSerializer()
        data = serializer.to_representation(currency_rates.first(), amount)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, data)
