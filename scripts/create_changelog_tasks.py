#!/usr/bin/env python3
"""
Create tasks from HRMS changelogs with time estimates

Analyzes changelogs and creates Quire tasks with realistic time estimates
for a 2-week sprint.
"""

import sys
import os
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quire import QuireClient


# Task list from changelogs with time estimates (2 weeks = 80 hours total)
TASKS = [
    # From CHANGELOG_DEC01.md - Manager Dashboard & Team Management
    {
        "name": "Manager Dashboard - Team Members Page Enhancement",
        "description": "Enhance /manager/team to show full employee details with team membership history. Already completed but needs review and polish.",
        "hours": 2,
        "priority": 2,
        "tags": ["frontend", "manager-dashboard", "review"]
    },
    {
        "name": "Manager Dashboard - Team Scoring Page",
        "description": "Complete /manager/scoring page for scoring team member KPIs. Basic structure exists, needs full implementation.",
        "hours": 6,
        "priority": 1,
        "tags": ["frontend", "manager-dashboard", "kpi"]
    },
    {
        "name": "Backend - Team Filtering by Manager",
        "description": "Enhance Teams API to filter by manager_id. Already implemented, needs testing.",
        "hours": 1,
        "priority": 3,
        "tags": ["backend", "api", "testing"]
    },
    {
        "name": "Database - Team Members View Optimization",
        "description": "Review and optimize team_members_with_details view for performance.",
        "hours": 2,
        "priority": 2,
        "tags": ["database", "optimization"]
    },
    
    # Employee Dashboard Improvements
    {
        "name": "Employee Dashboard - My KPIs Page Polish",
        "description": "Add visualizations and better UX to /me/kpis page. Fix any remaining edge cases.",
        "hours": 4,
        "priority": 1,
        "tags": ["frontend", "employee-dashboard", "kpi"]
    },
    {
        "name": "Error Handling - Add Global Error Boundary",
        "description": "Implement React error boundaries across the app for better error handling.",
        "hours": 3,
        "priority": 1,
        "tags": ["frontend", "error-handling"]
    },
    
    # Authentication & Security (from CHANGES.md)
    {
        "name": "Authentication - Add Two-Factor Authentication",
        "description": "Implement 2FA for admin accounts using TOTP (Google Authenticator style).",
        "hours": 8,
        "priority": 1,
        "tags": ["backend", "frontend", "security", "auth"]
    },
    {
        "name": "Authentication - Password Reset Flow",
        "description": "Create email-based password reset flow with secure tokens.",
        "hours": 6,
        "priority": 1,
        "tags": ["backend", "frontend", "auth"]
    },
    {
        "name": "Security - Implement Rate Limiting",
        "description": "Add rate limiting to login endpoints and API to prevent brute force attacks.",
        "hours": 4,
        "priority": 1,
        "tags": ["backend", "security"]
    },
    {
        "name": "Security - Add CSRF Protection",
        "description": "Implement CSRF tokens for all state-changing operations.",
        "hours": 3,
        "priority": 1,
        "tags": ["backend", "security"]
    },
    {
        "name": "Authentication - Refresh Token Implementation",
        "description": "Add refresh tokens for extended sessions without re-login.",
        "hours": 5,
        "priority": 2,
        "tags": ["backend", "auth"]
    },
    {
        "name": "Security - Account Lockout Mechanism",
        "description": "Lock accounts after N failed login attempts with time-based unlocking.",
        "hours": 4,
        "priority": 2,
        "tags": ["backend", "security"]
    },
    
    # UI/UX Improvements
    {
        "name": "UI - Password Strength Meter",
        "description": "Add visual password strength indicator on registration/password change.",
        "hours": 2,
        "priority": 3,
        "tags": ["frontend", "ux"]
    },
    {
        "name": "UI - Login History & Audit Logs",
        "description": "Create page showing login history, active sessions, and security events.",
        "hours": 6,
        "priority": 2,
        "tags": ["frontend", "backend", "security"]
    },
    {
        "name": "UI - Dark Mode Consistency",
        "description": "Ensure dark mode works perfectly across all pages and components.",
        "hours": 3,
        "priority": 3,
        "tags": ["frontend", "ui"]
    },
    {
        "name": "UI - RTL Language Support Testing",
        "description": "Comprehensive testing of RTL support across all pages.",
        "hours": 4,
        "priority": 2,
        "tags": ["frontend", "i18n", "testing"]
    },
    
    # Testing & Quality
    {
        "name": "Testing - Frontend Unit Tests",
        "description": "Add unit tests for critical components (auth, KPI, team management).",
        "hours": 8,
        "priority": 2,
        "tags": ["frontend", "testing"]
    },
    {
        "name": "Testing - API Integration Tests",
        "description": "Create integration tests for all API endpoints.",
        "hours": 6,
        "priority": 2,
        "tags": ["backend", "testing"]
    },
    {
        "name": "Testing - E2E Tests with Playwright",
        "description": "Set up Playwright and create E2E tests for critical user flows.",
        "hours": 8,
        "priority": 2,
        "tags": ["testing", "e2e"]
    },
    
    # Documentation
    {
        "name": "Documentation - API Documentation",
        "description": "Complete API documentation with examples for all endpoints.",
        "hours": 4,
        "priority": 3,
        "tags": ["documentation"]
    },
    {
        "name": "Documentation - User Guide",
        "description": "Create comprehensive user guide for employees, managers, and admins.",
        "hours": 5,
        "priority": 3,
        "tags": ["documentation"]
    },
    
    # Performance & Optimization
    {
        "name": "Performance - Database Query Optimization",
        "description": "Profile and optimize slow database queries, add indexes where needed.",
        "hours": 4,
        "priority": 2,
        "tags": ["backend", "database", "performance"]
    },
    {
        "name": "Performance - Frontend Bundle Optimization",
        "description": "Analyze and reduce bundle size, implement code splitting.",
        "hours": 3,
        "priority": 3,
        "tags": ["frontend", "performance"]
    },
]


