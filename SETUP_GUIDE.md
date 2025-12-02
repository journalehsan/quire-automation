# Quire API Setup Guide

## Step 1: Create OAuth App in Quire

1. **Login to Quire**: Go to https://quire.io and login with your account (journalehsan@gmail.com)

2. **Access Developer Console**:
   - Look for your account menu (top-right corner)
   - Go to **Settings** or **Account Settings**
   - Look for **Developer**, **Apps**, **API**, or **Integrations** section
   - If you're in an organization, you may need to select the organization first

3. **Create New App**:
   - Click "Create App" or "New Application"
   - Fill in the form:
     - **App Name**: HRMS Task Manager (or any name you prefer)
     - **Organization**: Select your organization
     - **Redirect URL**: `http://localhost:8080/callback`
     - **Permissions**: Select:
       - ✅ Read tasks
       - ✅ Write tasks
       - ✅ Read projects
       - ✅ Write projects

4. **Get Credentials**:
   - After creating the app, you'll see:
     - **Client ID**: A long string (copy this)
     - **Client Secret**: Another long string (copy this)

## Step 2: Configure Environment

Run this in terminal:

```bash
cd /home/ehsator/Documents/GitHub/hrms_project/scripts/quire
```

Create `.env` file:

```bash
cat > .env << 'EOF'
QUIRE_CLIENT_ID=your_client_id_here
QUIRE_CLIENT_SECRET=your_client_secret_here
QUIRE_REDIRECT_URI=http://localhost:8080/callback
EOF
```

**IMPORTANT**: Replace `your_client_id_here` and `your_client_secret_here` with the actual values from Step 1.

## Step 3: Get Access Token

Run the browser-based authentication:

```bash
./venv/bin/python scripts/easy_auth.py
```

This will:
1. Start a local server on port 8080
2. Open Quire authorization page in your browser
3. After you click "Allow", automatically capture the token
4. Save `QUIRE_REFRESH_TOKEN` to `.env`

## Step 4: Test the Setup

List your projects:

```bash
./venv/bin/python scripts/list_projects.py
```

You should see a list of your Quire projects with their OIDs.

## Step 5: Create Tasks from Changelogs

1. **Select Project**: From the list in Step 4, copy the OID of the project where you want to create tasks

2. **Set Default Project** (optional):
   ```bash
   echo 'QUIRE_DEFAULT_PROJECT=PROJECT_OID_HERE' >> .env
   ```

3. **Create Tasks**:
   ```bash
   ./venv/bin/python scripts/create_changelog_tasks.py
   ```
   
   Or with project OID as argument:
   ```bash
   ./venv/bin/python scripts/create_changelog_tasks.py PROJECT_OID_HERE
   ```

This will create 23 tasks from CHANGELOG_DEC01.md and CHANGES.md with:
- ⏱️ Time estimates (101 hours total, ~2.5 weeks)
- 📊 Priority levels (High, Medium, Low)
- 🏷️ Tags based on task type
- 📅 Due dates distributed over 2 weeks

## Alternative: Use Quick Commands

After setup, you can use these shortcuts:

```bash
# List projects
qprojects

# Create a task
qtask "Task name"

# Mark task as done
qdone TASK_ID

# List all tasks
qtasks
```

## Troubleshooting

### Can't find Developer section
- Check if you're logged into the right account
- Some features may require organization admin permissions
- Try accessing directly: https://quire.io/apps or https://quire.io/settings/apps

### Port 8080 already in use
- Close any programs using port 8080
- Or modify `easy_auth.py` to use a different port (e.g., 8081)
- Don't forget to update the Redirect URL in Quire app settings

### Token expired
- Re-run `./venv/bin/python scripts/easy_auth.py` to refresh the token
- The library automatically refreshes tokens, but manual refresh may be needed sometimes

## What Gets Created

The `create_changelog_tasks.py` script will create these 23 tasks:

**Week 1 - High Priority (34 hours)**
- Custom fields system - Backend & Frontend (8h)
- Custom field validation & API integration (6h)
- Teams feature implementation (6h)
- Employee profile page development (8h)
- Multi-language i18n system (6h)

**Week 1-2 - Medium Priority (49 hours)**
- RTL support for Arabic/Farsi (8h)
- Navigation i18n implementation (6h)
- Employee login system (6h)
- Custom fields UI refactoring (4h)
- Logout functionality for employees (2h)
- Profile section styling improvements (3h)
- Employee dashboard layout (4h)
- Login page improvements (3h)
- Database schema updates (4h)
- Infinite loop bug fixes (3h)
- Navigation cleanup (2h)
- Conditional rendering fixes (2h)
- Dual login system setup (2h)

**Week 2 - Low Priority (18 hours)**
- Custom fields management UI (4h)
- Teams data migration (3h)
- Login debugging & testing (3h)
- RTL testing & validation (3h)
- UI polish & improvements (3h)
- Documentation updates (2h)

## Next Steps

After all tasks are created:
- Review them in Quire
- Assign team members
- Set up task dependencies
- Configure Kanban boards or other views
- Start tracking progress!
