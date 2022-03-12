from django.urls import reverse
from django.utils.timezone import datetime, make_aware
from freezegun import freeze_time

from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_medicine, create_schedule
from body.urls.medication import SCHEDULE_DELETE_ROUTE


@freeze_time(make_aware(datetime(2022, 3, 1)))
class ScheduleListDeleteTests(LoginTestCase):
    def test_non_existent_get_returns_404(self):
        medicine = create_medicine(self.user)
        response = self.client.get(
            reverse(
                SCHEDULE_DELETE_ROUTE, kwargs={"medicinepk": medicine.pk, "pk": 12345}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_other_user_get_returns_404(self):
        other_medicine = create_medicine(self.other_user)
        other_schedule = create_schedule(
            other_medicine,
            make_aware(datetime(2022, 1, 1)),
            make_aware(datetime(2022, 1, 2)),
        )
        response = self.client.get(
            reverse(
                SCHEDULE_DELETE_ROUTE,
                kwargs={"medicinepk": other_medicine.pk, "pk": other_schedule.pk},
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_deleting_shows_message(self):
        medicine = create_medicine(self.user)
        schedule = create_schedule(
            medicine, make_aware(datetime(2022, 1, 1)), make_aware(datetime(2022, 1, 2))
        )
        response = self.client.post(
            reverse(
                SCHEDULE_DELETE_ROUTE,
                kwargs={"medicinepk": medicine.pk, "pk": schedule.pk},
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assert_message(response, "Schedule Deleted")
