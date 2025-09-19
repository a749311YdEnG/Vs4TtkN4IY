# 代码生成时间: 2025-09-20 03:08:26
# scheduler_service.py

"""
定时任务调度器服务，使用PYRAMID框架实现。
该服务将使用Python内置的APScheduler库来实现定时任务调度。
"""

from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# 导入日志模块
import logging

# 初始化日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义定时任务调度器类
class SchedulerService:
    def __init__(self):
        # 初始化调度器
        self.scheduler = BackgroundScheduler()
        
    # 添加任务到调度器
    def add_job(self, func, trigger):
        try:
            self.scheduler.add_job(func, trigger)
            logger.info(f"Task {func.__name__} added to scheduler with trigger {trigger}")
        except Exception as e:
            logger.error(f"Failed to add task to scheduler: {e}")
            raise
        
    # 启动调度器
    def start(self):
        try:
            self.scheduler.start()
            logger.info("Scheduler started")
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")
            raise
        
    # 关闭调度器
    def shutdown(self):
        self.scheduler.shutdown()
        logger.info("Scheduler shutdown\)

# 定义一个示例任务
def my_task():
    logger.info("Running scheduled task")

# Pyramid配置
def main(global_config, **settings):
    config = Configurator(settings=settings)
    
    # 创建调度器实例
    scheduler = SchedulerService()
    scheduler.add_job(my_task, IntervalTrigger(seconds=10))  # 每10秒运行一次
    scheduler.start()
    
    # 注册关闭处理函数，确保调度器能正常关闭
    config.registry.settings['pyramid.shutdown'] = scheduler.shutdown
    
    # 配置视图
    config.add_route('test', '/test')
    config.scan()
    return config.make_wsgi_app()

# 定义视图函数
@view_config(route_name='test', renderer='json')
def test(request):
    return {"message": "Hello from Pyramid!"}
