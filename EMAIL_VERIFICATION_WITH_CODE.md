# Email Verification with 6-Digit Code and Token

## Overview

The email verification system now supports **two methods** for verifying email addresses:

1. **6-Digit Code**: Users receive a 6-digit code in their email and can enter it on your frontend
2. **Verification Link**: Users can click a button/link in the email (original method)

Both methods use the same token record and expire after 24 hours.

## What's New

### Email Template

The verification email now displays:

- ✅ A prominent **6-digit verification code** in a green box with large font
- ✅ An "OR" divider
- ✅ The original verification button/link

### New GraphQL Mutation

- `verifyEmailWithCode` - Verify email using the 6-digit code

### Updated Database Model

- `VerifyToken` model now includes a `code` field (6 digits)

## GraphQL Mutations

### 1. Register User (Automatic Email with Code and Token)

```graphql
mutation RegisterUser {
  registerUser(
    email: "user@example.com"
    password: "securepassword123"
    name: "John Doe"
    role: INFLUENCER
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

**Result**: User receives an email with:

- 6-digit code (e.g., `123456`)
- Verification link (e.g., `http://localhost:3000/verify-email/token?email=...`)

---

### 2. Verify Email with Code (NEW!)

```graphql
mutation VerifyEmailWithCode {
  verifyEmailWithCode(code: "123456", email: "user@example.com") {
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
    "verifyEmailWithCode": {
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

**Error Cases:**

- Invalid code format: "Verification code must be exactly 6 digits."
- Wrong code: "Invalid verification code."
- Expired code: "This verification code has expired. Please request a new one."

---

### 3. Verify Email with Token (Original Method)

```graphql
mutation VerifyEmailWithToken {
  verifyEmailWithToken(
    token: "550e8400-e29b-41d4-a716-446655440000"
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

---

### 4. Resend Verification Email

```graphql
mutation ResendVerification {
  resendVerificationEmail(email: "user@example.com") {
    success
    message
  }
}
```

This generates a **new code and token** and sends a new email.

---

## Frontend Integration

### Option 1: Code Entry Form (Recommended)

Create a verification page where users can enter the 6-digit code:

```javascript
import { useState } from "react";
import { useMutation } from "@apollo/client";
import { gql } from "@apollo/client";

const VERIFY_EMAIL_CODE = gql`
  mutation VerifyEmailWithCode($code: String!, $email: String!) {
    verifyEmailWithCode(code: $code, email: $email) {
      success
      message
      user {
        id
        emailVerified
      }
    }
  }
`;

function VerifyEmailCodePage() {
  const [code, setCode] = useState("");
  const email = localStorage.getItem("registeredEmail"); // Store after registration

  const [verifyEmail, { loading, error, data }] = useMutation(
    VERIFY_EMAIL_CODE,
    {
      onCompleted: (data) => {
        if (data.verifyEmailWithCode.success) {
          // Redirect to login
          window.location.href = "/login";
        }
      },
    }
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    verifyEmail({ variables: { code, email } });
  };

  return (
    <div>
      <h2>Verify Your Email</h2>
      <p>Enter the 6-digit code sent to {email}</p>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={code}
          onChange={(e) =>
            setCode(e.target.value.replace(/\D/g, "").slice(0, 6))
          }
          placeholder="123456"
          maxLength="6"
          pattern="\d{6}"
          required
        />
        <button type="submit" disabled={loading || code.length !== 6}>
          {loading ? "Verifying..." : "Verify Email"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error.message}</p>}
      {data && (
        <p style={{ color: "green" }}>{data.verifyEmailWithCode.message}</p>
      )}
    </div>
  );
}
```

### Option 2: Link Verification (Original Method)

Create a page at `/verify-email/:token` for users who click the email link:

```javascript
import { useParams, useSearchParams, useNavigate } from "react-router-dom";
import { useMutation } from "@apollo/client";
import { gql } from "@apollo/client";
import { useEffect } from "react";

const VERIFY_EMAIL_TOKEN = gql`
  mutation VerifyEmailWithToken($token: String!, $email: String!) {
    verifyEmailWithToken(token: $token, email: $email) {
      success
      message
    }
  }
`;

function VerifyEmailTokenPage() {
  const { token } = useParams();
  const [searchParams] = useSearchParams();
  const email = searchParams.get("email");
  const navigate = useNavigate();

  const [verifyEmail, { loading, error, data }] = useMutation(
    VERIFY_EMAIL_TOKEN,
    {
      onCompleted: (data) => {
        if (data.verifyEmailWithToken.success) {
          setTimeout(() => navigate("/login"), 2000);
        }
      },
    }
  );

  useEffect(() => {
    if (token && email) {
      verifyEmail({ variables: { token, email } });
    }
  }, [token, email, verifyEmail]);

  return (
    <div>
      {loading && <p>Verifying your email...</p>}
      {error && <p style={{ color: "red" }}>{error.message}</p>}
      {data && (
        <p style={{ color: "green" }}>{data.verifyEmailWithToken.message}</p>
      )}
    </div>
  );
}
```

### Complete User Flow Example

```javascript
// 1. Registration Page
function RegisterPage() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    name: "",
  });
  const navigate = useNavigate();

  const [register] = useMutation(REGISTER_USER, {
    onCompleted: (data) => {
      if (data.registerUser.success) {
        // Store email for verification page
        localStorage.setItem("registeredEmail", formData.email);
        // Navigate to code verification page
        navigate("/verify-email");
      }
    },
  });

  // ... form implementation
}

// 2. Verification Page with Code Input
function VerifyEmailPage() {
  const email = localStorage.getItem("registeredEmail");
  // ... code input implementation from above
}
```

---

## Email Template

The email now looks like this:

```
🎉 Welcome to BrandFluence!

Hi John Doe,

Thank you for registering with BrandFluence!

To complete your registration, please verify your email using one of the methods below:

┌─────────────────────────────────┐
│  Method 1: Use this verification code  │
│                                 │
│         123456                  │  <- Big green box
│                                 │
│  Enter this code on the verification page │
└─────────────────────────────────┘

───────── OR ─────────

Method 2: Click the button below

[Verify Email Address]  <- Green button

Alternative: Copy and paste this link...
http://localhost:3000/verify-email/token?email=...

Important: This verification will expire in 24 hours.
```

---

## Database Schema

### VerifyToken Model

| Field      | Type           | Description                      |
| ---------- | -------------- | -------------------------------- |
| id         | Integer        | Primary key                      |
| user_id    | ForeignKey     | User who owns this token         |
| token      | CharField(255) | UUID token for link verification |
| code       | CharField(6)   | 6-digit numeric code             |
| created_at | DateTime       | When token was created           |
| expires_at | DateTime       | When token expires (24 hours)    |
| is_used    | Boolean        | Whether token/code has been used |

---

## Security Features

1. **Both methods share the same token record** - Using either the code OR the link marks the token as used
2. **6-digit codes are random** - Generated using secure random number generation
3. **Codes are indexed** - Fast lookup by code in the database
4. **Single use** - Once verified with either method, the token cannot be reused
5. **Time-limited** - Both code and token expire after 24 hours
6. **Email binding** - Code/token only works with the correct email address

---

## Testing

### Test the Code Generation

```python
from users.utils import generate_verification_code

code = generate_verification_code()
print(code)  # Output: 6-digit number like "847392"
```

### Test Complete Flow

```python
from django.contrib.auth import get_user_model
from users.utils import generate_verification_token, send_verification_email

User = get_user_model()
user = User.objects.get(email='test@example.com')

# Generate token with code
verify_token = generate_verification_token(user)
print(f"Token: {verify_token.token}")
print(f"Code: {verify_token.code}")

# Send email (will include both)
send_verification_email(user, verify_token.token, verify_token.code)
```

---

## Migration Applied

The database migration has been created and applied:

- Migration file: `users/migrations/0002_verifytoken.py`
- Creates the `verify_tokens` table with the `code` field

---

## Benefits of Dual Method Approach

1. **User Choice**: Some users prefer typing a code, others prefer clicking links
2. **Mobile Friendly**: Typing 6 digits is easier on mobile than clicking links
3. **Email Client Compatibility**: Some email clients block links but always show text
4. **Accessibility**: Screen readers can easily read out 6-digit codes
5. **Familiarity**: Similar to 2FA codes that users are accustomed to

---

## Troubleshooting

### Code Not Working

- Ensure code is exactly 6 digits
- Check if code has expired (24 hours)
- Verify email address matches
- Check if code was already used

### Both Methods Available

- Yes! Users can use either the code OR the link
- Whichever method is used first will mark the token as used
- The other method will then show "already used" error

### Resending Code

- Use `resendVerificationEmail` mutation
- This generates a NEW code and token
- Old codes become invalid (though they'll expire anyway)

---

## Production Recommendations

1. **Rate Limiting**: Limit resend requests to prevent abuse (e.g., 3 per hour)
2. **SMS Option**: Consider adding SMS verification as a third option
3. **Code Attempts**: Track failed verification attempts and lock after too many tries
4. **Analytics**: Track which verification method users prefer
5. **Professional Email**: Use a service like SendGrid, AWS SES, or Mailgun in production

---

## Summary

Your email verification system now provides:

- ✅ 6-digit verification codes
- ✅ Token-based link verification
- ✅ Both in one email
- ✅ Beautiful email template with green (#10B981) styling
- ✅ 24-hour expiration
- ✅ Single-use security
- ✅ Easy GraphQL API

Users can verify using whichever method they prefer!
