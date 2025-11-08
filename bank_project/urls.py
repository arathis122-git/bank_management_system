from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bank/', include('bank.urls', namespace='bank')),
    path('', RedirectView.as_view(pattern_name='bank:dashboard', permanent=False)),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
]