from django import forms

from medication.models import Consumption


class ConsumptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConsumptionForm, self).__init__(*args, **kwargs)
        self.fields["when"].input_formats = ["%B %d, %Y %I:%M %p"]

    class Meta:
        model = Consumption
        fields = ["when", "quantity"]
