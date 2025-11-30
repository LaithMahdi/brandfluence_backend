"""
Quick test script to check token cleanup functionality
"""
from django.utils import timezone
from users.models import VerifyToken, PasswordResetToken

# Get current time
now = timezone.now()

# Count all tokens
total_verify = VerifyToken.objects.count()
total_reset = PasswordResetToken.objects.count()

# Count expired tokens
expired_verify = VerifyToken.objects.filter(expires_at__lt=now).count()
expired_reset = PasswordResetToken.objects.filter(expires_at__lt=now).count()

# Count used tokens
used_verify = VerifyToken.objects.filter(is_used=True).count()
used_reset = PasswordResetToken.objects.filter(is_used=True).count()

# Display statistics
print("=" * 60)
print("TOKEN STATISTICS")
print("=" * 60)
print(f"\nVerification Tokens:")
print(f"  Total: {total_verify}")
print(f"  Expired: {expired_verify}")
print(f"  Used: {used_verify}")
print(f"  Active (valid): {total_verify - expired_verify}")

print(f"\nPassword Reset Tokens:")
print(f"  Total: {total_reset}")
print(f"  Expired: {expired_reset}")
print(f"  Used: {used_reset}")
print(f"  Active (valid): {total_reset - expired_reset}")

print(f"\nTokens that would be deleted by cleanup:")
print(f"  {expired_verify + expired_reset} total expired tokens")
print("=" * 60)
