import uuid
import httpx
from typing import List, Dict, Any
from datetime import datetime, timedelta
from src.agents.base_agent import BaseAgent
from src.models import News, Paper
from src.core import TaskResult
from config.settings import settings
import re


class ScraperAgent(BaseAgent):
    """信息抓取 Agent"""
    
    def __init__(self):
        """初始化"""
        super().__init__("ScraperAgent")
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def run(self, action: str, *args, **kwargs) -> TaskResult:
        """运行 Agent"""
        actions = {
            "scrape_all": self.scrape_all,
            "scrape_techcrunch": self.scrape_techcrunch,
            "scrape_jiqizhixin": self.scrape_jiqizhixin,
            "scrape_arxiv": self.scrape_arxiv
        }
        
        if action not in actions:
            return TaskResult.failed(f"未知操作: {action}")
        
        return await actions[action](*args, **kwargs)
    
    async def scrape_all(self) -> TaskResult:
        """抓取所有信息"""
        try:
            results = []
            
            # 抓取 TechCrunch
            if settings.TECHCRUNCH_ENABLED:
                tc_result = await self.scrape_techcrunch()
                if tc_result:
                    results.extend(tc_result.data or [])
            
            # 抓取机器之心
            if settings.JIQIZHIXIN_ENABLED:
                jqzx_result = await self.scrape_jiqizhixin()
                if jqzx_result:
                    results.extend(jqzx_result.data or [])
            
            # 抓取 arXiv
            arxiv_result = await self.scrape_arxiv()
            if arxiv_result:
                results.extend(arxiv_result.data or [])
            
            # 保存抓取状态
            self.json_store.save_scraper_state({
                "last_scraped": datetime.now().isoformat(),
                "total_items": len(results)
            })
            
            return self._handle_success(results, "抓取所有信息")
        except Exception as e:
            return self._handle_error(e, "抓取所有信息")
    
    async def scrape_techcrunch(self) -> TaskResult:
        """抓取 TechCrunch 新闻"""
        try:
            # 这里使用模拟数据，实际项目中需要实现真实的抓取逻辑
            news_items = [
                News(
                    id=str(uuid.uuid4()),
                    title="OpenAI 发布 GPT-5 预览版",
                    url="https://techcrunch.com/openai-gpt-5-preview/",
                    source="techcrunch",
                    summary="OpenAI 今日发布 GPT-5 预览版，带来更强大的语言理解和生成能力。",
                    published_at=datetime.now() - timedelta(days=1),
                    categories=["AI", "OpenAI"]
                ),
                News(
                    id=str(uuid.uuid4()),
                    title="Google 推出新的 AI 搜索功能",
                    url="https://techcrunch.com/google-ai-search/",
                    source="techcrunch",
                    summary="Google 推出基于 Gemini 的新搜索功能，提供更智能的搜索结果。",
                    published_at=datetime.now() - timedelta(days=2),
                    categories=["AI", "Google"]
                )
            ]
            return self._handle_success(news_items, "抓取 TechCrunch 新闻")
        except Exception as e:
            return self._handle_error(e, "抓取 TechCrunch 新闻")
    
    async def scrape_jiqizhixin(self) -> TaskResult:
        """抓取机器之心新闻"""
        try:
            # 这里使用模拟数据，实际项目中需要实现真实的抓取逻辑
            news_items = [
                News(
                    id=str(uuid.uuid4()),
                    title="国产大模型最新进展：智谱 AI 发布 GLM-4",
                    url="https://www.jiqizhixin.com/articles/2024-01-01",
                    source="jiqizhixin",
                    summary="智谱 AI 发布新一代大语言模型 GLM-4，性能对标 GPT-4。",
                    published_at=datetime.now() - timedelta(days=1),
                    categories=["AI", "国产大模型"]
                )
            ]
            return self._handle_success(news_items, "抓取机器之心新闻")
        except Exception as e:
            return self._handle_error(e, "抓取机器之心新闻")
    
    async def scrape_arxiv(self) -> TaskResult:
        """抓取 arXiv 论文"""
        try:
            # 这里使用模拟数据，实际项目中需要实现真实的 API 调用
            categories = settings.ARXIV_CATEGORIES.split(",")
            papers = []
            
            for cat in categories:
                papers.extend([
                    Paper(
                        id=str(uuid.uuid4()),
                        title=f"{cat} 领域的最新研究进展",
                        arxiv_id=f"2401.00001",
                        url=f"https://arxiv.org/abs/2401.00001",
                        authors=["Author 1", "Author 2"],
                        abstract="这是一篇关于 AI 领域的研究论文。",
                        published_at=datetime.now() - timedelta(days=1),
                        categories=[cat]
                    )
                ])
            
            return self._handle_success(papers, "抓取 arXiv 论文")
        except Exception as e:
            return self._handle_error(e, "抓取 arXiv 论文")
    
    def personalize_content(self, member_id: str) -> TaskResult:
        """根据成员研究方向个性化内容"""
        try:
            # 获取成员信息
            member_result = self.db.get_member(member_id)
            if not member_result:
                return member_result
            
            member = member_result.data
            interests = member.research_interests
            
            # 这里应该根据研究方向过滤内容
            # 简化实现，返回模拟数据
            personalized_content = {
                "member_name": member.name,
                "research_interests": interests,
                "recommended_news": [
                    {
                        "title": f"关于 {interests[0]} 的最新研究",
                        "url": "https://example.com/news1"
                    }
                    for interests in interests[:2]
                ],
                "recommended_papers": [
                    {
                        "title": f"{interests[0]} 领域的最新论文",
                        "url": "https://arxiv.org/abs/2401.00001"
                    }
                    for interests in interests[:2]
                ]
            }
            
            return self._handle_success(personalized_content, "个性化内容")
        except Exception as e:
            return self._handle_error(e, "个性化内容")
