from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Member:
    """成员模型"""
    id: str
    name: str
    student_id: str
    email: str
    research_interests: List[str]
    personal_website: Optional[str] = None
    github: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "student_id": self.student_id,
            "email": self.email,
            "research_interests": self.research_interests,
            "personal_website": self.personal_website,
            "github": self.github,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Member":
        """从字典创建"""
        return cls(
            id=data["id"],
            name=data["name"],
            student_id=data["student_id"],
            email=data["email"],
            research_interests=data["research_interests"],
            personal_website=data.get("personal_website"),
            github=data.get("github"),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat()))
        )
