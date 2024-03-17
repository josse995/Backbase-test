import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CurrencyConfig(AppConfig):
    name = 'mycurrency.core'
    verbose_name = _("Core")

    def ready(self):
        with contextlib.suppress(ImportError):
            import mycurrency.users.signals  # noqa: F401
