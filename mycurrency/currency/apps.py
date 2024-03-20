import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CurrencyConfig(AppConfig):
    name = "mycurrency.currency"
    verbose_name = _("Currency")

    def ready(self):
        with contextlib.suppress(ImportError):
            import mycurrency.users.signals  # noqa: F401
