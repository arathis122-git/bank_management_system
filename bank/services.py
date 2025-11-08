from django.db import transaction
from decimal import Decimal
from .models import Account, Transaction
from django.core.exceptions import ValidationError

def deposit(account: Account, amount: Decimal, note: str = '') -> Transaction:
    if amount <= 0:
        raise ValidationError("Amount must be positive.")
    with transaction.atomic():
        # lock row for update
        acc = Account.objects.select_for_update().get(pk=account.pk)
        acc.balance = acc.balance + amount
        acc.save()
        txn = Transaction.objects.create(
            txn_type=Transaction.DEPOSIT,
            account_to=acc,
            amount=amount,
            note=note
        )
    return txn

def withdraw(account: Account, amount: Decimal, note: str = '') -> Transaction:
    if amount <= 0:
        raise ValidationError("Amount must be positive.")
    with transaction.atomic():
        acc = Account.objects.select_for_update().get(pk=account.pk)
        if acc.balance < amount:
            raise ValidationError("Insufficient funds.")
        acc.balance = acc.balance - amount
        acc.save()
        txn = Transaction.objects.create(
            txn_type=Transaction.WITHDRAW,
            account_from=acc,
            amount=amount,
            note=note
        )
    return txn

def transfer(account_from: Account, account_to: Account, amount: Decimal, note: str = '') -> Transaction:
    if amount <= 0:
        raise ValidationError("Amount must be positive.")
    if account_from.pk == account_to.pk:
        raise ValidationError("Cannot transfer to same account.")
    with transaction.atomic():
        a_from = Account.objects.select_for_update().get(pk=account_from.pk)
        a_to = Account.objects.select_for_update().get(pk=account_to.pk)
        if a_from.balance < amount:
            raise ValidationError("Insufficient funds.")
        a_from.balance -= amount
        a_to.balance += amount
        a_from.save()
        a_to.save()
        txn = Transaction.objects.create(
            txn_type=Transaction.TRANSFER,
            account_from=a_from,
            account_to=a_to,
            amount=amount,
            note=note
        )
    return txn