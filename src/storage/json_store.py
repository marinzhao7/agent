import json
import os
from typing import Optional, Dict, Any, List
from datetime import datetime
from src.core import TaskResult
from config.settings import settings
from src.utils import logger


class JSONStorage:
    """JSON 存储类"""
    
    def __init__(self, base_path: str = None):
        """初始化"""
        self.base_path = base_path or settings.JSON_STORAGE_PATH
        os.makedirs(self.base_path, exist_ok=True)
    
    def _get_file_path(self, filename: str) -> str:
        """获取文件路径"""
        return os.path.join(self.base_path, filename)
    
    def read(self, filename: str) -> TaskResult:
        """读取 JSON 文件"""
        try:
            file_path = self._get_file_path(filename)
            if not os.path.exists(file_path):
                return TaskResult.success({})
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return TaskResult.success(data)
        except Exception as e:
            return TaskResult.failed(f"读取 JSON 文件失败: {e}")
    
    def write(self, filename: str, data: Any) -> TaskResult:
        """写入 JSON 文件"""
        try:
            file_path = self._get_file_path(filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            return TaskResult.success()
        except Exception as e:
            return TaskResult.failed(f"写入 JSON 文件失败: {e}")
    
    def update(self, filename: str, key: str, value: Any) -> TaskResult:
        """更新 JSON 文件中的某个键"""
        try:
            result = self.read(filename)
            if not result:
                data = {}
            else:
                data = result.data
            
            data[key] = value
            return self.write(filename, data)
        except Exception as e:
            return TaskResult.failed(f"更新 JSON 文件失败: {e}")
    
    def delete(self, filename: str, key: Optional[str] = None) -> TaskResult:
        """删除 JSON 文件或其中的某个键"""
        try:
            file_path = self._get_file_path(filename)
            if not os.path.exists(file_path):
                return TaskResult.success()
            
            if key:
                result = self.read(filename)
                if result:
                    data = result.data
                    if key in data:
                        del data[key]
                        return self.write(filename, data)
            else:
                os.remove(file_path)
            return TaskResult.success()
        except Exception as e:
            return TaskResult.failed(f"删除 JSON 文件失败: {e}")
    
    # 特定功能
    def save_settings(self, settings_data: Dict[str, Any]) -> TaskResult:
        """保存设置"""
        return self.write('settings.json', settings_data)
    
    def get_settings(self) -> TaskResult:
        """获取设置"""
        return self.read('settings.json')
    
    def save_scraper_state(self, state: Dict[str, Any]) -> TaskResult:
        """保存抓取器状态"""
        return self.write('scraper_state.json', state)
    
    def get_scraper_state(self) -> TaskResult:
        """获取抓取器状态"""
        return self.read('scraper_state.json')
    
    def save_daily_report(self, report: Dict[str, Any]) -> TaskResult:
        """保存日报"""
        filename = f"report_{datetime.now().strftime('%Y%m%d')}.json"
        return self.write(filename, report)
    
    def get_daily_reports(self) -> TaskResult:
        """获取所有日报"""
        try:
            reports = []
            for filename in os.listdir(self.base_path):
                if filename.startswith('report_') and filename.endswith('.json'):
                    result = self.read(filename)
                    if result:
                        reports.append(result.data)
            return TaskResult.success(reports)
        except Exception as e:
            return TaskResult.failed(f"获取日报失败: {e}")
