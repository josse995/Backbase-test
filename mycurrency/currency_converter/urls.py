from django.conf import settings
from django.urls import path
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from mycurrency.currency_converter import views

router = routers.DefaultRouter() if settings.DEBUG else SimpleRouter()

app_name = "currency_converter"

urlpatterns = [
    path(
        "currency-converter/",
        views.CurrencyConverterView.as_view(),
        name="currency-converter",
    ),
]
