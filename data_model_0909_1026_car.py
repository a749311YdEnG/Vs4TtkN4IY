# 代码生成时间: 2025-09-09 10:26:06
from pyramid.config import Configurator
from pyramid.security import Authenticated
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from zope.interface import implementer
from .interfaces import IDatabase
from pyramid.paster import get_appsettings

# 数据模型基类
Base = declarative_base()

# 数据库引擎配置
def get_engine(url, echo=True):
    return create_engine(url, echo=echo)

# 数据模型 User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    age = Column(Integer)
    create_date = Column(Date)
    update_date = Column(Date)
    
    # 用户的 __init__ 方法
    def __init__(self, name, email, age, create_date=None, update_date=None):
        self.name = name
        self.email = email
        self.age = age
        self.create_date = create_date
        self.update_date = update_date
    
    # 字符串表示
    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

# 数据库 session 工厂
def get_session_factory(engine):
    Session = sessionmaker(bind=engine)
    return Session

# 数据库 Transaction 管理器
@implementer(IDatabase)
class RootFactory:
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    # 获取 session
    def get_session(self):
        return self.request.db_session
    
    # 关闭 session
    def close_session(self):
        return self.request.db_session.close()

# Pyramid 配置
def main(global_config, **settings):
    """
    设置 Pyramid 的配置信息
    """
    config = Configurator(settings=settings)
    
    # 数据库 URL
    db_url = get_appsettings(settings)['sqlalchemy.url']
    
    # 创建数据库引擎
    engine = get_engine(db_url)
    
    # 创建 Session 工厂
   SessionFactory = get_session_factory(engine)
    
    # 配置扫描和模型基类
    config.registry['dbsession_factory'] = SessionFactory
    config.set_root_factory(RootFactory)
    config.include('.model')
    
    # 安全策略配置
    authn_policy = AuthTktAuthenticationPolicy('secret')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    
    # 路由配置
    config.add_route('home', '/')
    config.add_route('user_add', '/user/add')
    
    # 视图配置
    config.scan('.views')
    
    return config.make_wsgi_app()

# 配置文件接口
from zope.interface import Interface

class IDatabase(Interface):
    pass