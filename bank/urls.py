from django.urls import path
from . import views

app_name = 'bank'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('transactions/', views.transactions_list, name='transactions'),
]