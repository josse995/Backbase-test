import json
import os

import requests

from mycurrency.currency.models import CurrencyExchangeRate, Currency

from mycurrency.providers.provider_facade import ProviderFacade


class FixerProvider(ProviderFacade):
    """
    Provider specific for the source Fixer
    """

    def __init__(self):
        super().__init__("Fixer", "http://data.fixer.io/api/", 1)
        # NOTE: Due to the limitation of free Fixer.io API, the api_key is not provided anywhere on the project, but in
        # the case we were on a real env, with defining as environment variable on the task on AWS, for instance,
        # will be ok.
        self.api_key = os.getenv("FIXER_API_KEY")

    def get_exchange_rate_date(
        self, source_currency, exchanged_currency, valuation_date
    ):
        params = {
            "access_key": self.api_key,
            "base": source_currency,
            "symbols": exchanged_currency,
        }

        try:
            res = requests.get(self.url, params=params)
            res.raise_for_status()
            data = res.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    def load_from_response(self, data):
        try:
            data = json.loads(data)

            source_currency_code = data.get("base")
            source_currency = Currency.objects.get(code=source_currency_code)
            valuation_date = data.get("date")
            rates = data.get("rates")
            # NOTE: The request to Fixer will fail if a wrong/none currency is given,
            # so we can be sure we always have one currency to take
            exchanged_currency_code = list(rates.keys())[0]
            exchanged_currency = Currency.objects.get(code=exchanged_currency_code)
            exchange_rate = rates.get(exchanged_currency_code)
            currency_exchange_rate = CurrencyExchangeRate(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                rate_value=exchange_rate,
                valuation_date=valuation_date,
                provider=self.name,
            )
            currency_exchange_rate.save()
            return True
        except json.JSONDecodeError as error:
            print(error.msg)
            return False
