from django import forms

from body.models import BodyArea


class MassEntryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.report = kwargs.pop("report")
        super(MassEntryForm, self).__init__(*args, **kwargs)
        for body_area in BodyArea.objects.all():
            entry = self.report.entry_set.filter(body_area=body_area).first()
            self.fields[body_area.name] = forms.DecimalField(
                initial=entry.measurement if entry else None,
                required=False,
            )
