from django.urls import path
from .views import historical_rates_value_graph

app_name = "currency"

urlpatterns = [
    path('historical_rates_value_graph/', historical_rates_value_graph, name="historical-rates-value-graph"),
]
