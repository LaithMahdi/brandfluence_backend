# Email Verification Implementation Summary

## What Was Implemented

A complete email verification system for user registration with SMTP integration.

## Files Created/Modified

### 1. Created Files

#### `templates/emails/verify_email.html`

- Beautiful HTML email template
- Green button (#10B981) for verification
- Responsive design
- BrandFluence branding
- Alternative text link for email clients that don't support buttons

#### `users/utils.py`

- `generate_verification_token(user)`: Creates unique verification tokens
- `send_verification_email(user, token)`: Sends verification email via SMTP
- `verify_email_token(token, email)`: Verifies tokens and activates accounts

#### `test_email_verification.py`

- Test script to verify the email system works
- Tests configuration, token generation, and verification

#### `users/EMAIL_VERIFICATION_README.md`

- Complete documentation for the email verification system
- GraphQL mutation examples
- Frontend integration guide
- Troubleshooting tips

### 2. Modified Files

#### `brandfluence/settings.py`

Added email configuration:

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

#### `users/mutations/user_mutations.py`

- Updated `RegisterUser` mutation to send verification email automatically
- Added `VerifyEmailWithToken` mutation for token-based verification
- Added `ResendVerificationEmail` mutation to resend verification emails
- Added password length validation (minimum 8 characters)

#### `users/mutations/__init__.py`

- Exported new mutations: `VerifyEmailWithToken` and `ResendVerificationEmail`

## How It Works

### Registration Flow

1. **User Registers** → `registerUser` mutation

   ```graphql
   mutation {
     registerUser(
       email: "user@example.com"
       password: "password123"
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

2. **System Generates Token** → Unique UUID token created, expires in 24 hours

3. **Email Sent** → Beautiful HTML email with verification link:

   ```
   http://localhost:3000/verify-email/{token}?email={user_email}
   ```

4. **User Clicks Link** → Frontend captures token and email from URL

5. **Frontend Calls Mutation** → `verifyEmailWithToken`

   ```graphql
   mutation {
     verifyEmailWithToken(token: "token-from-url", email: "user@example.com") {
       success
       message
       user {
         id
         emailVerified
       }
     }
   }
   ```

6. **Account Verified** → User can now log in

### Login Protection

The existing `tokenAuth` mutation already checks for email verification:

- If email not verified → Error: "Please verify your email address before logging in."
- If email verified → Login successful

## GraphQL API

### New Mutations

1. **verifyEmailWithToken** - Verify email with token from email link
2. **resendVerificationEmail** - Request new verification email

### Updated Mutations

1. **registerUser** - Now sends verification email automatically

## Email Template Features

- ✓ Professional HTML design
- ✓ BrandFluence branding
- ✓ Green button (#10B981) matching your requirement
- ✓ Hover effects on button
- ✓ Alternative text link
- ✓ Responsive/mobile-friendly
- ✓ Security notice (24-hour expiration)
- ✓ Plain text fallback

## Frontend Integration Required

You need to create a page at `http://localhost:3000/verify-email/:token` that:

1. Extracts token from URL parameter
2. Extracts email from query string (`?email=...`)
3. Calls `verifyEmailWithToken` mutation
4. Shows success/error message
5. Redirects to login on success

See `users/EMAIL_VERIFICATION_README.md` for React example code.

## Security Features

- ✓ Tokens expire after 24 hours
- ✓ Single-use tokens (marked as used after verification)
- ✓ Tokens tied to specific email addresses
- ✓ No email enumeration (resend doesn't reveal if email exists)
- ✓ Secure UUID tokens

## Testing

Run the test script:

```bash
python test_email_verification.py
```

To test actual email sending, edit the script and add your email address.

## Environment Variables (Optional)

You can use environment variables instead of hardcoded values:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=shopy9245@gmail.com
EMAIL_HOST_PASSWORD=abwblmhdxeiznxgt
EMAIL_USE_TLS=True
FRONTEND_URL=http://localhost:3000
```

## Gmail Setup

If using Gmail, you need to:

1. Enable 2-factor authentication
2. Generate an App Password (recommended)
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the app password in `EMAIL_HOST_PASSWORD`

## Database

The `VerifyToken` model already exists in your database (from previous migrations).

Table: `verify_tokens`

- user_id (FK to users)
- token (UUID, unique)
- created_at
- expires_at
- is_used

## What to Test

1. Register a new user → Check email inbox
2. Click verification link → Should redirect to your frontend
3. Try verifying → Should show success
4. Try logging in before verification → Should show error
5. Try logging in after verification → Should succeed
6. Try using same token twice → Should show "already used" error
7. Wait 24 hours → Token should expire

## Next Steps

1. Test the registration flow
2. Implement the frontend verification page
3. Test email delivery
4. Customize email template if needed
5. Set up environment variables for production
6. Use a professional email service for production (SendGrid, AWS SES, etc.)

## Support

For issues or questions, refer to:

- `users/EMAIL_VERIFICATION_README.md` - Full documentation
- `test_email_verification.py` - Test utilities
- GraphQL playground - Test mutations interactively
