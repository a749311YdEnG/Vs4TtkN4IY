# 代码生成时间: 2025-09-12 16:38:50
import logging
from pyramid.config import Configurator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库配置
DB_URL = 'your_database_url'

# 创建数据库引擎
engine = create_engine(DB_URL, echo=True)

# 创建SessionLocal绑定
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    """获取数据库Session对象"""
    try:
        db = SessionLocal()
    except SQLAlchemyError as e:
        logger.error('Failed to get database session', exc_info=e)
        raise e
    return db

async def close_db(db):
    """关闭数据库Session对象"