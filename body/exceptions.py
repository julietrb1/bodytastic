class ExcessiveConsumptionQuantityError(Exception):
    def __init__(self, medicine_name, current_balance, subtraction_amount):
        super().__init__(
            f"Insufficient {medicine_name} balance ({current_balance}) for consumption cost ({subtraction_amount})."
        )
