from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse

LIST_ROUTE_NAME = "life_events:event-index"


@override_settings(AXES_HANDLER="axes.handlers.dummy.AxesDummyHandler")
class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            "john", "lennon@thebeatles.com", "johnpassword"
        )
        self.logged_in = self.client.force_login(self.user)


class EventListViewTests(LoginTestCase):
    def test_title_shown(self):
        """
        A nice simple test: Does the title show?
        """
        response = self.client.get(reverse(LIST_ROUTE_NAME))
        self.assertContains(response, "My Life")

    def test_empty_state_shown(self):
        """
        Shows the friendly empty state message with no events.
        """
        response = self.client.get(reverse(LIST_ROUTE_NAME))
        self.assertContains(
            response, "Make Something Great Happen. Add Your First Event Here."
        )
        self.assertQuerysetEqual(response.context["object_list"], [])
