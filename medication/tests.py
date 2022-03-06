from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse
from medication.models import Medicine, Consumption, Schedule
from django.utils.timezone import datetime, make_aware, timedelta


def create_medicine(user, name="Test meds"):
    return Medicine.objects.create(user=user, name=name)


def create_consumption(
    medicine, when=make_aware(datetime(2022, 1, 1, 14, 25)), quantity=1
):
    return Consumption.objects.create(medicine=medicine, when=when, quantity=quantity)


def create_schedule(
    medicine,
    start_date=None,
    end_date=None,
    frequency_in_days=1,
    time=make_aware(datetime(2022, 1, 1, 14, 25)).time(),
    quantity=1,
    tolerance_mins=30,
):
    start_date = start_date or make_aware(datetime.now() - timedelta(days=1))
    end_date = end_date or make_aware(datetime.now() + timedelta(days=1))

    return Schedule.objects.create(
        medicine=medicine,
        start_date=start_date,
        end_date=end_date,
        frequency_in_days=frequency_in_days,
        time=time,
        quantity=quantity,
        tolerance_mins=tolerance_mins,
    )


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
        self.assertContains(response, "1 Jan 2022")
        self.assertContains(response, "2:25 p.m.")


class ScheduleListViewTests(LoginTestCase):
    def test_with_schedule(self):
        """
        Given that a schedule exists for a medicine, it should be shown in the view.
        """
        medicine = create_medicine(self.user)
        create_schedule(medicine)
        response = self.client.get(
            reverse("medication:medicine-detail", args=[medicine.pk])
        )
        self.assertContains(response, "Every one day")
        self.assertContains(response, "Next:")
        self.assertContains(response, "2:25 p.m.")
