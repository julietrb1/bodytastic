from django.urls import reverse
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_medicine, create_schedule
from body.urls.medication import SCHEDULE_LIST_ROUTE
from django.utils.timezone import make_aware, datetime, localtime, timedelta
from freezegun import freeze_time


@freeze_time(make_aware(datetime(2022, 3, 1)))
class ScheduleListViewTests(LoginTestCase):
    def test_shows_active(self):
        medicine = create_medicine(self.user)
        create_schedule(medicine, localtime() - timedelta(days=2), None)
        response = self.client.get(
            reverse(SCHEDULE_LIST_ROUTE, kwargs={"medicinepk": medicine.pk})
        )

        self.assertContains(response, "Next:")
        self.assertNotContains(response, "Finished:")
        self.assertNotContains(response, "Starts:")

    def test_shows_future(self):
        medicine = create_medicine(self.user)
        create_schedule(medicine, localtime() + timedelta(days=2), None)
        response = self.client.get(
            reverse(SCHEDULE_LIST_ROUTE, kwargs={"medicinepk": medicine.pk})
        )

        self.assertNotContains(response, "Next:")
        self.assertNotContains(response, "Finished:")
        self.assertContains(response, "Starts:")

    def test_shows_past(self):
        medicine = create_medicine(self.user)
        create_schedule(
            medicine, localtime() - timedelta(days=2), localtime() - timedelta(days=1)
        )
        response = self.client.get(
            reverse(SCHEDULE_LIST_ROUTE, kwargs={"medicinepk": medicine.pk})
        )

        self.assertNotContains(response, "Next:")
        self.assertContains(response, "Finished:")
        self.assertNotContains(response, "Starts:")
