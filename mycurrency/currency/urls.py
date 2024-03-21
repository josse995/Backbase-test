from django.urls import path

from .views import historical_rates_value_graph, converter_online

app_name = "currency"

urlpatterns = [
    path(
        "historical_rates_value_graph/",
        historical_rates_value_graph,
        name="historical-rates-value-graph",
    ),
    path("converter_online/", converter_online, name="converter-online"),
]
