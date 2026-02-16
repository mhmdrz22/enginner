from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .validators import PasswordPolicyValidator, calculate_password_strength

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[PasswordPolicyValidator()]
    )
    password_confirm = serializers.CharField(write_only=True)
    privacy_policy_accepted = serializers.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'first_name', 'last_name',
            'privacy_policy_accepted', 'data_processing_consent', 'marketing_consent'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({"password": "Passwords don't match."})
        
        if not attrs.get('privacy_policy_accepted'):
            raise serializers.ValidationError(
                {"privacy_policy_accepted": "You must accept the privacy policy."}
            )
        
        return attrs
    
    def create(self, validated_data):
        from django.utils import timezone
        validated_data['privacy_policy_accepted_at'] = timezone.now()
        user = User.objects.create_user(**validated_data)
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        validators=[PasswordPolicyValidator()]
    )
    password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()


class TwoFactorSetupSerializer(serializers.Serializer):
    pass


class TwoFactorVerifySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=6, min_length=6)


class TwoFactorDisableSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)


class GDPRDataExportSerializer(serializers.Serializer):
    pass


class GDPRDataDeletionSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm = serializers.BooleanField()
    
    def validate_confirm(self, value):
        if not value:
            raise serializers.ValidationError(
                "You must confirm account deletion."
            )
        return value


class PasswordStrengthSerializer(serializers.Serializer):
    password = serializers.CharField()
    
    def validate(self, attrs):
        password = attrs['password']
        strength = calculate_password_strength(password)
        
        return {
            'strength': strength,
            'level': self._get_strength_level(strength),
            'feedback': self._get_feedback(strength)
        }
    
    def _get_strength_level(self, strength):
        if strength < 30:
            return 'weak'
        elif strength < 60:
            return 'medium'
        elif strength < 80:
            return 'strong'
        else:
            return 'very_strong'
    
    def _get_feedback(self, strength):
        if strength < 30:
            return 'Your password is weak. Consider adding more characters and variety.'
        elif strength < 60:
            return 'Your password is acceptable but could be stronger.'
        elif strength < 80:
            return 'Your password is strong!'
        else:
            return 'Excellent! Your password is very strong.'
