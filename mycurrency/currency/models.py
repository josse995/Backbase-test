from django.db import models
from django.db.models import Model


class Currency(Model):
    code = models.CharField(max_length=3, unique=True, primary_key=True)
    name = models.CharField(max_length=50, db_index=True)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.code} - {self.name}"


class CurrencyExchangeRate(Model):
    source_currency = models.ForeignKey(
        Currency,
        related_name="exchanges",
        on_delete=models.CASCADE,
    )
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)
    provider = models.CharField(max_length=50)

    def __str__(self):
        return (
            f"{self.source_currency.code} - {self.exchanged_currency.code} - "
            f"{self.valuation_date} - {self.provider.upper()}"
        )


class GraphViewModel(models.Model):
    """Dummy Analytics Model"""

    class Meta:
        verbose_name = "Historical Rate Value Graph"
        verbose_name_plural = "Historical Rate Value Graph"


class ConverterViewModel(models.Model):
    """Dummy Analytics Model"""

    class Meta:
        verbose_name = "Converter Online"
        verbose_name_plural = "Converter Online"
