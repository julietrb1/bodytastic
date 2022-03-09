from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import override_settings
from django.utils.html import escape

LIST_ROUTE_NAME = "home:index"


@override_settings(AXES_HANDLER="axes.handlers.dummy.AxesDummyHandler")
class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            "john", "lennon@thebeatles.com", "johnpassword"
        )
        self.logged_in = self.client.force_login(self.user)


class HomeViewTests(LoginTestCase):
    def test_title_shown(self):
        """
        A nice simple test: Does the title show?
        """
        response = self.client.get(reverse(LIST_ROUTE_NAME))
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
