from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.urls.medication import CONSUMPTION_CREATE_ROUTE
from freezegun import freeze_time
from body.tests.model_helpers import create_consumption, create_medicine
from django.forms.models import model_to_dict


@freeze_time("2022-03-01")
class ConsumptionCreateViewTests(LoginTestCase):
    def test_create_form_shows_when_field(self):
        medicine = create_medicine(self.user)
        response = self.client.get(
            reverse(CONSUMPTION_CREATE_ROUTE, kwargs={"medicinepk": medicine.pk})
        )
        self.assertContains(response, "When:")

    def test_create_form_adds_message(self):
        medicine = create_medicine(self.user, current_balance=2)
        response = self.client.post(
            reverse(CONSUMPTION_CREATE_ROUTE, kwargs={"medicinepk": medicine.pk}),
            model_to_dict(create_consumption(medicine)),
            follow=True,
        )
        self.assert_message(response, "Consumption Created")
