from rest_framework import serializers

from mycurrency.core.models import CurrencyExchangeRate, Currency


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for Currency objects"""

    class Meta:
        model = Currency
        fields = ("code", "name", "symbol")


class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    """Serializer for CurrencyExchangeRate objects"""

    source_currency = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Currency.objects.all(),
    )

    exchanged_currency = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Currency.objects.all(),
    )

    class Meta:
        model = CurrencyExchangeRate
        fields = (
            "source_currency",
            "exchanged_currency",
            "valuation_date",
            "rate_value",
        )
