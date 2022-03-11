from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.urls.medication import MEDICINE_CREATE_ROUTE
from freezegun import freeze_time


@freeze_time("2022-03-01")
class MedicineCreateViewTests(LoginTestCase):
    def test_loads_form(self):
        response = self.client.get(reverse(MEDICINE_CREATE_ROUTE))
        self.assertContains(response, "Add")
