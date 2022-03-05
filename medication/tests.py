from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse
from medication.models import Medicine, Consumption
from django.utils.timezone import datetime, make_aware


def create_medicine(user, name="Test meds"):
    return Medicine.objects.create(user=user, name=name)


def create_consumption(medicine, when=make_aware(datetime(2022, 1, 1)), quantity=1):
    return Consumption.objects.create(medicine=medicine, when=when, quantity=quantity)


@override_settings(AXES_HANDLER="axes.handlers.dummy.AxesDummyHandler")
class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            "john", "lennon@thebeatles.com", "johnpassword"
        )
        self.logged_in = self.client.force_login(self.user)


class MedicineListViewTests(LoginTestCase):
    def test_no_medicines(self):
        """
        If no medicines exist, the empty state is shown.
        """
        response = self.client.get(reverse("medication:medicine-index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Potential for Medicine Is Upon Us.")
        self.assertQuerysetEqual(response.context["object_list"], [])


class MedicineDetailViewTests(LoginTestCase):
    def test_with_consumptions(self):
        """
        Given that a consumption exists for a medicine, it should be shown in the view.
        """
        medicine = create_medicine(self.user)
        create_consumption(medicine)
        response = self.client.get(
            reverse("medication:medicine-detail", args=[medicine.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1 Jan 2022")
