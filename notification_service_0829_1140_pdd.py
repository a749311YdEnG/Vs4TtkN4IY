# 代码生成时间: 2025-08-29 11:40:22
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pyramid.request import Request

# 定义数据库模型
# TODO: 优化性能
Base = declarative_base()

class Notification(Base):
# 添加错误处理
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# 数据库配置
DATABASE_URL = 'sqlite:///notification.db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
# 优化算法效率
Session = sessionmaker(bind=engine)

# 消息通知系统服务
class NotificationService:
    def __init__(self, session):
        self.session = session
    
    def create_notification(self, message):
        """创建通知"""
        notification = Notification(message=message)
        try:
            self.session.add(notification)
            self.session.commit()
            return {'id': notification.id}
        except Exception as e:
            self.session.rollback()
            raise e
    
    def get_notifications(self):
        "