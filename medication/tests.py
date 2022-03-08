from django.db import IntegrityError
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse
from medication.models import LedgerEntry, Medicine, Consumption, Schedule
from django.utils.timezone import datetime, make_aware, timedelta


def create_medicine(user, name="Test meds", current_balance=0):
    return Medicine.objects.create(
        user=user, name=name, current_balance=current_balance
    )


def create_ledger_entry(medicine, quantity, when=make_aware(datetime.now())):
    return LedgerEntry.objects.create(medicine=medicine, quantity=quantity, when=when)


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
        medicine = create_medicine(self.user, current_balance=1)
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


class MedicineTests(LoginTestCase):
    def test_ledger_recalculates(self):
        """
        Recalculating the current balance of a medicine correctly uses ledger entries to do so.
        """
        medicine = create_medicine(self.user)
        create_ledger_entry(medicine, 4)
        create_ledger_entry(medicine, -1)
        medicine.recalculate_balance_from_ledger()
        self.assertEqual(medicine.current_balance, 3)


class ConsumptionTests(LoginTestCase):
    def test_new_consumption_adds_ledger_entry(self):
        """
        A new consumption should add to the ledger with same medicine, negative quantity, and date/time.
        """
        self.assertEqual(len(LedgerEntry.objects.all()), 0)
        medicine = create_medicine(self.user, current_balance=2)
        consumption = create_consumption(medicine)
        all_ledger_entries = LedgerEntry.objects.all()
        self.assertEqual(len(all_ledger_entries), 1)
        self.assertEqual(all_ledger_entries[0].when, consumption.when)
        self.assertEqual(all_ledger_entries[0].quantity, -1)
        self.assertEqual(all_ledger_entries[0].medicine, consumption.medicine)

    def test_updating_consumption_matches_ledger_entry(self):
        """
        As with adding new consumptions, changing existing consumptions should update the ledger entries.
        """
        medicine = create_medicine(self.user, current_balance=5)
        consumption = create_consumption(medicine)
        consumption.quantity = 2
        consumption.save()
        all_ledger_entries = LedgerEntry.objects.all()
        self.assertEqual(len(all_ledger_entries), 1)
        self.assertEqual(all_ledger_entries[0].quantity, -2)

    def test_deleting_consumption_removes_ledger_entry(self):
        medicine = create_medicine(self.user, current_balance=1)
        consumption = create_consumption(medicine)
        self.assertEqual(medicine.ledgerentry_set.count(), 1)
        consumption.delete()
        self.assertEqual(medicine.ledgerentry_set.count(), 0)


class LedgerEntryTests(LoginTestCase):
    def test_creating_ledger_entry_changes_balance(self):
        medicine = create_medicine(self.user)
        self.assertEqual(medicine.current_balance, 0)
        create_ledger_entry(medicine, 4)
        self.assertEqual(medicine.current_balance, 4)

    def test_updating_ledger_entry_changes_balance(self):
        medicine = create_medicine(self.user)
        ledger_entry = create_ledger_entry(medicine, 4)
        ledger_entry.quantity = 3
        ledger_entry.save()
        self.assertEqual(medicine.current_balance, 3)

    def test_deleting_ledger_entry_changes_balance(self):
        medicine = create_medicine(self.user)
        ledger_entry = create_ledger_entry(medicine, 4)
        self.assertEqual(medicine.current_balance, 4)
        ledger_entry.delete()
        self.assertEqual(medicine.current_balance, 0)

    def test_negative_balance_raises_exception(self):
        medicine = create_medicine(self.user)
        with self.assertRaises(IntegrityError):
            create_ledger_entry(medicine, -1)
