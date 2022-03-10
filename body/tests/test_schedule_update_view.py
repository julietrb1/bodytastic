from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_medicine, create_schedule
from django.utils.timezone import make_aware, datetime

BODY_SCHEDULE_UPDATE_ROUTE = "schedule-update"


class ScheduleUpdateViewTests(LoginTestCase):
    def test_no_other_user_schedules_shown(self):
        other_medicine = create_medicine(self.other_user)
        other_schedule = create_schedule(
            other_medicine, make_aware(datetime(2022, 1, 1)), None
        )
        response = self.client.get(
            reverse(
                BODY_SCHEDULE_UPDATE_ROUTE,
                kwargs={"medicinepk": other_medicine.pk, "pk": other_schedule.pk},
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_report_404(self):
        medicine = create_medicine(self.user)
        response = self.client.get(
            reverse(
                BODY_SCHEDULE_UPDATE_ROUTE,
                kwargs={"medicinepk": medicine.pk, "pk": 12345},
            )
        )
        self.assertEqual(response.status_code, 404)
