from django_filters import FilterSet, CharFilter, NumberFilter
from rest_framework import serializers, status
from rest_framework.response import Response

from mycurrency.currency.models import CurrencyExchangeRate, Currency


class GetCurrencyConverterFilter(FilterSet):
    source_currency = CharFilter(
        field_name="source_currency",
        label="Source currency",
        help_text="Source currency code (e.g., USD)",
        required=True,
    )
    exchanged_currency = CharFilter(
        field_name="exchanged_currency",
        label="Exchange currency",
        help_text="Exchange currency code (e.g., USD)",
        required=True,
    )
    amount = NumberFilter(
        field_name="amount",
        label="Positive number that represents the amount to "
        "convert from source_currency to exchanged_currency",
        required=True,
    )


class GetCurrencyConverterSerializer(serializers.ModelSerializer):
    source_currency = serializers.CharField(source="source_currency.code")
    exchanged_currency = serializers.CharField(source="exchanged_currency.code")

    class Meta:
        model = CurrencyExchangeRate
        fields = ("source_currency", "exchanged_currency", "rate_value")

    def to_representation(self, instance, amount):
        # NOTE: it could be useful to have also the rate_value for,
        # for instance, have a confirmation message when the transaction
        # is going to be made and know source currency,
        # exchanged currency, the rate and the final amount.
        representation = super().to_representation(instance)
        if amount is not None:
            representation["amount"] = float(instance.rate_value) * float(amount)
        return representation


def validate_fields(request):
    source_currency = request.query_params.get("source_currency", None)
    if source_currency is None:
        return Response(
            data={"error": "Parameter 'source_currency' is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if Currency.objects.filter(code=source_currency.upper()).count() <= 0:
        return Response(
            data={"error": f"Incorrect source currency '{source_currency}'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    exchanged_currency = request.query_params.get("exchanged_currency", None)
    if exchanged_currency is None:
        return Response(
            data={"error": "Parameter 'exchanged_currency' is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if Currency.objects.filter(code=exchanged_currency.upper()).count() <= 0:
        return Response(
            data={"error": f"Incorrect exchange currency '{exchanged_currency}'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    amount = request.query_params.get("amount", None)
    if amount is None:
        return Response(
            data={"error": "Parameter 'amount' is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not amount.isnumeric() or float(amount) <= 0:
        return Response(
            data={
                "error": "Parameter 'amount' must be a positive number greater than 0"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None
