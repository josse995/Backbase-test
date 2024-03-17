from datetime import datetime

from django_filters import FilterSet, CharFilter, NumberFilter, DateFilter
from rest_framework import serializers
from rest_framework.response import Response

from mycurrency.core.models import Currency


class GetCurrencyRateOfReturnFilter(FilterSet):
    source_currency = CharFilter(field_name='source_currency', label='Source currency',
                                 help_text='Source currency code (e.g., USD)', required=True)
    exchanged_currency = CharFilter(field_name='exchanged_currency', label='Exchange currency',
                                    help_text='Exchange currency code (e.g., USD)', required=True)
    amount = NumberFilter(field_name='amount',
                          label='Positive number that represents the amount to convert from source_currency '
                                'to exchange_currency',
                          required=True)
    start_date = DateFilter(field_name='start_date', lookup_expr='gte',
                            label='Start date for calculating the time-weighted rate of return (YYYY-MM-DD)',
                            required=True)


class GetCurrencyRateOfReturnSerializer(serializers.Serializer):
    date = serializers.DateField()
    rate_value = serializers.DecimalField(max_digits=18, decimal_places=6)
    twr = serializers.DecimalField(max_digits=18, decimal_places=6)


def validate_fields(request):
    source_currency = request.query_params.get('source_currency', None)
    if Currency.objects.filter(code=source_currency.upper()).count() <= 0:
        return Response({'error': f'Source currency \'{source_currency}\' not found'}, status=404)
    exchanged_currency = request.query_params.get('exchanged_currency', None)
    if Currency.objects.filter(code=exchanged_currency.upper()).count() <= 0:
        return Response({'error': f'Exchange currency \'{exchanged_currency}\' not found'}, status=404)
    try:
        datetime.strptime(request.query_params.get('start_date', None), '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': f'Invalid date format for field \'start_from\''}, status=400)
    amount = request.query_params.get('amount', None)
    if not amount.isnumeric() or float(amount) <= 0:
        return Response({"error": f'Parameter \'amount\' must be a positive number greater than 0'}, status=400)
    return None
