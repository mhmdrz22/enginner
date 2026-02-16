import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


# Common passwords to blacklist
COMMON_PASSWORDS = [
    'password', 'password123', '12345678', 'qwerty', 'abc123',
    'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
    'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
    'bailey', 'passw0rd', 'shadow', '123123', '654321',
    'superman', 'qazwsx', 'michael', 'football', 'welcome',
]


class PasswordPolicyValidator:
    """Validate password against security policy"""
    
    def __init__(self, min_length=8, require_uppercase=True,
                 require_lowercase=True, require_digit=True,
                 require_special=True):
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special
    
    def validate(self, password, user=None):
        errors = []
        
        # Minimum length
        if len(password) < self.min_length:
            errors.append(
                _(f'Password must be at least {self.min_length} characters long.')
            )
        
        # Uppercase letter
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append(_('Password must contain at least one uppercase letter.'))
        
        # Lowercase letter
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append(_('Password must contain at least one lowercase letter.'))
        
        # Digit
        if self.require_digit and not re.search(r'\d', password):
            errors.append(_('Password must contain at least one digit.'))
        
        # Special character
        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append(_('Password must contain at least one special character.'))
        
        # Check against common passwords
        if password.lower() in COMMON_PASSWORDS:
            errors.append(_('This password is too common. Please choose a stronger password.'))
        
        # Check if contains user info (if user provided)
        if user:
            user_info = [
                user.email.split('@')[0].lower(),
                user.first_name.lower(),
                user.last_name.lower(),
            ]
            for info in user_info:
                if info and len(info) > 2 and info in password.lower():
                    errors.append(_('Password cannot contain your personal information.'))
                    break
        
        # Check password history
        if user and hasattr(user, 'is_password_in_history'):
            if user.is_password_in_history(password):
                errors.append(_('You cannot reuse a recent password.'))
        
        if errors:
            raise ValidationError(errors)
    
    def get_help_text(self):
        requirements = []
        if self.min_length:
            requirements.append(f'at least {self.min_length} characters')
        if self.require_uppercase:
            requirements.append('one uppercase letter')
        if self.require_lowercase:
            requirements.append('one lowercase letter')
        if self.require_digit:
            requirements.append('one digit')
        if self.require_special:
            requirements.append('one special character')
        
        return _('Your password must contain ') + ', '.join(requirements) + '.'


def calculate_password_strength(password):
    """Calculate password strength (0-100)"""
    score = 0
    
    # Length bonus
    score += min(len(password) * 4, 40)
    
    # Character diversity
    if re.search(r'[a-z]', password):
        score += 10
    if re.search(r'[A-Z]', password):
        score += 10
    if re.search(r'\d', password):
        score += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 15
    
    # Penalty for common patterns
    if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
        score -= 10
    if re.search(r'(abc|bcd|cde|def)', password, re.IGNORECASE):
        score -= 10
    if password.lower() in COMMON_PASSWORDS:
        score -= 30
    
    # Unique characters bonus
    unique_chars = len(set(password))
    score += min(unique_chars * 2, 15)
    
    return max(0, min(score, 100))
