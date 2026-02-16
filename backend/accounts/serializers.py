from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .security import validate_password_strength, check_password_history, save_password_to_history
from .models import GDPRRequest, LoginAttempt
import pyotp
import qrcode
import io
import base64

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    password_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'email_verified', 'two_factor_enabled', 'date_joined',
            'password_expired', 'gdpr_consent', 'is_staff'
        ]
        read_only_fields = ['id', 'email', 'date_joined', 'email_verified', 'two_factor_enabled']
    
    def get_password_expired(self, obj):
        return obj.is_password_expired()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    gdpr_consent = serializers.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'gdpr_consent']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        
        validate_password_strength(attrs['password'])
        
        if not attrs.get('gdpr_consent'):
            raise serializers.ValidationError({"gdpr_consent": "You must consent to data processing."})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        save_password_to_history(user)
        
        # Generate verification token
        user.generate_verification_token()
        
        return user


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        
        validate_password_strength(attrs['password'])
        
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Passwords don't match."})
        
        user = self.context['request'].user
        
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Incorrect password."})
        
        validate_password_strength(attrs['new_password'], user)
        check_password_history(user, attrs['new_password'])
        
        return attrs


class TwoFactorEnableSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)


class TwoFactorVerifySerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=6)


class TwoFactorDisableSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)


class TwoFactorQRCodeSerializer(serializers.Serializer):
    qr_code = serializers.CharField(read_only=True)
    secret = serializers.CharField(read_only=True)
    backup_codes = serializers.ListField(child=serializers.CharField(), read_only=True)


class GDPRConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['gdpr_consent', 'data_processing_consent']


class GDPRExportRequestSerializer(serializers.Serializer):
    pass


class GDPRDeleteRequestSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    confirmation = serializers.CharField(required=True)
    
    def validate_confirmation(self, value):
        if value != 'DELETE MY ACCOUNT':
            raise serializers.ValidationError('Please type "DELETE MY ACCOUNT" to confirm.')
        return value


class GDPRRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GDPRRequest
        fields = ['id', 'request_type', 'status', 'requested_at', 'completed_at']
        read_only_fields = ['id', 'status', 'requested_at', 'completed_at']


class LoginAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginAttempt
        fields = ['email', 'ip_address', 'success', 'timestamp', 'failure_reason']
        read_only_fields = fields
