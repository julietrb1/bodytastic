from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.urls.mybody import REPORT_CREATE_ROUTE
from freezegun import freeze_time
from django.utils.timezone import datetime, make_aware


@freeze_time(make_aware(datetime(2022, 3, 1)))
class MedicineCreateViewTests(LoginTestCase):
    def test_loads_form(self):
        response = self.client.get(reverse(REPORT_CREATE_ROUTE))
        self.assertContains(response, "Add")

    def test_medicine_creation_shows_message(self):
        response = self.client.post(
            reverse(REPORT_CREATE_ROUTE), {"when": "March 2, 2022"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assert_message(response, "Report Created")
