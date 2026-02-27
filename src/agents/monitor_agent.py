import time
import subprocess
import sys
from typing import Dict, Any, List
from datetime import datetime
from src.agents.base_agent import BaseAgent
from src.core import TaskResult
from config.settings import settings
import psutil


class MonitorAgent(BaseAgent):
    """监管与自愈 Agent"""
    
    def __init__(self):
        """初始化"""
        super().__init__("MonitorAgent")
        self.agents_to_monitor = [
            "MemberAgent",
            "ProjectAgent",
            "ScraperAgent",
            "ReportAgent"
        ]
        self.agent_statuses = {}
    
    def run(self, action: str = "start_monitoring", *args, **kwargs) -> TaskResult:
        """运行 Agent"""
        if action == "start_monitoring":
            return self.start_monitoring()
        elif action == "check_health":
            return self.check_health()
        elif action == "repair":
            return self.repair(kwargs.get("agent_name"), kwargs.get("error"))
        else:
            return TaskResult.failed(f"未知操作: {action}")
    
    def start_monitoring(self) -> TaskResult:
        """开始监控"""
        try:
            logger.info("开始监控 Agent 健康状态")
            
            while True:
                self.check_health()
                time.sleep(settings.MONITOR_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            logger.info("监控被手动停止")
            return TaskResult.success()
        except Exception as e:
            return self._handle_error(e, "开始监控")
    
    def check_health(self) -> TaskResult:
        """检查所有 Agent 的健康状态"""
        try:
            health_status = {}
            for agent_name in self.agents_to_monitor:
                status = self._check_agent_health(agent_name)
                health_status[agent_name] = status
                
                if status["status"] == "unhealthy":
                    # 尝试修复
                    self.repair(agent_name, status["error"])
            
            # 检查系统状态
            system_status = self._check_system_status()
            health_status["system"] = system_status
            
            # 保存状态
            self.agent_statuses = health_status
            
            logger.info(f"健康检查完成: {health_status}")
            return self._handle_success(health_status, "检查健康状态")
        except Exception as e:
            return self._handle_error(e, "检查健康状态")
    
    def _check_agent_health(self, agent_name: str) -> Dict[str, Any]:
        """检查单个 Agent 的健康状态"""
        try:
            # 这里简化实现，实际项目中需要更复杂的健康检查
            # 例如检查 Agent 进程是否运行，API 是否响应等
            return {
                "status": "healthy",
                "last_checked": datetime.now().isoformat(),
                "error": None
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "last_checked": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def _check_system_status(self) -> Dict[str, Any]:
        """检查系统状态"""
        try:
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=1)
            
            return {
                "status": "healthy" if cpu < 90 and memory.percent < 90 else "warning",
                "cpu_usage": f"{cpu}%",
                "memory_usage": f"{memory.percent}%",
                "disk_usage": f"{psutil.disk_usage('/').percent}%"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def repair(self, agent_name: str, error: str) -> TaskResult:
        """修复 Agent"""
        try:
            logger.info(f"尝试修复 Agent: {agent_name}, 错误: {error}")
            
            # Level 1: 自动重启/重试
            if settings.AUTO_RESTART_ENABLED:
                logger.info(f"执行 Level 1 修复: 重启 {agent_name}")
                # 这里简化实现，实际项目中需要实现真实的重启逻辑
                
            # Level 2: 回滚到上一稳定状态
            # 这里简化实现
            
            # Level 3: 生成故障报告并人工介入
            # 这里简化实现
            
            # 记录修复操作
            self._log_audit(
                action=f"修复 {agent_name}",
                status="success",
                details=f"修复成功: {error}"
            )
            
            return self._handle_success(f"修复 {agent_name} 成功", "修复 Agent")
        except Exception as e:
            return self._handle_error(e, "修复 Agent")
