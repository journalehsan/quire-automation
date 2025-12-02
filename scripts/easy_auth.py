#!/usr/bin/env python3
"""
Easy OAuth - Browser-based authentication with local token cache

This script:
1. Opens browser automatically for OAuth
2. Runs a local server to catch the callback
3. Saves tokens to .env automatically
4. Reuses valid tokens (no re-auth needed)
"""

import os
import sys
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv, set_key
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quire.auth import QuireAuth


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback from Quire"""
    
    authorization_code = None
    
    def log_message(self, format, *args):
        """Suppress server logs"""
        pass
    
    def do_GET(self):
        """Handle the OAuth callback"""
        # Parse the URL
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)
        
        if 'code' in params:
            # Got the authorization code!
            OAuthCallbackHandler.authorization_code = params['code'][0]
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Authentication Successful</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    }
                    .container {
                        background: white;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        text-align: center;
                        max-width: 500px;
                    }
                    .success-icon {
                        font-size: 64px;
                        margin-bottom: 20px;
                    }
                    h1 {
                        color: #333;
                        margin-bottom: 10px;
                    }
                    p {
                        color: #666;
                        line-height: 1.6;
                    }
                    .close-btn {
                        margin-top: 20px;
                        padding: 10px 20px;
                        background: #667eea;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        font-size: 16px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="success-icon">✅</div>
                    <h1>Authentication Successful!</h1>
                    <p>You can now close this window and return to the terminal.</p>
                    <p>Your Quire account has been connected successfully.</p>
                    <button class="close-btn" onclick="window.close()">Close Window</button>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        else:
            # Error in callback
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Error: No authorization code received</h1>")


def get_env_file_path():
    """Get the path to .env file"""
    script_dir = Path(__file__).parent.parent
    return script_dir / '.env'


def save_tokens_to_env(client_id, client_secret, refresh_token):
    """Save tokens to .env file"""
    env_path = get_env_file_path()
    
    # Create .env if it doesn't exist
    if not env_path.exists():
        env_path.touch()
    
    # Update or set values
    set_key(env_path, 'QUIRE_CLIENT_ID', client_id)
    set_key(env_path, 'QUIRE_CLIENT_SECRET', client_secret)
    set_key(env_path, 'QUIRE_REFRESH_TOKEN', refresh_token)
    
    print(f"\n✅ Tokens saved to: {env_path}")


def easy_auth():
    """Easy browser-based authentication"""
    
    print("🔐 Quire Easy Authentication\n")
    print("=" * 80)
    
    # Load existing env
    load_dotenv()
    
    # Step 1: Get or request credentials
    client_id = os.getenv('QUIRE_CLIENT_ID')
    client_secret = os.getenv('QUIRE_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("\n📝 First-time setup required!\n")
        print("Please create a Quire OAuth app:")
        print("1. Go to: https://quire.io/dev/apps")
        print("2. Click 'Create New App'")
        print("3. Set redirect URI to: http://localhost:8080")
        print("4. Copy your credentials:\n")
        
        client_id = input("Enter Client ID: ").strip()
        client_secret = input("Enter Client Secret: ").strip()
        
        if not client_id or not client_secret:
            print("\n❌ Client ID and Secret are required!")
            sys.exit(1)
        
        print("\n✅ Credentials received!")
    else:
        print(f"\n✓ Using existing Client ID: {client_id[:20]}...")
    
    # Step 2: Check if we already have a valid refresh token
    refresh_token = os.getenv('QUIRE_REFRESH_TOKEN')
    
    if refresh_token:
        print("\n🔄 Testing existing refresh token...")
        try:
            auth = QuireAuth(client_id=client_id, client_secret=client_secret, refresh_token=refresh_token)
            token_data = auth.refresh_access_token()
            print("✅ Existing token is valid! No need to re-authenticate.")
            print(f"   Token expires in: {token_data.get('expires_in', 'N/A')} seconds")
            return True
        except Exception as e:
            print(f"⚠️  Existing token invalid: {e}")
            print("   Need to re-authenticate...\n")
    
    # Step 3: Start local server to catch callback
    print("\n🌐 Starting local callback server on http://localhost:8080...")
    
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, OAuthCallbackHandler)
    
    # Step 4: Generate authorization URL and open browser
    redirect_uri = "http://localhost:8080"
    auth_url = f"https://quire.io/oauth?client_id={client_id}&redirect_uri={redirect_uri}"
    
    print(f"\n🚀 Opening browser for authentication...")
    print(f"   If browser doesn't open, visit: {auth_url}\n")
    
    # Open browser
    webbrowser.open(auth_url)
    
    print("⏳ Waiting for you to authorize the app in your browser...")
    print("   (This window is running a local server to catch the response)")
    
    # Wait for callback (timeout after 5 minutes)
    httpd.timeout = 300
    httpd.handle_request()
    
    if not OAuthCallbackHandler.authorization_code:
        print("\n❌ No authorization code received. Did you approve the app?")
        sys.exit(1)
    
    print("\n✅ Authorization code received!")
    
    # Step 5: Exchange code for tokens
    print("\n🔄 Exchanging authorization code for tokens...")
    
    try:
        auth = QuireAuth(client_id=client_id, client_secret=client_secret)
        token_data = auth.exchange_code_for_tokens(OAuthCallbackHandler.authorization_code)
        
        print("✅ Tokens received successfully!")
        
        # Step 6: Save to .env
        print("\n💾 Saving tokens to .env file...")
        save_tokens_to_env(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=token_data['refresh_token']
        )
        
        print("\n" + "=" * 80)
        print("🎉 Authentication complete!")
        print("\nYou can now use Quire commands:")
        print("  ./scripts/quire.sh projects")
        print("  ./scripts/quire.sh tasks PROJECT_OID")
        print("  ./scripts/quire.sh update TASK_OID --status 10")
        print("=" * 80 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error exchanging tokens: {e}")
        sys.exit(1)


def main():
    try:
        easy_auth()
    except KeyboardInterrupt:
        print("\n\n⚠️  Authentication cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
