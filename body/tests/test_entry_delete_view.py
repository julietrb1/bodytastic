from datetime import datetime

from django.urls import reverse
from django.utils.timezone import make_aware, localdate

from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_body_area, create_entry, create_report
from body.urls.mybody import ENTRY_DELETE_ROUTE
from freezegun import freeze_time


@freeze_time(make_aware(datetime(2022, 3, 1)))
class EntryDeleteViewTests(LoginTestCase):
    def test_has_data(self):
        body_area = create_body_area()
        report = create_report(self.user, when=make_aware(datetime(2022, 3, 1)))
        entry = create_entry(report, body_area)
        response = self.client.get(
            reverse(ENTRY_DELETE_ROUTE, kwargs={"reportpk": report.pk, "pk": entry.pk})
        )
        self.assertContains(response, "Delete Entry?")
        self.assertContains(response, body_area.name)
