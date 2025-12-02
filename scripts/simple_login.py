#!/usr/bin/env python3
"""
Quire Simple Auth - No OAuth needed!

Uses Quire API with your account credentials directly.
Much simpler than OAuth for personal use.
"""

import sys
import os
import requests
import json
from pathlib import Path

def get_env_file():
    """Get .env file path"""
    return Path(__file__).parent.parent / '.env'

def save_to_env(key, value):
    """Save key-value to .env file"""
    env_file = get_env_file()
    
    # Read existing content
    lines = []
    if env_file.exists():
        lines = env_file.read_text().splitlines()
    
    # Update or add the key
    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            found = True
            break
    
    if not found:
        lines.append(f"{key}={value}")
    
    # Write back
    env_file.write_text('\n'.join(lines) + '\n')

def login_to_quire():
    """Login to Quire and get session token"""
    print("=" * 80)
    print("  🔐 Quire Simple Login")
    print("=" * 80)
    print("\nThis will log you in with your Quire email and password.")
    print("Your credentials are only used to get an API token.")
    print("The token will be saved locally in .env file.\n")
    
    email = input("Quire Email: ").strip()
    
    # Get password securely
    import getpass
    password = getpass.getpass("Quire Password: ")
    
    print("\n🔄 Logging in...")
    
    try:
        # Quire login endpoint
        response = requests.post(
            'https://quire.io/api/user/login',
            json={
                'email': email,
                'password': password
            },
            headers={
                'Content-Type': 'application/json'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract session or token
            # Quire might return a session cookie or bearer token
            session_cookie = response.cookies.get('quire-sid')
            
            if session_cookie:
                print("\n✅ Login successful!")
                print(f"   Session token obtained")
                
                # Save session
                save_to_env('QUIRE_SESSION', session_cookie)
                save_to_env('QUIRE_EMAIL', email)
                
                print(f"\n💾 Credentials saved to: {get_env_file()}")
                
                # Test the session
                print("\n🧪 Testing API access...")
                test_response = requests.get(
                    'https://quire.io/api/user/id/me',
                    cookies={'quire-sid': session_cookie}
                )
                
                if test_response.status_code == 200:
                    user_data = test_response.json()
                    print(f"✅ API access confirmed!")
                    print(f"   Logged in as: {user_data.get('name', email)}")
                    return True
                else:
                    print(f"⚠️  API test returned: {test_response.status_code}")
            else:
                # Try to extract bearer token from response
                if 'token' in data:
                    token = data['token']
                    save_to_env('QUIRE_TOKEN', token)
                    print("\n✅ Login successful!")
                    print(f"   Bearer token obtained")
                    return True
                else:
                    print("\n⚠️  Login succeeded but no token found in response")
                    print(f"Response: {json.dumps(data, indent=2)[:500]}")
                    return False
        else:
            print(f"\n❌ Login failed: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if login_to_quire():
        print("\n" + "=" * 80)
        print("  🎉 Setup Complete!")
        print("=" * 80)
        print("\nNext steps:")
        print("  1. List projects: ./venv/bin/python scripts/list_projects.py")
        print("  2. Set default project: echo 'QUIRE_DEFAULT_PROJECT=PROJECT_OID' >> .env")
        print("  3. Create tasks: ./venv/bin/python scripts/create_changelog_tasks.py")
        print("\n" + "=" * 80)
    else:
        print("\n❌ Setup failed. Please try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
