# 代码生成时间: 2025-08-21 23:20:15
from pyramid.config import Configurator
from pyramid.view import view_config
from sqlalchemy import create_engine, Column, Integer, String, Float, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import transaction
from pyramid.security import Authenticated, Allow

# 数据库配置
DATABASE_URL = 'sqlite:///inventory.db'

# 创建数据库引擎
engine = create_engine(DATABASE_URL)
DBSession = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = DBSession.query_property()

# 定义库存项模型
class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    id = Column(Integer, Sequence('inventory_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price
    
    def __repr__(self):
        return f"<InventoryItem(name={self.name}, quantity={self.quantity}, price={self.price})>"

# 初始化数据库
def init_db():
    Base.metadata.create_all(bind=engine)

# 添加库存项视图
@view_config(route_name='add_inventory', request_method='POST', permission=Authenticated)
def add_inventory(request):
    name = request.params.get('name')
    quantity = request.params.get('quantity', type=int)
    price = request.params.get('price', type=float)
    
    if not name or quantity is None or price is None:
        return Response(json_body={'error': 'Invalid input'}, content_type='application/json', status=400)
    
    try:
        new_item = InventoryItem(name, quantity, price)
        DBSession.add(new_item)
        transaction.commit()
    except Exception as e:
        return Response(json_body={'error': str(e)}, content_type='application/json', status=500)
    
    return HTTPFound(location=request.route_url('view_inventory'))

# 查看库存项视图
@view_config(route_name='view_inventory')
def view_inventory(request):
    items = DBSession.query(InventoryItem).all()
    return Response(json_body=[{'name': item.name, 'quantity': item.quantity, 'price': item.price} for item in items], content_type='application/json')

# Pyramid配置
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    
    config.add_route('add_inventory', '/add')
    config.add_route('view_inventory', '/')
    
    config.scan()
    return config.make_wsgi_app()
    
# 运行应用
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({})
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()