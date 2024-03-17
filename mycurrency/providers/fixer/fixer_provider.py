import json
import os
from mycurrency.core.models import CurrencyExchangeRate, Currency

from mycurrency.providers.base_provider import Provider


class FixerProvider(Provider):

    def __init__(self):
        super().__init__("Fixer", "http://data.fixer.io/api/", 1)
        self.api_key = os.getenv("FIXER_API_KEY")

    def get_exchange_rate_date(self, source_currency, exchange_currency, valuation_date):
        return """{
          "success": true,
          "timestamp": 1710547199,
          "historical": true,
          "base": "EUR",
          "date": "2024-03-17",
          "rates": {
            "USD": 1.089858
          }
        }"""

    def load_from_json(self, json_data):
        try:
            data = json.loads(json_data)

            source_currency_code = data.get("base")
            source_currency = Currency.objects.get(code=source_currency_code)
            valuation_date = data.get("date")
            rates = data.get("rates")
            # NOTE: The request to Fixer will fail if a wrong/none currency is given,
            # so we can be sure we always have one currency to take
            exchanged_currency_code = list(rates.keys())[0]
            exchanged_currency = Currency.objects.get(code=exchanged_currency_code)
            exchange_rate = rates.get(exchanged_currency_code)
            currency_exchange_rate = CurrencyExchangeRate(source_currency=source_currency,
                                                          exchanged_currency=exchanged_currency,
                                                          rate_value=exchange_rate,
                                                          valuation_date=valuation_date,
                                                          provider=self.name)
            currency_exchange_rate.save()
            return True
        except json.JSONDecodeError as error:
            print(error.msg)
            return False

