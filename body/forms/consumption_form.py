from body.forms.form_mixins import WhenModelForm
from body.models import Consumption
import logging

logger = logging.getLogger(__name__)


class ConsumptionForm(WhenModelForm):
    class Meta:
        model = Consumption
        fields = ["when", "quantity"]
