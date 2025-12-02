#!/usr/bin/env bash
# Simple Quire authentication setup

echo "=============================================="
echo "  Quire Authentication Setup"
echo "=============================================="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo "Please provide your Quire OAuth credentials:"
echo "(Get these from: https://quire.io/dev/apps)"
echo ""

read -p "Client ID: " CLIENT_ID
read -p "Client Secret: " CLIENT_SECRET

# Save to .env
echo "QUIRE_CLIENT_ID=$CLIENT_ID" > .env
echo "QUIRE_CLIENT_SECRET=$CLIENT_SECRET" >> .env

echo ""
echo "✅ Credentials saved to .env"
echo ""
echo "Now, let's get your authorization code:"
echo ""
echo "1. Open this URL in your browser:"
echo "   https://quire.io/oauth?client_id=$CLIENT_ID&redirect_uri=http://localhost:8080"
echo ""
echo "2. Click 'Allow' to authorize"
echo ""
echo "3. You'll be redirected to: http://localhost:8080/?code=SOMETHING"
echo "   (The page won't load, that's OK!)"
echo ""
echo "4. Copy the 'code' parameter from the URL"
echo ""

read -p "Paste the authorization code here: " AUTH_CODE

echo ""
echo "Getting your refresh token..."

# Exchange code for tokens
RESPONSE=$(curl -s -X POST https://quire.io/oauth/token \
  -d "grant_type=authorization_code" \
  -d "code=$AUTH_CODE" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET")

# Extract refresh token (simple grep, works for most cases)
REFRESH_TOKEN=$(echo $RESPONSE | grep -oP '"refresh_token":"?\K[^",}]+')

if [ -z "$REFRESH_TOKEN" ]; then
    echo "❌ Error getting token. Response:"
    echo $RESPONSE
    exit 1
fi

# Save refresh token
echo "QUIRE_REFRESH_TOKEN=$REFRESH_TOKEN" >> .env

echo ""
echo "=============================================="
echo "  ✅ Authentication Complete!"
echo "=============================================="
echo ""
echo "Your tokens are saved in .env"
echo ""
echo "Next steps:"
echo "  1. List projects: ./venv/bin/python scripts/list_projects.py"
echo "  2. Create tasks: ./venv/bin/python scripts/create_changelog_tasks.py PROJECT_OID"
echo ""
