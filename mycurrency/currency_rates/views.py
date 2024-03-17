from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from mycurrency.core.api.serializers import CurrencyExchangeRateSerializer
from mycurrency.core.models import CurrencyExchangeRate
from mycurrency.currency_rates.serializers import GetCurrencyRatesFilter, validate_fields
from mycurrency.providers.services import get_all_currency_exchange_rates_for_source_currency


class CurrencyRatesView(ListAPIView):
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = CurrencyExchangeRateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GetCurrencyRatesFilter

    def get(self, request, *args, **kwargs):
        validation = validate_fields(request)
        if validation is None:
            source_currency = request.query_params.get('source_currency', None)
            date_from = datetime.strptime(request.query_params.get('date_from', None), '%Y-%m-%d').date()
            date_to = datetime.strptime(request.query_params.get('date_to', None), '%Y-%m-%d').date()
            if date_from > date_to:
                return Response({"error": f'dateFrom must be greater than dateTo'}, status=400)

            queryset = get_all_currency_exchange_rates_for_source_currency(source_currency, date_from, date_to)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        else:
            return validation

