from django.urls import reverse
from django.utils.html import escape
from django.utils.timezone import make_aware, datetime

from body.tests.login_test_case import LoginTestCase
from body.urls.home import HOME_INDEX_ROUTE
from freezegun import freeze_time


@freeze_time("2022-03-01")
class HomeViewTests(LoginTestCase):
    def test_title_shown(self):
        """
        A nice simple test: Does the title show?
        """
        response = self.client.get(reverse(HOME_INDEX_ROUTE))
        self.assertContains(
            response,
            "Never miss a beat. Keep track of consumption and schedules for your meds.",
        )
        self.assertContains(
            response, "Measurements matter. Keep track of trends and make notes here."
        )
        self.assertContains(
            response,
            escape(
                "Significant, small, or otherwise, it's probably worth remembering. Note it down here."
            ),
        )

    def test_shows_greeting(self):
        for hours, hello_part in zip(
            ((0, 5), (6, 10), (11, 14), (15, 17), (18, 23)),
            (
                "Burning the Midnight Oil",
                "Good Morning",
                "Good Day",
                "Good Afternoon",
                "Good Evening",
            ),
        ):
            for hour in hours:
                with freeze_time(lambda: make_aware(datetime(2022, 1, 1, hour))):
                    response = self.client.get(reverse(HOME_INDEX_ROUTE))
                    self.assertContains(response, f"{hello_part}, Jennifer")
