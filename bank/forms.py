from django import forms
from decimal import Decimal
from .models import Account

class DepositForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.all())
    amount = forms.DecimalField(decimal_places=2, max_digits=12, min_value=Decimal('0.01'))
    note = forms.CharField(required=False, max_length=255)

class WithdrawForm(DepositForm):
    pass

class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all())
    to_account = forms.ModelChoiceField(queryset=Account.objects.all())
    amount = forms.DecimalField(decimal_places=2, max_digits=12, min_value=Decimal('0.01'))
    note = forms.CharField(required=False,max_length=255)