from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_medicine, create_schedule
from freezegun import freeze_time
from django.utils.timezone import make_aware, datetime


@freeze_time(make_aware(datetime(2022, 3, 1, 8, 1)))
class ScheduleTests(LoginTestCase):
    def test_next_consumption_today_no_end(self):
        """
        When a schedule has no end date, and the time for the schedule hasn't passed, the next consumption should be today.
        """
        medicine = create_medicine(self.user)
        schedule = create_schedule(
            medicine,
            make_aware(datetime(2022, 2, 1)).date(),
            None,
            time=datetime(2022, 3, 1, 9, 0).time(),
        )
        self.assertEqual(
            schedule.next_consumption, make_aware(datetime(2022, 3, 1, 9, 0))
        )

    def test_next_consumption_today_one_more(self):
        """
        When a schedule has an end date of today, but the time for the schedule hasn't passed, the next (and final) consumption should be today.
        """
        medicine = create_medicine(self.user)
        schedule = create_schedule(
            medicine,
            make_aware(datetime(2022, 2, 1)).date(),
            make_aware(datetime(2022, 3, 1)).date(),
            time=datetime(2022, 3, 1, 9, 0).time(),
        )
        self.assertEqual(
            schedule.next_consumption, make_aware(datetime(2022, 3, 1, 9, 0))
        )

    def test_next_consumption_past_time_none_same_day(self):
        """
        When a schedule has an end date of today, and the time for the schedule has passed, the next consumption should be None.
        """
        medicine = create_medicine(self.user)
        schedule = create_schedule(
            medicine,
            make_aware(datetime(2022, 2, 1)).date(),
            make_aware(datetime(2022, 3, 1)).date(),
            time=datetime(2022, 3, 1, 8, 0).time(),
        )
        self.assertIsNone(schedule.next_consumption)

    def test_next_consumption_past_time_none_tomorrow(self):
        """
        The next date on a schedule should be None if the end date is tomorrow, but the schedule's time hasn't passed.
        """
        medicine = create_medicine(self.user)
        schedule = create_schedule(
            medicine,
            make_aware(datetime(2022, 2, 1)).date(),
            make_aware(datetime(2022, 2, 28)).date(),
            time=datetime(2022, 3, 1, 10, 0).time(),
        )
        self.assertIsNone(schedule.next_consumption)
