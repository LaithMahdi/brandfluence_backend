#!/usr/bin/env python
"""
Decode the exact token being used to see what's in it
"""
import jwt

def decode_token():
    """Decode without verification to see payload"""
    
    # The token you just generated
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1haGRpbGFpdGhAZ21haWwuY29tIiwiZXhwIjoxNzYxOTQ3MzQ0LCJvcmlnSWF0IjoxNzYxOTQzNzQ0fQ.wLTg8ZPvCeIHcyK95rrfDITFqeZADAQZNdVebWZbThQ"
    
    try:
        # Decode without verification
        payload = jwt.decode(token, options={"verify_signature": False})
        
        print("=== JWT Token Payload ===")
        for key, value in payload.items():
            print(f"{key}: {value}")
        
        print("\n=== Issue ===")
        print("The JWT payload only contains 'email', 'exp', and 'origIat'")
        print("It does NOT contain the 'role' field!")
        print("\nThe role must be fetched from the database using the email.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    decode_token()
