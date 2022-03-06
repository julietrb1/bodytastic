from django import forms

from life_events.models import Event


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["when"].input_formats = ["%B %d, %Y %I:%M %p"]

    class Meta:
        model = Event
        fields = ["name", "when", "category"]
