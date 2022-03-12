from body.exceptions import ExcessiveConsumptionQuantityError
from body.models import LedgerEntry
from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_consumption, create_medicine
from freezegun import freeze_time
from django.utils.timezone import datetime, make_aware


@freeze_time(make_aware(datetime(2022, 1, 1)))
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

    def test_creating_consumption_exceeds_balance(self):
        medicine = create_medicine(self.user, current_balance=0)
        with self.assertRaises(ExcessiveConsumptionQuantityError):
            create_consumption(medicine)

    def test_is_today(self):
        medicine = create_medicine(self.user, current_balance=1)
        consumption = create_consumption(medicine)
        self.assertTrue(consumption.is_today())

        with freeze_time(make_aware(datetime(2021, 12, 31))):
            self.assertFalse(consumption.is_today())

        with freeze_time(make_aware(datetime(2022, 1, 2))):
            self.assertFalse(consumption.is_today())
