from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse


@override_settings(AXES_HANDLER="axes.handlers.dummy.AxesDummyHandler")
class MedicineListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            "john", "lennon@thebeatles.com", "johnpassword"
        )
        self.logged_in = self.client.force_login(self.user)

    def test_no_medicines(self):
        """
        If no medicines exist, the empty state is shown.
        """
        response = self.client.get(reverse("medication:medicine-index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Potential for Medicine Is Upon Us.")
        self.assertQuerysetEqual(response.context["object_list"], [])
