#!/usr/bin/env fish
# Quick Quire commands - Source this file for easy task management

set QUIRE_DIR (dirname (status --current-filename))
set VENV_PYTHON "$QUIRE_DIR/venv/bin/python"

# Check if venv exists
if not test -f $VENV_PYTHON
    echo "⚠️  Virtual environment not found. Setting up..."
    python -m venv $QUIRE_DIR/venv
    source $QUIRE_DIR/venv/bin/activate.fish
    pip install -r $QUIRE_DIR/requirements.txt
end

# Authenticate (opens browser, saves tokens)
function qauth
    source $QUIRE_DIR/venv/bin/activate.fish
    $VENV_PYTHON $QUIRE_DIR/scripts/easy_auth.py $argv
end

# Create task
function qtask
    source $QUIRE_DIR/venv/bin/activate.fish
    $VENV_PYTHON $QUIRE_DIR/scripts/qtask.py $argv
end

# Mark task done
function qdone
    source $QUIRE_DIR/venv/bin/activate.fish
    $VENV_PYTHON $QUIRE_DIR/scripts/qdone.py $argv
end

# List tasks
function qtasks
    source $QUIRE_DIR/venv/bin/activate.fish
    $VENV_PYTHON $QUIRE_DIR/scripts/qtasks.py $argv
end

# List projects
function qprojects
    source $QUIRE_DIR/venv/bin/activate.fish
    $VENV_PYTHON $QUIRE_DIR/scripts/list_projects.py $argv
end

echo "✅ Quire commands loaded!"
echo ""
echo "Quick Commands:"
echo "  qauth        - Authenticate with Quire (browser-based)"
echo "  qtask 'Name' - Create new task"
echo "  qdone OID    - Mark task as done"
echo "  qtasks       - List all tasks"
echo "  qprojects    - List all projects"
echo ""
echo "First time? Run: qauth"
