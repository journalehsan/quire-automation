"""
Main Quire API client
"""

import os
import requests
from typing import List, Optional, Dict, Any
from .auth import QuireAuth
from .models import Project, Task, User, Comment


class QuireClient:
    """Main client for interacting with Quire API"""
    
    def __init__(
        self,
        auth: Optional[QuireAuth] = None,
        api_base: Optional[str] = None,
    ):
        """
        Initialize Quire API client
        
        Args:
            auth: QuireAuth instance (creates new one if not provided)
            api_base: API base URL (default: https://quire.io/api)
        """
        self.auth = auth or QuireAuth()
        self.api_base = api_base or os.getenv("QUIRE_API_BASE", "https://quire.io/api")
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Any:
        """
        Make authenticated API request
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without base URL)
            data: JSON body for POST/PUT
            params: URL query parameters
            
        Returns:
            JSON response
        """
        url = f"{self.api_base}/{endpoint.lstrip('/')}"
        headers = {
            **self.auth.get_auth_headers(),
            "Content-Type": "application/json",
        }
        
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
            params=params,
        )
        
        response.raise_for_status()
        return response.json()
    
    # User methods
    
    def get_current_user(self) -> User:
        """Get currently authenticated user"""
        data = self._request("GET", "/user/id/me")
        return User.from_dict(data)
    
    # Project methods
    
    def list_projects(self) -> List[Project]:
        """List all projects accessible to the user"""
        data = self._request("GET", "/project/list")
        return [Project.from_dict(p) for p in data]
    
    def get_project(self, project_oid: str) -> Project:
        """
        Get project by OID
        
        Args:
            project_oid: Project OID
            
        Returns:
            Project instance
        """
        data = self._request("GET", f"/project/id/{project_oid}")
        return Project.from_dict(data)
    
    # Task methods
    
    def list_tasks(
        self,
        project_oid: str,
        status: Optional[int] = None,
        assignee: Optional[str] = None,
    ) -> List[Task]:
        """
        List tasks in a project
        
        Args:
            project_oid: Project OID
            status: Filter by status code (optional)
            assignee: Filter by assignee OID (optional)
            
        Returns:
            List of Task instances
        """
        params = {}
        if status is not None:
            params["status"] = status
        if assignee:
            params["assignee"] = assignee
        
        data = self._request("GET", f"/project/id/{project_oid}/task/list", params=params)
        return [Task.from_dict(t) for t in data]
    
    def get_task(self, task_oid: str) -> Task:
        """
        Get task by OID
        
        Args:
            task_oid: Task OID
            
        Returns:
            Task instance
        """
        data = self._request("GET", f"/task/id/{task_oid}")
        return Task.from_dict(data)
    
    def create_task(
        self,
        project_oid: str,
        name: str,
        description: Optional[str] = None,
        assignee: Optional[str] = None,
        status: Optional[int] = None,
        priority: Optional[int] = None,
        start: Optional[str] = None,
        due: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Task:
        """
        Create a new task
        
        Args:
            project_oid: Project OID to create task in
            name: Task name
            description: Task description (optional)
            assignee: Assignee user OID (optional)
            status: Status code (optional)
            priority: Priority level (optional)
            start: Start date (ISO format, optional)
            due: Due date (ISO format, optional)
            tags: List of tag names (optional)
            
        Returns:
            Created Task instance
        """
        task_data = {"name": name}
        
        if description:
            task_data["description"] = description
        if assignee:
            task_data["assignee"] = assignee
        if status is not None:
            task_data["status"] = status
        if priority is not None:
            task_data["priority"] = priority
        if start:
            task_data["start"] = start
        if due:
            task_data["due"] = due
        if tags:
            task_data["tags"] = tags
        
        data = self._request("POST", f"/project/id/{project_oid}/task", data=task_data)
        return Task.from_dict(data)
    
    def update_task(
        self,
        task_oid: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[int] = None,
        priority: Optional[int] = None,
        start: Optional[str] = None,
        due: Optional[str] = None,
        assignee: Optional[str] = None,
    ) -> Task:
        """
        Update an existing task
        
        Args:
            task_oid: Task OID to update
            name: New task name (optional)
            description: New description (optional)
            status: New status code (optional)
            priority: New priority (optional)
            start: New start date (optional)
            due: New due date (optional)
            assignee: New assignee OID (optional)
            
        Returns:
            Updated Task instance
        """
        update_data = {}
        
        if name:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if status is not None:
            update_data["status"] = status
        if priority is not None:
            update_data["priority"] = priority
        if start:
            update_data["start"] = start
        if due:
            update_data["due"] = due
        if assignee:
            update_data["assignee"] = assignee
        
        data = self._request("PUT", f"/task/id/{task_oid}", data=update_data)
        return Task.from_dict(data)
    
    def delete_task(self, task_oid: str) -> bool:
        """
        Delete a task
        
        Args:
            task_oid: Task OID to delete
            
        Returns:
            True if successful
        """
        self._request("DELETE", f"/task/id/{task_oid}")
        return True
    
    # Comment methods
    
    def add_comment(self, task_oid: str, content: str) -> Comment:
        """
        Add a comment to a task
        
        Args:
            task_oid: Task OID
            content: Comment content
            
        Returns:
            Created Comment instance
        """
        data = self._request(
            "POST",
            f"/task/id/{task_oid}/comment",
            data={"description": content}
        )
        return Comment.from_dict(data)
    
    def list_comments(self, task_oid: str) -> List[Comment]:
        """
        List comments on a task
        
        Args:
            task_oid: Task OID
            
        Returns:
            List of Comment instances
        """
        data = self._request("GET", f"/task/id/{task_oid}/comment/list")
        return [Comment.from_dict(c) for c in data]
