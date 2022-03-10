from django import forms
from body.models import LedgerEntry


class RefillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RefillForm, self).__init__(*args, **kwargs)
        self.fields["when"].input_formats = ["%B %d, %Y %I:%M %p"]

    class Meta:
        model = LedgerEntry
        fields = ["when", "quantity"]
