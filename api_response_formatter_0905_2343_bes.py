# 代码生成时间: 2025-09-05 23:43:45
# api_response_formatter.py

"""
API响应格式化工具，用于以统一格式返回API响应。

该工具遵循PYTHON最佳实践，确保代码的可维护性和可扩展性。
"""

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config


# 定义一个类，用于格式化API响应
class ApiResponseFormatter:
    def __init__(self):
        """初始化格式化器"""
        pass

    def format_response(self, data, status_code=200):
        """
        格式化API响应

        Args:
            data (dict): 响应数据
            status_code (int): HTTP状态码，默认为200

        Returns:
            Response: 格式化后的响应
        """
        response_data = {
            "status": "success",
            "data": data,
            "message": f"Request successful with status code {status_code}"
        }
        return Response(json_body=response_data, status=status_code)

    def format_error_response(self, error_message, status_code=400):
        """
        格式化错误响应

        Args:
            error_message (str): 错误信息
            status_code (int): HTTP状态码，默认为400

        Returns:
            Response: 格式化的错误响应
        """
        response_data = {
            "status": "error",
            "message": error_message,
            "data": {}
        }
        return Response(json_body=response_data, status=status_code)


# 配置Pyramid应用
def main(global_config, **settings):
    """配置Pyramid应用"""
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.scan()
    return config.make_wsgi_app()


# 定义视图函数，使用ApiResponseFormatter格式化响应
@view_config(route_name='api_response', renderer='json')
def api_response_view(request):
    """示例API视图，返回格式化的响应"""
    try:
        # 假设这里是业务逻辑
        data = {"key": "value"}
        response_formatter = ApiResponseFormatter()
        return response_formatter.format_response(data)
    except Exception as e:
        # 处理异常，返回错误响应
        response_formatter = ApiResponseFormatter()
        return response_formatter.format_error_response(str(e), status_code=500)
