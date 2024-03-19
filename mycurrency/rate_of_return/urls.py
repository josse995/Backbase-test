from django.conf import settings
from django.urls import path
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from mycurrency.rate_of_return import views

router = routers.DefaultRouter() if settings.DEBUG else SimpleRouter()

app_name = "rate_of_return"

urlpatterns = [
    path("rate-of-return/", views.RateOfReturnView.as_view(), name="rate-of-return"),
]
