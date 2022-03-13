from django import forms
import logging
from django.forms.fields import DateField, DateTimeField

logger = logging.getLogger(__name__)


class WhenModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WhenModelForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            logger.debug("Not showing when, as no instance in ReportForm.")
            del self.fields["when"]
        elif type(self.fields["when"]) == DateField:
            self.fields["when"].input_formats = ["%B %d, %Y"]
        elif type(self.fields["when"]) == DateTimeField:
            self.fields["when"].input_formats = ["%B %d, %Y %I:%M %p"]
