from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BeamsAndColumnsConfig(AppConfig):
    name = "timberframes.beams_and_columns"
    verbose_name = _("Beams and Columns")

    def ready(self):
        try:
            import timberframes.beams_and_columns.signals  # noqa F401
        except ImportError:
            pass
