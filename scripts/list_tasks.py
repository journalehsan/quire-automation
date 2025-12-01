#!/usr/bin/env python3
"""
List tasks in a Quire project
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
    
    parser = argparse.ArgumentParser(description="List tasks in a Quire project")
    parser.add_argument("project_oid", help="Project OID")
    parser.add_argument("--status", type=int, help="Filter by status code")
    parser.add_argument("--assignee", help="Filter by assignee OID")
    
    args = parser.parse_args()
    
    print(f"📝 Tasks in Project: {args.project_oid}\n")
    print("=" * 80)
    
    try:
        client = QuireClient()
        
        # Get project info
        project = client.get_project(args.project_oid)
        print(f"Project: {project.name}")
        if project.description:
            print(f"Description: {project.description}")
        print()
        
        # List tasks
        tasks = client.list_tasks(
            args.project_oid,
            status=args.status,
            assignee=args.assignee,
        )
        
        if not tasks:
            print("No tasks found.")
            return
        
        print(f"Found {len(tasks)} task(s):\n")
        
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
            print(f"   OID: {task.oid}")
            if task.description:
                desc = task.description[:100] + "..." if len(task.description) > 100 else task.description
                print(f"   Description: {desc}")
            if task.status is not None:
                print(f"   Status: {task.status}")
            if task.priority is not None:
                print(f"   Priority: {task.priority}")
            if task.assignees:
                assignee_names = ", ".join([a.name for a in task.assignees])
                print(f"   Assignees: {assignee_names}")
            if task.due:
                print(f"   Due: {task.due}")
            if task.tags:
                print(f"   Tags: {', '.join(task.tags)}")
            print()
        
        print("=" * 80)
        print("\n💡 Tip: Update a task with:")
        print("   python scripts/update_task.py <TASK_OID> --status 10 --comment 'Done!'\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
