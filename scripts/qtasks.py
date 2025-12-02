#!/usr/bin/env python3
"""
Quick task lister - List today's tasks

Usage: 
  qtasks              # List all tasks in default project
  qtasks PROJECT_OID  # List tasks in specific project
"""

import sys
import os
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quire import QuireClient


def main():
    load_dotenv()
    
    # Get project OID from args or env
    project_oid = sys.argv[1] if len(sys.argv) > 1 else os.getenv('QUIRE_DEFAULT_PROJECT')
    
    if not project_oid:
        print("❌ No project specified!")
        print("\nOptions:")
        print("  1. qtasks PROJECT_OID")
        print("  2. Set default: echo 'QUIRE_DEFAULT_PROJECT=PROJECT_OID' >> .env")
        print("\nList projects: ./scripts/quire.sh projects")
        sys.exit(1)
    
    try:
        client = QuireClient()
        
        # Get project info
        project = client.get_project(project_oid)
        print(f"\n📋 {project.name}\n")
        print("=" * 80)
        
        # List tasks
        tasks = client.list_tasks(project_oid)
        
        if not tasks:
            print("No tasks found.")
            return
        
        # Group by status
        pending = [t for t in tasks if not t.completed]
        done = [t for t in tasks if t.completed]
        
        if pending:
            print(f"\n⏳ Pending ({len(pending)}):\n")
            for i, task in enumerate(pending, 1):
                print(f"  {i}. {task.name}")
                print(f"     OID: {task.oid}")
                if task.priority:
                    priority_map = {1: "🔴 High", 2: "🟡 Medium", 3: "🟢 Low"}
                    print(f"     Priority: {priority_map.get(task.priority, task.priority)}")
                print()
        
        if done:
            print(f"✅ Completed ({len(done)}):\n")
            for task in done[:5]:  # Show last 5
                print(f"  • {task.name}")
        
        print("=" * 80)
        print(f"\n💡 Create task: qtask 'Task name'")
        print(f"💡 Mark done: qdone TASK_OID\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
