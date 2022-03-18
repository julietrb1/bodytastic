from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.urls.mybody import REPORT_CREATE_ROUTE
from freezegun import freeze_time
from django.utils.timezone import datetime, make_aware, localdate
from body.tests.model_helpers import create_report


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

    def test_form_has_initial_date(self):
        """
        Given that a report for the current date does not exist,
        then the date should be automatically populated.
        """
        response = self.client.get(reverse(REPORT_CREATE_ROUTE))
        self.assertEqual(response.context["form"]["when"].initial, localdate())

    def test_form_without_initial_date(self):
        """
        Given that a report for the current date exists,
        then the date should not be automatically populated.
        """
        create_report(self.user, localdate())
        response = self.client.get(reverse(REPORT_CREATE_ROUTE))
        self.assertEqual(response.context["form"]["when"].initial, None)
