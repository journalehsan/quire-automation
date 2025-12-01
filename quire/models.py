"""
Data models for Quire API responses
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """Quire user model"""
    id: str
    oid: str
    name: str
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Create User from API response"""
        return cls(
            id=data.get("id", ""),
            oid=data.get("oid", ""),
            name=data.get("name", ""),
            email=data.get("email"),
            website=data.get("website"),
            description=data.get("description"),
            image=data.get("image"),
        )


@dataclass
class Project:
    """Quire project model"""
    id: str
    oid: str
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    archived: bool = False
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """Create Project from API response"""
        return cls(
            id=data.get("id", ""),
            oid=data.get("oid", ""),
            name=data.get("name", ""),
            description=data.get("description"),
            color=data.get("color"),
            archived=data.get("archived", False),
        )


@dataclass
class Task:
    """Quire task model"""
    id: str
    oid: str
    name: str
    description: Optional[str] = None
    status: Optional[int] = None
    priority: Optional[int] = None
    start: Optional[str] = None
    due: Optional[str] = None
    assignees: List[User] = None
    tags: List[str] = None
    completed: bool = False
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create Task from API response"""
        assignees = []
        if data.get("assignees"):
            assignees = [User.from_dict(a) for a in data["assignees"]]
        
        return cls(
            id=data.get("id", ""),
            oid=data.get("oid", ""),
            name=data.get("name", ""),
            description=data.get("description"),
            status=data.get("status"),
            priority=data.get("priority"),
            start=data.get("start"),
            due=data.get("due"),
            assignees=assignees,
            tags=data.get("tags", []),
            completed=data.get("status") == 10,  # 10 is typically "Done"
        )
    
    def __str__(self) -> str:
        status_icon = "✅" if self.completed else "⏳"
        return f"{status_icon} [{self.oid}] {self.name}"


@dataclass
class Comment:
    """Quire comment model"""
    id: str
    oid: str
    content: str
    user: User
    created_at: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Comment":
        """Create Comment from API response"""
        user = User.from_dict(data.get("user", {}))
        return cls(
            id=data.get("id", ""),
            oid=data.get("oid", ""),
            content=data.get("description", ""),
            user=user,
            created_at=data.get("createdAt", ""),
        )
