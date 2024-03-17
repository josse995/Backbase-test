from mycurrency.core.models import Currency
from mycurrency.providers.enums import CURRENCY_INFO


def initialize_currency_table():
    if Currency.objects.count() < CURRENCY_INFO.count():
        print('Initializing currency table')
        for currency in CURRENCY_INFO:
            Currency.objects.create(code=currency["code"], name=currency["name"], symbol=currency["symbol"])
