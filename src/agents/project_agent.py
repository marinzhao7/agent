import uuid
from typing import List, Optional
from datetime import datetime, timedelta
from src.agents.base_agent import BaseAgent
from src.models import Project, Milestone
from src.core import TaskResult
from config.settings import settings


class ProjectAgent(BaseAgent):
    """项目追踪 Agent"""
    
    def __init__(self):
        """初始化"""
        super().__init__("ProjectAgent")
    
    def run(self, action: str, *args, **kwargs) -> TaskResult:
        """运行 Agent"""
        actions = {
            "create": self.create_project,
            "get": self.get_project,
            "get_all": self.get_all_projects,
            "update": self.update_project,
            "delete": self.delete_project,
            "add_milestone": self.add_milestone,
            "update_milestone": self.update_milestone,
            "check_stagnation": self.check_stagnation
        }
        
        if action not in actions:
            return TaskResult.failed(f"未知操作: {action}")
        
        return actions[action](*args, **kwargs)
    
    def create_project(self, name: str, description: str, members: List[str], 
                      milestones: Optional[List[Milestone]] = None) -> TaskResult:
        """创建项目"""
        try:
            project_id = str(uuid.uuid4())
            now = datetime.now()
            
            project = Project(
                id=project_id,
                name=name,
                description=description,
                members=members,
                status="active",
                milestones=milestones or [],
                last_updated=now,
                created_at=now
            )
            
            result = self.db.create_project(project)
            if result:
                return self._handle_success(project, "创建项目")
            else:
                return result
        except Exception as e:
            return self._handle_error(e, "创建项目")
    
    def get_project(self, project_id: str) -> TaskResult:
        """获取项目"""
        try:
            result = self.db.get_project(project_id)
            if result:
                return self._handle_success(result.data, "获取项目")
            else:
                return result
        except Exception as e:
            return self._handle_error(e, "获取项目")
    
    def get_all_projects(self, status: Optional[str] = None) -> TaskResult:
        """获取所有项目"""
        try:
            result = self.db.get_all_projects()
            if not result:
                return result
            
            projects = result.data
            if status:
                projects = [p for p in projects if p.status == status]
            
            return self._handle_success(projects, "获取所有项目")
        except Exception as e:
            return self._handle_error(e, "获取所有项目")
    
    def update_project(self, project_id: str, **kwargs) -> TaskResult:
        """更新项目"""
        try:
            # 先获取现有项目
            result = self.db.get_project(project_id)
            if not result:
                return result
            
            project = result.data
            
            # 更新字段
            for key, value in kwargs.items():
                if hasattr(project, key):
                    setattr(project, key, value)
            
            project.last_updated = datetime.now()
            
            result = self.db.update_project(project)
            if result:
                return self._handle_success(project, "更新项目")
            else:
                return result
        except Exception as e:
            return self._handle_error(e, "更新项目")
    
    def delete_project(self, project_id: str) -> TaskResult:
        """删除项目"""
        try:
            result = self.db.delete_project(project_id)
            if result:
                return self._handle_success(None, "删除项目")
            else:
                return result
        except Exception as e:
            return self._handle_error(e, "删除项目")
    
    def add_milestone(self, project_id: str, name: str, description: str, due_date: datetime) -> TaskResult:
        """添加里程碑"""
        try:
            # 先获取项目
            result = self.db.get_project(project_id)
            if not result:
                return result
            
            project = result.data
            
            # 创建里程碑
            milestone_id = str(uuid.uuid4())
            milestone = Milestone(
                id=milestone_id,
                name=name,
                description=description,
                due_date=due_date,
                status="pending"
            )
            
            project.milestones.append(milestone)
            project.last_updated = datetime.now()
            
            result = self.db.update_project(project)
            if result:
                return self._handle_success(milestone, "添加里程碑")
            else:
                return result
        except Exception as e:
            return self._handle_error(e, "添加里程碑")
    
    def update_milestone(self, project_id: str, milestone_id: str, **kwargs) -> TaskResult:
        """更新里程碑"""
        try:
            # 先获取项目
            result = self.db.get_project(project_id)
            if not result:
                return result
            
            project = result.data
            
            # 找到里程碑
            milestone = None
            for m in project.milestones:
                if m.id == milestone_id:
                    milestone = m
                    break
            
            if not milestone:
                return TaskResult.failed("里程碑不存在")
            
            # 更新里程碑
            for key, value in kwargs.items():
                if hasattr(milestone, key):
                    setattr(milestone, key, value)
            
            # 如果状态变为 completed，设置完成时间
            if kwargs.get("status") == "completed" and not milestone.completed_at:
                milestone.completed_at = datetime.now()
            
            project.last_updated = datetime.now()
            
            result = self.db.update_project(project)
            if result:
                return self._handle_success(milestone, "更新里程碑")
            else:
                return result
        except Exception as e:
            return self._handle_error(e, "更新里程碑")
    
    def check_stagnation(self) -> TaskResult:
        """检查项目进度停滞"""
        try:
            result = self.db.get_all_projects()
            if not result:
                return result
            
            projects = result.data
            stagnated_projects = []
            
            threshold = datetime.now() - timedelta(days=settings.STAGNATION_DAYS)
            
            for project in projects:
                if project.status == "active" and project.last_updated < threshold:
                    stagnated_projects.append({
                        "project_id": project.id,
                        "project_name": project.name,
                        "last_updated": project.last_updated,
                        "days_since_update": (datetime.now() - project.last_updated).days
                    })
            
            if stagnated_projects:
                logger.info(f"检测到 {len(stagnated_projects)} 个项目进度停滞")
                # 这里可以添加提醒逻辑
            
            return self._handle_success(stagnated_projects, "检查项目进度停滞")
        except Exception as e:
            return self._handle_error(e, "检查项目进度停滞")
