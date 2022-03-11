from django import forms

from body.models import Report
import logging

logger = logging.getLogger(__name__)


class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields["when"].input_formats = ["%B %d, %Y"]
        if self.instance:
            logger.debug("Not showing when, as no instance in ReportForm.")
            del self.fields["when"]

    class Meta:
        model = Report
        fields = ["when", "weight_in_kg"]
