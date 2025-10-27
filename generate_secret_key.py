"""
Generate a new Django SECRET_KEY
Run this script to generate a secure secret key for production
"""

from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print("\n" + "="*70)
    print("🔐 Your new Django SECRET_KEY:")
    print("="*70)
    print(f"\n{secret_key}\n")
    print("="*70)
    print("\n✅ Copy this and add it to your Vercel environment variables")
    print("   as: SECRET_KEY=your-key-here\n")
    print("⚠️  Never commit this key to version control!\n")
