#!/usr/bin/env bash
# Simple Quire setup using Personal Access Token (easier than OAuth)

echo "=============================================="
echo "  Quire Setup - Personal Access Token"
echo "=============================================="
echo ""
echo "Quire OAuth apps might require organization admin access."
echo "Instead, let's use a Personal Access Token (simpler!):"
echo ""
echo "Steps:"
echo "1. Go to: https://quire.io/r/setting"
echo "2. Click 'Personal' or 'Profile' tab"
echo "3. Scroll to 'Personal Access Tokens' or 'API'"
echo "4. Click 'Generate New Token'"
echo "5. Give it a name (e.g., 'HRMS Project')"
echo "6. Copy the token"
echo ""
read -p "Paste your Personal Access Token here: " ACCESS_TOKEN

# Save to .env
echo "QUIRE_ACCESS_TOKEN=$ACCESS_TOKEN" > .env

echo ""
echo "✅ Token saved to .env"
echo ""
echo "Testing token..."

# Test the token
RESPONSE=$(curl -s https://quire.io/api/user/id/me \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$RESPONSE" | grep -q "oid"; then
    echo "✅ Token works! You're authenticated."
    echo ""
    echo "Next steps:"
    echo "  1. List projects: ./venv/bin/python scripts/list_projects.py"
    echo "  2. Get project OID from the list"
    echo "  3. Create tasks: ./venv/bin/python scripts/create_changelog_tasks.py PROJECT_OID"
else
    echo "❌ Token test failed. Response:"
    echo "$RESPONSE"
    echo ""
    echo "Please check your token and try again."
fi

echo ""
