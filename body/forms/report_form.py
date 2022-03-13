from body.forms.form_mixins import WhenModelForm

from body.models import Report
import logging

logger = logging.getLogger(__name__)


class ReportForm(WhenModelForm):
    class Meta:
        model = Report
        fields = ["when", "weight_in_kg"]
