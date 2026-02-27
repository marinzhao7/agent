from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """系统配置类"""
    # 数据库配置
    DATABASE_URL: str = "sqlite:///data/db/research_team.db"
    JSON_STORAGE_PATH: str = "data/json/"
    
    # API 配置
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "data/logs/app.log"
    
    # 信息抓取配置
    SCRAPER_INTERVAL_HOURS: int = 24
    ARXIV_CATEGORIES: str = "cs.AI,cs.LG,cs.CL"
    TECHCRUNCH_ENABLED: bool = True
    JIQIZHIXIN_ENABLED: bool = True
    
    # 项目追踪配置
    STAGNATION_DAYS: int = 7
    
    # 日报配置
    REPORT_TIME: str = "24:00"
    REPORT_FORMAT: str = "markdown"
    REPORT_OUTPUT_PATH: str = "data/reports/"
    
    # 监管与自愈配置
    MONITOR_INTERVAL_SECONDS: int = 60
    MAX_RETRIES: int = 3
    AUTO_RESTART_ENABLED: bool = True
    
    # 扩展模块配置（预留）
    MEMORY_ENABLED: bool = False
    VECTOR_DB_TYPE: str = "chroma"
    CHROMA_PATH: str = "data/vectordb/"
    SKILLS_PATH: str = "src/skills/"
    RAG_ENABLED: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
