from django.db import models
from django.db.models import Model


class Currency(Model):

    code = models.CharField(max_length=3, unique=True, primary_key=True)
    name = models.CharField(max_length=50, db_index=True)
    symbol = models.CharField(max_length=10)


class CurrencyExchangeRate(Model):

    source_currency = models.ForeignKey(Currency, related_name='exchanges', on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)
    provider = models.CharField(max_length=50)

