from django.db import IntegrityError
from body.tests.login_test_case import LoginTestCase

from body.tests.model_helpers import create_ledger_entry, create_medicine
from freezegun import freeze_time


@freeze_time("2022-03-01")
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
