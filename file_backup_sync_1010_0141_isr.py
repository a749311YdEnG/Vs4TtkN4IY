# 代码生成时间: 2025-10-10 01:41:25
import os
import shutil
import logging
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置PYRAMID
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('backup_sync', '/backup_sync')
    config.scan()
    app = config.make_wsgi_app()
    return app

# 备份文件
def backup_file(source, destination):
    """
    备份文件函数，将源文件复制到目标位置。
    :param source: 源文件路径
    :param destination: 目标文件路径
    """
    try:
        shutil.copy2(source, destination)
        logger.info(f'File {source} has been backed up to {destination}')
    except Exception as e:
        logger.error(f'Failed to backup file {source}. Error: {e}')
        raise

# 同步文件
def sync_files(source_dir, target_dir):
    """
    同步文件函数，将源目录下的所有文件同步到目标目录。
    :param source_dir: 源目录路径
    :param target_dir: 目标目录路径
    """
    try:
        for item in os.listdir(source_dir):
            source_item = os.path.join(source_dir, item)
            target_item = os.path.join(target_dir, item)
            if os.path.isfile(source_item):
                # 如果目标文件存在，则备份
                if os.path.exists(target_item):
                    backup_file(source_item, target_item)
                # 如果目标文件不存在，则复制
                else:
                    shutil.copy2(source_item, target_item)
                    logger.info(f'File {source_item} has been synced to {target_item}')
            elif os.path.isdir(source_item):
                # 如果目标目录不存在，则创建目录并递归同步
                if not os.path.exists(target_item):
                    os.makedirs(target_item)
                    logger.info(f'Directory {target_item} has been created')
                sync_files(source_item, target_item)
    except Exception as e:
        logger.error(f'Failed to sync files from {source_dir} to {target_dir}. Error: {e}')
        raise

# PYRAMID视图函数
@view_config(route_name='backup_sync')
def backup_sync(request):
    """
    视图函数，处理文件备份和同步请求。
    :param request: 请求对象
    """
    source = request.params.get('source')
    destination = request.params.get('destination')
    try:
        # 执行文件备份
        if source and destination:
            backup_file(source, destination)
        # 执行目录同步
        elif source and destination:
            sync_files(source, destination)
        else:
            raise ValueError('Source and destination parameters are required')
        return Response('Backup and sync operation completed successfully')
    except Exception as e:
        return Response(f'Error: {e}', status=500)
