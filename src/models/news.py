from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class News:
    """新闻模型"""
    id: str
    title: str
    url: str
    source: str  # techcrunch, jiqizhixin
    summary: str
    published_at: datetime
    categories: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "summary": self.summary,
            "published_at": self.published_at.isoformat(),
            "categories": self.categories
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "News":
        """从字典创建"""
        return cls(
            id=data["id"],
            title=data["title"],
            url=data["url"],
            source=data["source"],
            summary=data["summary"],
            published_at=datetime.fromisoformat(data["published_at"]),
            categories=data.get("categories", [])
        )


@dataclass
class Paper:
    """论文模型"""
    id: str
    title: str
    arxiv_id: str
    url: str
    authors: List[str]
    abstract: str
    published_at: datetime
    categories: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "arxiv_id": self.arxiv_id,
            "url": self.url,
            "authors": self.authors,
            "abstract": self.abstract,
            "published_at": self.published_at.isoformat(),
            "categories": self.categories
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Paper":
        """从字典创建"""
        return cls(
            id=data["id"],
            title=data["title"],
            arxiv_id=data["arxiv_id"],
            url=data["url"],
            authors=data["authors"],
            abstract=data["abstract"],
            published_at=datetime.fromisoformat(data["published_at"]),
            categories=data.get("categories", [])
        )
