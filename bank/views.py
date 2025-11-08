from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from .forms import DepositForm, WithdrawForm, TransferForm
from .models import Account, Transaction
from .services import deposit, withdraw, transfer
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    customer = request.user.customer_profile
    accounts = customer.accounts.all()
    return render(request, 'bank/dashboard.html', {'accounts': accounts})

@login_required
def deposit_view(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            amount = Decimal(form.cleaned_data['amount'])
            note = form.cleaned_data['note']
            try:
                deposit(account, amount, note)
                messages.success(request, 'Deposit successful.')
                return redirect('bank:dashboard')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = DepositForm()
    return render(request, 'bank/deposit.html', {'form': form})

@login_required
def withdraw_view(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            amount = Decimal(form.cleaned_data['amount'])
            note = form.cleaned_data['note']
            try:
                withdraw(account, amount, note)
                messages.success(request, 'Withdrawal successful.')
                return redirect('bank:dashboard')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = WithdrawForm()
    return render(request, 'bank/withdraw.html', {'form': form})

@login_required
def transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            a_from = form.cleaned_data['from_account']
            a_to = form.cleaned_data['to_account']
            amount = Decimal(form.cleaned_data['amount'])
            note = form.cleaned_data['note']
            try:
                transfer(a_from, a_to, amount, note)
                messages.success(request, 'Transfer successful.')
                return redirect('bank:dashboard')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = TransferForm()
    return render(request, 'bank/transfer.html', {'form': form})

@login_required
def transactions_list(request):
    customer = request.user.customer_profile
    accounts = customer.accounts.all()
    txns = Transaction.objects.filter(
        account_from__in=accounts
    ) | Transaction.objects.filter(account_to__in=accounts)
    txns = txns.order_by('-timestamp')
    return render(request, 'bank/transactions.html', {'transactions': txns})