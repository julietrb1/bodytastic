from django import forms

from mind_and_soul.models import EmotionReport


class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields["when"].input_formats = ["%B %d, %Y"]

    class Meta:
        model = EmotionReport
        fields = ["when", "notes", "energy_level"]
