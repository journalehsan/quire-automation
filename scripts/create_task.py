#!/usr/bin/env python3
"""
Create a new task in a Quire project
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
    
    parser = argparse.ArgumentParser(description="Create a new Quire task")
    parser.add_argument("project_oid", help="Project OID to create task in")
    parser.add_argument("name", help="Task name")
    parser.add_argument("--description", help="Task description")
    parser.add_argument("--status", type=int, help="Status code")
    parser.add_argument("--priority", type=int, help="Priority level")
    parser.add_argument("--assignee", help="Assignee OID")
    parser.add_argument("--start", help="Start date (ISO format: YYYY-MM-DD)")
    parser.add_argument("--due", help="Due date (ISO format: YYYY-MM-DD)")
    parser.add_argument("--tags", nargs="+", help="Tags (space-separated)")
    
    args = parser.parse_args()
    
    print(f"➕ Creating Task in Project: {args.project_oid}\n")
    print("=" * 80)
    
    try:
        client = QuireClient()
        
        # Get project info
        project = client.get_project(args.project_oid)
        print(f"Project: {project.name}\n")
        
        # Create task
        print(f"Creating task: {args.name}")
        
        task = client.create_task(
            project_oid=args.project_oid,
            name=args.name,
            description=args.description,
            status=args.status,
            priority=args.priority,
            assignee=args.assignee,
            start=args.start,
            due=args.due,
            tags=args.tags,
        )
        
        print("\n✅ Task created successfully!\n")
        print(f"OID: {task.oid}")
        print(f"Name: {task.name}")
        if task.description:
            print(f"Description: {task.description}")
        if task.status is not None:
            print(f"Status: {task.status}")
        if task.priority is not None:
            print(f"Priority: {task.priority}")
        if task.assignees:
            assignee_names = ", ".join([a.name for a in task.assignees])
            print(f"Assignees: {assignee_names}")
        if task.due:
            print(f"Due: {task.due}")
        if task.tags:
            print(f"Tags: {', '.join(task.tags)}")
        
        print("\n" + "=" * 80)
        print(f"🎉 Task created! OID: {task.oid}\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
