from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.urls.medication import CONSUMPTION_UPDATE_ROUTE
from freezegun import freeze_time
from body.tests.model_helpers import create_consumption, create_medicine
from django.forms.models import model_to_dict


@freeze_time("2022-03-01")
class ConsumptionUpdateViewTests(LoginTestCase):
    def test_update_form_doesnt_show_when_field(self):
        medicine = create_medicine(self.user, current_balance=1)
        consumption = create_consumption(medicine)
        response = self.client.get(
            reverse(
                CONSUMPTION_UPDATE_ROUTE,
                kwargs={"medicinepk": medicine.pk, "pk": consumption.pk},
            )
        )
        self.assertNotContains(response, "When:")

    def test_update_form_adds_message(self):
        medicine = create_medicine(self.user, current_balance=2)
        consumption = create_consumption(medicine)
        response = self.client.post(
            reverse(
                CONSUMPTION_UPDATE_ROUTE,
                kwargs={"medicinepk": medicine.pk, "pk": consumption.pk},
            ),
            model_to_dict(create_consumption(medicine)),
            follow=True,
        )
        self.assert_message(response, "Consumption Updated")
