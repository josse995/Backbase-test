from datetime import datetime

from django_filters import FilterSet, CharFilter, NumberFilter, DateFilter
from rest_framework import serializers, status
from rest_framework.response import Response

from mycurrency.core.models import Currency


class GetCurrencyRateOfReturnFilter(FilterSet):
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
        label="Positive number that represents the amount to convert from source_currency "
        "to exchanged_currency",
        required=True,
    )
    start_date = DateFilter(
        field_name="start_date",
        lookup_expr="gte",
        label="Start date for calculating the time-weighted rate of return (YYYY-MM-DD)",
        required=True,
    )


class GetCurrencyRateOfReturnSerializer(serializers.Serializer):
    date = serializers.DateField()
    twr = serializers.DecimalField(max_digits=18, decimal_places=6)


def validate_fields(request):
    source_currency = request.query_params.get("source_currency")
    if not source_currency:
        return Response(
            {"error": "Parameter 'source_currency' is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if Currency.objects.filter(code=source_currency.upper()).count() <= 0:
        return Response(
            {"error": f"Incorrect source currency '{source_currency}'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    exchanged_currency = request.query_params.get("exchanged_currency", None)
    if exchanged_currency is None:
        return Response(
            {"error": "Parameter 'exchanged_currency' is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if Currency.objects.filter(code=exchanged_currency.upper()).count() <= 0:
        return Response(
            {"error": f"Incorrect exchanged currency '{exchanged_currency}'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    start_date_str = request.query_params.get("start_date", None)
    if start_date_str is None:
        return Response(
            {"error": "Parameter 'start_date' is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        datetime.strptime(start_date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response(
            {"error": "Invalid date format for parameter 'start_date'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    amount = request.query_params.get("amount", None)
    if amount is None:
        return Response(
            {"error": "Parameter 'amount' is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not amount.isnumeric() or float(amount) <= 0:
        return Response(
            {"error": "Parameter 'amount' must be a positive number greater than 0"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None
