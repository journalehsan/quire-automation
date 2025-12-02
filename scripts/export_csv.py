#!/usr/bin/env python3
"""
Export changelog tasks to CSV for Quire import
Since OAuth app creation requires specific account permissions,
this creates a CSV file you can import directly into Quire.
"""
import csv
from datetime import datetime, timedelta
from pathlib import Path

# The 23 tasks from changelogs with time estimates and priorities
TASKS = [
    # Week 1 - High Priority (34 hours total)
    {"name": "Custom fields system - Backend & Frontend", "priority": "High", "hours": 8, "tags": "backend,frontend", "week": 1},
    {"name": "Custom field validation & API integration", "priority": "High", "hours": 6, "tags": "backend,api", "week": 1},
    {"name": "Teams feature implementation", "priority": "High", "hours": 6, "tags": "feature,backend", "week": 1},
    {"name": "Employee profile page development", "priority": "High", "hours": 8, "tags": "frontend,profile", "week": 1},
    {"name": "Multi-language i18n system", "priority": "High", "hours": 6, "tags": "frontend,i18n", "week": 1},
    
    # Week 1-2 - Medium Priority (49 hours total)
    {"name": "RTL support for Arabic/Farsi", "priority": "Medium", "hours": 8, "tags": "frontend,rtl", "week": 1},
    {"name": "Navigation i18n implementation", "priority": "Medium", "hours": 6, "tags": "frontend,i18n", "week": 1},
    {"name": "Employee login system", "priority": "Medium", "hours": 6, "tags": "auth,backend", "week": 1},
    {"name": "Custom fields UI refactoring", "priority": "Medium", "hours": 4, "tags": "frontend,refactor", "week": 1},
    {"name": "Logout functionality for employees", "priority": "Medium", "hours": 2, "tags": "auth,frontend", "week": 1},
    {"name": "Profile section styling improvements", "priority": "Medium", "hours": 3, "tags": "frontend,ui", "week": 2},
    {"name": "Employee dashboard layout", "priority": "Medium", "hours": 4, "tags": "frontend,dashboard", "week": 2},
    {"name": "Login page improvements", "priority": "Medium", "hours": 3, "tags": "frontend,auth", "week": 2},
    {"name": "Database schema updates", "priority": "Medium", "hours": 4, "tags": "backend,database", "week": 2},
    {"name": "Infinite loop bug fixes", "priority": "Medium", "hours": 3, "tags": "bugfix,frontend", "week": 2},
    {"name": "Navigation cleanup", "priority": "Medium", "hours": 2, "tags": "frontend,cleanup", "week": 2},
    {"name": "Conditional rendering fixes", "priority": "Medium", "hours": 2, "tags": "frontend,bugfix", "week": 2},
    {"name": "Dual login system setup", "priority": "Medium", "hours": 2, "tags": "auth,backend", "week": 2},
    
    # Week 2 - Low Priority (18 hours total)
    {"name": "Custom fields management UI", "priority": "Low", "hours": 4, "tags": "frontend,ui", "week": 2},
    {"name": "Teams data migration", "priority": "Low", "hours": 3, "tags": "backend,migration", "week": 2},
    {"name": "Login debugging & testing", "priority": "Low", "hours": 3, "tags": "testing,auth", "week": 2},
    {"name": "RTL testing & validation", "priority": "Low", "hours": 3, "tags": "testing,rtl", "week": 2},
    {"name": "UI polish & improvements", "priority": "Low", "hours": 3, "tags": "frontend,polish", "week": 2},
    {"name": "Documentation updates", "priority": "Low", "hours": 2, "tags": "docs", "week": 2},
]

def export_to_csv():
    """Export tasks to Quire-compatible CSV format"""
    
    output_file = Path(__file__).parent.parent / "quire_tasks_import.csv"
    
    # Calculate due dates
    start_date = datetime.now()
    
    # Quire CSV format
    fieldnames = [
        "Task Name",
        "Priority",
        "Tags",
        "Due Date",
        "Time Estimate (hours)",
        "Description",
        "Status"
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for task in TASKS:
            # Calculate due date based on week
            week_offset = (task["week"] - 1) * 7
            due_date = start_date + timedelta(days=week_offset + 5)  # Friday of that week
            
            # Priority mapping
            priority_value = {
                "High": "1",
                "Medium": "0", 
                "Low": "-1"
            }[task["priority"]]
            
            # Description with details
            description = f"Estimated: {task['hours']} hours\nWeek {task['week']}\nPriority: {task['priority']}"
            
            writer.writerow({
                "Task Name": task["name"],
                "Priority": priority_value,
                "Tags": task["tags"],
                "Due Date": due_date.strftime("%Y-%m-%d"),
                "Time Estimate (hours)": task["hours"],
                "Description": description,
                "Status": "0"  # Not started
            })
    
    return output_file

def main():
    print("=" * 80)
    print("  📤 Exporting Tasks to CSV for Quire Import")
    print("=" * 80)
    print()
    print(f"Creating CSV with {len(TASKS)} tasks...")
    print()
    
    output_file = export_to_csv()
    
    print(f"✅ CSV file created: {output_file}")
    print()
    print("=" * 80)
    print("  📋 How to Import to Quire")
    print("=" * 80)
    print()
    print("1. Open your HRMS project in Quire:")
    print("   https://quire.io/w/PMO436/5550")
    print()
    print("2. Click the '⋮' (three dots) menu in the top-right")
    print()
    print("3. Select 'Import' → 'CSV'")
    print()
    print("4. Upload the file:")
    print(f"   {output_file}")
    print()
    print("5. Map the columns:")
    print("   - Task Name → Name")
    print("   - Priority → Priority")
    print("   - Tags → Tags")
    print("   - Due Date → Due")
    print("   - Time Estimate → Time Estimate")
    print("   - Description → Description")
    print()
    print("6. Click 'Import' and you're done!")
    print()
    print("=" * 80)
    print()
    print("📊 Task Summary:")
    print(f"   Total Tasks: {len(TASKS)}")
    print(f"   Total Hours: {sum(t['hours'] for t in TASKS)}")
    print(f"   High Priority: {len([t for t in TASKS if t['priority'] == 'High'])}")
    print(f"   Medium Priority: {len([t for t in TASKS if t['priority'] == 'Medium'])}")
    print(f"   Low Priority: {len([t for t in TASKS if t['priority'] == 'Low'])}")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
