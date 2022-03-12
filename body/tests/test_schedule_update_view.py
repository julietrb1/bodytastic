from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_medicine, create_schedule
from django.utils.timezone import make_aware, datetime
from freezegun import freeze_time
from django.forms.models import model_to_dict

from body.urls.medication import SCHEDULE_UPDATE_ROUTE


@freeze_time("2022-03-01")
class ScheduleUpdateViewTests(LoginTestCase):
    def test_initial_values_set_in_form(self):
        start_date = make_aware(datetime(2022, 1, 1)).date()
        end_date = None
        time = datetime(2022, 1, 1, 8).time()
        frequency_in_days = 2
        quantity = 3
        tolerance_mins = 45
        schedule = create_schedule(
            create_medicine(self.user),
            start_date,
            end_date,
            frequency_in_days,
            time,
            quantity,
            tolerance_mins,
        )
        response = self.client.get(
            reverse(
                SCHEDULE_UPDATE_ROUTE,
                kwargs={"medicinepk": schedule.medicine.pk, "pk": schedule.pk},
            )
        )
        self.assertEqual(response.context["form"].initial["start_date"], start_date)
        self.assertEqual(response.context["form"].initial["end_date"], end_date)
        self.assertEqual(response.context["form"].initial["time"], time)
        self.assertEqual(
            response.context["form"].initial["frequency_in_days"], frequency_in_days
        )
        self.assertEqual(response.context["form"].initial["quantity"], quantity)
        self.assertEqual(
            response.context["form"].initial["tolerance_mins"], tolerance_mins
        )

    def test_no_other_user_schedules_shown(self):
        other_medicine = create_medicine(self.other_user)
        other_schedule = create_schedule(
            other_medicine, make_aware(datetime(2022, 1, 1)), None
        )
        response = self.client.get(
            reverse(
                SCHEDULE_UPDATE_ROUTE,
                kwargs={"medicinepk": other_medicine.pk, "pk": other_schedule.pk},
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_report_404(self):
        medicine = create_medicine(self.user)
        response = self.client.get(
            reverse(
                SCHEDULE_UPDATE_ROUTE,
                kwargs={"medicinepk": medicine.pk, "pk": 12345},
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_updating_schedule_adds_message(self):
        schedule = create_schedule(
            create_medicine(self.user),
            make_aware(datetime(2022, 1, 1)),
            make_aware(datetime(2022, 1, 2)),
        )
        response = self.client.post(
            reverse(
                SCHEDULE_UPDATE_ROUTE,
                kwargs={"medicinepk": schedule.medicine.pk, "pk": schedule.pk},
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
        self.assert_message(response, "Schedule Updated")
