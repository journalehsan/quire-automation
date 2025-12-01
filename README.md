# Quire Automation

Python scripts for automating Quire task management via OAuth2 and REST API.

## Features

- 🔐 OAuth2 authentication with token refresh
- 📝 List tasks from projects
- ✅ Update task status
- ➕ Create new tasks
- 💬 Add comments to tasks
- 🔄 Auto-refresh access tokens

## Quick Start

### 1. Set up Quire OAuth App

1. Go to **Quire → Developers → My Apps**
2. Create a new application
3. Set redirect URL to `https://localhost`
4. Copy **Client ID** and **Client Secret**

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
QUIRE_CLIENT_ID=your_client_id_here
QUIRE_CLIENT_SECRET=your_client_secret_here
QUIRE_REFRESH_TOKEN=your_refresh_token_here
```

### 4. Get Initial Tokens

Run the OAuth flow to get your refresh token:

```bash
python scripts/get_tokens.py
```

This will:
1. Print an authorization URL
2. Open it in your browser
3. After you approve, copy the code from the redirect URL
4. Paste it back to get your tokens

### 5. Use the Scripts

```bash
# List all projects
python scripts/list_projects.py

# List tasks in a project
python scripts/list_tasks.py PROJECT_OID

# Update task status
python scripts/update_task.py TASK_OID --status 10 --comment "Completed!"

# Create a new task
python scripts/create_task.py PROJECT_OID "Task name" --description "Details here"
```

## Project Structure

```
quire-automation/
├── quire/
│   ├── __init__.py
│   ├── client.py          # Main Quire API client
│   ├── auth.py            # OAuth2 authentication
│   └── models.py          # Data models
├── scripts/
│   ├── get_tokens.py      # OAuth flow helper
│   ├── list_projects.py   # List all projects
│   ├── list_tasks.py      # List tasks in project
│   ├── update_task.py     # Update task status/details
│   └── create_task.py     # Create new task
├── .env.example           # Environment template
├── .gitignore
├── requirements.txt
└── README.md
```

## Usage Examples

### List Projects
```bash
python scripts/list_projects.py
```

### List Tasks
```bash
# By project OID
python scripts/list_tasks.py abc123xyz

# Filter by status
python scripts/list_tasks.py abc123xyz --status-name "In Progress"
```

### Update Task
```bash
# Change status
python scripts/update_task.py task_oid --status 10

# Add comment
python scripts/update_task.py task_oid --comment "Work completed by AI"

# Both
python scripts/update_task.py task_oid --status 10 --comment "✅ Done!"
```

### Create Task
```bash
python scripts/create_task.py project_oid "Implement feature X" \
  --description "Details about the feature" \
  --assignee user_oid
```

## Task Status Codes

Common status values (check your project for exact values):
- `0` - New/Open
- `10` - Done/Completed
- Custom statuses vary by project

Use `list_tasks.py` to see available statuses in your project.

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Update Quire on Merge

on:
  pull_request:
    types: [closed]

jobs:
  update-quire:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Update Quire task
        env:
          QUIRE_CLIENT_ID: ${{ secrets.QUIRE_CLIENT_ID }}
          QUIRE_CLIENT_SECRET: ${{ secrets.QUIRE_CLIENT_SECRET }}
          QUIRE_REFRESH_TOKEN: ${{ secrets.QUIRE_REFRESH_TOKEN }}
        run: |
          # Extract task OID from branch name or PR description
          TASK_OID=$(echo "${{ github.head_ref }}" | grep -oP 'task-\K[a-zA-Z0-9]+')
          
          if [ ! -z "$TASK_OID" ]; then
            python scripts/update_task.py "$TASK_OID" \
              --status 10 \
              --comment "✅ PR #${{ github.event.pull_request.number }} merged"
          fi
```

## Security Notes

⚠️ **Never commit your `.env` file or tokens to git!**

- Store tokens in environment variables or secrets manager
- Use `.gitignore` to exclude `.env`
- In production, use GitHub Secrets, AWS Secrets Manager, etc.

## API Reference

- [Quire API Documentation](https://quire.io/dev/api/)
- [OAuth Tutorial](https://quire.io/dev/tutorial)

## License

MIT

## Contributing

PRs welcome! This is a simple automation tool, feel free to extend it.
