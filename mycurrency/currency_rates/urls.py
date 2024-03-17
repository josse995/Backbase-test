from django.conf import settings
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from mycurrency.currency_rates import views

router = routers.DefaultRouter() if settings.DEBUG else SimpleRouter()

app_name = 'currency_rates'

urlpatterns = [
    path('currency-rates/', views.CurrencyRatesView.as_view()),
]
