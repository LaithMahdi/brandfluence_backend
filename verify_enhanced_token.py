#!/usr/bin/env python
"""
Decode the new enhanced token
"""
import jwt

def decode_new_token():
    """Decode the new token with enhanced payload"""
    
    # The new token with custom payload
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1haGRpbGFpdGhAZ21haWwuY29tIiwiZXhwIjoxNzYxOTQ3NTY2LCJvcmlnSWF0IjoxNzYxOTQzOTY2LCJuYW1lIjoiTGFpdGggTWFoZGkiLCJyb2xlIjoiSU5GTFVFTkNFUiIsInVzZXJJZCI6MX0.09IkzaLdP3TyE_yzBwG3Va0n8TDUevCQNezItINjwfY"
    
    try:
        # Decode without verification
        payload = jwt.decode(token, options={"verify_signature": False})
        
        print("=" * 70)
        print("🎉 NEW JWT TOKEN PAYLOAD WITH CUSTOM FIELDS")
        print("=" * 70)
        for key, value in payload.items():
            print(f"  {key}: {value}")
        
        print("\n" + "=" * 70)
        print("✅ Token now includes: email, name, role, and userId")
        print("=" * 70)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    decode_new_token()
