from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mycurrency.core.models import CurrencyExchangeRate
from mycurrency.currency_converter.serializers import (
    GetCurrencyConverterFilter,
    GetCurrencyConverterSerializer,
    validate_fields,
)
from mycurrency.providers.services import get_latest_currency_exchange_rate


class CurrencyConverterView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = GetCurrencyConverterSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = GetCurrencyConverterFilter

    def get(self, request, *args, **kwargs):
        validation = validate_fields(request)
        if validation is None:
            source_currency = request.query_params.get("source_currency", None)
            exchanged_currency = request.query_params.get("exchanged_currency", None)
            amount = request.query_params.get("amount", None)

            queryset = get_latest_currency_exchange_rate(
                source_currency, exchanged_currency
            )
            if queryset.count() <= 0:
                # NOTE: If we implement a monitoring tool like sentry, this error will be nice to send a message through
                # slack, email or another comm tool to be aware of it.
                return Response(
                    {
                        "error": f"An error occurred when retrieving latest exchange rate. Try it again later. "
                        f"If the error persist, contact the administrator, with all "
                        f"possible information to replicate the error."
                    },
                    status=500,
                )
            serializer = self.serializer_class()
            data = serializer.to_representation(queryset.first(), amount)
            return Response(data)
        else:
            return validation
