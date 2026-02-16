# Security Features Documentation

## Overview

Comprehensive security implementation with **authentication, authorization, rate limiting, 2FA, and GDPR compliance**.

---

## 1. Email Verification

### Features
- ✅ Email verification required on registration
- ✅ Token-based verification (24-hour expiry)
- ✅ Resend verification email
- ✅ Automatic email sending

### Endpoints

```python
# Register (sends verification email)
POST /api/accounts/register/
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "gdpr_consent": true
}

# Verify email
POST /api/accounts/verify-email/{token}/

# Resend verification
POST /api/accounts/resend-verification/
Authorization: Bearer <token>
```

### Token Expiry
- Verification tokens expire after **24 hours**
- Tokens are single-use
- Secure random generation (`secrets.token_urlsafe`)

---

## 2. Password Reset Flow

### Features
- ✅ Secure token-based reset
- ✅ 1-hour token expiry
- ✅ Email notification
- ✅ Password reuse prevention
- ✅ Failed login reset on successful password change

### Endpoints

```python
# Request password reset
POST /api/accounts/password-reset/
{
  "email": "user@example.com"
}

# Confirm password reset
POST /api/accounts/password-reset/{token}/
{
  "new_password": "NewSecurePass123!",
  "new_password_confirm": "NewSecurePass123!"
}

# Change password (authenticated)
POST /api/accounts/password-change/
Authorization: Bearer <token>
{
  "old_password": "OldPass123!",
  "new_password": "NewPass123!",
  "new_password_confirm": "NewPass123!"
}
```

### Security
- Reset tokens expire after **1 hour**
- Email existence not revealed
- Password history tracking (last 5 passwords)
- Cannot reuse previous passwords

---

## 3. Rate Limiting

### Per-Endpoint Limits

| Endpoint | Anonymous | Authenticated | Notes |
|----------|-----------|---------------|-------|
| **Login** | 5/hour | N/A | IP-based |
| **API (General)** | 100/hour | 1000/hour | User-based |
| **Password Reset** | 3/hour | N/A | IP-based |

### Configuration

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'accounts.throttling.PerUserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'login': '5/hour',
    }
}
```

### Custom Throttling

```python
from accounts.throttling import LoginRateThrottle

@throttle_classes([LoginRateThrottle])
def login(request):
    # Limited to 5 attempts per hour per IP
    pass
```

---

## 4. Two-Factor Authentication (2FA)

### Features
- ✅ TOTP-based (Google Authenticator compatible)
- ✅ QR code generation
- ✅ 10 backup codes
- ✅ Enable/disable with password confirmation

### Endpoints

```python
# Enable 2FA
POST /api/accounts/2fa/enable/
Authorization: Bearer <token>

Response:
{
  "secret": "JBSWY3DPEHPK3PXP",
  "qr_code": "data:image/png;base64,...",
  "backup_codes": ["abc123", "def456", ...],
  "message": "Scan QR code with authenticator app"
}

# Verify 2FA setup
POST /api/accounts/2fa/verify/
Authorization: Bearer <token>
{
  "code": "123456"
}

# Disable 2FA
POST /api/accounts/2fa/disable/
Authorization: Bearer <token>
{
  "password": "YourPassword123!"
}

# Login with 2FA
POST /api/accounts/login/
{
  "email": "user@example.com",
  "password": "Password123!",
  "totp_code": "123456"  # or backup code
}
```

### Implementation

```python
from pyotp import TOTP

# User model
def enable_two_factor(self):
    self.two_factor_secret = pyotp.random_base32()
    self.two_factor_enabled = True
    self.generate_backup_codes()
    return self.two_factor_secret

def verify_totp(self, code):
    totp = TOTP(self.two_factor_secret)
    return totp.verify(code, valid_window=1)
