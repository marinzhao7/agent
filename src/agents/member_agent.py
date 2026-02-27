import uuid
from typing import List, Optional
from datetime import datetime
from src.agents.base_agent import BaseAgent
from src.models import Member
from src.core import TaskResult


class MemberAgent(BaseAgent):
    """成员注册 Agent"""
    
    def __init__(self):
        """初始化"""
        super().__init__("MemberAgent")
    
    def run(self, action: str, *args, **kwargs) -> TaskResult:
        """运行 Agent"""
        actions = {
            "create": self.create_member,
            "get": self.get_member,
            "get_all": self.get_all_members,
            "update": self.update_member,
            "delete": self.delete_member
        }
        
        if action not in actions:
            return TaskResult.failed(f"未知操作: {action}")
        
        return actions[action](*args, **kwargs)
    
    def create_member(self, name: str, student_id: str, email: str, research_interests: List[str], 
                      personal_website: Optional[str] = None, github: Optional[str] = None) -> TaskResult:
        """创建成员"""
        try:
            member_id = str(uuid.uuid4())
            now = datetime.now()
            
            member = Member(
                id=member_id,
                name=name,
                student_id=student_id,
                email=email,
                research_interests=research_interests,
                personal_website=personal_website,
                github=github,
                created_at=now,
                updated_at=now
            )
            
            result = self.db.create_member(member)
            if result:
                return self._handle_success(member, "创建成员")
            else:
                return result
        except Exception as e:
            return self._handle_error(e, "创建成员")
    
    def get_member(self, member_id: str) -> TaskResult:
        """获取成员"""
        try:
            result = self.db.get_member(member_id)
            if result:
                return self._handle_success(result.data, "获取成员")
            else:
                return result
        except Exception as e:
            return self._handle_error(e, "获取成员")
    
    def get_all_members(self) -> TaskResult:
        """获取所有成员"""
        try:
            result = self.db.get_all_members()
            if result:
                return self._handle_success(result.data, "获取所有成员")
            else:
                return result
        except Exception as e:
            return self._handle_error(e, "获取所有成员")
    
    def update_member(self, member_id: str, **kwargs) -> TaskResult:
        """更新成员"""
        try:
            # 先获取现有成员
            result = self.db.get_member(member_id)
            if not result:
                return result
            
            member = result.data
            
            # 更新字段
            for key, value in kwargs.items():
                if hasattr(member, key):
                    setattr(member, key, value)
            
            member.updated_at = datetime.now()
            
            result = self.db.update_member(member)
            if result:
                return self._handle_success(member, "更新成员")
            else:
                return result
        except Exception as e:
            return self._handle_error(e, "更新成员")
    
    def delete_member(self, member_id: str) -> TaskResult:
        """删除成员"""
        try:
            result = self.db.delete_member(member_id)
            if result:
                return self._handle_success(None, "删除成员")
            else:
                return result
        except Exception as e:
            return self._handle_error(e, "删除成员")
