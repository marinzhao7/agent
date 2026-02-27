from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from src.agents import MemberAgent, ProjectAgent, ScraperAgent, ReportAgent
from src.core import TaskResult
import asyncio

router = APIRouter()

# 初始化 Agent
member_agent = MemberAgent()
project_agent = ProjectAgent()
scraper_agent = ScraperAgent()
report_agent = ReportAgent()

# Pydantic 模型
class MemberCreate(BaseModel):
    name: str
    student_id: str
    email: str
    research_interests: List[str]
    personal_website: Optional[str] = None
    github: Optional[str] = None

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    student_id: Optional[str] = None
    email: Optional[str] = None
    research_interests: Optional[List[str]] = None
    personal_website: Optional[str] = None
    github: Optional[str] = None

class ProjectCreate(BaseModel):
    name: str
    description: str
    members: List[str]

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    members: Optional[List[str]] = None
    status: Optional[str] = None

class MilestoneCreate(BaseModel):
    name: str
    description: str
    due_date: str  # ISO format

class MilestoneUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None

# 成员管理路由
@router.post("/members")
async def create_member(member: MemberCreate):
    """创建成员"""
    result = member_agent.run(
        "create",
        name=member.name,
        student_id=member.student_id,
        email=member.email,
        research_interests=member.research_interests,
        personal_website=member.personal_website,
        github=member.github
    )
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

@router.get("/members")
async def get_all_members():
    """获取所有成员"""
    result = member_agent.run("get_all")
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

@router.get("/members/{member_id}")
async def get_member(member_id: str):
    """获取单个成员"""
    result = member_agent.run("get", member_id)
    if not result:
        raise HTTPException(status_code=404, detail=result.error_msg)
    return result.data

@router.put("/members/{member_id}")
async def update_member(member_id: str, member: MemberUpdate):
    """更新成员"""
    result = member_agent.run("update", member_id, **member.model_dump(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

@router.delete("/members/{member_id}")
async def delete_member(member_id: str):
    """删除成员"""
    result = member_agent.run("delete", member_id)
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return {"message": "成员删除成功"}

# 项目管理路由
@router.post("/projects")
async def create_project(project: ProjectCreate):
    """创建项目"""
    result = project_agent.run(
        "create",
        name=project.name,
        description=project.description,
        members=project.members
    )
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

@router.get("/projects")
async def get_all_projects(status: Optional[str] = None):
    """获取所有项目"""
    result = project_agent.run("get_all", status=status)
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

@router.get("/projects/{project_id}")
async def get_project(project_id: str):
    """获取单个项目"""
    result = project_agent.run("get", project_id)
    if not result:
        raise HTTPException(status_code=404, detail=result.error_msg)
    return result.data

@router.put("/projects/{project_id}")
async def update_project(project_id: str, project: ProjectUpdate):
    """更新项目"""
    result = project_agent.run("update", project_id, **project.model_dump(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

@router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    """删除项目"""
    result = project_agent.run("delete", project_id)
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return {"message": "项目删除成功"}

# 里程碑路由
@router.post("/projects/{project_id}/milestones")
async def add_milestone(project_id: str, milestone: MilestoneCreate):
    """添加里程碑"""
    from datetime import datetime
    due_date = datetime.fromisoformat(milestone.due_date)
    result = project_agent.run(
        "add_milestone",
        project_id=project_id,
        name=milestone.name,
        description=milestone.description,
        due_date=due_date
    )
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

@router.put("/projects/{project_id}/milestones/{milestone_id}")
async def update_milestone(project_id: str, milestone_id: str, milestone: MilestoneUpdate):
    """更新里程碑"""
    update_data = milestone.model_dump(exclude_unset=True)
    if "due_date" in update_data:
        from datetime import datetime
        update_data["due_date"] = datetime.fromisoformat(update_data["due_date"])
    
    result = project_agent.run(
        "update_milestone",
        project_id=project_id,
        milestone_id=milestone_id,
        **update_data
    )
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

# 项目状态检查
@router.get("/projects/check-stagnation")
async def check_project_stagnation():
    """检查项目进度停滞"""
    result = project_agent.run("check_stagnation")
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

# 信息抓取路由
@router.post("/scraper/scrape-all")
async def scrape_all():
    """抓取所有信息"""
    result = await scraper_agent.run("scrape_all")
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

@router.post("/scraper/scrape-techcrunch")
async def scrape_techcrunch():
    """抓取 TechCrunch 新闻"""
    result = await scraper_agent.run("scrape_techcrunch")
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

@router.post("/scraper/scrape-jiqizhixin")
async def scrape_jiqizhixin():
    """抓取机器之心新闻"""
    result = await scraper_agent.run("scrape_jiqizhixin")
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

@router.post("/scraper/scrape-arxiv")
async def scrape_arxiv():
    """抓取 arXiv 论文"""
    result = await scraper_agent.run("scrape_arxiv")
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

@router.get("/scraper/personalize/{member_id}")
async def personalize_content(member_id: str):
    """个性化内容"""
    result = scraper_agent.personalize_content(member_id)
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

# 日报路由
@router.post("/reports/generate")
async def generate_daily_report():
    """生成日报"""
    result = report_agent.run("generate_daily")
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data

@router.get("/reports")
async def get_reports(days: int = 7):
    """获取最近的日报"""
    result = report_agent.run("get_reports", days=days)
    if not result:
        raise HTTPException(status_code=400, detail=result.error_msg)
    return result.data
