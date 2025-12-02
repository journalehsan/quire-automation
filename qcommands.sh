#!/usr/bin/env bash
# Quick Quire commands - Source this file for easy task management

QUIRE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$QUIRE_DIR/venv/bin/python"

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "⚠️  Virtual environment not found. Setting up..."
    python -m venv "$QUIRE_DIR/venv"
    source "$QUIRE_DIR/venv/bin/activate"
    pip install -r "$QUIRE_DIR/requirements.txt"
fi

# Authenticate (opens browser, saves tokens)
qauth() {
    source "$QUIRE_DIR/venv/bin/activate"
    "$VENV_PYTHON" "$QUIRE_DIR/scripts/easy_auth.py" "$@"
}

# Create task
qtask() {
    source "$QUIRE_DIR/venv/bin/activate"
    "$VENV_PYTHON" "$QUIRE_DIR/scripts/qtask.py" "$@"
}

# Mark task done
qdone() {
    source "$QUIRE_DIR/venv/bin/activate"
    "$VENV_PYTHON" "$QUIRE_DIR/scripts/qdone.py" "$@"
}

# List tasks
qtasks() {
    source "$QUIRE_DIR/venv/bin/activate"
    "$VENV_PYTHON" "$QUIRE_DIR/scripts/qtasks.py" "$@"
}

# List projects
qprojects() {
    source "$QUIRE_DIR/venv/bin/activate"
    "$VENV_PYTHON" "$QUIRE_DIR/scripts/list_projects.py" "$@"
}

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
