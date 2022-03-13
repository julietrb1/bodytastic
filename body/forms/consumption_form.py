from django import forms
from body.models import Consumption
import logging

logger = logging.getLogger(__name__)


class ConsumptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConsumptionForm, self).__init__(*args, **kwargs)
        self.fields["when"].input_formats = ["%B %d, %Y %I:%M %p"]
        if self.instance.pk:
            logger.debug("Not showing when, as no instance in ConsumptionForm.")
            del self.fields["when"]

    class Meta:
        model = Consumption
        fields = ["when", "quantity"]
