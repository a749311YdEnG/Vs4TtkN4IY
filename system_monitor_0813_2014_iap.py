# 代码生成时间: 2025-08-13 20:14:05
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import psutil
import json

# SystemMonitor class that will handle the performance monitoring
class SystemMonitor:
    def __init__(self):
        pass

    @view_config(route_name='system_monitor', renderer='json')
    def get_system_info(self):
        """
        View to return system performance data
        """
        try:
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            network_data = psutil.net_io_counters()

            system_info = {
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage,
                'network_data': {
                    'bytes_sent': network_data.bytes_sent,
                    'bytes_recv': network_data.bytes_recv,
                },
            }

            return system_info
        except Exception as e:
            return {'error': str(e)}

# Initialize Pyramid application with system monitor view
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_route('system_monitor', '/system_monitor')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    main({})