def calculate_time_distribution():
    """Calculate total hours and distribution"""
    total_hours = sum(task['hours'] for task in TASKS)
    high_priority = sum(task['hours'] for task in TASKS if task['priority'] == 1)
    medium_priority = sum(task['hours'] for task in TASKS if task['priority'] == 2)
    low_priority = sum(task['hours'] for task in TASKS if task['priority'] == 3)
    
    return {
        'total': total_hours,
        'high': high_priority,
        'medium': medium_priority,
        'low': low_priority,
        'weeks': total_hours / 40  # Assuming 40 hours/week
    }


def main():
    load_dotenv()
    
    print("=" * 80)
    print("  📋 HRMS Task Creation from Changelogs")
    print("=" * 80)
    
    # Calculate time distribution
    time_dist = calculate_time_distribution()
    
    print(f"\n📊 Task Overview:")
    print(f"   Total Tasks: {len(TASKS)}")
    print(f"   Total Hours: {time_dist['total']} hours ({time_dist['weeks']:.1f} weeks)")
    print(f"   High Priority: {time_dist['high']} hours")
    print(f"   Medium Priority: {time_dist['medium']} hours")
    print(f"   Low Priority: {time_dist['low']} hours")
    
    # Check for project
    project_oid = os.getenv('QUIRE_DEFAULT_PROJECT')
    
    if not project_oid:
        print("\n⚠️  No default project set!")
        print("\nOptions:")
        print("  1. Set project: echo 'QUIRE_DEFAULT_PROJECT=PROJECT_OID' >> .env")
        print("  2. List projects: qprojects")
        print("  3. Pass project as argument: python create_changelog_tasks.py PROJECT_OID")
        
        if len(sys.argv) > 1:
            project_oid = sys.argv[1]
            print(f"\n✅ Using project from argument: {project_oid}")
        else:
            sys.exit(1)
    else:
        print(f"\n✅ Using default project: {project_oid}")
    
    # Confirm before creating
    print(f"\n⚠️  About to create {len(TASKS)} tasks in Quire.")
    response = input("Continue? [y/N]: ").strip().lower()
    
    if response != 'y':
        print("❌ Cancelled.")
        sys.exit(0)
    
    # Create tasks
    print(f"\n🚀 Creating tasks...\n")
    
    try:
        client = QuireClient()
        created_tasks = []
        
        for i, task_data in enumerate(TASKS, 1):
            # Calculate due date (distribute over 2 weeks)
            # High priority: Week 1, Medium: Week 1-2, Low: Week 2
            from datetime import datetime, timedelta
            today = datetime.now()
            
            if task_data['priority'] == 1:
                due_date = (today + timedelta(days=7)).strftime('%Y-%m-%d')
            elif task_data['priority'] == 2:
                due_date = (today + timedelta(days=10)).strftime('%Y-%m-%d')
            else:
                due_date = (today + timedelta(days=14)).strftime('%Y-%m-%d')
            
            # Add time estimate to description
            description = f"{task_data['description']}\n\n⏱️ Estimated: {task_data['hours']} hours"
            if task_data.get('tags'):
                description += f"\n🏷️ Tags: {', '.join(task_data['tags'])}"
            
            print(f"[{i}/{len(TASKS)}] Creating: {task_data['name'][:50]}...")
            
            task = client.create_task(
                project_oid=project_oid,
                name=task_data['name'],
                description=description,
                priority=task_data['priority'],
                due=due_date,
                tags=task_data.get('tags', [])
            )
            
            created_tasks.append({
                'name': task.name,
                'oid': task.oid,
                'hours': task_data['hours'],
                'priority': task_data['priority']
            })
            
            print(f"   ✅ Created: {task.oid}")
        
        # Summary
        print("\n" + "=" * 80)
        print("  🎉 All Tasks Created!")
        print("=" * 80)
        
        print(f"\n📋 Summary:")
        print(f"   Tasks Created: {len(created_tasks)}")
        print(f"   Total Estimated Time: {time_dist['total']} hours")
        print(f"   Target Completion: 2 weeks")
        
        print(f"\n💡 Next Steps:")
        print(f"   1. Review tasks: qtasks")
        print(f"   2. Start working on high-priority items")
        print(f"   3. Mark complete: qdone TASK_OID")
        
        # Save task list for reference
        print(f"\n📝 Task OIDs saved for reference:\n")
        for task in created_tasks[:5]:
            priority_emoji = {1: "🔴", 2: "🟡", 3: "🟢"}
            print(f"   {priority_emoji[task['priority']]} {task['name'][:60]}")
            print(f"      OID: {task['oid']} ({task['hours']}h)")
        
        if len(created_tasks) > 5:
            print(f"\n   ... and {len(created_tasks) - 5} more")
        
        print("\n" + "=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
