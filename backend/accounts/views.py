from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from .serializers import (
    UserSerializer, RegisterSerializer, EmailVerificationSerializer,
    ResendVerificationSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer, ChangePasswordSerializer,
    TwoFactorEnableSerializer, TwoFactorVerifySerializer, TwoFactorDisableSerializer,
    TwoFactorQRCodeSerializer, GDPRConsentSerializer, GDPRExportRequestSerializer,
    GDPRDeleteRequestSerializer, GDPRRequestSerializer, LoginAttemptSerializer
)
from .models import GDPRRequest, LoginAttempt
from .security import (
    LoginRateThrottle, PasswordResetRateThrottle, UserRateThrottle,
    save_password_to_history, email_verified_required
)
from .emails import (
    send_verification_email, send_password_reset_email,
    send_password_changed_email, send_2fa_enabled_email, send_account_locked_email
)
import json
import qrcode
import io
import base64
from datetime import timedelta

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    throttle_classes = [LoginRateThrottle]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send verification email
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={user.email_verification_token}"
        send_verification_email(user, verification_url)
        
        return Response({
            'detail': 'Registration successful. Please check your email to verify your account.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([LoginRateThrottle])
def verify_email(request):
    """Verify email with token."""
    serializer = EmailVerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    token = serializer.validated_data['token']
    
    try:
        user = User.objects.get(email_verification_token=token)
        if user.verify_email(token):
            return Response({'detail': 'Email verified successfully.'})
        else:
            return Response(
                {'detail': 'Invalid or expired token.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except User.DoesNotExist:
        return Response(
            {'detail': 'Invalid token.'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([PasswordResetRateThrottle])
def resend_verification(request):
    """Resend verification email."""
    serializer = ResendVerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data['email']
    
    try:
        user = User.objects.get(email=email)
        
        if user.email_verified:
            return Response({'detail': 'Email already verified.'})
        
        # Generate new token
        user.generate_verification_token()
        
        # Send email
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={user.email_verification_token}"
        send_verification_email(user, verification_url)
        
        return Response({'detail': 'Verification email sent.'})
    except User.DoesNotExist:
        # Don't reveal if email exists
        return Response({'detail': 'If the email exists, a verification email will be sent.'})


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([PasswordResetRateThrottle])
def password_reset_request(request):
    """Request password reset."""
    serializer = PasswordResetRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data['email']
    
    try:
        user = User.objects.get(email=email)
        
        # Generate reset token
        token = user.generate_password_reset_token()
        
        # Send email
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        send_password_reset_email(user, reset_url)
        
        return Response({'detail': 'Password reset email sent.'})
    except User.DoesNotExist:
        # Don't reveal if email exists
        return Response({'detail': 'If the email exists, a password reset email will be sent.'})


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([PasswordResetRateThrottle])
def password_reset_confirm(request):
    """Confirm password reset."""
    serializer = PasswordResetConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    token = serializer.validated_data['token']
    password = serializer.validated_data['password']
    
    try:
        user = User.objects.get(password_reset_token=token)
        
        if user.reset_password(token, password):
            save_password_to_history(user)
            send_password_changed_email(user)
            
            return Response({'detail': 'Password reset successful.'})
        else:
            return Response(
                {'detail': 'Invalid or expired token.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except User.DoesNotExist:
        return Response(
            {'detail': 'Invalid token.'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def change_password(request):
    """Change password for authenticated user."""
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    user.set_password(serializer.validated_data['new_password'])
    user.password_changed_at = timezone.now()
    user.save()
    
    save_password_to_history(user)
    send_password_changed_email(user)
    
    return Response({'detail': 'Password changed successfully.'})


# 2FA Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enable_2fa(request):
    """Enable 2FA for user."""
    serializer = TwoFactorEnableSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    
    # Verify password
    if not user.check_password(serializer.validated_data['password']):
        return Response(
            {'detail': 'Incorrect password.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Enable 2FA
    secret = user.enable_two_factor()
    
    # Generate QR code
    totp_uri = user.get_totp_uri()
    qr = qrcode.make(totp_uri)
    buffer = io.BytesIO()
    qr.save(buffer, format='PNG')
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    
    send_2fa_enabled_email(user)
    
    return Response({
        'detail': '2FA enabled successfully.',
        'secret': secret,
        'qr_code': f'data:image/png;base64,{qr_code}',
        'backup_codes': user.backup_codes
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disable_2fa(request):
    """Disable 2FA for user."""
    serializer = TwoFactorDisableSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    
    if not user.check_password(serializer.validated_data['password']):
        return Response(
            {'detail': 'Incorrect password.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.disable_two_factor()
    
    return Response({'detail': '2FA disabled successfully.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_2fa(request):
    """Verify 2FA code."""
    serializer = TwoFactorVerifySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    code = serializer.validated_data['code']
    
    # Try TOTP first
    if user.verify_totp(code):
        request.session['2fa_verified'] = True
        return Response({'detail': '2FA verified successfully.'})
    
    # Try backup code
    if user.verify_backup_code(code):
        request.session['2fa_verified'] = True
        return Response({
            'detail': '2FA verified with backup code.',
            'remaining_backup_codes': len(user.backup_codes)
        })
    
    return Response(
        {'detail': 'Invalid 2FA code.'},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_2fa_qr_code(request):
    """Get QR code for 2FA setup."""
    user = request.user
    
    if not user.two_factor_enabled or not user.two_factor_secret:
        return Response(
            {'detail': '2FA not enabled.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    totp_uri = user.get_totp_uri()
    qr = qrcode.make(totp_uri)
    buffer = io.BytesIO()
    qr.save(buffer, format='PNG')
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    
    return Response({
        'qr_code': f'data:image/png;base64,{qr_code}',
        'secret': user.two_factor_secret,
        'backup_codes': user.backup_codes
    })


# GDPR Views
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_gdpr_consent(request):
    """Update GDPR consent."""
    serializer = GDPRConsentSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.save()
    if user.gdpr_consent:
        user.gdpr_consent_date = timezone.now()
        user.save()
    
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_data_export(request):
    """Request GDPR data export."""
    user = request.user
    
    # Create GDPR request
    gdpr_request = GDPRRequest.objects.create(
        user=user,
        request_type='export',
        status='pending'
    )
    
    # Export data (simplified - in production, use Celery task)
    user_data = {
        'profile': UserSerializer(user).data,
        'tasks': list(user.tasks.values()),
        'login_history': list(user.login_attempts.values()[:100]),
        'gdpr_requests': list(user.gdpr_requests.values()),
    }
    
    # In production, save to file and send download link
    return Response({
        'detail': 'Data export request created.',
        'request_id': gdpr_request.id,
        'data': user_data  # In production, send email with download link
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_account_deletion(request):
    """Request account deletion (GDPR right to be forgotten)."""
    serializer = GDPRDeleteRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    
    # Verify password
    if not user.check_password(serializer.validated_data['password']):
        return Response(
            {'detail': 'Incorrect password.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create GDPR request
    gdpr_request = GDPRRequest.objects.create(
        user=user,
        request_type='delete',
        status='pending'
    )
    
    # In production, process deletion after grace period (e.g., 30 days)
    # For now, just create the request
    
    return Response({
        'detail': 'Account deletion request created. Your account will be deleted in 30 days.',
        'request_id': gdpr_request.id
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_login_history(request):
    """Get login attempt history."""
    user = request.user
    attempts = LoginAttempt.objects.filter(email=user.email)[:50]
    serializer = LoginAttemptSerializer(attempts, many=True)
    return Response(serializer.data)


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
