from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import qrcode
import io
import base64

from .models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    PasswordChangeSerializer,
    TwoFactorEnableSerializer,
    TwoFactorVerifySerializer,
    GDPRConsentSerializer,
)
from .throttling import LoginRateThrottle


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle])
def register(request):
    """Register new user with email verification"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate verification token
        token = user.generate_verification_token()
        
        # Send verification email
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
        send_mail(
            'Verify Your Email',
            f'Click the link to verify your email: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
        
        return Response({
            'message': 'Registration successful. Please check your email to verify your account.',
            'email': user.email,
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request, token):
    """Verify email with token"""
    try:
        user = User.objects.get(verification_token=token)
        if user.verify_email(token):
            return Response({'message': 'Email verified successfully'})
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resend_verification(request):
    """Resend verification email"""
    user = request.user
    
    if user.is_verified:
        return Response({'error': 'Email already verified'}, status=status.HTTP_400_BAD_REQUEST)
    
    token = user.generate_verification_token()
    verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
    
    send_mail(
        'Verify Your Email',
        f'Click the link to verify your email: {verification_url}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    
    return Response({'message': 'Verification email sent'})


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([LoginRateThrottle])
def login(request):
    """Login with email and password (with 2FA support)"""
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    totp_code = serializer.validated_data.get('totp_code')
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check if account is locked
    if user.is_locked():
        return Response({
            'error': f'Account locked until {user.locked_until.strftime("%Y-%m-%d %H:%M")}'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Authenticate user
    user_auth = authenticate(request, email=email, password=password)
    
    if not user_auth:
        user.record_failed_login()
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check email verification
    if not user.is_verified:
        return Response({'error': 'Please verify your email first'}, status=status.HTTP_403_FORBIDDEN)
    
    # Check 2FA
    if user.two_factor_enabled:
        if not totp_code:
            return Response({
                'requires_2fa': True,
                'message': 'Please provide 2FA code'
            }, status=status.HTTP_200_OK)
        
        if not user.verify_totp(totp_code) and not user.verify_backup_code(totp_code):
            user.record_failed_login()
            return Response({'error': 'Invalid 2FA code'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Reset failed login attempts
    user.reset_failed_logins()
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])
    
    # Generate tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'user': UserSerializer(user).data,
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle])
def password_reset_request(request):
    """Request password reset"""
    serializer = PasswordResetRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    
    try:
        user = User.objects.get(email=email)
        token = user.generate_reset_token()
        
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_url}\n\nThis link expires in 1 hour.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        pass  # Don't reveal if email exists
    
    return Response({'message': 'If email exists, password reset link has been sent'})


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request, token):
    """Confirm password reset with token"""
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(reset_token=token)
        
        if not user.verify_reset_token(token):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = serializer.validated_data['new_password']
        
        # Check password reuse
        if user.check_password_reuse(new_password):
            return Response({
                'error': 'Cannot reuse previous passwords'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.add_to_password_history()
        user.reset_password(new_password)
        
        return Response({'message': 'Password reset successful'})
        
    except User.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def password_change(request):
    """Change password for authenticated user"""
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    new_password = serializer.validated_data['new_password']
    
    # Check password reuse
    if user.check_password_reuse(new_password):
        return Response({
            'error': 'Cannot reuse previous passwords'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user.add_to_password_history()
    user.set_password(new_password)
    user.password_changed_at = timezone.now()
    user.save()
    
    return Response({'message': 'Password changed successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enable_two_factor(request):
    """Enable 2FA for user"""
    user = request.user
    
    if user.two_factor_enabled:
        return Response({'error': '2FA already enabled'}, status=status.HTTP_400_BAD_REQUEST)
    
    secret = user.enable_two_factor()
    totp_uri = user.get_totp_uri()
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    
    return Response({
        'secret': secret,
        'qr_code': f'data:image/png;base64,{qr_code}',
        'backup_codes': user.backup_codes,
        'message': 'Scan QR code with authenticator app'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_two_factor(request):
    """Verify and activate 2FA"""
    serializer = TwoFactorVerifySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    code = serializer.validated_data['code']
    
    if user.verify_totp(code):
        return Response({'message': '2FA verified successfully'})
    
    return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disable_two_factor(request):
    """Disable 2FA"""
    user = request.user
    password = request.data.get('password')
    
    if not user.check_password(password):
        return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.disable_two_factor()
    return Response({'message': '2FA disabled successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gdpr_consent(request):
    """Give GDPR consent"""
    serializer = GDPRConsentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    user.give_gdpr_consent()
    
    return Response({'message': 'GDPR consent recorded'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_data(request):
    """Export user's personal data (GDPR)"""
    user = request.user
    data = user.export_personal_data()
    
    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """Delete user account (GDPR right to be forgotten)"""
    user = request.user
    password = request.data.get('password')
    
    if not user.check_password(password):
        return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
    
    email = user.email
    user.delete()
    
    return Response({'message': f'Account {email} deleted successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get user profile"""
    return Response(UserSerializer(request.user).data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def update_profile(request):
    """Update user profile"""
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
