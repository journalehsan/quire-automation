#!/usr/bin/env python3
"""
OAuth flow helper to get initial refresh token
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import quire package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quire.auth import QuireAuth


def main():
    load_dotenv()
    
    print("🔐 Quire OAuth Token Generator\n")
    print("=" * 50)
    
    # Initialize auth (will read from env)
    try:
        auth = QuireAuth()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have set:")
        print("  QUIRE_CLIENT_ID")
        print("  QUIRE_CLIENT_SECRET")
        print("\nin your .env file or environment variables.")
        sys.exit(1)
    
    # Step 1: Get authorization URL
    auth_url = auth.get_authorization_url()
    
    print("\n📋 Step 1: Authorize the app")
    print("-" * 50)
    print("Open this URL in your browser:\n")
    print(f"  {auth_url}\n")
    print("After you click 'Allow', you'll be redirected to:")
    print("  https://localhost/?code=AUTHORIZATION_CODE\n")
    print("Copy the code from the URL.")
    print("-" * 50)
    
    # Step 2: Get the code from user
    code = input("\n📥 Paste the authorization code here: ").strip()
    
    if not code:
        print("❌ No code provided. Exiting.")
        sys.exit(1)
    
    # Step 3: Exchange code for tokens
    print("\n🔄 Exchanging code for tokens...")
    
    try:
        tokens = auth.exchange_code_for_tokens(code)
        
        print("\n✅ Success! Tokens received:\n")
        print("=" * 50)
        print(f"Access Token:  {tokens['access_token'][:30]}...")
        print(f"Refresh Token: {tokens['refresh_token'][:30]}...")
        print(f"Expires In:    {tokens['expires_in']} seconds")
        print("=" * 50)
        
        print("\n📝 Add this to your .env file:\n")
        print(f"QUIRE_REFRESH_TOKEN={tokens['refresh_token']}")
        print("\n✨ You're all set! The refresh token will be used to automatically")
        print("   get new access tokens whenever needed.\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the authorization code is correct and hasn't expired.")
        print("Authorization codes are single-use and expire quickly.")
        sys.exit(1)


if __name__ == "__main__":
    main()
