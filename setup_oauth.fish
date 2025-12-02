#!/usr/bin/env fish
# Quick setup script for Quire authentication

echo "🔧 Quire OAuth Setup"
echo "===================="
echo ""
echo "Paste your Client ID from Quire:"
read -l client_id

echo ""
echo "Paste your Client Secret from Quire:"
read -l client_secret

echo ""
echo "💾 Saving to .env file..."

cd /home/ehsator/Documents/GitHub/hrms_project/scripts/quire

# Create or update .env file
echo "QUIRE_CLIENT_ID=$client_id" > .env
echo "QUIRE_CLIENT_SECRET=$client_secret" >> .env
echo "QUIRE_REDIRECT_URI=http://localhost:8080/callback" >> .env
echo "QUIRE_DEFAULT_PROJECT=MTNIrancell/HRMS" >> .env

echo ""
echo "✅ Configuration saved!"
echo ""
echo "🚀 Now running authentication..."
echo ""

# Run the easy_auth script
./venv/bin/python scripts/easy_auth.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Get your HRMS project OID:"
echo "     ./venv/bin/python scripts/list_projects.py"
echo ""
echo "  2. Create the 23 tasks from changelogs:"
echo "     ./venv/bin/python scripts/create_changelog_tasks.py PROJECT_OID"
echo ""
