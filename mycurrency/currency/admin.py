from django.contrib import admin
from django.urls import path

from .models import Currency, CurrencyExchangeRate, GraphViewModel, ConverterViewModel
from .views import converter_online, historical_rates_value_graph_currencies_selector


class GraphViewModelAdmin(admin.ModelAdmin):
    model = GraphViewModel  # dummy model

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('historical_rates_value_graph_selector/', historical_rates_value_graph_currencies_selector,
                 name=view_name),
        ]


class ConverterViewModelAdmin(admin.ModelAdmin):
    model = ConverterViewModel

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('converter_online/', converter_online,
                 name=view_name),
        ]


admin.site.register(Currency)
admin.site.register(CurrencyExchangeRate)
admin.site.register(GraphViewModel, GraphViewModelAdmin)
admin.site.register(ConverterViewModel, ConverterViewModelAdmin)
