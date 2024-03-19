from datetime import datetime, timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mycurrency.core.models import CurrencyExchangeRate
from mycurrency.providers.services import get_currency_exchange_rates
from mycurrency.rate_of_return.serializers import (
    GetCurrencyRateOfReturnSerializer,
    GetCurrencyRateOfReturnFilter,
    validate_fields,
)


def iterate_over_dates(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)


def calculate_twr(initial_value, final_value):
    # Calculate the holding period return
    holding_period_return = (final_value - initial_value) / initial_value
    # Convert compounded return to percentage
    return holding_period_return * 100


def build_twr_elements(amount, initial_converted_amount, queryset):
    response = []
    for currency_exchange_rate in queryset:
        date = currency_exchange_rate.valuation_date
        rate_value = float(currency_exchange_rate.rate_value)
        final_value = float(amount) * float(rate_value)
        twr = calculate_twr(initial_converted_amount, final_value)
        response.append({"date": date, "twr": twr})
    return response


class RateOfReturnView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = GetCurrencyRateOfReturnSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = GetCurrencyRateOfReturnFilter

    def get(self, request, *args, **kwargs):
        validation = validate_fields(request)
        if validation is None:
            source_currency = request.query_params.get("source_currency", None)
            exchanged_currency = request.query_params.get("exchanged_currency", None)
            amount = float(request.query_params.get("amount", None))
            start_date = datetime.strptime(
                request.query_params.get("start_date", None),
                "%Y-%m-%d",
            ).date()
            end_date = datetime.utcnow().date()

            queryset = get_currency_exchange_rates(
                source_currency, exchanged_currency, start_date, end_date
            )
            start_currency_exchanged_rate = queryset.get(valuation_date=start_date)
            initial_converted_amount = float(amount) * float(
                start_currency_exchanged_rate.rate_value
            )

            response = build_twr_elements(amount, initial_converted_amount, queryset)
            serializer = self.serializer_class(response, many=True)
            return Response(serializer.data)
        return validation
