from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model (without username)."""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'is_active', 'is_staff', 'is_superuser', 'is_verified',
            'created_date', 'last_login_date'
        )
        read_only_fields = (
            'id', 'is_active', 'is_staff', 'is_superuser',
            'created_date', 'last_login_date'
        )
    
    def get_full_name(self, obj):
        """Return full name of the user."""
        return obj.get_full_name()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration (email-based, no username)."""
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=8,
        label='Confirm Password',
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name',
            'password', 'password2'
        )
        read_only_fields = ('id',)

    def validate_email(self, value):
        """Check that email is unique."""
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'A user with that email already exists.'
            )
        return value.lower()

    def validate(self, data):
        """Check that passwords match."""
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'}
            )
        return data

    def create(self, validated_data):
        """Create a new user with encrypted password."""
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
    
    def update(self, instance, validated_data):
        """Update user profile fields."""
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
