# 代码生成时间: 2025-08-06 11:49:53
# system_performance_monitor.py

"""
A Pyramid-based system performance monitoring tool.

This script uses the Pyramid framework to create a RESTful API for monitoring
system performance metrics such as CPU usage, memory usage, and disk usage.
"""

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
import psutil
import json


# View function to get CPU usage percentage
@view_config(route_name='cpu_usage', renderer='json')
def cpu_usage(request):
    try:
        cpu_usage_percentage = psutil.cpu_percent(interval=1)
        return {'cpu_usage': cpu_usage_percentage}
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)


# View function to get memory usage
@view_config(route_name='memory_usage', renderer='json')
def memory_usage(request):
    try:
        memory_info = psutil.virtual_memory()
        return {
            'total': memory_info.total,
            'available': memory_info.available,
            'used': memory_info.used,
            'free': memory_info.free,
            'percent': memory_info.percent
        }
    except Exception as e:
# 添加错误处理
        return Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)


# View function to get disk usage
@view_config(route_name='disk_usage', renderer='json')
def disk_usage(request):
    try:
        disk_partitions = psutil.disk_partitions()
        disk_usage_info = []
        for partition in disk_partitions:
# FIXME: 处理边界情况
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage_info.append({
                'device': partition.device,
# FIXME: 处理边界情况
                'mountpoint': partition.mountpoint,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            })
        return disk_usage_info
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)


# Configure the Pyramid application
def main(global_config, **settings):
    """
    This function sets up the Pyramid application.
    :param global_config: The global configuration dictionary.
    :param settings: Additional settings.
    """
    config = Configurator(settings=settings)
    config.add_route('cpu_usage', '/cpu_usage')
    config.add_route('memory_usage', '/memory_usage')
# NOTE: 重要实现细节
    config.add_route('disk_usage', '/disk_usage')
# NOTE: 重要实现细节
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    main({})
