from django import forms

from medication.models import Consumption, Schedule


class ConsumptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConsumptionForm, self).__init__(*args, **kwargs)
        self.fields["when"].input_formats = ["%B %d, %Y %I:%M %p"]

    class Meta:
        model = Consumption
        fields = ["when", "quantity"]


class ScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields["start_date"].input_formats = ["%B %d, %Y"]
        self.fields["end_date"].input_formats = ["%B %d, %Y"]
        self.fields["time"].input_formats = ["%I:%M %p"]

    class Meta:
        model = Schedule
        fields = [
            "start_date",
            "end_date",
            "frequency_in_days",
            "time",
            "quantity",
            "tolerance_mins",
        ]
