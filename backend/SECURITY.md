# Security Features Documentation

Comprehensive security implementation for TaskBoard application.

## Table of Contents

1. [Email Verification](#email-verification)
2. [Password Reset Flow](#password-reset-flow)
3. [Rate Limiting](#rate-limiting)
4. [Two-Factor Authentication (2FA)](#two-factor-authentication-2fa)
5. [Account Lockout](#account-lockout)
6. [Password Policy](#password-policy)
7. [GDPR Compliance](#gdpr-compliance)
8. [Configuration](#configuration)
9. [Testing](#testing)
10. [Deployment Checklist](#deployment-checklist)

---

## Email Verification

### Features
- Secure token generation (32-byte URL-safe)
- Token expiration (24 hours)
- Verification status tracking
- Resend verification capability

### API Endpoints

```
POST /api/accounts/register/
- Registers user and sends verification email
- Returns: User data + verification sent message

POST /api/accounts/verify-email/
Body: {"token": "verification_token"}
- Verifies email with token
- Returns: Success or error message

POST /api/accounts/resend-verification/
Body: {"email": "user@example.com"}
- Resends verification email
- Rate limited: 3/hour
```

### Usage Example

```python
# Register user
response = requests.post('/api/accounts/register/', {
    'email': 'user@example.com',
    'password': 'SecurePass123!',
    'password2': 'SecurePass123!',
    'first_name': 'John',
    'last_name': 'Doe',
    'gdpr_consent': True
})

# User receives email with verification link
# Click link or call API:
response = requests.post('/api/accounts/verify-email/', {
    'token': 'received_token'
})
```

---

## Password Reset Flow

### Features
- Secure token generation
- Token expiration (1 hour)
- Email notification
- Rate limiting (3 requests/hour)

### API Endpoints

```
POST /api/accounts/password-reset/request/
Body: {"email": "user@example.com"}
- Sends password reset email
- Rate limited: 3/hour

POST /api/accounts/password-reset/confirm/
Body: {
    "token": "reset_token",
    "password": "NewSecurePass123!",
    "password2": "NewSecurePass123!"
}
- Resets password with token
- Validates password policy
- Checks password history
```

### Flow

1. User requests password reset
2. System sends email with reset link
3. User clicks link (valid for 1 hour)
4. User enters new password
5. System validates password policy
6. System checks password history (last 5)
7. Password updated, notification sent

---

## Rate Limiting

### Implementation

**Redis-based throttling** for all sensitive endpoints.

### Rate Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| Login | 5 attempts | 1 hour |
| Password Reset | 3 requests | 1 hour |
| Email Verification | 3 requests | 1 hour |
| General API (Auth) | 1000 requests | 1 hour |
| General API (Anon) | 100 requests | 1 hour |

### Configuration

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'login': '5/hour',
        'password_reset': '3/hour',
    },
}
```

### Custom Rate Limiting

```python
from accounts.security import rate_limit

@rate_limit('custom_action', limit=10, period=3600)
def my_view(request):
    # Only 10 requests per hour
    pass
```

---

## Two-Factor Authentication (2FA)

### Features
- TOTP-based (RFC 6238)
- Google Authenticator compatible
- QR code generation
- 10 backup codes
- Optional per user

### API Endpoints

```
POST /api/accounts/2fa/enable/
Body: {"password": "current_password"}
- Enables 2FA
- Returns: QR code, secret, backup codes

POST /api/accounts/2fa/disable/
Body: {"password": "current_password"}
- Disables 2FA

POST /api/accounts/2fa/verify/
Body: {"code": "123456"}
- Verifies 2FA code
- Accepts TOTP or backup code

GET /api/accounts/2fa/qr-code/
- Gets QR code and backup codes
```

### Setup Flow

1. User enables 2FA with password
2. System generates secret and backup codes
3. User scans QR code with authenticator app
4. User verifies with first code
5. User saves backup codes securely

### Login with 2FA

1. User enters email + password
2. System verifies credentials
3. System prompts for 2FA code
4. User enters TOTP code
5. System verifies code
6. Session marked as 2FA verified

---

## Account Lockout

### Features
- Automatic lockout after failed attempts
- Configurable threshold (default: 5)
- Timed lockout (default: 30 minutes)
- Email notification
- Admin unlock capability

### Configuration

```python
# settings.py
ACCOUNT_LOCKOUT_ATTEMPTS = 5
ACCOUNT_LOCKOUT_DURATION = 30  # minutes
```

### Behavior

- **Failed attempts tracked** per user
- **Lockout triggered** at threshold
- **Auto-unlock** after duration
- **Manual unlock** by admin
- **Counter reset** on successful login

### Model Methods

```python
user.is_locked()  # Check if locked
user.increment_failed_login()  # Increment counter
user.reset_failed_login()  # Reset counter
```

---

## Password Policy

### Requirements

✅ **Minimum 8 characters**  
✅ **At least one uppercase letter**  
✅ **At least one lowercase letter**  
✅ **At least one digit**  
✅ **At least one special character** (!@#$%^&*...)

### Additional Features

- **Password history**: Cannot reuse last 5 passwords
- **Password expiry**: 90 days (configurable)
- **Complexity validation**: Django's built-in validators
- **Common password check**: Prevents common passwords

### Configuration

```python
# settings.py
PASSWORD_HISTORY_COUNT = 5
PASSWORD_EXPIRY_DAYS = 90

AUTH_PASSWORD_VALIDATORS = [
    # ... Django's default validators
    {
        'NAME': 'accounts.security.PasswordPolicyValidator',
    },
]
```

### Usage

```python
from accounts.security import validate_password_strength, check_password_history

# Validate new password
validate_password_strength(password, user)

# Check against history
check_password_history(user, password)
```

---

## GDPR Compliance

### Features Implemented

✅ **Data Export** (Right to Access)  
✅ **Account Deletion** (Right to be Forgotten)  
✅ **Consent Tracking**  
✅ **Data Processing Records**  
✅ **Privacy Settings**

### API Endpoints

```
PATCH /api/accounts/gdpr/consent/
Body: {
    "gdpr_consent": true,
    "data_processing_consent": true
}
- Updates consent preferences

POST /api/accounts/gdpr/export/
- Requests data export
- Returns: All user data in JSON

POST /api/accounts/gdpr/delete/
Body: {
    "password": "current_password",
    "confirmation": "DELETE MY ACCOUNT"
}
- Requests account deletion
- 30-day grace period
```

### Data Export Format

```json
{
  "profile": {
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2026-01-01T00:00:00Z"
  },
  "tasks": [...],
  "login_history": [...],
  "gdpr_requests": [...]
}
```

### Deletion Process

1. User requests deletion
2. System verifies password
3. 30-day grace period begins
4. Email notifications sent
5. After grace period:
   - User data anonymized or deleted
   - Tasks transferred or deleted
   - Account marked as deleted

---

## Configuration

### Environment Variables

```bash
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@taskboard.com

# Frontend URL
FRONTEND_URL=https://taskboard.com

# Redis
REDIS_URL=redis://localhost:6379/1

# Security
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

### Django Settings

```python
# Import security settings
from .settings_security import *

# Add apps
INSTALLED_APPS = [
    # ...
    'django_redis',
]

# Add middleware
MIDDLEWARE = [
    # ...
    'django.middleware.security.SecurityMiddleware',
]
```

---

## Testing

### Run Security Tests

```bash
# All security tests
pytest accounts/tests/test_security.py -v

# Specific features
pytest accounts/tests/test_email_verification.py
pytest accounts/tests/test_password_reset.py
pytest accounts/tests/test_2fa.py
pytest accounts/tests/test_rate_limiting.py
pytest accounts/tests/test_account_lockout.py
pytest accounts/tests/test_password_policy.py
pytest accounts/tests/test_gdpr.py
```

### Coverage

```bash
pytest --cov=accounts --cov-report=html
```

---

## Deployment Checklist

### Before Production

- [ ] **Configure Redis** for rate limiting
- [ ] **Set up email service** (SMTP/SendGrid/SES)
- [ ] **Enable HTTPS** (SSL/TLS)
- [ ] **Set secure cookies** (SECURE=True)
- [ ] **Configure CORS** properly
- [ ] **Set strong SECRET_KEY**
- [ ] **Enable HSTS** headers
- [ ] **Test all security features**
- [ ] **Review rate limits**
- [ ] **Configure monitoring** (Sentry)
- [ ] **Set up backups**
- [ ] **Document emergency procedures**

### Environment-Specific

**Development:**
```
DEBUG=True
SECURE_SSL_REDIRECT=False
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**Production:**
```
DEBUG=False
SECURE_SSL_REDIRECT=True
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
SECURE_HSTS_SECONDS=31536000
```

---

## Security Best Practices

1. **Never commit secrets** to git
2. **Use environment variables** for sensitive data
3. **Keep dependencies updated**
4. **Monitor failed login attempts**
5. **Regular security audits**
6. **Implement logging** for security events
7. **Use HTTPS** in production
8. **Regular backups**
9. **Incident response plan**
10. **Security training** for team

---

## Support

For security issues, contact: security@taskboard.com

**Do not** publicly disclose security vulnerabilities.
