# 代码生成时间: 2025-08-27 09:59:41
from pyramid.config import Configurator
from pyramid.view import view_config
import psutil
import json

def includeme(config):
    # 注册视图函数
    config.scan()

def memory_usage_analysis_view(request):
    """
    这个视图函数返回当前机器的内存使用情况。
    """
    try:
        # 获取系统内存信息
        mem = psutil.virtual_memory()
        # 构造内存使用情况的字典
        memory_info = {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "free": mem.free,
            "percent": mem.percent,
        }
        # 返回JSON格式的响应
        return json.dumps(memory_info)
    except Exception as e:
        # 错误处理
        return json.dumps({"error": str(e)})

@view_config(route_name='memory_usage', renderer='json')
def memory_usage_view(request):
    # 调用内存使用情况分析函数
    return memory_usage_analysis_view(request)

def main(global_config, **settings):
    """
    Pyramid WSGI应用的入口点。
    """
    config = Configurator(settings=settings)
    config.include(includeme)
    config.add_route('memory_usage', '/memory_usage')
    # 添加视图
    config.scan()
    return config.make_wsgi_app()
