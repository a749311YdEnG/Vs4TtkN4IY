# 代码生成时间: 2025-08-30 12:34:49
# hash_calculator.py

from pyramid.view import view_config
from pyramid.response import Response
import hashlib
from pyramid.httpexceptions import HTTPBadRequest

# 定义哈希值计算工具类
class HashCalculator:
    def __init__(self, request):
        self.request = request

    # 提供哈希值计算服务
    @view_config(route_name='calculate_hash', renderer='json')
    def calculate_hash(self):
        """
        计算哈希值的视图函数。
        接收输入字符串，返回其SHA256哈希值。
        :param data: 待计算哈希的字符串数据
        :return: 哈希值的JSON响应
        """
        try:
            # 从请求中获取待计算哈希的字符串
            data = self.request.params.get('data')
            if not data:
                raise ValueError('Missing data parameter')

            # 计算SHA256哈希值
            hash_object = hashlib.sha256(data.encode())
            hash_value = hash_object.hexdigest()

            # 返回包含哈希值的JSON响应
            return {'hash': hash_value}
        except ValueError as e:
            # 处理数据参数错误
            return HTTPBadRequest(json_body={'error': str(e)})
        except Exception as e:
            # 处理其他潜在错误
            return HTTPBadRequest(json_body={'error': 'An error occurred during hash calculation'})

# 将哈希值计算工具类注册为PYRAMID视图
def main(global_config, **settings):
    """
    Pyramid应用的初始化函数。
    :param global_config: 全局配置
    :param settings: 应用设置
    :return: 应用配置
    """
    from pyramid.config import Configurator
    config = Configurator(settings=settings)
    config.add_route('calculate_hash', '/calculate_hash')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    main()