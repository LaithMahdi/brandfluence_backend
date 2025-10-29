# Quick Reference: Email Verification with Code & Token

## 📧 What Gets Sent in Email

When a user registers, they receive an email with:

1. **6-digit code** (e.g., `847392`) displayed in a large green box
2. **Verification link** button (e.g., `http://localhost:3000/verify-email/token?email=...`)

Both expire in 24 hours. Using either one marks it as used.

---

## 🔑 GraphQL Mutations

### Register (sends email automatically)

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
  }
}
```

### Verify with Code ⭐ NEW

```graphql
mutation {
  verifyEmailWithCode(code: "123456", email: "user@example.com") {
    success
    message
    user {
      id
      emailVerified
    }
  }
}
```

### Verify with Token (link)

```graphql
mutation {
  verifyEmailWithToken(
    token: "550e8400-e29b-41d4-a716-446655440000"
    email: "user@example.com"
  ) {
    success
    message
    user {
      id
      emailVerified
    }
  }
}
```

### Resend Email

```graphql
mutation {
  resendVerificationEmail(email: "user@example.com") {
    success
    message
  }
}
```

---

## 🎨 Frontend Examples

### Code Input Form

```jsx
const [code, setCode] = useState('');
const [verifyEmail] = useMutation(VERIFY_EMAIL_CODE);

<input
  value={code}
  onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
  placeholder="Enter 6-digit code"
  maxLength="6"
/>
<button onClick={() => verifyEmail({ variables: { code, email } })}>
  Verify
</button>
```

### Link Handler (for email clicks)

```jsx
// Route: /verify-email/:token
const { token } = useParams();
const email = useSearchParams().get("email");

useEffect(() => {
  verifyEmailWithToken({ variables: { token, email } });
}, [token, email]);
```

---

## 📊 Database Schema

**VerifyToken Table:**

- `token` - UUID string (for link verification)
- `code` - 6-digit string (for code verification) ⭐ NEW
- `user_id` - FK to User
- `expires_at` - DateTime (24 hours from creation)
- `is_used` - Boolean

---

## ✅ Testing

1. **Register a user** → Check email inbox
2. **Try the code method** → Enter 6 digits on frontend
3. **Try the link method** → Click button in email
4. **Try resending** → Request new code/token
5. **Test expiration** → Wait 24 hours (or modify expires_at)

---

## 🔒 Security

- ✅ 6-digit codes are randomly generated
- ✅ Both methods use same token record (can't use both)
- ✅ Single use - marked as used after verification
- ✅ Time-limited - expires in 24 hours
- ✅ Email-bound - must match registered email

---

## 📝 Files Modified

1. `users/models.py` - Added `code` field to VerifyToken
2. `users/utils.py` - Added `generate_verification_code()` and `verify_email_code()`
3. `users/mutations/user_mutations.py` - Added `VerifyEmailWithCode` mutation
4. `templates/emails/verify_email.html` - Updated to show code prominently
5. `users/migrations/0002_verifytoken.py` - Migration applied ✅

---

## 🚀 What You Need to Do

### Backend: ✅ Done!

- Email sending configured
- Database migrated
- Mutations created

### Frontend: TODO

1. Create code input page (recommended)
2. Create link handler page
3. Update registration flow to redirect to verification
4. Add resend option

---

## 💡 User Flow

```
Registration → Email sent with code + link
              ↓
              User has 2 choices:
              ↓
    ┌─────────┴──────────┐
    ↓                    ↓
Type code          Click link
on frontend        in email
    ↓                    ↓
    └─────────┬──────────┘
              ↓
        Email verified!
              ↓
        Can now login
```

---

## 📞 Support

- Full docs: `EMAIL_VERIFICATION_WITH_CODE.md`
- Original docs: `users/EMAIL_VERIFICATION_README.md`
- Summary: `EMAIL_VERIFICATION_SUMMARY.md`
