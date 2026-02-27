import pytest
from src.agents import MemberAgent
from src.core import TaskResult


@pytest.fixture
def member_agent():
    """成员 Agent  fixture"""
    return MemberAgent()


def test_create_member(member_agent):
    """测试创建成员"""
    result = member_agent.run(
        "create",
        name="张三",
        student_id="20230001",
        email="zhangsan@example.com",
        research_interests=["AI", "Machine Learning"]
    )
    assert isinstance(result, TaskResult)
    assert result.status == "success"
    assert result.data.name == "张三"
    assert result.data.student_id == "20230001"


def test_get_member(member_agent):
    """测试获取成员"""
    # 先创建成员
    create_result = member_agent.run(
        "create",
        name="李四",
        student_id="20230002",
        email="lisi@example.com",
        research_interests=["NLP", "Computer Vision"]
    )
    member_id = create_result.data.id
    
    # 获取成员
    get_result = member_agent.run("get", member_id)
    assert get_result.status == "success"
    assert get_result.data.name == "李四"


def test_get_all_members(member_agent):
    """测试获取所有成员"""
    result = member_agent.run("get_all")
    assert result.status == "success"
    assert isinstance(result.data, list)


def test_update_member(member_agent):
    """测试更新成员"""
    # 先创建成员
    create_result = member_agent.run(
        "create",
        name="王五",
        student_id="20230003",
        email="wangwu@example.com",
        research_interests=["Reinforcement Learning"]
    )
    member_id = create_result.data.id
    
    # 更新成员
    update_result = member_agent.run(
        "update",
        member_id,
        name="王五（更新）",
        github="https://github.com/wangwu"
    )
    assert update_result.status == "success"
    assert update_result.data.name == "王五（更新）"
    assert update_result.data.github == "https://github.com/wangwu"


def test_delete_member(member_agent):
    """测试删除成员"""
    # 先创建成员
    create_result = member_agent.run(
        "create",
        name="赵六",
        student_id="20230004",
        email="zhaoliu@example.com",
        research_interests=["Robotics"]
    )
    member_id = create_result.data.id
    
    # 删除成员
    delete_result = member_agent.run("delete", member_id)
    assert delete_result.status == "success"
    
    # 验证成员已删除
    get_result = member_agent.run("get", member_id)
    assert get_result.status == "failed"
