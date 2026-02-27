import pytest
from datetime import datetime, timedelta
from src.agents import ProjectAgent, MemberAgent
from src.core import TaskResult


@pytest.fixture
def project_agent():
    """项目 Agent fixture"""
    return ProjectAgent()


@pytest.fixture
def member_agent():
    """成员 Agent fixture"""
    return MemberAgent()


def test_create_project(project_agent, member_agent):
    """测试创建项目"""
    # 先创建一些成员
    member1 = member_agent.run(
        "create",
        name="张三",
        student_id="20230001",
        email="zhangsan@example.com",
        research_interests=["AI"]
    )
    member2 = member_agent.run(
        "create",
        name="李四",
        student_id="20230002",
        email="lisi@example.com",
        research_interests=["ML"]
    )
    
    # 创建项目
    result = project_agent.run(
        "create",
        name="AI 研究项目",
        description="研究人工智能的应用",
        members=[member1.data.id, member2.data.id]
    )
    assert result.status == "success"
    assert result.data.name == "AI 研究项目"
    assert len(result.data.members) == 2


def test_get_project(project_agent, member_agent):
    """测试获取项目"""
    # 先创建项目
    member = member_agent.run(
        "create",
        name="张三",
        student_id="20230001",
        email="zhangsan@example.com",
        research_interests=["AI"]
    )
    
    create_result = project_agent.run(
        "create",
        name="测试项目",
        description="测试项目描述",
        members=[member.data.id]
    )
    project_id = create_result.data.id
    
    # 获取项目
    get_result = project_agent.run("get", project_id)
    assert get_result.status == "success"
    assert get_result.data.name == "测试项目"


def test_get_all_projects(project_agent, member_agent):
    """测试获取所有项目"""
    # 先创建项目
    member = member_agent.run(
        "create",
        name="张三",
        student_id="20230001",
        email="zhangsan@example.com",
        research_interests=["AI"]
    )
    
    project_agent.run(
        "create",
        name="项目 1",
        description="项目 1 描述",
        members=[member.data.id]
    )
    
    project_agent.run(
        "create",
        name="项目 2",
        description="项目 2 描述",
        members=[member.data.id]
    )
    
    # 获取所有项目
    result = project_agent.run("get_all")
    assert result.status == "success"
    assert isinstance(result.data, list)
    assert len(result.data) >= 2


def test_add_milestone(project_agent, member_agent):
    """测试添加里程碑"""
    # 先创建项目
    member = member_agent.run(
        "create",
        name="张三",
        student_id="20230001",
        email="zhangsan@example.com",
        research_interests=["AI"]
    )
    
    create_result = project_agent.run(
        "create",
        name="带里程碑的项目",
        description="测试里程碑功能",
        members=[member.data.id]
    )
    project_id = create_result.data.id
    
    # 添加里程碑
    due_date = datetime.now() + timedelta(days=30)
    milestone_result = project_agent.run(
        "add_milestone",
        project_id=project_id,
        name="里程碑 1",
        description="完成项目设计",
        due_date=due_date
    )
    assert milestone_result.status == "success"
    assert milestone_result.data.name == "里程碑 1"


def test_update_milestone(project_agent, member_agent):
    """测试更新里程碑"""
    # 先创建项目和里程碑
    member = member_agent.run(
        "create",
        name="张三",
        student_id="20230001",
        email="zhangsan@example.com",
        research_interests=["AI"]
    )
    
    create_result = project_agent.run(
        "create",
        name="测试项目",
        description="测试项目",
        members=[member.data.id]
    )
    project_id = create_result.data.id
    
    due_date = datetime.now() + timedelta(days=30)
    milestone_result = project_agent.run(
        "add_milestone",
        project_id=project_id,
        name="里程碑 1",
        description="完成设计",
        due_date=due_date
    )
    milestone_id = milestone_result.data.id
    
    # 更新里程碑
    update_result = project_agent.run(
        "update_milestone",
        project_id=project_id,
        milestone_id=milestone_id,
        status="completed"
    )
    assert update_result.status == "success"
    assert update_result.data.status == "completed"
