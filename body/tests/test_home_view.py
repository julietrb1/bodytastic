from django.urls import reverse
from django.utils.html import escape

from body.tests.login_test_case import LoginTestCase

HOME_INDEX_ROUTE = "index"


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