```

---

## 5. Account Lockout

### Features
- ✅ Automatic lockout after 5 failed attempts
- ✅ 30-minute lockout duration
- ✅ Automatic unlock after timeout
- ✅ Manual unlock by admin

### Mechanism

```python
class User(AbstractBaseUser):
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    
    def record_failed_login(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.locked_until = timezone.now() + timedelta(minutes=30)
        self.save()
    
    def is_locked(self):
        if self.locked_until and timezone.now() < self.locked_until:
            return True
        return False
```

### Login Flow

1. Check if account is locked
2. If locked, return `403 Forbidden`
3. Authenticate credentials
4. If successful, reset failed attempts
5. If failed, increment counter

---

## 6. Password Policy

### Requirements

✅ **Minimum 8 characters**  
✅ **At least 1 uppercase letter**  
✅ **At least 1 lowercase letter**  
✅ **At least 1 digit**  
✅ **At least 1 special character** (!@#$%^&*...)  
✅ **Cannot reuse last 5 passwords**  
✅ **Must be different from old password**

### Validation

```python
def validate_password(self, value):
    # Length
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters')
    
    # Complexity
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Must contain uppercase letter')
    
    if not re.search(r'[a-z]', value):
        raise ValidationError('Must contain lowercase letter')
    
    if not re.search(r'[0-9]', value):
        raise ValidationError('Must contain digit')
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError('Must contain special character')
    
    return value
```

### Password History

```python
def check_password_reuse(self, raw_password):
    """Check if password was used in last 5 passwords"""
    for old_hash in self.password_history:
        if check_password(raw_password, old_hash):
            return True
    return False
```

---

## 7. GDPR Compliance

### Features

✅ **Consent Management** - Explicit GDPR consent on registration  
✅ **Data Export** - Export all personal data  
✅ **Right to Be Forgotten** - Delete account and all data  
✅ **Data Processing Consent** - Separate consent tracking  
✅ **Privacy Policy Acceptance** - Timestamped consent

### Endpoints

```python
# Give GDPR consent
POST /api/accounts/gdpr/consent/
Authorization: Bearer <token>
{
  "consent": true
}

# Export personal data
GET /api/accounts/gdpr/export/
Authorization: Bearer <token>

Response:
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_joined": "2026-01-01T00:00:00Z",
  "last_login": "2026-02-16T00:00:00Z",
  "is_verified": true,
  "two_factor_enabled": true,
  "gdpr_consent": true,
  "gdpr_consent_date": "2026-01-01T00:00:00Z"
}

# Delete account (requires password)
DELETE /api/accounts/gdpr/delete/
Authorization: Bearer <token>
{
  "password": "YourPassword123!"
}
```

### Data Model

```python
class User(AbstractBaseUser):
    gdpr_consent = models.BooleanField(default=False)
    gdpr_consent_date = models.DateTimeField(null=True)
    data_processing_consent = models.BooleanField(default=False)
    
    def export_personal_data(self):
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            # ... all personal data
        }
```

---

## Security Headers

### Django Settings

```python
# Session security
SESSION_COOKIE_SECURE = True  # HTTPS only
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# CSRF protection
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS (production)
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## Environment Variables

```bash
# Email configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@taskboard.com

# Frontend URL for email links
FRONTEND_URL=http://localhost:3000

# Redis for rate limiting (optional)
REDIS_URL=redis://localhost:6379/0
```

---

## Testing Security Features

### Email Verification
```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "gdpr_consent": true
  }'
```

### 2FA Setup
```bash
curl -X POST http://localhost:8000/api/accounts/2fa/enable/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Password Reset
```bash
curl -X POST http://localhost:8000/api/accounts/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

---

## Dependencies

```txt
pyotp==2.9.0         # TOTP for 2FA
qrcode[pil]==7.4.2   # QR code generation
redis==5.0.1         # Rate limiting cache
```

---

## Best Practices

1. **Always use HTTPS in production**
2. **Store secrets in environment variables**
3. **Enable 2FA for admin accounts**
4. **Monitor failed login attempts**
5. **Regular security audits**
6. **Keep dependencies updated**
7. **Implement logging for security events**

---

## Compliance Checklist

- [x] Email verification
- [x] Password reset flow
- [x] Rate limiting per user
- [x] 2FA (TOTP)
- [x] Account lockout
- [x] Password policy enforcement
- [x] GDPR consent
- [x] Data export
- [x] Right to be forgotten
- [x] Secure session management
- [x] Security headers
- [x] HTTPS enforcement

---

**All security features implemented and production-ready!** 🔒
