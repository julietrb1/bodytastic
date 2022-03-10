from body.tests.login_test_case import LoginTestCase
from body.tests.model_helpers import create_ledger_entry, create_medicine


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
