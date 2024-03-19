import json
import random

from mycurrency.core.models import CurrencyExchangeRate, Currency
from mycurrency.providers.provider_facade import ProviderFacade


class MockProvider(ProviderFacade):
    """Mock provider"""

    def __init__(self):
        super().__init__("Mock", None, 0)
        self.api_key = None

    def get_exchange_rate_date(
        self, source_currency, exchanged_currency, valuation_date
    ):

        response_map = {
            "source_currency_code": source_currency,
            "exchanged_currency_code": exchanged_currency,
            "rate_value": round(random.uniform(0, 10), 4),
            "valuation_date": valuation_date,
        }
        return json.dumps(response_map)

    def load_from_response(self, data):
        try:
            data = json.loads(data)

            source_currency_code = data.get("source_currency_code")
            source_currency = Currency.objects.get(code=source_currency_code)
            exchanged_currency_code = data.get("exchanged_currency_code")
            exchanged_currency = Currency.objects.get(code=exchanged_currency_code)
            valuation_date = data.get("valuation_date")
            rate_value = data.get("rate_value")

            currency_exchange_rate = CurrencyExchangeRate(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                valuation_date=valuation_date,
                rate_value=rate_value,
            )
            currency_exchange_rate.save()
            return True
        except json.JSONDecodeError as error:
            print(error.msg)
            return False
