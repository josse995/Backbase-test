from django_filters import FilterSet, CharFilter, NumberFilter
from rest_framework import serializers
from rest_framework.response import Response

from mycurrency.core.models import CurrencyExchangeRate, Currency


class GetCurrencyConverterFilter(FilterSet):
    source_currency = CharFilter(field_name='source_currency', label='Source currency',
                                 help_text='Source currency code (e.g., USD)', required=True)
    exchanged_currency = CharFilter(field_name='exchanged_currency', label='Exchange currency',
                                    help_text='Exchange currency code (e.g., USD)', required=True)
    amount = NumberFilter(field_name='amount',
                          label='Positive number that represents the amount to convert from source_currency '
                                'to exchange_currency',
                          required=True)


class GetCurrencyConverterSerializer(serializers.ModelSerializer):
    source_currency = serializers.CharField(source='source_currency.code')
    exchanged_currency = serializers.CharField(source='exchanged_currency.code')

    class Meta:
        model = CurrencyExchangeRate
        fields = ('source_currency', 'exchanged_currency', 'rate_value')

    def to_representation(self, instance, amount):
        # NOTE: it could be useful to have also the rate_value for,
        # for instance, have a confirmation message when the transaction
        # is going to be made and know source currency,
        # exchanged currency, the rate and the final amount.
        representation = super().to_representation(instance)
        if amount is not None:
            representation['amount'] = float(instance.rate_value) * float(amount)
        return representation


def validate_fields(request):
    source_currency = request.query_params.get('source_currency', None)
    if Currency.objects.filter(code=source_currency.upper()).count() <= 0:
        return Response({'error': f'Source currency \'{source_currency}\' not found'}, status=404)
    exchanged_currency = request.query_params.get('exchanged_currency', None)
    if Currency.objects.filter(code=exchanged_currency.upper()).count() <= 0:
        return Response({'error': f'Exchange currency \'{exchanged_currency}\' not found'}, status=404)
    amount = request.query_params.get('amount', None)
    if not amount.isnumeric() or float(amount) <= 0:
        return Response({"error": f'Parameter \'amount\' must be a positive number greater than 0'}, status=400)
    return None
