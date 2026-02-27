from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from src.core import TaskResult
from src.storage import SQLiteStorage, JSONStorage
from src.utils import logger


class BaseAgent(ABC):
    """Agent 基类"""
    
    def __init__(self, name: str):
        """初始化"""
        self.name = name
        self.db = SQLiteStorage()
        self.json_store = JSONStorage()
        logger.info(f"初始化 Agent: {self.name}")
    
    @abstractmethod
    def run(self, *args, **kwargs) -> TaskResult:
        """运行 Agent"""
        pass
    
    def _log_audit(self, action: str, status: str, details: Optional[str] = None) -> None:
        """记录审计日志"""
        self.db.add_audit_log(
            agent_name=self.name,
            action=action,
            status=status,
            details=details
        )
    
    def _handle_error(self, error: Exception, action: str) -> TaskResult:
        """处理错误"""
        error_msg = f"{action} 失败: {str(error)}"
        logger.error(error_msg)
        self._log_audit(action, "failed", error_msg)
        return TaskResult.failed(error_msg)
    
    def _handle_success(self, data: Any = None, action: str = "操作") -> TaskResult:
        """处理成功"""
        logger.info(f"{action} 成功")
        self._log_audit(action, "success")
        return TaskResult.success(data)
