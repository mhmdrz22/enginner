from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    AdminOverviewView,
    AdminNotifyView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Admin endpoints
    path('admin/overview/', AdminOverviewView.as_view(), name='admin-overview'),
    path('admin/notify/', AdminNotifyView.as_view(), name='admin-notify'),
]
