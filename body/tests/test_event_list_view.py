from django.urls import reverse

from body.tests.login_test_case import LoginTestCase
from body.urls.life_events import EVENT_LIST_ROUTE
from freezegun import freeze_time


@freeze_time("2022-03-01")
class EventListViewTests(LoginTestCase):
    def test_title_shown(self):
        """
        A nice simple test: Does the title show?
        """
        response = self.client.get(reverse(EVENT_LIST_ROUTE))
        self.assertContains(response, "My Life")

    def test_empty_state_shown(self):
        """
        Shows the friendly empty state message with no events.
        """
        response = self.client.get(reverse(EVENT_LIST_ROUTE))
        self.assertContains(
            response, "Make Something Great Happen. Add Your First Event Here."
        )
        self.assertQuerysetEqual(response.context["object_list"], [])
