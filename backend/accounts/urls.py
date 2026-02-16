from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    # Email Verification
    path('verify-email/', views.verify_email, name='verify-email'),
    path('resend-verification/', views.resend_verification, name='resend-verification'),
    
    # Password Management
    path('password-reset/request/', views.password_reset_request, name='password-reset-request'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password-reset-confirm'),
    path('change-password/', views.change_password, name='change-password'),
    
    # 2FA
    path('2fa/enable/', views.enable_2fa, name='2fa-enable'),
    path('2fa/disable/', views.disable_2fa, name='2fa-disable'),
    path('2fa/verify/', views.verify_2fa, name='2fa-verify'),
    path('2fa/qr-code/', views.get_2fa_qr_code, name='2fa-qr-code'),
    
    # GDPR
    path('gdpr/consent/', views.update_gdpr_consent, name='gdpr-consent'),
    path('gdpr/export/', views.request_data_export, name='gdpr-export'),
    path('gdpr/delete/', views.request_account_deletion, name='gdpr-delete'),
    
    # Security
    path('login-history/', views.get_login_history, name='login-history'),
]
