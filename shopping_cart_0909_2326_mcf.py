# 代码生成时间: 2025-09-09 23:26:32
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.request import Request


# 购物车类
class ShoppingCart:
    def __init__(self):
        self.items = []  # 存储购物车中的项目

    def add_item(self, item):
        """添加商品到购物车"""
        self.items.append(item)

    def remove_item(self, item_id):
        """从购物车中移除商品"""
        self.items = [item for item in self.items if item['id'] != item_id]

    def get_cart_items(self):
        """获取购物车中所有商品"""
        return self.items


# Pyramid视图函数
@view_config(route_name='add_to_cart', request_method='POST')
def add_to_cart(request: Request):
    cart = request.registry.cart
    item_id = request.json_body.get('item_id')
    if not item_id:
        return Response("Item ID is required", status=400)
    cart.add_item({'id': item_id, 'quantity': 1})  # 假设添加的商品数量为1
    return Response("Item added to cart", status=200)

@view_config(route_name='remove_from_cart', request_method='POST')
def remove_from_cart(request: Request):
    cart = request.registry.cart
    item_id = request.json_body.get('item_id')
    if not item_id:
        return Response("Item ID is required", status=400)
    cart.remove_item(item_id)
    return Response("Item removed from cart", status=200)

@view_config(route_name='view_cart', request_method='GET')
def view_cart(request: Request):
    cart = request.registry.cart
    cart_items = cart.get_cart_items()
    return Response(json_body=cart_items, content_type='application/json')

# Pyramid配置函数
def main(global_config, **settings):
    config = Configurator(settings=settings)
    # 创建购物车实例
    cart = ShoppingCart()
    config.registry.cart = cart
    config.add_route('add_to_cart', '/add_to_cart')
    config.add_route('remove_from_cart', '/remove_from_cart')
    config.add_route('view_cart', '/view_cart')
    config.scan()
    return config.make_wsgi_app()
