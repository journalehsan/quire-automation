# Quick Commands - Super Easy Quire Task Management

Stop typing long commands! Use simple, memorable shortcuts.

## 🚀 One-Time Setup (2 minutes)

### 1. Create Quire OAuth App
1. Go to https://quire.io/dev/apps
2. Click "Create New App"
3. Redirect URI: `http://localhost:8080`
4. Save Client ID & Secret

### 2. Load Commands & Authenticate
```bash
# Load the quick commands
source scripts/quire/qcommands.fish  # or qcommands.sh for bash

# Authenticate (browser opens automatically!)
qauth
```

That's it! You're done. ✨

---

## 📝 Daily Usage

### Create Task
```bash
qtask "Implement login feature"
qtask "Fix bug #123" -d "Details here" --priority 1
```

### Mark Done
```bash
qdone abc123xyz
qdone abc123xyz -c "Completed and tested!"
```

### List Tasks
```bash
qtasks              # Lists all tasks
qtasks PROJECT_OID  # Specific project
```

### List Projects
```bash
qprojects  # See all your projects
```

---

## ⚡ Power User Tips

### Set Default Project
```bash
# Add to .env
echo 'QUIRE_DEFAULT_PROJECT=your_project_oid' >> scripts/quire/.env

# Now just:
qtask "New task"  # No project needed!
```

### Auto-Load Commands
Add to `~/.config/fish/config.fish`:
```fish
source ~/Documents/GitHub/hrms_project/scripts/quire/qcommands.fish
```

Or for bash in `~/.bashrc`:
```bash
source ~/Documents/GitHub/hrms_project/scripts/quire/qcommands.sh
```

Now commands work from anywhere!

---

## 🎯 Workflow Example

```bash
# Morning: Check tasks
qtasks

# Create new task
qtask "Implement employee dashboard"
# Output: ✅ Task created
#         OID: abc123xyz

# Work on it...
# (code, test, commit)

# Done! Mark complete
qdone abc123xyz -c "Implemented, tested, deployed ✅"

# See updated list
qtasks
```

---

## 🔐 How Authentication Works

1. **First time:** Run `qauth`
   - Browser opens automatically
   - You enter Client ID/Secret (saved forever)
   - Click "Allow" on Quire
   - Tokens saved to `.env`

2. **After that:** Just use commands!
   - Tokens refresh automatically
   - Never think about auth again
   - Valid for 30 days, auto-renews

---

## 📋 All Commands

| Command | Description | Example |
|---------|-------------|---------|
| `qauth` | Authenticate (browser-based) | `qauth` |
| `qtask` | Create new task | `qtask "Fix bug"` |
| `qdone` | Mark task done | `qdone abc123xyz` |
| `qtasks` | List all tasks | `qtasks` |
| `qprojects` | List all projects | `qprojects` |

---

## 🔧 Options

### qtask options
```bash
qtask "Task name" \
  -p PROJECT_OID \      # Project (or use default)
  -d "Description" \    # Task description
  --priority 1 \        # 1=high, 2=medium, 3=low
  --due 2024-12-15      # Due date
```

### qdone options
```bash
qdone TASK_OID \
  -c "Comment" \        # Add completion comment
  -s 10                 # Status code (default: 10=Done)
```

---

## 💡 Integration with Your Workflow

### Git Workflow
```bash
# Create task for feature
qtask "Implement user settings" -p abc123
# Output: OID: xyz789

# Create branch with task OID
git checkout -b feature/xyz789-user-settings

# Work on it...
git commit -m "feat: user settings"
git push

# Mark done when merged
qdone xyz789 -c "Feature complete ✅"
```

### CI/CD Integration
Already built-in! When PR is merged:
- Branch name: `feature/TASK_OID-description`
- Task automatically marked done
- Comment added with PR link

---

## 🆘 Troubleshooting

### "Command not found: qauth"
```bash
source scripts/quire/qcommands.fish  # Load commands first
```

### "No module named 'dotenv'"
```bash
cd scripts/quire
source venv/bin/activate.fish
pip install -r requirements.txt
```

### "No project specified"
Set default project:
```bash
echo 'QUIRE_DEFAULT_PROJECT=your_oid' >> scripts/quire/.env
```

---

## 🌟 Why This is Better

**Before:**
```bash
cd scripts/quire
source venv/bin/activate.fish
python scripts/create_task.py PROJECT_OID "Task name" --description "..." --priority 1
python scripts/update_task.py TASK_OID --status 10 --comment "Done"
```

**Now:**
```bash
qtask "Task name"
qdone TASK_OID
```

Simple. Fast. Memorable. 🚀

---

**Ready to start?** Run: `source scripts/quire/qcommands.fish && qauth`
