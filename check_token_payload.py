#!/usr/bin/env python
"""
Decode the exact token being used to see what's in it
"""
import jwt

def decode_token():
    """Decode without verification to see payload"""
    
    # The token you just generated
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImtvcmViNjk2MDJAZ2FtaW50b3IuY29tIiwiZXhwIjoxNzY2NTE5NzM0LCJvcmlnSWF0IjoxNzY2NTE2MTM0LCJuYW1lIjoiZG9ycmEgemFycm91ayIsInJvbGUiOiJJTkZMVUVOQ0VSIiwidXNlcklkIjozNX0.G3Erfn1p3iL7qI5aZftsg-qRoYtN0tfjCRQ2My_lQCA "
    
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
