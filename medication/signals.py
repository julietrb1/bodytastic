from medication.models import LedgerEntry


def ledger_entry_pre_save(sender, **kwargs):
    ledger_entry = kwargs["instance"]
    ledger_entry_created = ledger_entry.pk is None

    if ledger_entry_created:
        quantity_diff = ledger_entry.quantity
    else:
        old_ledger_entry = LedgerEntry.objects.get(pk=ledger_entry.pk)
        quantity_diff = ledger_entry.quantity - old_ledger_entry.quantity

    ledger_entry.medicine.current_balance += quantity_diff
    ledger_entry.medicine.save()


def ledger_entry_post_delete(sender, **kwargs):
    ledger_entry = kwargs["instance"]
    ledger_entry.medicine.current_balance -= ledger_entry.quantity
    ledger_entry.medicine.save()


def consumption_post_save(sender, **kwargs):
    consumption = kwargs["instance"]
    consumption_created = kwargs["created"]

    if consumption_created:
        LedgerEntry.objects.create(
            consumption=consumption,
            medicine=consumption.medicine,
            # Note the negative quantity here
            quantity=-consumption.quantity,
            when=consumption.when,
        )

    # If there's no ledger entry here, one shouldn't be added as this will mess with the medicine balance.
    elif consumption.ledgerentry:
        # Note the negative quantity here
        consumption.ledgerentry.quantity = -consumption.quantity
        consumption.ledgerentry.when = consumption.when
        consumption.ledgerentry.medicine = consumption.medicine
        consumption.ledgerentry.save()
