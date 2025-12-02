#!/usr/bin/env python3
"""
Manual Quire OAuth Setup Guide

This script guides you through setting up Quire OAuth authentication manually.
"""
import os
import webbrowser
from pathlib import Path


def main():
    print("\n" + "=" * 80)
    print("  🔧 Quire OAuth Manual Setup Guide")
    print("=" * 80)
    print()
    
    print("📋 Step-by-step instructions to set up Quire API access:\n")
    
    print("STEP 1: Create Quire OAuth App")
    print("─" * 80)
    print("1. Open Quire in your browser (will open automatically)")
    print("2. Try these URLs to find the developer settings:")
    print("   • https://quire.io/apps")
    print("   • https://quire.io/settings/apps")
    print("   • https://quire.io/dev")
    print("   • https://quire.io/settings")
    print("3. Look for 'Developer', 'Apps', 'API', or 'Integrations' section")
    print("4. Create a new application/OAuth app")
    print("5. Set redirect URL to: http://localhost:8080/callback")
    print()
    
    input("Press Enter to open Quire in your browser...")
    
    # Try opening different possible URLs
    urls = [
        "https://quire.io/settings",
        "https://quire.io/apps",
        "https://quire.io/dev",
    ]
    
    for url in urls:
        webbrowser.open(url)
    
    print("\n✅ Browser opened. Please navigate to find the developer/API settings.")
    print()
    
    print("STEP 2: Get OAuth Credentials")
    print("─" * 80)
    print("Once you create the app, you'll receive:")
    print("  • Client ID (long string)")
    print("  • Client Secret (long string)")
    print()
    
    client_id = input("Enter your Client ID: ").strip()
    client_secret = input("Enter your Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("\n❌ Client ID and Secret are required. Please try again.")
        return
    
    # Save to .env
    env_path = Path(__file__).parent.parent / ".env"
    
    with open(env_path, "w") as f:
        f.write(f"QUIRE_CLIENT_ID={client_id}\n")
        f.write(f"QUIRE_CLIENT_SECRET={client_secret}\n")
        f.write(f"QUIRE_REDIRECT_URI=http://localhost:8080/callback\n")
        f.write("# Add QUIRE_REFRESH_TOKEN after running easy_auth.py\n")
    
    print(f"\n✅ Saved to {env_path}")
    print()
    
    print("STEP 3: Get Refresh Token")
    print("─" * 80)
    print("Now run the OAuth flow to get your refresh token:")
    print()
    print("  cd scripts/quire")
    print("  ./venv/bin/python scripts/easy_auth.py")
    print()
    print("This will:")
    print("  1. Start a local server on port 8080")
    print("  2. Open Quire authorization page in browser")
    print("  3. After you approve, automatically get your tokens")
    print("  4. Save refresh token to .env")
    print()
    
    print("STEP 4: Test and Use")
    print("─" * 80)
    print("After authentication, you can use:")
    print()
    print("  # List projects")
    print("  ./venv/bin/python scripts/list_projects.py")
    print()
    print("  # Create tasks from changelogs")
    print("  ./venv/bin/python scripts/create_changelog_tasks.py PROJECT_OID")
    print()
    
    print("=" * 80)
    print("Setup guide complete! Follow the steps above.")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
