from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_medicine, create_schedule
from django.utils.timezone import make_aware, datetime
from freezegun import freeze_time

from body.urls.medication import SCHEDULE_CREATE_ROUTE


@freeze_time("2022-03-01")
class ScheduleCreateViewTests(LoginTestCase):
    def test_initial_values_set_in_form(self):
        medicine = create_medicine(self.user)
        response = self.client.get(
            reverse(
                SCHEDULE_CREATE_ROUTE,
                kwargs={"medicinepk": medicine.pk},
            )
        )
        self.assertIsNone(response.context["form"]["start_date"].initial)
        self.assertIsNone(response.context["form"]["end_date"].initial)
        self.assertIsNone(response.context["form"]["time"].initial)
        self.assertEqual(response.context["form"]["frequency_in_days"].initial, 1)
        self.assertEqual(response.context["form"]["quantity"].initial, 1)
        self.assertEqual(response.context["form"]["tolerance_mins"].initial, 30)

    def test_creating_schedule_adds_message(self):
        medicine = create_medicine(self.user)
        response = self.client.post(
            reverse(
                SCHEDULE_CREATE_ROUTE,
                kwargs={"medicinepk": medicine.pk},
            ),
            {
                "start_date": "March 2, 2022",
                "end_date": "March 3, 2022",
                "time": "8:30 AM",
                "frequency_in_days": 1,
                "quantity": 1,
                "tolerance_mins": 30,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assert_message(response, "Schedule Created")
