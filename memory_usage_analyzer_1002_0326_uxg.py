# 代码生成时间: 2025-10-02 03:26:20
import os
import psutil
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# 定义一个金字塔视图函数以返回内存使用情况
@view_config(route_name='memory_usage')
def memory_usage(request):
    # 获取当前进程的内存使用情况
    process = psutil.Process(os.getpid())
    try:
        # 获取内存使用信息
        memory_info = process.memory_info()
        # 格式化内存使用为可读形式
        memory_usage = {
            'RSS': memory_info.rss / (1024 * 1024),  # 以MB为单位
            'VMS': memory_info.vms / (1024 * 1024),  # 以MB为单位
        }
        return Response(
            json_body={
                'status': 'success',
                'memory_usage': memory_usage
            },
            content_type='application/json',
            charset='utf-8'
        )
    except Exception as e:
        # 错误处理
        return Response(
            json_body={'status': 'error', 'message': str(e)},
            content_type='application/json',
            charset='utf-8',
            status=500
        )

# 配置金字塔应用程序
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        # 添加视图
        config.add_route('memory_usage', '/memory_usage')
        # 扫描当前目录并注册视图
        config.scan()

# 入口点
if __name__ == '__main__':
    main({})