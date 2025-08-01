# 代码生成时间: 2025-08-02 03:37:22
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import json

# 定义数学计算工具类
class MathCalculator:
    def add(self, a, b):
        """Add two numbers"""
        return a + b

    def subtract(self, a, b):
        """Subtract two numbers"""
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers"""
        return a * b

    def divide(self, a, b):
        """Divide two numbers"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

# 创建视图函数
@view_config(route_name='add', renderer='json')
def add_view(request):
    try:
        a = float(request.matchdict['a'])
        b = float(request.matchdict['b'])
        result = MathCalculator().add(a, b)
        return {'result': result}
    except ValueError as e:
        return Response(json.dumps({'error': str(e)}), content_type='application/json', status=400)

@view_config(route_name='subtract', renderer='json')
def subtract_view(request):
    try:
        a = float(request.matchdict['a'])
        b = float(request.matchdict['b'])
        result = MathCalculator().subtract(a, b)
        return {'result': result}
    except ValueError as e:
        return Response(json.dumps({'error': str(e)}), content_type='application/json', status=400)

@view_config(route_name='multiply', renderer='json')
def multiply_view(request):
    try:
        a = float(request.matchdict['a'])
        b = float(request.matchdict['b'])
        result = MathCalculator().multiply(a, b)
        return {'result': result}
    except ValueError as e:
        return Response(json.dumps({'error': str(e)}), content_type='application/json', status=400)

@view_config(route_name='divide', renderer='json')
def divide_view(request):
    try:
        a = float(request.matchdict['a'])
        b = float(request.matchdict['b'])
        result = MathCalculator().divide(a, b)
        return {'result': result}
    except ValueError as e:
        return Response(json.dumps({'error': str(e)}), content_type='application/json', status=400)

# 设置 Pyramid 配置
def main(global_config, **settings):
    config = Configurator(settings=settings)

    # 添加路由和视图
    config.add_route('add', '/add/{a}/{b}')
    config.add_view(add_view, route_name='add')

    config.add_route('subtract', '/subtract/{a}/{b}')
    config.add_view(subtract_view, route_name='subtract')

    config.add_route('multiply', '/multiply/{a}/{b}')
    config.add_view(multiply_view, route_name='multiply')

    config.add_route('divide', '/divide/{a}/{b}')
    config.add_view(divide_view, route_name='divide')

    # 扫描视图函数所在的模块
    config.scan()

    return config.make_wsgi_app()