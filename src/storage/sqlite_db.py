import sqlite3
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from src.models import Member, Project, Milestone, News, Paper
from src.core import TaskResult
from config.settings import settings
from src.utils import logger


class SQLiteStorage:
    """SQLite 存储类"""
    
    def __init__(self, db_path: str = None):
        """初始化"""
        self.db_path = db_path or settings.DATABASE_URL.replace("sqlite:///", "")
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 创建成员表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS members (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    student_id TEXT NOT NULL,
                    email TEXT NOT NULL,
                    research_interests TEXT NOT NULL,
                    personal_website TEXT,
                    github TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # 创建项目表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    members TEXT NOT NULL,
                    status TEXT NOT NULL,
                    milestones TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # 创建新闻表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS news (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    source TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    published_at TEXT NOT NULL,
                    categories TEXT
                )
            ''')
            
            # 创建论文表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS papers (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    arxiv_id TEXT NOT NULL,
                    url TEXT NOT NULL,
                    authors TEXT NOT NULL,
                    abstract TEXT NOT NULL,
                    published_at TEXT NOT NULL,
                    categories TEXT
                )
            ''')
            
            # 创建审计日志表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    action TEXT NOT NULL,
                    status TEXT NOT NULL,
                    details TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("数据库初始化成功")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
    
    def _execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """执行 SQL 查询（用于 INSERT/UPDATE/DELETE）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _query(self, query: str, params: tuple = ()) -> list:
        """执行 SQL 查询（用于 SELECT）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            conn.close()
    
    # 成员管理
    def create_member(self, member: Member) -> TaskResult:
        """创建成员"""
        try:
            query = '''
                INSERT INTO members (id, name, student_id, email, research_interests, personal_website, github, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                member.id,
                member.name,
                member.student_id,
                member.email,
                json.dumps(member.research_interests),
                member.personal_website,
                member.github,
                member.created_at.isoformat(),
                member.updated_at.isoformat()
            )
            self._execute(query, params)
            return TaskResult.success(member)
        except Exception as e:
            return TaskResult.failed(f"创建成员失败: {e}")
    
    def get_member(self, member_id: str) -> TaskResult:
        """获取成员"""
        try:
            query = "SELECT * FROM members WHERE id = ?"
            rows = self._query(query, (member_id,))
            if not rows:
                return TaskResult.failed("成员不存在")
            row = rows[0]
            
            member = Member(
                id=row[0],
                name=row[1],
                student_id=row[2],
                email=row[3],
                research_interests=json.loads(row[4]),
                personal_website=row[5],
                github=row[6],
                created_at=datetime.fromisoformat(row[7]),
                updated_at=datetime.fromisoformat(row[8])
            )
            return TaskResult.success(member)
        except Exception as e:
            return TaskResult.failed(f"获取成员失败: {e}")
    
    def get_all_members(self) -> TaskResult:
        """获取所有成员"""
        try:
            query = "SELECT * FROM members"
            rows = self._query(query)
            
            members = []
            for row in rows:
                member = Member(
                    id=row[0],
                    name=row[1],
                    student_id=row[2],
                    email=row[3],
                    research_interests=json.loads(row[4]),
                    personal_website=row[5],
                    github=row[6],
                    created_at=datetime.fromisoformat(row[7]),
                    updated_at=datetime.fromisoformat(row[8])
                )
                members.append(member)
            
            return TaskResult.success(members)
        except Exception as e:
            return TaskResult.failed(f"获取所有成员失败: {e}")
    
    def update_member(self, member: Member) -> TaskResult:
        """更新成员"""
        try:
            query = '''
                UPDATE members
                SET name = ?, student_id = ?, email = ?, research_interests = ?, 
                    personal_website = ?, github = ?, updated_at = ?
                WHERE id = ?
            '''
            params = (
                member.name,
                member.student_id,
                member.email,
                json.dumps(member.research_interests),
                member.personal_website,
                member.github,
                member.updated_at.isoformat(),
                member.id
            )
            cursor = self._execute(query, params)
            if cursor.rowcount == 0:
                return TaskResult.failed("成员不存在")
            return TaskResult.success(member)
        except Exception as e:
            return TaskResult.failed(f"更新成员失败: {e}")
    
    def delete_member(self, member_id: str) -> TaskResult:
        """删除成员"""
        try:
            query = "DELETE FROM members WHERE id = ?"
            cursor = self._execute(query, (member_id,))
            if cursor.rowcount == 0:
                return TaskResult.failed("成员不存在")
            return TaskResult.success()
        except Exception as e:
            return TaskResult.failed(f"删除成员失败: {e}")
    
    # 项目管理
    def create_project(self, project: Project) -> TaskResult:
        """创建项目"""
        try:
            query = '''
                INSERT INTO projects (id, name, description, members, status, milestones, last_updated, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            milestones_data = [m.to_dict() for m in project.milestones]
            params = (
                project.id,
                project.name,
                project.description,
                json.dumps(project.members),
                project.status,
                json.dumps(milestones_data),
                project.last_updated.isoformat(),
                project.created_at.isoformat()
            )
            self._execute(query, params)
            return TaskResult.success(project)
        except Exception as e:
            return TaskResult.failed(f"创建项目失败: {e}")
    
    def get_project(self, project_id: str) -> TaskResult:
        """获取项目"""
        try:
            query = "SELECT * FROM projects WHERE id = ?"
            rows = self._query(query, (project_id,))
            if not rows:
                return TaskResult.failed("项目不存在")
            row = rows[0]
            
            milestones_data = json.loads(row[5])
            milestones = [Milestone.from_dict(m) for m in milestones_data]
            
            project = Project(
                id=row[0],
                name=row[1],
                description=row[2],
                members=json.loads(row[3]),
                status=row[4],
                milestones=milestones,
                last_updated=datetime.fromisoformat(row[6]),
                created_at=datetime.fromisoformat(row[7])
            )
            return TaskResult.success(project)
        except Exception as e:
            return TaskResult.failed(f"获取项目失败: {e}")
    
    def get_all_projects(self) -> TaskResult:
        """获取所有项目"""
        try:
            query = "SELECT * FROM projects"
            rows = self._query(query)
            
            projects = []
            for row in rows:
                milestones_data = json.loads(row[5])
                milestones = [Milestone.from_dict(m) for m in milestones_data]
                
                project = Project(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    members=json.loads(row[3]),
                    status=row[4],
                    milestones=milestones,
                    last_updated=datetime.fromisoformat(row[6]),
                    created_at=datetime.fromisoformat(row[7])
                )
                projects.append(project)
            
            return TaskResult.success(projects)
        except Exception as e:
            return TaskResult.failed(f"获取所有项目失败: {e}")
    
    def update_project(self, project: Project) -> TaskResult:
        """更新项目"""
        try:
            query = '''
                UPDATE projects
                SET name = ?, description = ?, members = ?, status = ?, 
                    milestones = ?, last_updated = ?
                WHERE id = ?
            '''
            milestones_data = [m.to_dict() for m in project.milestones]
            params = (
                project.name,
                project.description,
                json.dumps(project.members),
                project.status,
                json.dumps(milestones_data),
                project.last_updated.isoformat(),
                project.id
            )
            cursor = self._execute(query, params)
            if cursor.rowcount == 0:
                return TaskResult.failed("项目不存在")
            return TaskResult.success(project)
        except Exception as e:
            return TaskResult.failed(f"更新项目失败: {e}")
    
    def delete_project(self, project_id: str) -> TaskResult:
        """删除项目"""
        try:
            query = "DELETE FROM projects WHERE id = ?"
            cursor = self._execute(query, (project_id,))
            if cursor.rowcount == 0:
                return TaskResult.failed("项目不存在")
            return TaskResult.success()
        except Exception as e:
            return TaskResult.failed(f"删除项目失败: {e}")
    
    # 审计日志
    def add_audit_log(self, agent_name: str, action: str, status: str, details: Optional[str] = None) -> TaskResult:
        """添加审计日志"""
        try:
            import uuid
            log_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            
            query = '''
                INSERT INTO audit_logs (id, timestamp, agent_name, action, status, details)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            params = (log_id, timestamp, agent_name, action, status, details)
            self._execute(query, params)
            return TaskResult.success()
        except Exception as e:
            return TaskResult.failed(f"添加审计日志失败: {e}")
