# 代码生成时间: 2025-08-06 18:20:24
import os
import shutil
import logging
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response

# 设置日志
logging.basicConfig(level=logging.INFO)

# 定义备份和同步的函数
def backup_file(source, destination):
    """备份文件到指定目的地"""
    try:
        shutil.copy2(source, destination)
        logging.info(f"文件 {source} 已成功备份到 {destination}")
    except IOError as e:
        logging.error(f"备份文件 {source} 至 {destination} 失败：{e}")
        raise


def sync_files(source, destination):
    """同步源文件夹到目标文件夹"""
    try:
        shutil.copytree(source, destination)
        logging.info(f"文件夹 {source} 已成功同步到 {destination}")
    except OSError as e:
        logging.error(f"同步文件夹 {source} 至 {destination} 失败：{e}")
        raise

# Pyramid视图函数
@view_config(route_name='backup_file', renderer='json')
def backup_file_view(request):
    """HTTP视图函数，用于触发文件备份"""
    source = request.params.get('source')
    destination = request.params.get('destination')
    if not source or not destination:
        return Response(json_body={'error': '缺少源或目标文件路径参数'}, status=400)
    try:
        backup_file(source, destination)
        return Response(json_body={'message': '文件备份成功'}, status=200)
    except Exception as e:
        return Response(json_body={'error': str(e)}, status=500)

@view_config(route_name='sync_files', renderer='json')
def sync_files_view(request):
    """HTTP视图函数，用于触发文件夹同步"""
    source = request.params.get('source')
    destination = request.params.get('destination')
    if not source or not destination:
        return Response(json_body={'error': '缺少源或目标文件夹路径参数'}, status=400)
    try:
        sync_files(source, destination)
        return Response(json_body={'message': '文件夹同步成功'}, status=200)
    except Exception as e:
        return Response(json_body={'error': str(e)}, status=500)

# Pyramid设置函数
def main(global_config, **settings):
    """设置Pyramid应用"""
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_route('backup_file', '/backup')
    config.add_route('sync_files', '/sync')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    main({})