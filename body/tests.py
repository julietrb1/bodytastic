from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from django.test import override_settings


@override_settings(AXES_HANDLER="axes.handlers.dummy.AxesDummyHandler")
class ReportListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            "john", "lennon@thebeatles.com", "johnpassword"
        )
        self.logged_in = self.client.force_login(self.user)

    def test_no_reports(self):
        """
        If no reports exist, the empty state is shown.
        """
        response = self.client.get(reverse("body:report-index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Reports Here, But there could be...")
        self.assertQuerysetEqual(response.context["object_list"], [])
