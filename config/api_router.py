from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from mycurrency.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)

app_name = "api"
urlpatterns = [
                  path("", include('mycurrency.currency_rates.urls')),
                  path("", include('mycurrency.currency_converter.urls')),
                  path("", include('mycurrency.rate_of_return.urls')),
              ] + router.urls
