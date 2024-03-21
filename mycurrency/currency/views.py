from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render

from mycurrency.currency.models import CurrencyExchangeRate, Currency


def historical_rates_value_graph_currencies_selector(request):
    currencies = Currency.objects.all()
    data = {
        "source_currency_list": currencies,
        "exchanged_currency_list": currencies
    }
    if request.POST:
        selected_source_currency = request.POST.get('source_currency')
        selected_exchanged_currency = request.POST.get('exchanged_currency')
        data.update({"selected_source_currency": selected_exchanged_currency,
                     "selected_exchanged_currency": selected_source_currency})

    return render(request, 'backoffice/graph_currencies_selector.html', context=data)


def historical_rates_value_graph(request):
    source_currency = request.POST.get('source_currency')
    exchanged_currency = request.POST.get('exchanged_currency')
    if source_currency == exchanged_currency:
        messages.error(request, "To get historical rate value graph please select two different currencies.")
        return historical_rates_value_graph_currencies_selector(request)
    else:
        labels = []
        values = []
        source_currency = request.POST.get('source_currency')
        exchanged_currency = request.POST.get('exchanged_currency')

        currency_exchange_rate_list_to_show = CurrencyExchangeRate.objects.filter(
            Q(source_currency__code=source_currency) &
            Q(exchanged_currency__code=exchanged_currency)).order_by('valuation_date')

        # For each valuation date, get the rate_value
        for currency_exchange_rate_to_show in currency_exchange_rate_list_to_show:
            labels.append(currency_exchange_rate_to_show.valuation_date.strftime("%Y-%m-%d"))
            values.append(float(currency_exchange_rate_to_show.rate_value))

        # Prepare data to be sent as JSON
        data = {
            'labels': labels,
            'values': values,
            'source_currency': source_currency,
            'exchanged_currency': exchanged_currency,
            'title': 'Currency Exchange Rates',
        }
        return render(request, 'backoffice/graph_template.html', context=data)


def converter_online(request):
    currencies = Currency.objects.all()
    data = {
        "source_currency_list": currencies,
        "exchanged_currency_list": currencies,
    }
    if request.POST:
        source_currency = request.POST.get('source_currency')
        exchanged_currency = request.POST.get('exchanged_currency')
        amount = request.POST.get('currency-amount')
        queryset = (CurrencyExchangeRate.objects
                    .filter(Q(source_currency__code=source_currency) &
                            Q(exchanged_currency__code=exchanged_currency))
                    .order_by('valuation_date'))
        last_exchanged_rate = queryset.last()
        final_amount = float(amount) * float(last_exchanged_rate.rate_value)
        data.update({
            "selected_source_currency": source_currency,
            "selected_exchanged_currency": exchanged_currency,
            "final_amount": final_amount
        })

    return render(request, 'backoffice/currencies_converter.html', context=data)
