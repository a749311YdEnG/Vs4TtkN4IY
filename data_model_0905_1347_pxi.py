# 代码生成时间: 2025-09-05 13:47:17
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from pyramid.config import Configurator
from pyramid.paster import get_appsettings, setup_logging
from sqlalchemy import create_engine

# 数据模型基类
Base = declarative_base()

# 定义用户模型
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  # 用户ID
    name = Column(String(50), nullable=False)  # 用户名
    email = Column(String(100), unique=True, nullable=False)  # 用户邮箱
    password = Column(String(100), nullable=False)  # 用户密码

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

# 定义博客文章模型
class BlogPost(Base):
    __tablename__ = 'blog_posts'
    id = Column(Integer, primary_key=True)  # 文章ID
    title = Column(String(255), nullable=False)  # 文章标题
    content = Column(String, nullable=False)  # 文章内容
    user_id = Column(Integer, ForeignKey('users.id'))  # 外键，关联用户ID
    user = relationship('User', backref='blog_posts')  # 关联用户

    def __repr__(self):
        return f"<BlogPost(title='{self.title}', user='{self.user.name}')>"

# Pyramid配置函数
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    setup_logging(config.registry)
    config.include('pyramid_chameleon')
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()

# 数据库连接和模型初始化
if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()

    # 创建示例用户和博客文章
    user = User(name='John Doe', email='john@example.com', password='password123')
    session.add(user)
    blog_post = BlogPost(title='Hello World', content='This is a blog post.', user=user)
    session.add(blog_post)

    # 提交事务
    session.commit()
