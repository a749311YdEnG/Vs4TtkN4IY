# 代码生成时间: 2025-08-04 21:15:39
import os
import shutil
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# 文件夹结构整理器的配置和视图
class FolderOrganizer:
    def __init__(self, request):
        self.request = request

    # 视图函数，用于整理文件夹结构
    @view_config(route_name='organize_folder', renderer='json')
    def organize(self):
        # 获取目标文件夹路径
        target_folder = self.request.params.get('folder_path')
        if not target_folder:
            return Response(json_body={'error': 'No folder path provided.'}, status=400)

        # 检查路径是否存在
        if not os.path.exists(target_folder):
            return Response(json_body={'error': 'Folder does not exist.'}, status=404)

        # 检查路径是否为文件夹
        if not os.path.isdir(target_folder):
            return Response(json_body={'error': 'Provided path is not a folder.'}, status=400)

        try:
            # 调用整理函数
            self._sort_folder(target_folder)
            return Response(json_body={'message': 'Folder organized successfully.'})
        except Exception as e:
            return Response(json_body={'error': str(e)}, status=500)

    def _sort_folder(self, folder_path):
        # 遍历文件夹中的文件和子文件夹
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                # 如果是文件，移动到指定的文件目录
                self._move_file(item_path)
            elif os.path.isdir(item_path):
                # 如果是文件夹，递归整理
                self._sort_folder(item_path)

    def _move_file(self, file_path):
        # 定义文件的目标目录
        file_target_dir = os.path.join(os.path.dirname(file_path), 'files')
        # 确保目标目录存在
        if not os.path.exists(file_target_dir):
            os.makedirs(file_target_dir)
        # 移动文件到目标目录
        shutil.move(file_path, file_target_dir)

# Pyramid配置
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include(".folder_organizer")  # 包含视图
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    main({})