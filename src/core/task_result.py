from typing import Any, Optional, Literal
from dataclasses import dataclass


@dataclass
class TaskResult:
    """任务结果类"""
    status: Literal["success", "failed", "partial"]
    data: Any = None
    error_msg: Optional[str] = None
    
    def __bool__(self) -> bool:
        """返回结果是否成功"""
        return self.status == "success"
    
    @classmethod
    def success(cls, data: Any = None) -> "TaskResult":
        """创建成功结果"""
        return cls(status="success", data=data)
    
    @classmethod
    def failed(cls, error_msg: str, data: Any = None) -> "TaskResult":
        """创建失败结果"""
        return cls(status="failed", data=data, error_msg=error_msg)
    
    @classmethod
    def partial(cls, data: Any = None, error_msg: Optional[str] = None) -> "TaskResult":
        """创建部分成功结果"""
        return cls(status="partial", data=data, error_msg=error_msg)
