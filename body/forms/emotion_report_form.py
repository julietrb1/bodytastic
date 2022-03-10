from django import forms

from body.models import EmotionReport


class EmotionReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmotionReportForm, self).__init__(*args, **kwargs)
        self.fields["when"].input_formats = ["%B %d, %Y"]

    class Meta:
        model = EmotionReport
        fields = ["when", "notes", "energy_level"]
