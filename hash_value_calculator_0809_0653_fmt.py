# 代码生成时间: 2025-08-09 06:53:59
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import hashlib
import json

# 定义哈希值计算工具类
class HashValueCalculatorTool:
    def __init__(self):
        pass

    def calculate_hash(self, input_string):
        """
        计算输入字符串的哈希值
        :param input_string: 需要计算哈希值的字符串
        :return: 计算得到的哈希值
        """
        try:
            # 使用sha256算法计算哈希值
            hash_object = hashlib.sha256(input_string.encode())
            return hash_object.hexdigest()
        except Exception as e:
            # 错误处理
            return f"Error calculating hash: {str(e)}"

# 定义 Pyramid 视图函数
@view_config(route_name='calculate_hash', renderer='json')
def calculate_hash_view(request):
    """
    计算哈希值的视图函数
    :param request: Pyramid 请求对象
    :return: 包含哈希值的 JSON 响应
    """
    input_string = request.json.get('input_string', '')

    if not input_string:
        # 检查输入字符串是否有效
        return Response(json.dumps({'error': 'Input string is required'}), content_type='application/json', status=400)

    calculator_tool = HashValueCalculatorTool()
    hash_value = calculator_tool.calculate_hash(input_string)

    return Response(json.dumps({'hash_value': hash_value}), content_type='application/json', status=200)

# 配置 Pyramid 应用
def main(global_config, **settings):
    """
    Pyramid 应用的主函数
    :param global_config: Pyramid 全局配置
    :param settings: 应用设置
    :return: 无
    """
    config = Configurator(settings=settings)
    
    # 添加路由和视图
    config.add_route('calculate_hash', '/calculate_hash')
    config.scan()

    app = config.make_wsgi_app()
    return app

# 运行 Pyramid 应用
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    
    # 运行开发服务器
    server = make_server('0.0.0.0', 6543, main)
    server.serve_forever()