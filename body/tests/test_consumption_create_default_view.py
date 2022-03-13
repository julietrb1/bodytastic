from django.urls import reverse
from body.models import Consumption, Medicine
from body.tests.login_test_case import LoginTestCase
from body.urls.medication import CONSUMPTION_CREATE_DEFAULT_ROUTE, MEDICINE_DETAIL_ROUTE
from freezegun import freeze_time
from body.tests.model_helpers import create_consumption, create_medicine
from django.utils.timezone import datetime, make_aware


@freeze_time(make_aware(datetime(2022, 1, 1)))
class ConsumptionCreateViewTests(LoginTestCase):
    def test_default_consumption_works(self):
        self.assertEqual(Consumption.objects.count(), 0)
        medicine = create_medicine(self.user, current_balance=5)
        response = self.client.post(
            reverse(
                CONSUMPTION_CREATE_DEFAULT_ROUTE, kwargs={"medicinepk": medicine.pk}
            ),
            follow=True,
        )
        self.assertRedirects(
            response, reverse(MEDICINE_DETAIL_ROUTE, args=[medicine.pk])
        )
        self.assertEqual(Consumption.objects.count(), 1)
        self.assertEqual(Medicine.objects.get(pk=medicine.pk).current_balance, 4)

    def test_default_consumption_shows_message(self):
        medicine = create_medicine(self.user, current_balance=5)
        response = self.client.post(
            reverse(
                CONSUMPTION_CREATE_DEFAULT_ROUTE, kwargs={"medicinepk": medicine.pk}
            ),
            follow=True,
        )
        self.assert_message(response, "Default Consumption Logged")

    def test_default_consumption_other_user(self):
        other_medicine = create_medicine(self.other_user, current_balance=5)
        response = self.client.post(
            reverse(
                CONSUMPTION_CREATE_DEFAULT_ROUTE,
                kwargs={"medicinepk": other_medicine.pk},
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Consumption.objects.count(), 0)
        self.assertEqual(Medicine.objects.get(pk=other_medicine.pk).current_balance, 5)

    def test_default_consumption_nonexistent(self):
        response = self.client.post(
            reverse(
                CONSUMPTION_CREATE_DEFAULT_ROUTE,
                kwargs={"medicinepk": 12345},
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 404)
