from django import forms

from body.models import BodyAreaReport


class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields["when"].input_formats = ["%B %d, %Y"]

    class Meta:
        model = BodyAreaReport
        fields = ["when", "weight_in_kg"]
