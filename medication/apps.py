"""App config module for Medication."""

from django.apps import AppConfig


class MedicationConfig(AppConfig):
    """App config class for Medication."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medication'
