"""
Decode and inspect a JWT token
"""
import jwt
import json

print("="*80)
print("JWT Token Decoder")
print("="*80)

token = input("\nPaste your JWT token here: ").strip()

# Remove 'Bearer ' prefix if present
if token.startswith('Bearer '):
    token = token[7:]

try:
    # Decode without verification to inspect payload
    decoded = jwt.decode(token, options={"verify_signature": False})
    
    print("\n" + "="*80)
    print("📦 TOKEN PAYLOAD")
    print("="*80)
    print(json.dumps(decoded, indent=2))
    
    print("\n" + "="*80)
    print("👤 USER INFO FROM TOKEN")
    print("="*80)
    print(f"User ID: {decoded.get('userId', 'N/A')}")
    print(f"Username: {decoded.get('username', 'N/A')}")
    print(f"Email: {decoded.get('email', 'N/A')}")
    print(f"Name: {decoded.get('name', 'N/A')}")
    print(f"Role: {decoded.get('role', 'N/A')}")
    
    # Check expiration
    from datetime import datetime
    if 'exp' in decoded:
        exp_timestamp = decoded['exp']
        exp_date = datetime.fromtimestamp(exp_timestamp)
        now = datetime.now()
        
        print(f"\n⏰ Token expires: {exp_date}")
        if exp_date < now:
            print("❌ Token is EXPIRED!")
        else:
            time_left = exp_date - now
            print(f"✓ Token is valid for {time_left}")
    
    print("\n" + "="*80)
    
    # Provide guidance
    role = decoded.get('role', '')
    if role == 'ADMIN':
        print("⚠️  This token is for an ADMIN user!")
        print("To access influencer features, you need to login with an INFLUENCER account.")
    elif role == 'INFLUENCER':
        print("✓ This token is for an INFLUENCER user - it should work!")
    elif role == 'COMPANY':
        print("⚠️  This token is for a COMPANY user!")
    else:
        print(f"⚠️  Unknown role: {role}")
    
except jwt.DecodeError:
    print("\n❌ Invalid JWT token format!")
except Exception as e:
    print(f"\n❌ Error decoding token: {e}")
