"""初始化数据库"""
from src.storage import SQLiteStorage
from src.utils import logger

if __name__ == "__main__":
    logger.info("开始初始化数据库...")
    db = SQLiteStorage()
    logger.info("数据库初始化完成！")
