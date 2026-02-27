from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Milestone:
    """里程碑模型"""
    id: str
    name: str
    description: str
    due_date: datetime
    status: str  # pending, in_progress, completed
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "due_date": self.due_date.isoformat(),
            "status": self.status,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Milestone":
        """从字典创建"""
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            due_date=datetime.fromisoformat(data["due_date"]),
            status=data["status"],
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None
        )


@dataclass
class Project:
    """项目模型"""
    id: str
    name: str
    description: str
    members: List[str]  # member IDs
    status: str  # active, archived
    milestones: List[Milestone]
    last_updated: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "members": self.members,
            "status": self.status,
            "milestones": [m.to_dict() for m in self.milestones],
            "last_updated": self.last_updated.isoformat(),
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        """从字典创建"""
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            members=data["members"],
            status=data["status"],
            milestones=[Milestone.from_dict(m) for m in data["milestones"]],
            last_updated=datetime.fromisoformat(data.get("last_updated", datetime.now().isoformat())),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        )
