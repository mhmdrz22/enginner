from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    
    # Email verification
    path('verify-email/<str:token>/', views.verify_email, name='verify-email'),
    path('resend-verification/', views.resend_verification, name='resend-verification'),
    
    # Password reset
    path('password-reset/', views.password_reset_request, name='password-reset-request'),
    path('password-reset/<str:token>/', views.password_reset_confirm, name='password-reset-confirm'),
    path('password-change/', views.password_change, name='password-change'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update-profile'),
    
    # 2FA
    path('2fa/enable/', views.enable_two_factor, name='2fa-enable'),
    path('2fa/verify/', views.verify_two_factor, name='2fa-verify'),
    path('2fa/disable/', views.disable_two_factor, name='2fa-disable'),
    
    # GDPR
    path('gdpr/consent/', views.gdpr_consent, name='gdpr-consent'),
    path('gdpr/export/', views.export_data, name='gdpr-export'),
    path('gdpr/delete/', views.delete_account, name='gdpr-delete'),
]
