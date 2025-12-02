#!/usr/bin/env python3
"""
Authentication Flow Demo - Shows how Quire OAuth2 works

This demonstrates the authentication process with detailed explanations.
No real credentials needed - just shows the flow.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def print_step(number, title):
    """Print step header"""
    print(f"\n{'─' * 80}")
    print(f"  STEP {number}: {title}")
    print(f"{'─' * 80}\n")


def demo_authentication_flow():
    """Demonstrate the complete OAuth2 flow"""
    
    print_header("🔐 Quire OAuth2 Authentication - How It Works")
    
    print("This demo explains the complete authentication process used by")
    print("the Quire automation library.\n")
    
    # Step 1: Setup
    print_step(1, "Initial Setup - Create Quire OAuth App")
    print("📍 Location: https://quire.io/dev/apps\n")
    print("Actions:")
    print("  1. Click 'Create New App'")
    print("  2. Fill in:")
    print("     - Name: HRMS Automation")
    print("     - Redirect URI: https://localhost")
    print("  3. Get credentials:")
    print("     - Client ID: abc123xyz...")
    print("     - Client Secret: secret456...")
    print("\n💾 Save to: scripts/quire/.env")
    print("     QUIRE_CLIENT_ID=abc123xyz...")
    print("     QUIRE_CLIENT_SECRET=secret456...")
    
    # Step 2: Authorization
    print_step(2, "User Authorization - Get Authorization Code")
    print("🔗 Authorization URL Format:")
    print("   https://quire.io/oauth?client_id=YOUR_CLIENT_ID&redirect_uri=https://localhost")
    print("\n📱 User Flow:")
    print("  1. User opens authorization URL in browser")
    print("  2. Quire shows: 'HRMS Automation wants to access your Quire account'")
    print("  3. User clicks 'Allow'")
    print("  4. Quire redirects to:")
    print("     https://localhost/?code=AUTH_CODE_HERE")
    print("\n📋 You copy the 'code' parameter from the URL")
    
    # Step 3: Token Exchange
    print_step(3, "Token Exchange - Get Access & Refresh Tokens")
    print("📤 POST Request to: https://quire.io/oauth/token")
    print("\nRequest Body:")
    print("  {")
    print("    grant_type: 'authorization_code',")
    print("    code: 'AUTH_CODE_FROM_STEP_2',")
    print("    client_id: 'YOUR_CLIENT_ID',")
    print("    client_secret: 'YOUR_CLIENT_SECRET'")
    print("  }")
    print("\n📥 Response:")
    print("  {")
    print("    access_token: 'eyJ0eXAi...',  // Valid for ~30 days")
    print("    refresh_token: 'def5020...',  // Never expires (use to get new access tokens)")
    print("    token_type: 'bearer',")
    print("    expires_in: 2592000  // 30 days in seconds")
    print("  }")
    print("\n💾 Save refresh_token to .env:")
    print("   QUIRE_REFRESH_TOKEN=def5020...")
    
    # Step 4: Using Tokens
    print_step(4, "Making API Requests - Using Access Token")
    print("📤 Every API request includes the access token:")
    print("\nHTTP Header:")
    print("  Authorization: Bearer eyJ0eXAi...")
    print("\nExample API Call:")
    print("  GET https://quire.io/api/project/list")
    print("  Headers: {")
    print("    'Authorization': 'Bearer ACCESS_TOKEN',")
    print("    'Content-Type': 'application/json'")
    print("  }")
    print("\n✅ Quire validates the token and returns data")
    
    # Step 5: Auto-Refresh
    print_step(5, "Token Refresh - Automatic When Expired")
    print("⏰ When access token expires (after ~30 days):")
    print("\n📤 POST Request to: https://quire.io/oauth/token")
    print("  {")
    print("    grant_type: 'refresh_token',")
    print("    refresh_token: 'YOUR_REFRESH_TOKEN',")
    print("    client_id: 'YOUR_CLIENT_ID',")
    print("    client_secret: 'YOUR_CLIENT_SECRET'")
    print("  }")
    print("\n📥 Response: New access token + new refresh token")
    print("\n🔄 This happens AUTOMATICALLY in QuireAuth.get_valid_access_token()")
    print("   - Checks if token is expired")
    print("   - If yes, refreshes it transparently")
    print("   - You don't need to do anything!")
    
    # Code Implementation
    print_step(6, "Code Implementation - How QuireAuth Works")
    print("Python Code Overview:\n")
    print("class QuireAuth:")
    print("    def __init__(self):")
    print("        # Read credentials from environment")
    print("        self.client_id = os.getenv('QUIRE_CLIENT_ID')")
    print("        self.client_secret = os.getenv('QUIRE_CLIENT_SECRET')")
    print("        self.refresh_token = os.getenv('QUIRE_REFRESH_TOKEN')")
    print("        self.access_token = None")
    print("        self.token_expires_at = None")
    print("")
    print("    def get_valid_access_token(self):")
    print("        # Auto-refresh if expired")
    print("        if not self.access_token or self._is_token_expired():")
    print("            self.refresh_access_token()")
    print("        return self.access_token")
    print("")
    print("    def refresh_access_token(self):")
    print("        # POST to /oauth/token with refresh_token")
    print("        # Update self.access_token and self.token_expires_at")
    print("")
    print("    def get_auth_headers(self):")
    print("        token = self.get_valid_access_token()")
    print("        return {'Authorization': f'Bearer {token}'}")
    
    # Usage Example
    print_step(7, "Usage Example - Complete Flow")
    print("from quire import QuireClient\n")
    print("# Initialize client (reads .env automatically)")
    print("client = QuireClient()")
    print("")
    print("# List projects - auth happens automatically!")
    print("projects = client.list_projects()")
    print("for project in projects:")
    print("    print(f'{project.name} ({project.oid})')")
    print("")
    print("# Update task - token auto-refreshes if needed")
    print("client.update_task('task123', status=10)")
    print("")
    print("# Add comment")
    print("client.add_comment('task123', 'Completed!')")
    print("\n✨ All authentication is handled automatically!")
    
    # Security
    print_step(8, "Security Best Practices")
    print("🔒 Security Features:\n")
    print("  ✅ OAuth2 - Industry standard authentication")
    print("  ✅ Client Secret never exposed to users")
    print("  ✅ Access tokens expire (30 days)")
    print("  ✅ Refresh tokens stored securely in .env")
    print("  ✅ .env file is gitignored (never committed)")
    print("  ✅ Tokens auto-refresh transparently")
    print("\n⚠️  Important:")
    print("  - Never commit .env file to git")
    print("  - Use GitHub Secrets for CI/CD")
    print("  - Rotate tokens if compromised")
    
    # Summary
    print_header("📚 Summary - Complete Authentication Flow")
    print("1️⃣  Create OAuth app on Quire → Get Client ID & Secret")
    print("2️⃣  User authorizes app → Get authorization code")
    print("3️⃣  Exchange code → Get access token + refresh token")
    print("4️⃣  Save refresh token to .env")
    print("5️⃣  Use QuireClient → Automatically handles all auth!")
    print("6️⃣  Tokens auto-refresh when expired")
    print("\n🎯 From your perspective:")
    print("   - One-time setup: Run ./scripts/quire.sh tokens")
    print("   - Then: Just use QuireClient - auth is automatic!")
    print("\n" + "=" * 80 + "\n")


def main():
    demo_authentication_flow()
    
    print("💡 To actually set up authentication:\n")
    print("  1. Create Quire OAuth app: https://quire.io/dev/apps")
    print("  2. Run: ./scripts/quire.sh setup")
    print("  3. Run: ./scripts/quire.sh tokens")
    print("  4. Start using: ./scripts/quire.sh projects\n")


if __name__ == "__main__":
    main()
