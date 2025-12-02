#!/usr/bin/env python3
"""
Quick task completer - Mark Quire task as done

Usage: 
  qdone TASK_OID
  qdone TASK_OID -c "Completed message"
"""

import sys
import argparse
from dotenv import load_dotenv

# Add parent directory to path
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quire import QuireClient


def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Quick mark task as done")
    parser.add_argument("task_oid", help="Task OID")
    parser.add_argument("-c", "--comment", help="Completion comment")
    parser.add_argument("-s", "--status", type=int, default=10, help="Status code (default: 10=Done)")
    
    args = parser.parse_args()
    
    try:
        client = QuireClient()
        
        # Get current task
        task = client.get_task(args.task_oid)
        print(f"📝 Task: {task.name}")
        
        # Update to done
        updated = client.update_task(args.task_oid, status=args.status)
        print(f"✅ Status updated to: {args.status}")
        
        # Add comment if provided
        if args.comment:
            client.add_comment(args.task_oid, args.comment)
            print(f"💬 Comment added: {args.comment}")
        
        print(f"\n🎉 Task marked as done!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
