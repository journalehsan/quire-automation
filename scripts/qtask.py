#!/usr/bin/env python3
"""
Quick task creator - Create Quire task with one command

Usage: 
  qtask "Task name"
  qtask "Task name" -d "Description" -p 1
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quire import QuireClient


def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Quick create Quire task")
    parser.add_argument("name", help="Task name")
    parser.add_argument("-p", "--project", help="Project OID (or set QUIRE_DEFAULT_PROJECT)")
    parser.add_argument("-d", "--description", help="Task description")
    parser.add_argument("--priority", type=int, help="Priority (1=high, 2=medium, 3=low)")
    parser.add_argument("--due", help="Due date (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    # Get project OID
    project_oid = args.project or os.getenv('QUIRE_DEFAULT_PROJECT')
    
    if not project_oid:
        print("❌ No project specified!")
        print("\nOptions:")
        print("  1. Pass project: qtask 'Task' -p PROJECT_OID")
        print("  2. Set default: echo 'QUIRE_DEFAULT_PROJECT=PROJECT_OID' >> .env")
        print("\nList projects: ./scripts/quire.sh projects")
        sys.exit(1)
    
    try:
        client = QuireClient()
        
        # Create task
        task = client.create_task(
            project_oid=project_oid,
            name=args.name,
            description=args.description,
            priority=args.priority,
            due=args.due,
        )
        
        print(f"✅ Task created: {task.name}")
        print(f"   OID: {task.oid}")
        if task.description:
            print(f"   Description: {task.description}")
        
        # Save OID for easy reference
        print(f"\n💡 To mark as done:")
        print(f"   qdone {task.oid}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
