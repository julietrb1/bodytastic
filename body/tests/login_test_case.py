from django.test import Client, TestCase, override_settings
from django.contrib.auth.models import User
from django.urls import reverse


@override_settings(AXES_HANDLER="axes.handlers.dummy.AxesDummyHandler")
class LoginTestCase(TestCase):
    def setUp(self):
        self.client: Client = Client()
        self.user: User = User.objects.create_user(
            "jennifer",
            "jennifer@example.com",
            "jenpassword",
            first_name="Jennifer",
            last_name="Appleseed",
        )
        self.other_user = User.objects.create_user(
            "jane",
            "jane@example.com",
            "janepassword",
            first_name="Jane",
            last_name="Appleseed",
        )
        self.logged_in = self.client.force_login(self.user)

    def verify_redirect(self, route_path, kwargs=None):
        route_path = reverse(route_path, kwargs=kwargs)
        response = self.client.get(route_path)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={route_path}",
            fetch_redirect_response=False,
        )

    def assert_message(self, response, message_content):
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertIn(
            message_content,
            str(messages[0]),
        )
