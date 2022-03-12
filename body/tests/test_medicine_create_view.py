from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.urls.medication import MEDICINE_CREATE_ROUTE
from freezegun import freeze_time
from body.tests.model_helpers import create_medicine
from django.forms.models import model_to_dict


@freeze_time("2022-03-01")
class MedicineCreateViewTests(LoginTestCase):
    def test_create_form_shows_name_field(self):
        response = self.client.get(reverse(MEDICINE_CREATE_ROUTE))
        self.assertContains(response, "Name:")

    def test_create_form_adds_message(self):
        response = self.client.post(
            reverse(MEDICINE_CREATE_ROUTE),
            model_to_dict(create_medicine(self.user)),
            follow=True,
        )
        self.assert_message(response, "Medicine Created")
