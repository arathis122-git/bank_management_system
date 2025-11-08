from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def _str_(self):
        return f"{self.user.get_full_name() or self.user.username}"

class Account(models.Model):
    SAVINGS = 'SAV'
    CHECKING = 'CHK'
    ACCOUNT_TYPES = [
        (SAVINGS, 'Savings'),
        (CHECKING, 'Checking'),
    ]
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=3, choices=ACCOUNT_TYPES, default=SAVINGS)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"{self.account_number} - {self.owner}"

class Transaction(models.Model):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'
    TRANSFER = 'TRANSFER'
    TYPES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdraw'),
        (TRANSFER, 'Transfer'),
    ]

    txn_type = models.CharField(max_length=10, choices=TYPES)
    account_from = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='outgoing_transactions', null=True, blank=True)
    account_to = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='incoming_transactions', null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    note = models.CharField(max_length=255, blank=True)

    def _str_(self):
        return f"{self.txn_type} {self.amount} on {self.timestamp}"