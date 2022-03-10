from django import forms
from body.models import Schedule


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
