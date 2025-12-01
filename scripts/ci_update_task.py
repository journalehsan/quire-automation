#!/usr/bin/env python3
"""
CI/CD automation example: Update Quire task when PR is merged

This script demonstrates how to integrate Quire with your CI/CD pipeline.
It extracts the task OID from the branch name and updates the task status.

Expected branch naming: feature/TASK_OID-description
Example: feature/abc123xyz-implement-login
"""

import os
import sys
import re
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quire import QuireClient


def extract_task_oid_from_branch(branch_name: str) -> str:
    """
    Extract task OID from branch name
    
    Patterns supported:
    - feature/TASK_OID-description
    - task/TASK_OID
    - TASK_OID-anything
    """
    patterns = [
        r'feature/([a-zA-Z0-9]+)-',  # feature/abc123-description
        r'task/([a-zA-Z0-9]+)',       # task/abc123
        r'([a-zA-Z0-9]+)-',           # abc123-description
    ]
    
    for pattern in patterns:
        match = re.search(pattern, branch_name)
        if match:
            return match.group(1)
    
    return None


def main():
    load_dotenv()
    
    # Get environment variables from CI/CD
    branch_name = os.getenv("BRANCH_NAME") or os.getenv("CI_COMMIT_BRANCH") or sys.argv[1] if len(sys.argv) > 1 else None
    pr_number = os.getenv("PR_NUMBER") or os.getenv("CI_MERGE_REQUEST_IID")
    build_url = os.getenv("BUILD_URL") or os.getenv("CI_PIPELINE_URL")
    
    if not branch_name:
        print("❌ Error: No branch name provided")
        print("Set BRANCH_NAME environment variable or pass as argument")
        sys.exit(1)
    
    print("🤖 CI/CD Quire Task Updater\n")
    print("=" * 80)
    print(f"Branch: {branch_name}")
    if pr_number:
        print(f"PR/MR: #{pr_number}")
    print()
    
    # Extract task OID
    task_oid = extract_task_oid_from_branch(branch_name)
    
    if not task_oid:
        print("⚠️  No task OID found in branch name")
        print("Expected format: feature/TASK_OID-description")
        print("Example: feature/abc123xyz-implement-login")
        print("\nSkipping Quire update.")
        sys.exit(0)  # Exit successfully, just skip update
    
    print(f"📌 Found task OID: {task_oid}\n")
    
    try:
        client = QuireClient()
        
        # Get current task
        task = client.get_task(task_oid)
        print(f"Current task: {task.name}")
        print(f"Current status: {task.status}\n")
        
        # Update to "Done" (status code 10)
        print("Updating task to 'Done' (status: 10)...")
        updated_task = client.update_task(task_oid, status=10)
        
        # Add comment with CI/CD info
        comment_parts = ["✅ Completed via CI/CD pipeline"]
        if pr_number:
            comment_parts.append(f"PR/MR: #{pr_number}")
        if build_url:
            comment_parts.append(f"Build: {build_url}")
        
        comment = "\n".join(comment_parts)
        print(f"Adding comment: {comment}\n")
        client.add_comment(task_oid, comment)
        
        print("=" * 80)
        print("🎉 Task updated successfully!\n")
        print(f"Task: {updated_task.name}")
        print(f"Status: {updated_task.status}")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error updating Quire task: {e}")
        print("\nThis is non-critical - continuing CI/CD pipeline")
        sys.exit(0)  # Don't fail the build if Quire update fails


if __name__ == "__main__":
    main()
