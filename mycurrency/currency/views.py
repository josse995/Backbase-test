from django.db.models import Q
from django.shortcuts import render

from mycurrency.currency.models import CurrencyExchangeRate


def historical_rates_value_graph(request):
    # Retrieve data for the chart from the Book model
    labels = []
    values = []
    currency_exchange_rate_id = request.GET.get('currency_exchange_rate_id')
    currency_exchange_rate = CurrencyExchangeRate.objects.filter(id=currency_exchange_rate_id).first()

    currency_exchange_rate_list_to_show = CurrencyExchangeRate.objects.filter(
        Q(source_currency=currency_exchange_rate.source_currency) &
        Q(exchanged_currency=currency_exchange_rate.exchanged_currency)).order_by('valuation_date')

    # For each valuation date, get the rate_value
    for currency_exchange_rate_to_show in currency_exchange_rate_list_to_show:
        labels.append(currency_exchange_rate_to_show.valuation_date.strftime("%Y-%m-%d"))
        print(currency_exchange_rate_to_show.rate_value)
        values.append(float(currency_exchange_rate_to_show.rate_value))

    # Prepare data to be sent as JSON
    data = {
        'labels': labels,
        'values': values,
        'source_currency': currency_exchange_rate.source_currency,
        'exchanged_currency': currency_exchange_rate.exchanged_currency,
        'title': 'Currency Exchange Rates',
    }
    print(data)
    return render(request, 'backoffice/graph_template.html', context=data)
