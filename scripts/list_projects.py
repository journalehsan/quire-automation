#!/usr/bin/env python3
"""
List all Quire projects
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quire import QuireClient


def main():
    load_dotenv()
    
    print("📋 Quire Projects\n")
    print("=" * 80)
    
    try:
        client = QuireClient()
        
        # Get current user
        user = client.get_current_user()
        print(f"👤 Logged in as: {user.name} ({user.email})\n")
        
        # List projects
        projects = client.list_projects()
        
        if not projects:
            print("No projects found.")
            return
        
        print(f"Found {len(projects)} project(s):\n")
        
        for i, project in enumerate(projects, 1):
            status = "📦" if not project.archived else "📁"
            print(f"{i}. {status} {project.name}")
            print(f"   OID: {project.oid}")
            if project.description:
                print(f"   Description: {project.description}")
            if project.color:
                print(f"   Color: {project.color}")
            print()
        
        print("=" * 80)
        print("\n💡 Tip: Use the OID to list tasks in a project:")
        print("   python scripts/list_tasks.py <PROJECT_OID>\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
