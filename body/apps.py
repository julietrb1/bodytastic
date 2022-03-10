from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save, post_delete


class BodyConfig(AppConfig):
    """App config class for Medication."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "body"

    def ready(self):
        from body.signals import (
            consumption_pre_save,
            consumption_post_save,
            ledger_entry_pre_save,
            ledger_entry_post_delete,
        )
        from body.models import Consumption, LedgerEntry

        pre_save.connect(
            consumption_pre_save,
            dispatch_uid="consumption_pre_save",
            sender=Consumption,
        )

        post_save.connect(
            consumption_post_save,
            dispatch_uid="consumption_post_save",
            sender=Consumption,
        )

        pre_save.connect(
            ledger_entry_pre_save,
            dispatch_uid="ledger_entry_pre_save",
            sender=LedgerEntry,
        )

        post_delete.connect(
            ledger_entry_post_delete,
            dispatch_uid="ledger_entry_post_delete",
            sender=LedgerEntry,
        )
