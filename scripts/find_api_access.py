#!/usr/bin/env python3
"""
Quire API Access - Check available authentication methods
"""
import webbrowser
import time

print("=" * 80)
print("  🔍 Checking Quire API Access Options")
print("=" * 80)
print()

print("Let's try to find where you can get API credentials...")
print()

# Try different possible URLs
urls = [
    ("Personal Access Tokens", "https://quire.io/settings/tokens"),
    ("Account Settings", "https://quire.io/settings"),
    ("Developer Apps (Organization)", "https://quire.io/apps"),
    ("API Documentation", "https://quire.io/dev/api"),
]

print("Opening different Quire settings pages to find API access...")
print("Look for: 'Personal Access Token', 'API Token', or 'Developer Apps'")
print()

for i, (name, url) in enumerate(urls, 1):
    print(f"{i}. Opening: {name}")
    print(f"   URL: {url}")
    webbrowser.open(url)
    print()
    
    if i < len(urls):
        input("   Press Enter to open next page...")
        print()

print("=" * 80)
print("📋 What to look for:")
print("=" * 80)
print()
print("Option 1: Personal Access Token")
print("  - Look for a 'Tokens', 'API', or 'Developer' section in settings")
print("  - Create a new token")
print("  - Copy the token value")
print()
print("Option 2: OAuth App")
print("  - In Developer Apps, click 'Create new app'")
print("  - Select 'MTNIrancell' organization")
print("  - Get Client ID and Client Secret")
print()
print("Option 3: Use Quire's App Directory")
print("  - Some accounts can only use pre-approved apps")
print("  - In this case, we'll need to use CSV export/import")
print()
print("=" * 80)

answer = input("\nDid you find any API credentials option? (yes/no): ").strip().lower()

if answer == 'yes':
    print("\n🎉 Great! What did you find?")
    print("1. Personal Access Token")
    print("2. OAuth App (Client ID/Secret)")
    print("3. Other")
    
    choice = input("\nEnter number (1-3): ").strip()
    
    if choice == "1":
        print("\n✅ Perfect! Enter your Personal Access Token:")
        token = input("Token: ").strip()
        
        # Save to .env
        with open('.env', 'w') as f:
            f.write(f'QUIRE_PERSONAL_TOKEN={token}\n')
        
        print("\n✅ Token saved to .env!")
        print("\nTest it with:")
        print("  ./venv/bin/python scripts/list_projects.py")
        
    elif choice == "2":
        print("\n✅ Perfect! Enter your OAuth credentials:")
        client_id = input("Client ID: ").strip()
        client_secret = input("Client Secret: ").strip()
        
        with open('.env', 'w') as f:
            f.write(f'QUIRE_CLIENT_ID={client_id}\n')
            f.write(f'QUIRE_CLIENT_SECRET={client_secret}\n')
            f.write('QUIRE_REDIRECT_URI=http://localhost:8080/callback\n')
        
        print("\n✅ Credentials saved!")
        print("\nNow run the authorization:")
        print("  ./venv/bin/python scripts/easy_auth.py")
else:
    print("\n🤔 No worries! Let's try an alternative approach...")
    print("\nWe can create tasks using CSV export/import:")
    print("1. Generate CSV from changelogs")
    print("2. Import to Quire manually")
    print("\nWould you like me to generate the CSV file? (yes/no)")
    
    csv_choice = input().strip().lower()
    if csv_choice == 'yes':
        print("\n✅ I'll create a CSV export script for you!")
        print("Coming up next...")

print("\n" + "=" * 80)
