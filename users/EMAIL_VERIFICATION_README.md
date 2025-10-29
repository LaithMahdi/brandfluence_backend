# Email Verification System

This document describes the email verification system implemented for user registration.

## Overview

When a user registers, they receive a verification email with a link to verify their email address. The user must verify their email before they can log in.

## Features

1. **Automatic Email Sending**: When a user registers, an email with a verification link is automatically sent
2. **Beautiful Email Template**: HTML email template with BrandFluence branding and a green (#10B981) button
3. **Token-based Verification**: Secure token-based verification with 24-hour expiration
4. **Resend Verification**: Users can request a new verification email if needed
5. **Security**: Tokens are single-use and expire after 24 hours

## Configuration

### Email Settings (in `settings.py`)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'shopy9245@gmail.com'
EMAIL_HOST_PASSWORD = 'abwblmhdxeiznxgt'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'shopy9245@gmail.com'
FRONTEND_URL = 'http://localhost:3000'
```

### Environment Variables

You can override these settings using environment variables:

- `EMAIL_HOST`: SMTP server (default: smtp.gmail.com)
- `EMAIL_PORT`: SMTP port (default: 587)
- `EMAIL_HOST_USER`: Email address to send from
- `EMAIL_HOST_PASSWORD`: Email password or app password
- `EMAIL_USE_TLS`: Use TLS (default: True)
- `FRONTEND_URL`: Frontend URL for verification links (default: http://localhost:3000)

## GraphQL Mutations

### 1. Register User (with automatic email)

```graphql
mutation RegisterUser {
  registerUser(
    email: "user@example.com"
    password: "securepassword123"
    name: "John Doe"
    role: INFLUENCER
    phoneNumber: "+1234567890"
  ) {
    success
    message
    user {
      id
      email
      name
      emailVerified
    }
  }
}
```

**Response:**

```json
{
  "data": {
    "registerUser": {
      "success": true,
      "message": "User registered successfully! Please check your email to verify your account.",
      "user": {
        "id": "1",
        "email": "user@example.com",
        "name": "John Doe",
        "emailVerified": false
      }
    }
  }
}
```

### 2. Verify Email with Token

This mutation is called from the frontend when the user clicks the verification link.

```graphql
mutation VerifyEmail {
  verifyEmailWithToken(
    token: "abc123-token-from-email"
    email: "user@example.com"
  ) {
    success
    message
    user {
      id
      email
      emailVerified
    }
  }
}
```

**Response:**

```json
{
  "data": {
    "verifyEmailWithToken": {
      "success": true,
      "message": "Email verified successfully! You can now log in.",
      "user": {
        "id": "1",
        "email": "user@example.com",
        "emailVerified": true
      }
    }
  }
}
```

### 3. Resend Verification Email

```graphql
mutation ResendVerification {
  resendVerificationEmail(email: "user@example.com") {
    success
    message
  }
}
```

**Response:**

```json
{
  "data": {
    "resendVerificationEmail": {
      "success": true,
      "message": "Verification email sent successfully! Please check your inbox."
    }
  }
}
```

## Frontend Integration

### Verification Link Format

The verification link sent in the email follows this format:

```
http://localhost:3000/verify-email/{token}?email={user_email}
```

Example:

```
http://localhost:3000/verify-email/550e8400-e29b-41d4-a716-446655440000?email=user@example.com
```

### Frontend Implementation

On your frontend (`http://localhost:3000`), create a page at `/verify-email/:token` that:

1. Extracts the token from the URL parameter
2. Extracts the email from the query string
3. Calls the `verifyEmailWithToken` mutation
4. Shows success or error message
5. Redirects to login page on success

**Example React Code:**

```javascript
import { useParams, useSearchParams, useNavigate } from "react-router-dom";
import { useMutation } from "@apollo/client";
import { gql } from "@apollo/client";

const VERIFY_EMAIL = gql`
  mutation VerifyEmail($token: String!, $email: String!) {
    verifyEmailWithToken(token: $token, email: $email) {
      success
      message
      user {
        id
        email
        emailVerified
      }
    }
  }
`;

function VerifyEmailPage() {
  const { token } = useParams();
  const [searchParams] = useSearchParams();
  const email = searchParams.get("email");
  const navigate = useNavigate();

  const [verifyEmail, { loading, error, data }] = useMutation(VERIFY_EMAIL, {
    variables: { token, email },
    onCompleted: (data) => {
      if (data.verifyEmailWithToken.success) {
        // Show success message
        setTimeout(() => navigate("/login"), 3000);
      }
    },
  });

  useEffect(() => {
    if (token && email) {
      verifyEmail();
    }
  }, [token, email]);

  return (
    <div>
      {loading && <p>Verifying your email...</p>}
      {error && <p>Error: {error.message}</p>}
      {data && <p>{data.verifyEmailWithToken.message}</p>}
    </div>
  );
}
```

## Email Template

The email template is located at `templates/emails/verify_email.html` and features:

- Clean, responsive design
- BrandFluence branding
- Green verification button (#10B981)
- Alternative link for users whose email clients don't support buttons
- Professional styling with hover effects
- Mobile-friendly layout

## Security Features

1. **Token Expiration**: Tokens expire after 24 hours
2. **Single Use**: Tokens can only be used once
3. **Email Binding**: Tokens are tied to specific email addresses
4. **No Email Enumeration**: The resend function doesn't reveal if an email exists

## Login Requirements

The login mutation has been updated to check for email verification:

```graphql
mutation Login {
  tokenAuth(email: "user@example.com", password: "password123") {
    token
    refreshToken
    user {
      id
      email
      emailVerified
    }
  }
}
```

**Error Response (if email not verified):**

```json
{
  "errors": [
    {
      "message": "Please verify your email address before logging in."
    }
  ]
}
```

## Database Models

### User Model

- `email_verified`: Boolean field indicating if email is verified
- `verified_at`: Timestamp when email was verified

### VerifyToken Model

- `user`: Foreign key to User
- `token`: Unique token string (UUID)
- `created_at`: Timestamp when token was created
- `expires_at`: Timestamp when token expires
- `is_used`: Boolean indicating if token has been used

## Troubleshooting

### Email Not Sending

1. Check Gmail settings:

   - Enable "Less secure app access" OR use App Password (recommended)
   - Make sure 2-factor authentication is enabled if using App Password

2. Check the logs for error messages

3. Test email configuration:

```python
from django.core.mail import send_mail
send_mail('Test', 'Test message', 'shopy9245@gmail.com', ['recipient@example.com'])
```

### Token Expired

Users can request a new verification email using the `resendVerificationEmail` mutation.

### Token Not Found

Make sure the user is using the exact link from the email and hasn't modified it.

## Admin Verification

Admins can still manually verify users using the `verifyEmail` mutation (original mutation that doesn't require a token).

## Future Enhancements

1. Add email template customization
2. Add multiple email template options
3. Implement email verification reminders
4. Add verification statistics to admin panel
5. Support for email template internationalization
