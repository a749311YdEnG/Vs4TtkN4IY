# 代码生成时间: 2025-09-23 16:50:29
from pyramid.config import Configurator
from pyramid.view import view_config
import random

"""
随机数生成器 Web 应用
"""

# 定义视图函数
@view_config(route_name='generate_random', renderer='json')
def generate_random(request):
    # 从请求中获取参数
    try:
        min_val = int(request.params.get('min', '0'))  # 默认最小值 0
        max_val = int(request.params.get('max', '100'))  # 默认最大值 100
    except ValueError:
        # 参数不是整数时抛出异常
        return {'error': 'Min and max values must be integers'}

    # 检查参数有效性
    if min_val > max_val:
        return {'error': 'Min value must be less than or equal to max value'}

    # 生成随机数
    random_number = random.randint(min_val, max_val)
    # 返回结果
    return {'random_number': random_number}

# 配置 Pyramid 应用
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')  # 配置模板引擎
    config.add_route('generate_random', '/generate_random')
    config.scan()  # 自动扫描并注册视图函数
    return config.make_wsgi_app()


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main(global_config=None, **{'reload': True})
    server = make_server('0.0.0.0', 6543, app)
    print('Serving on 0.0.0.0 port 6543...')
    server.serve_forever()