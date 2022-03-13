import logging
from django.forms.fields import DateField, DateTimeField

logger = logging.getLogger(__name__)


class WhenFieldMixin:
    def get_form(self, *args, **kwargs):
        form = super(WhenFieldMixin, self).get_form(*args, **kwargs)
        if form.instance.pk:
            logger.debug("Not showing when, as no instance in ReportForm.")
            del form.fields["when"]
        elif type(form.fields["when"]) == DateField:
            form.fields["when"].input_formats = ["%B %d, %Y"]
        elif type(form.fields["when"]) == DateTimeField:
            form.fields["when"].input_formats = ["%B %d, %Y %I:%M %p"]

        return form
