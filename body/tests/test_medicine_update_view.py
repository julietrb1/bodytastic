from django.urls import reverse
from django.utils.timezone import datetime, make_aware
from freezegun import freeze_time
from django.forms.models import model_to_dict

from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_medicine
from body.urls.medication import MEDICINE_UPDATE_ROUTE


@freeze_time(make_aware(datetime(2022, 3, 1)))
class MedicineListUpdateTests(LoginTestCase):
    def test_non_existent_get_returns_404(self):
        response = self.client.get(reverse(MEDICINE_UPDATE_ROUTE, args=[12345]))
        self.assertEqual(response.status_code, 404)

    def test_other_user_get_returns_404(self):
        medicine = create_medicine(self.other_user)
        response = self.client.get(reverse(MEDICINE_UPDATE_ROUTE, args=[medicine.pk]))
        self.assertEqual(response.status_code, 404)

    def test_updating_shows_message(self):
        medicine = create_medicine(self.user)
        response = self.client.post(
            reverse(MEDICINE_UPDATE_ROUTE, args=[medicine.pk]),
            model_to_dict(medicine),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assert_message(response, "Medicine Updated")
