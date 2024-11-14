from django.apps import AppConfig
from ocr.functions import setup


class OcrConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ocr"

    def ready(self) -> None:
        setup()
        return super().ready()