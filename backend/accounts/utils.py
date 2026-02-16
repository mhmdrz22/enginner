from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import qrcode
import io
import base64


def send_verification_email(user, token):
    """Send email verification link"""
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    
    context = {
        'user': user,
        'verification_url': verification_url,
    }
    
    html_message = render_to_string('emails/verify_email.html', context)
    plain_message = f"""Hello {user.first_name},
    
    Please verify your email by clicking the link below:
    {verification_url}
    
    This link will expire in 24 hours.
    
    If you didn't create an account, please ignore this email.
    
    Best regards,
    TaskBoard Team
    """
    
    send_mail(
        subject='Verify your email - TaskBoard',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_password_reset_email(user, token):
    """Send password reset link"""
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    
    context = {
        'user': user,
        'reset_url': reset_url,
    }
    
    html_message = render_to_string('emails/reset_password.html', context)
    plain_message = f"""Hello {user.first_name},
    
    You requested to reset your password. Click the link below:
    {reset_url}
    
    This link will expire in 1 hour.
    
    If you didn't request a password reset, please ignore this email.
    
    Best regards,
    TaskBoard Team
    """
    
    send_mail(
        subject='Reset your password - TaskBoard',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_account_locked_email(user):
    """Notify user about account lockout"""
    context = {'user': user}
    
    html_message = render_to_string('emails/account_locked.html', context)
    plain_message = f"""Hello {user.first_name},
    
    Your account has been temporarily locked due to multiple failed login attempts.
    
    Your account will be automatically unlocked in 30 minutes.
    
    If this wasn't you, please reset your password immediately.
    
    Best regards,
    TaskBoard Team
    """
    
    send_mail(
        subject='Account Locked - TaskBoard',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def generate_qr_code(data):
    """Generate QR code for 2FA setup"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_user_activity(user, action, details=None, request=None):
    """Log user activity for GDPR compliance"""
    from .models import UserActivity
    
    UserActivity.objects.create(
        user=user,
        action=action,
        details=details or {},
        ip_address=get_client_ip(request) if request else None,
    )
