from django.urls import path

from mycurrency.currency_rates import views

app_name = "currency_rates"

urlpatterns = [
    path("currency-rates/", views.CurrencyRatesView.as_view(), name="currency-rates"),
]
