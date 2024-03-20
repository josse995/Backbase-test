from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Currency, CurrencyExchangeRate


def historical_rates_value_graph_action(modeladmin, request, queryset):
    selected_currency_exchange_rates = queryset.values_list('id', flat=True)
    if selected_currency_exchange_rates.count() > 1:
        messages.error(request, "To get historical rate value graph please select only one exchange rate.")
    else:
        url = (reverse("currency:historical-rates-value-graph") + "?currency_exchange_rate_id=" +
               ','.join(map(str, selected_currency_exchange_rates)))
        return HttpResponseRedirect(url)


class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    actions = [historical_rates_value_graph_action]


admin.site.register(Currency)
admin.site.register(CurrencyExchangeRate, CurrencyExchangeRateAdmin)
