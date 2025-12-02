#!/usr/bin/env python3
"""
Quick Start - First-time Quire setup with browser authentication

This script helps you get started in 3 simple steps!
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def print_banner():
    print("\n" + "=" * 80)
    print("  🚀 QUIRE QUICK START - Browser-Based Setup")
    print("=" * 80 + "\n")


def check_requirements():
    """Check if requirements are installed"""
    try:
        import requests
        from dotenv import load_dotenv
        return True
    except ImportError:
        return False


def main():
    print_banner()
    
    # Check if venv exists
    venv_dir = Path(__file__).parent.parent / "venv"
    
    if not venv_dir.exists():
        print("📦 Step 1: Setting up Python virtual environment...")
        print("\nRun these commands:\n")
        print("  cd scripts/quire")
        print("  python -m venv venv")
        print("  source venv/bin/activate.fish  # or venv/bin/activate for bash")
        print("  pip install -r requirements.txt")
        print("\nThen run this script again.")
        return
    
    # Check if dependencies installed
    if not check_requirements():
        print("⚠️  Dependencies not installed!")
        print("\nRun:")
        print("  source venv/bin/activate.fish")
        print("  pip install -r requirements.txt")
        return
    
    # Check if .env exists
    env_file = Path(__file__).parent.parent / ".env"
    
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_example = Path(__file__).parent.parent / ".env.example"
        import shutil
        shutil.copy(env_example, env_file)
        print(f"✅ Created {env_file}")
    
    # Instructions
    print("🎯 THREE EASY STEPS TO START:\n")
    
    print("─" * 80)
    print("STEP 1: Create Quire OAuth App (2 minutes)")
    print("─" * 80)
    print("\n1. Go to: https://quire.io/dev/apps")
    print("2. Click 'Create New App'")
    print("3. Fill in:")
    print("   Name: HRMS Automation (or any name)")
    print("   Redirect URI: http://localhost:8080")
    print("4. Click 'Create'")
    print("5. You'll get Client ID and Secret")
    
    print("\n─" * 80)
    print("STEP 2: Run Easy Authentication (30 seconds)")
    print("─" * 80)
    print("\nRun this command (it will open your browser):")
    print("\n  source scripts/quire/qcommands.fish  # Load commands")
    print("  qauth                                 # Authenticate!")
    print("\nWhat happens:")
    print("  • Browser opens automatically")
    print("  • You enter Client ID & Secret (one time)")
    print("  • Click 'Allow' on Quire")
    print("  • Tokens saved automatically!")
    print("  • Done! ✨")
    
    print("\n─" * 80)
    print("STEP 3: Start Using (instant)")
    print("─" * 80)
    print("\nNow you can use simple commands:")
    print("\n  qprojects              # List your projects")
    print("  qtask 'Implement X'    # Create task")
    print("  qtasks                 # List all tasks")
    print("  qdone TASK_OID         # Mark task done")
    
    print("\n" + "=" * 80)
    print("💡 PRO TIPS")
    print("=" * 80)
    print("\n1. Set default project (optional but recommended):")
    print("   echo 'QUIRE_DEFAULT_PROJECT=your_project_oid' >> scripts/quire/.env")
    print("\n2. Add to your shell startup (~/.config/fish/config.fish):")
    print("   source ~/Documents/GitHub/hrms_project/scripts/quire/qcommands.fish")
    print("\n3. Then from anywhere:")
    print("   qtask 'New feature'    # Create task")
    print("   qdone abc123xyz        # Mark done")
    
    print("\n" + "=" * 80)
    print("🎉 THAT'S IT!")
    print("=" * 80)
    print("\nYou authenticate ONCE with the browser, then just use commands.")
    print("Tokens auto-refresh, so you never think about auth again!\n")
    
    # Show next step
    print("📍 NEXT: Run 'qauth' to authenticate\n")


if __name__ == "__main__":
    main()
