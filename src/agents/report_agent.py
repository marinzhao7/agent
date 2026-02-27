from typing import Dict, Any, List
from datetime import datetime
from src.agents.base_agent import BaseAgent
from src.core import TaskResult
from config.settings import settings
import os


class ReportAgent(BaseAgent):
    """日报生成 Agent"""
    
    def __init__(self):
        """初始化"""
        super().__init__("ReportAgent")
    
    def run(self, action: str, *args, **kwargs) -> TaskResult:
        """运行 Agent"""
        actions = {
            "generate_daily": self.generate_daily_report,
            "get_reports": self.get_reports
        }
        
        if action not in actions:
            return TaskResult.failed(f"未知操作: {action}")
        
        return actions[action](*args, **kwargs)
    
    def generate_daily_report(self) -> TaskResult:
        """生成日报"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            # 收集数据
            report_data = {
                "date": today,
                "generated_at": datetime.now().isoformat(),
                "summary": {
                    "total_members": 0,
                    "active_projects": 0,
                    "completed_milestones": 0,
                    "news_items": 0,
                    "papers": 0
                },
                "system_metrics": {
                    "uptime": "24h",
                    "memory_usage": "45%",
                    "cpu_usage": "30%"
                },
                "events": [],
                "logs": []
            }
            
            # 获取成员数量
            members_result = self.db.get_all_members()
            if members_result:
                report_data["summary"]["total_members"] = len(members_result.data)
            
            # 获取活跃项目数量
            projects_result = self.db.get_all_projects()
            if projects_result:
                active_projects = [p for p in projects_result.data if p.status == "active"]
                report_data["summary"]["active_projects"] = len(active_projects)
                
                # 统计完成的里程碑
                completed_milestones = 0
                for project in projects_result.data:
                    for milestone in project.milestones:
                        if milestone.status == "completed":
                            completed_milestones += 1
                report_data["summary"]["completed_milestones"] = completed_milestones
            
            # 生成 Markdown 报告
            markdown_report = self._generate_markdown(report_data)
            
            # 生成 JSON 报告
            json_report = report_data
            
            # 保存报告
            os.makedirs(settings.REPORT_OUTPUT_PATH, exist_ok=True)
            
            # 保存 Markdown 报告
            md_file_path = os.path.join(settings.REPORT_OUTPUT_PATH, f"report_{today}.md")
            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_report)
            
            # 保存 JSON 报告
            json_file_path = os.path.join(settings.REPORT_OUTPUT_PATH, f"report_{today}.json")
            import json
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(json_report, f, ensure_ascii=False, indent=2, default=str)
            
            # 保存到 JSON 存储
            self.json_store.save_daily_report(json_report)
            
            return self._handle_success({
                "markdown_path": md_file_path,
                "json_path": json_file_path,
                "report": json_report
            }, "生成日报")
        except Exception as e:
            return self._handle_error(e, "生成日报")
    
    def _generate_markdown(self, data: Dict[str, Any]) -> str:
        """生成 Markdown 报告"""
        md = f"# 科研团队管理系统日报\n"
        md += f"日期: {data['date']}\n"
        md += f"生成时间: {data['generated_at']}\n\n"
        
        md += "## 摘要\n"
        md += f"- 总成员数: {data['summary']['total_members']}\n"
        md += f"- 活跃项目数: {data['summary']['active_projects']}\n"
        md += f"- 完成里程碑数: {data['summary']['completed_milestones']}\n"
        md += f"- 新闻条数: {data['summary']['news_items']}\n"
        md += f"- 论文条数: {data['summary']['papers']}\n\n"
        
        md += "## 系统运行指标\n"
        md += f"- 运行时间: {data['system_metrics']['uptime']}\n"
        md += f"- 内存使用率: {data['system_metrics']['memory_usage']}\n"
        md += f"- CPU 使用率: {data['system_metrics']['cpu_usage']}\n\n"
        
        md += "## 今日事件\n"
        if data['events']:
            for event in data['events']:
                md += f"- {event}\n"
        else:
            md += "- 无异常事件\n"
        
        return md
    
    def get_reports(self, days: int = 7) -> TaskResult:
        """获取最近几天的报告"""
        try:
            result = self.json_store.get_daily_reports()
            if not result:
                return result
            
            reports = result.data
            # 按日期排序
            reports.sort(key=lambda x: x.get('date', ''), reverse=True)
            
            # 限制天数
            if days > 0:
                reports = reports[:days]
            
            return self._handle_success(reports, "获取报告")
        except Exception as e:
            return self._handle_error(e, "获取报告")
