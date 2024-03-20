import random

from datetime import datetime, timezone, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from mycurrency.currency.models import CurrencyExchangeRate
from mycurrency.currency.tests.utils import (
    sample_currency_eur,
    sample_currency_exchange_rates,
)
from mycurrency.providers.services import date_ranges_in_days
from mycurrency.rate_of_return.serializers import GetCurrencyRateOfReturnSerializer
from mycurrency.rate_of_return.views import build_twr_elements


class PublicRateOfReturnTest(APITestCase):
    """Test unauthenticated rate of return"""

    def setUp(self):
        self.url = reverse("rate_of_return:rate-of-return")

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedRateOfReturnTest(APITestCase):
    """Test authenticated rate of return"""

    def setUp(self) -> None:
        self.url = reverse("rate_of_return:rate-of-return")
        self.user = get_user_model().objects.create_user("test@test.com", "test")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_missing_parameter_source_currency(self):
        """Test that request without source_currency return 400."""
        params = {
            "amount": 100,
            "exchanged_currency": "EUR",
            "start_date": "2024-01-01",
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Parameter 'source_currency' is required.")

    def test_missing_parameter_amount(self):
        """Test that request without amount return 400."""
        currency = sample_currency_eur()
        params = {
            "source_currency": currency.code,
            "exchanged_currency": currency.code,
            "start_date": "2024-01-01",
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Parameter 'amount' is required.")

    def test_missing_parameter_exchanged_currency(self):
        """Test that request without exchanged_currency return 400."""
        currency = sample_currency_eur()
        params = {
            "source_currency": currency.code,
            "amount": 100,
            "start_date": "2024-01-01",
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["error"],
            "Parameter 'exchanged_currency' is required.",
        )

    def test_missing_parameter_start_date(self):
        """Test that request without start_date returns 400."""
        currency = sample_currency_eur()
        params = {
            "source_currency": currency.code,
            "amount": 100,
            "exchanged_currency": currency.code,
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Parameter 'start_date' is required.")

    def test_parameter_source_currency_incorrect(self):
        """Test that given source currency returns 400."""
        params = {
            "source_currency": "AAA",
            "amount": 100,
            "exchanged_currency": "EUR",
            "start_date": "2024-01-01",
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Incorrect source currency 'AAA'")

    def test_parameter_amount_not_a_number(self):
        """Test that given amount returns 400."""
        currency = sample_currency_eur()
        params = {
            "source_currency": currency.code,
            "exchanged_currency": currency.code,
            "amount": "a",
            "start_date": "2024-01-01",
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
            "exchanged_currency": currency.code,
            "amount": -100,
            "start_date": "2024-01-01",
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["error"],
            "Parameter 'amount' must be a positive number greater than 0",
        )

    def test_parameter_exchanged_currency_incorrect(self):
        """Test that given exchanged currency returns 400."""
        currency = sample_currency_eur()
        params = {
            "source_currency": currency.code,
            "exchanged_currency": "AAA",
            "amount": 100,
            "start_date": "2024-01-01",
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Incorrect exchanged currency 'AAA'")

    def test_parameter_start_date_wrong_format(self):
        """Test that given start_date returns 400."""
        currency = sample_currency_eur()
        params = {
            "source_currency": currency.code,
            "exchanged_currency": currency.code,
            "amount": 100,
            "start_date": "a",
        }
        res = self.client.get(self.url, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["error"],
            "Invalid date format for parameter 'start_date'",
        )

    def test_retrieve_rate_of_return(self):
        """Test that retrieved rate of return is correct"""
        today_date = datetime.now(timezone.utc)
        start_date = today_date - timedelta(days=2)
        start_date_str = start_date.strftime("%Y-%m-%d")
        amount = 100

        dates = list(date_ranges_in_days(start_date, today_date))
        for interation_date in dates:
            rate_value = round(random.uniform(0, 10), 4)
            sample_currency_exchange_rates(interation_date, rate_value)
        params = {
            "source_currency": "EUR",
            "exchanged_currency": "USD",
            "amount": amount,
            "start_date": start_date_str,
        }
        res = self.client.get(self.url, params)

        currency_rates = CurrencyExchangeRate.objects.all()
        start_currency_exchanged_rate = currency_rates.get(valuation_date=start_date)
        initial_converted_amount = float(amount) * float(
            start_currency_exchanged_rate.rate_value,
        )
        twr_elements = build_twr_elements(
            amount, initial_converted_amount, currency_rates
        )
        serializer = GetCurrencyRateOfReturnSerializer(twr_elements, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
