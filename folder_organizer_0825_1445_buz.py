# 代码生成时间: 2025-08-25 14:45:27
import os
import shutil
from collections import defaultdict
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response

# 定义一个类来处理文件夹结构整理
class FolderOrganizer:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.folder_structure = defaultdict(list)

    # 扫描目录并构建文件夹结构
    def scan_directory(self):
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, self.root_dir)
                self.folder_structure[rel_path].append(file_path)

    # 整理文件夹结构
    def organize_folders(self):
        for rel_path, files in self.folder_structure.items():
            target_dir = os.path.join(self.root_dir, rel_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            for file in files:
                rel_file_path = os.path.relpath(file, self.root_dir)
                dest_file_path = os.path.join(self.root_dir, rel_file_path)
                shutil.move(file, dest_file_path)

# 定义一个视图函数来处理HTTP请求
@view_config(route_name='organize', renderer='json')
def organize(request):
    try:
        # 获取根目录路径
        root_dir = request.params.get('root_dir')
        if not root_dir:
            raise ValueError('Root directory is required')

        # 创建文件夹结构整理器实例
        organizer = FolderOrganizer(root_dir)

        # 扫描目录并整理文件夹结构
        organizer.scan_directory()
        organizer.organize_folders()

        # 返回成功响应
        return {'status': 'success', 'message': 'Folder structure organized successfully'}
    except Exception as e:
        # 返回错误响应
        return {'status': 'error', 'message': str(e)}

# 配置Pyramid应用
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_route('organize', '/organize')
        config.scan()

# 运行Pyramid应用
if __name__ == '__main__':
    main({})
