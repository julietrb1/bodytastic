from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse


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
        response = self.client.get(reverse("life_events:event-index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Life")
