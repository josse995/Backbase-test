from datetime import datetime

from django_filters import FilterSet, DateFilter, CharFilter
from rest_framework.response import Response

from mycurrency.core.models import Currency


class GetCurrencyRatesFilter(FilterSet):
    source_currency = CharFilter(field_name='source_currency__name', label='Source currency',
                                 help_text='Source currency code (e.g., USD)', required=True)
    date_from = DateFilter(field_name='date_from', lookup_expr='gte',
                           label='Start date for exchange rates (YYYY-MM-DD)', required=True)
    date_to = DateFilter(field_name='date_from', lookup_expr='lte', label='Start date for exchange rates (YYYY-MM-DD)',
                         required=True)


def validate_fields(request):
    source_currency = request.query_params.get('source_currency', None)
    if Currency.objects.filter(code=source_currency.upper()).count() <= 0:
        return Response({'error': f'Source currency \'{source_currency}\' not found'}, status=404)
    try:
        datetime.strptime(request.query_params.get('date_from', None), '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': f'Invalid date format for field \'date_from\''}, status=400)
    try:
        datetime.strptime(request.query_params.get('date_to', None), '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': f'Invalid date format for field \'date_to\''}, status=400)
    return None
