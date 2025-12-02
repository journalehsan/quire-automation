# Quick Setup - Quire OAuth App

## Issue: "You cannot add project without adding an organization first"

You need to create a Quire organization before you can create an OAuth app.

## Step-by-Step Solution

### 1. Create a Quire Organization

1. Go to: https://quire.io/organizations/new
2. Fill in the form:
   - **Organization Name**: HRMS Project (or any name you prefer)
   - **Organization ID**: hrms-project (or any unique ID)
3. Click **Create Organization**

### 2. Create OAuth App

After creating the organization:

1. Go back to: https://quire.io/apps
2. Click **Create new app**
3. Now it should work! Fill in:
   - **App Name**: HRMS Task Manager
   - **Organization**: Select "HRMS Project" (or the org you just created)
   - **Redirect URL**: `http://localhost:8080/callback`
   - **Permissions**: 
     - ✅ Read user data
     - ✅ Read projects
     - ✅ Write projects
     - ✅ Read tasks
     - ✅ Write tasks
4. Click **Create**
5. **COPY** the Client ID and Client Secret

### 3. Configure .env File

```bash
cd /home/ehsator/Documents/GitHub/hrms_project/scripts/quire
```

Edit `.env` file (or create it):

```bash
nano .env
```

Add these lines (replace with your actual values):

```
QUIRE_CLIENT_ID=your_client_id_from_step_2
QUIRE_CLIENT_SECRET=your_client_secret_from_step_2
QUIRE_REDIRECT_URI=http://localhost:8080/callback
```

Save and exit (Ctrl+X, Y, Enter)

### 4. Authenticate

```bash
./venv/bin/python scripts/easy_auth.py
```

This will:
- Start a local server
- Open Quire in your browser
- Ask you to authorize the app
- Automatically save the refresh token

### 5. Create Tasks

```bash
# List your projects first
./venv/bin/python scripts/list_projects.py

# Then create tasks (replace PROJECT_OID with actual value)
./venv/bin/python scripts/create_changelog_tasks.py PROJECT_OID
```

---

## Alternative: Use Existing Organization

If you already have an organization in Quire:

1. Go to your organization page
2. Click on organization settings
3. Go to the **Developer Apps** section
4. Create app there directly

---

## Quick Links

- Create Organization: https://quire.io/organizations/new
- Developer Apps: https://quire.io/apps
- API Documentation: https://quire.io/dev/api

---

## Still Having Issues?

If you're still stuck, you might be on a free plan that doesn't allow custom OAuth apps. In that case, we have two options:

### Option A: Use Zapier/Make.com Integration
- These services provide pre-built Quire integrations
- No OAuth app needed
- Can trigger via webhooks from our scripts

### Option B: Manual CSV Import
- Export tasks from our script to CSV
- Import manually to Quire
- Less automation but works on any plan

Let me know which approach you'd prefer!
