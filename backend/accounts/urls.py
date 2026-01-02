from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    AdminOverviewView,
    AdminNotifyView,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('admin/overview/', AdminOverviewView.as_view(), name='admin-overview'),
    path('admin/notify/', AdminNotifyView.as_view(), name='admin-notify'),
]
