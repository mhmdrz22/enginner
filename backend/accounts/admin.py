from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PasswordHistory, LoginAttempt, GDPRRequest


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'email_verified', 'two_factor_enabled', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'email_verified', 'two_factor_enabled', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Email Verification', {'fields': ('email_verified', 'email_verification_token', 'email_verification_sent_at')}),
        ('Security', {
            'fields': ('failed_login_attempts', 'locked_until', 'password_changed_at', 'password_expiry_days'),
        }),
        ('Two-Factor Auth', {'fields': ('two_factor_enabled', 'two_factor_secret', 'backup_codes')}),
        ('GDPR', {'fields': ('gdpr_consent', 'gdpr_consent_date', 'data_processing_consent')}),
        ('Important Dates', {'fields': ('date_joined',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'gdpr_consent'),
        }),
    )
    
    readonly_fields = ['date_joined', 'email_verification_sent_at', 'password_changed_at', 'gdpr_consent_date']
    
    actions = ['unlock_accounts', 'verify_emails', 'disable_2fa']
    
    def unlock_accounts(self, request, queryset):
        for user in queryset:
            user.reset_failed_login()
        self.message_user(request, f'{queryset.count()} accounts unlocked.')
    unlock_accounts.short_description = 'Unlock selected accounts'
    
    def verify_emails(self, request, queryset):
        queryset.update(email_verified=True, email_verification_token=None)
        self.message_user(request, f'{queryset.count()} emails verified.')
    verify_emails.short_description = 'Verify emails'
    
    def disable_2fa(self, request, queryset):
        for user in queryset:
            user.disable_two_factor()
        self.message_user(request, f'2FA disabled for {queryset.count()} users.')
    disable_2fa.short_description = 'Disable 2FA'


@admin.register(PasswordHistory)
class PasswordHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email']
    readonly_fields = ['user', 'password_hash', 'created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ['email', 'ip_address', 'success', 'timestamp', 'failure_reason']
    list_filter = ['success', 'timestamp']
    search_fields = ['email', 'ip_address']
    readonly_fields = ['email', 'ip_address', 'user_agent', 'success', 'timestamp', 'failure_reason']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(GDPRRequest)
class GDPRRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'request_type', 'status', 'requested_at', 'completed_at']
    list_filter = ['request_type', 'status', 'requested_at']
    search_fields = ['user__email']
    readonly_fields = ['user', 'request_type', 'requested_at']
    date_hierarchy = 'requested_at'
    
    actions = ['mark_completed', 'mark_failed']
    
    def mark_completed(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'{queryset.count()} requests marked as completed.')
    mark_completed.short_description = 'Mark as completed'
    
    def mark_failed(self, request, queryset):
        queryset.update(status='failed')
        self.message_user(request, f'{queryset.count()} requests marked as failed.')
    mark_failed.short_description = 'Mark as failed'
