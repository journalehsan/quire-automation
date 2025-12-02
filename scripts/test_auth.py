#!/usr/bin/env python3
"""
Test Quire authentication flow

This demonstrates how the OAuth2 authentication works step by step.
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quire.auth import QuireAuth


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def test_auth_flow():
    """Test the authentication flow"""
    load_dotenv()
    
    print_section("🔐 Quire OAuth2 Authentication Flow Test")
    
    # Step 1: Check environment variables
    print("Step 1: Checking environment variables...")
    client_id = os.getenv("QUIRE_CLIENT_ID")
    client_secret = os.getenv("QUIRE_CLIENT_SECRET")
    refresh_token = os.getenv("QUIRE_REFRESH_TOKEN")
    
    print(f"  ✓ Client ID: {client_id[:20] + '...' if client_id else '❌ NOT SET'}")
    print(f"  ✓ Client Secret: {client_secret[:20] + '...' if client_secret else '❌ NOT SET'}")
    print(f"  ✓ Refresh Token: {refresh_token[:20] + '...' if refresh_token else '❌ NOT SET'}")
    
    if not client_id or not client_secret:
        print("\n❌ Missing credentials!")
        print("\nTo set up authentication:")
        print("1. Go to https://quire.io/dev/apps")
        print("2. Create a new app")
        print("3. Copy credentials to scripts/quire/.env:")
        print("   QUIRE_CLIENT_ID=your_client_id")
        print("   QUIRE_CLIENT_SECRET=your_client_secret")
        print("4. Run: ./scripts/quire.sh tokens")
        return False
    
    # Step 2: Initialize auth
    print_section("Step 2: Initialize QuireAuth")
    try:
        auth = QuireAuth()
        print("✅ QuireAuth initialized successfully")
        print(f"  - Client ID set: Yes")
        print(f"  - Client Secret set: Yes")
        print(f"  - Refresh Token set: {'Yes' if refresh_token else 'No (will need to get one)'}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Step 3: Show authorization URL (if no refresh token)
    if not refresh_token:
        print_section("Step 3: Get Authorization URL")
        auth_url = auth.get_authorization_url()
        print("To complete OAuth setup, you need an authorization code.")
        print("\n📋 Authorization URL:")
        print(f"  {auth_url}\n")
        print("Steps:")
        print("1. Open the URL above in your browser")
        print("2. Click 'Allow' to authorize the app")
        print("3. Copy the 'code' parameter from the redirect URL")
        print("4. Run: ./scripts/quire.sh tokens")
        print("5. Paste the code when prompted")
        return False
    
    # Step 4: Test token refresh
    print_section("Step 3: Test Token Refresh")
    print("Attempting to refresh access token using refresh token...")
    try:
        token_data = auth.refresh_access_token()
        print("✅ Token refresh successful!")
        print(f"  - Access Token: {auth.access_token[:30]}...")
        print(f"  - Token Type: {token_data.get('token_type', 'bearer')}")
        print(f"  - Expires In: {token_data.get('expires_in', 'N/A')} seconds")
        print(f"  - Token Valid Until: {auth.token_expires_at}")
    except Exception as e:
        print(f"❌ Token refresh failed: {e}")
        print("\nYour refresh token may be expired or invalid.")
        print("Run: ./scripts/quire.sh tokens")
        return False
    
    # Step 5: Test getting valid token
    print_section("Step 4: Test Auto-Refresh Mechanism")
    print("Getting valid access token (auto-refreshes if expired)...")
    try:
        valid_token = auth.get_valid_access_token()
        print("✅ Valid access token retrieved!")
        print(f"  - Token: {valid_token[:30]}...")
        
        # Show auth headers
        headers = auth.get_auth_headers()
        print(f"\n📤 Authorization headers ready:")
        print(f"  {headers}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Step 6: Explain how it's used
    print_section("Step 5: How Authentication Works")
    print("The QuireAuth class handles OAuth2 authentication automatically:\n")
    print("1️⃣  INITIALIZATION")
    print("   - Reads credentials from environment variables")
    print("   - Stores refresh token for later use\n")
    
    print("2️⃣  FIRST-TIME SETUP (get_tokens.py)")
    print("   - User opens authorization URL in browser")
    print("   - Quire redirects with authorization code")
    print("   - Code is exchanged for access + refresh tokens")
    print("   - Refresh token saved to .env\n")
    
    print("3️⃣  AUTOMATIC TOKEN REFRESH")
    print("   - Before each API call, checks if token is expired")
    print("   - If expired, uses refresh token to get new access token")
    print("   - Happens transparently - you don't need to worry about it!\n")
    
    print("4️⃣  API REQUESTS")
    print("   - QuireClient calls auth.get_auth_headers()")
    print("   - Returns: {'Authorization': 'Bearer ACCESS_TOKEN'}")
    print("   - Added to all API requests automatically\n")
    
    print("✅ Authentication test complete!")
    return True


def main():
    success = test_auth_flow()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 Authentication is working correctly!")
        print("\nNext steps:")
        print("  - Test API calls: ./scripts/quire.sh projects")
        print("  - List tasks: ./scripts/quire.sh tasks PROJECT_OID")
        print("  - Update task: ./scripts/quire.sh update TASK_OID --status 10")
    else:
        print("⚠️  Authentication setup incomplete")
        print("\nRun: ./scripts/quire.sh setup")
        print("Then: ./scripts/quire.sh tokens")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
