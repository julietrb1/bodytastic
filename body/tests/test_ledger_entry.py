from django.db import IntegrityError
from body.tests.login_test_case import LoginTestCase
from django.utils.timezone import datetime, make_aware

from body.tests.model_helpers import (
    create_consumption,
    create_ledger_entry,
    create_medicine,
)
from freezegun import freeze_time


@freeze_time("2022-03-01")
class LedgerEntryTests(LoginTestCase):
    def test_remaining_consumptions_nothing(self):
        """
        Given a refill (10) with no consumptions,
        then 10 consumptions should remain.
        """
        medicine = create_medicine(self.user)
        refill = create_ledger_entry(medicine, 10)
        self.assertEqual(refill.remaining_consumptions, 10)

    def test_remaining_consumptions_two_consumptions(self):
        """
        Given a refill (10) with two consumptions of two each,
        then six consumptions should remain.
        """
        medicine = create_medicine(self.user)
        refill = create_ledger_entry(
            medicine, 10, when=make_aware(datetime(2022, 1, 1, 8))
        )
        create_consumption(
            medicine, quantity=2, when=make_aware(datetime(2022, 1, 1, 8, 1))
        )
        create_consumption(
            medicine, quantity=2, when=make_aware(datetime(2022, 1, 1, 8, 2))
        )
        self.assertEqual(refill.remaining_consumptions, 6)

    def test_remaining_consumptions_one_consumption_before(self):
        """
        Given a refill (10) with one consumption (2) before and one (3) after,
        then seven consumptions should remain as the before shouldn't count.
        """
        medicine = create_medicine(self.user)
        refill = create_ledger_entry(
            medicine, 10, when=make_aware(datetime(2022, 1, 1, 8))
        )
        create_consumption(
            medicine, quantity=2, when=make_aware(datetime(2022, 1, 1, 7))
        )
        create_consumption(
            medicine, quantity=3, when=make_aware(datetime(2022, 1, 1, 9))
        )
        self.assertEqual(refill.remaining_consumptions, 7)

    def test_remaining_consumptions_after_refill_not_counted(self):
        """
        Given a refill (10) with one consumption (2) and another refill (5) with one consumption (4),
        then the first has eight remaining and the second has one remaining.
        """
        medicine = create_medicine(self.user)
        refill_one = create_ledger_entry(
            medicine, 10, when=make_aware(datetime(2022, 1, 1, 8))
        )
        create_consumption(
            medicine, quantity=2, when=make_aware(datetime(2022, 1, 1, 9))
        )
        refill_two = create_ledger_entry(
            medicine, 5, when=make_aware(datetime(2022, 1, 1, 10))
        )
        create_consumption(
            medicine, quantity=4, when=make_aware(datetime(2022, 1, 1, 11))
        )
        self.assertEqual(refill_one.remaining_consumptions, 8)
        self.assertEqual(refill_two.remaining_consumptions, 1)

    def test_remaining_consumptions_two_consecutive_refills(self):
        """
        Given a refill (10) immediately followed by another (5) with one consumption (2),
        then the first should still have 10 remaining and the second should have three.
        """
        medicine = create_medicine(self.user)
        refill_one = create_ledger_entry(
            medicine, 10, when=make_aware(datetime(2022, 1, 1, 8))
        )
        refill_two = create_ledger_entry(
            medicine, 5, when=make_aware(datetime(2022, 1, 1, 9))
        )
        create_consumption(
            medicine, quantity=2, when=make_aware(datetime(2022, 1, 1, 10))
        )
        self.assertEqual(refill_one.remaining_consumptions, 10)
        self.assertEqual(refill_two.remaining_consumptions, 3)

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
