from datetime import datetime

from django_filters import FilterSet, DateFilter, CharFilter
from rest_framework import status
from rest_framework.response import Response

from mycurrency.core.models import Currency


class GetCurrencyRatesFilter(FilterSet):
    source_currency = CharFilter(
        field_name="source_currency__name",
        label="Source currency",
        help_text="Source currency code (e.g., USD)",
        required=True,
    )
    date_from = DateFilter(
        field_name="date_from",
        lookup_expr="gte",
        label="Start date for exchange rates (YYYY-MM-DD)",
        required=True,
    )
    date_to = DateFilter(
        field_name="date_from",
        lookup_expr="lte",
        label="Start date for exchange rates (YYYY-MM-DD)",
        required=True,
    )


def validate_fields(request):
    source_currency = request.query_params.get("source_currency", None)
    if source_currency is None:
        return Response(
            {"error": f"Parameter 'source_currency' is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if Currency.objects.filter(code=source_currency.upper()).count() <= 0:
        return Response(
            {"error": f"Incorrect source currency '{source_currency}'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    date_from_str = request.query_params.get("date_from", None)
    if date_from_str is None:
        return Response(
            {"error": f"Parameter 'date_from' is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
    except ValueError:
        return Response(
            {"error": f"Invalid date format for parameter 'date_from'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    date_to_str = request.query_params.get("date_to", None)
    if date_to_str is None:
        return Response(
            {"error": f"Parameter 'date_to' is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        date_to = datetime.strptime(
            request.query_params.get("date_to", None), "%Y-%m-%d"
        ).date()
    except ValueError:
        return Response(
            {"error": f"Invalid date format for parameter 'date_to'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if date_from > date_to:
        return Response(
            {
                "error": f"Parameter 'date_from' must be greater than parameter 'date_to'"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None
