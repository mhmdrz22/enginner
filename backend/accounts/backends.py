from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with their email
    address instead of username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user with email and password.
        
        Args:
            request: The HTTP request object
            username: Email address (used as username parameter for compatibility)
            password: User password
            **kwargs: Additional keyword arguments
        
        Returns:
            User object if authentication successful, None otherwise
        """
        if username is None or password is None:
            return None
        
        try:
            # Try to fetch the user by email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user
            User().set_password(password)
            return None
        
        # Check password and return user if valid
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None

    def get_user(self, user_id):
        """
        Get user by ID.
        
        Args:
            user_id: Primary key of the user
        
        Returns:
            User object if found, None otherwise
        """
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
        return user if self.user_can_authenticate(user) else None
