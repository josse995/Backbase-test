from datetime import datetime, timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from mycurrency.core.models import CurrencyExchangeRate
from mycurrency.providers.services import get_currency_exchange_rates
from mycurrency.rate_of_return.serializers import GetCurrencyRateOfReturnSerializer, GetCurrencyRateOfReturnFilter, \
    validate_fields


def iterate_over_dates(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)


def calculate_twr(initial_value, final_value, start_date, end_date):
    # Calculate the number of days the investment was held
    days_held = (end_date - start_date).days
    print(end_date, start_date, days_held)
    # Calculate the daily return
    daily_return = ((final_value / initial_value) ** (1 / days_held)) - 1
    # Calculate the compounded return
    compounded_return = (1 + daily_return) ** days_held - 1
    # Convert compounded return to percentage
    twr_percentage = compounded_return * 100

    return twr_percentage


class RateOfReturnView(ListAPIView):
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = GetCurrencyRateOfReturnSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = GetCurrencyRateOfReturnFilter

    def get(self, request, *args, **kwargs):
        validation = validate_fields(request)
        if validation is None:
            response = []
            source_currency = request.query_params.get('source_currency', None)
            exchanged_currency = request.query_params.get('exchanged_currency', None)
            amount = float(request.query_params.get('amount', None))
            start_date = datetime.strptime(request.query_params.get('start_date', None), '%Y-%m-%d').date()
            print(start_date)
            end_date = datetime.utcnow().date()

            queryset = get_currency_exchange_rates(source_currency, exchanged_currency, start_date, end_date - timedelta(days=1))

            for currency_exchange_rate in queryset:
                date = currency_exchange_rate.valuation_date
                rate_value = float(currency_exchange_rate.rate_value)
                final_value = float(amount)*float(currency_exchange_rate.rate_value)
                twr = calculate_twr(amount, final_value, date, end_date)
                response.append({"date": date,
                                 "rate_value": rate_value,
                                 "twr": twr})
            serializer = self.serializer_class(response, many=True)
            return Response(serializer.data)
        else:
            return validation

