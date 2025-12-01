#!/usr/bin/env python3
"""
Update a Quire task
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
    
    parser = argparse.ArgumentParser(description="Update a Quire task")
    parser.add_argument("task_oid", help="Task OID to update")
    parser.add_argument("--name", help="New task name")
    parser.add_argument("--description", help="New task description")
    parser.add_argument("--status", type=int, help="New status code (e.g., 10 for Done)")
    parser.add_argument("--priority", type=int, help="New priority level")
    parser.add_argument("--assignee", help="New assignee OID")
    parser.add_argument("--start", help="Start date (ISO format)")
    parser.add_argument("--due", help="Due date (ISO format)")
    parser.add_argument("--comment", help="Add a comment to the task")
    
    args = parser.parse_args()
    
    # Check if any update arguments provided
    update_args = {
        "name": args.name,
        "description": args.description,
        "status": args.status,
        "priority": args.priority,
        "assignee": args.assignee,
        "start": args.start,
        "due": args.due,
    }
    
    has_updates = any(v is not None for v in update_args.values())
    
    if not has_updates and not args.comment:
        print("❌ Error: No updates specified. Use --help to see available options.")
        sys.exit(1)
    
    print(f"🔄 Updating Task: {args.task_oid}\n")
    print("=" * 80)
    
    try:
        client = QuireClient()
        
        # Get current task info
        task = client.get_task(args.task_oid)
        print(f"Current task: {task.name}")
        print(f"Status: {task.status}")
        print()
        
        # Update task if any fields provided
        if has_updates:
            print("Applying updates...")
            updated_task = client.update_task(
                args.task_oid,
                **{k: v for k, v in update_args.items() if v is not None}
            )
            
            print("✅ Task updated successfully!\n")
            print(f"Name: {updated_task.name}")
            if updated_task.description:
                print(f"Description: {updated_task.description[:100]}")
            print(f"Status: {updated_task.status}")
            if updated_task.priority is not None:
                print(f"Priority: {updated_task.priority}")
            print()
        
        # Add comment if provided
        if args.comment:
            print("Adding comment...")
            comment = client.add_comment(args.task_oid, args.comment)
            print(f"✅ Comment added: {args.comment}\n")
        
        print("=" * 80)
        print("🎉 All done!\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
