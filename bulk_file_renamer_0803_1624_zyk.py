# 代码生成时间: 2025-08-03 16:24:35
import os
import re
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# 定义批量重命名工具类
class BulkRenamer:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    # 递归遍历目录下的所有文件
    def list_files(self):
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                yield os.path.join(root, file)

    # 重命名文件
    def rename_files(self, pattern, replacement):
        for file_path in self.list_files():
            try:
                # 构建新的文件名
                new_name = re.sub(pattern, replacement, os.path.basename(file_path))
                new_path = os.path.join(os.path.dirname(file_path), new_name)

                # 重命名文件
                os.rename(file_path, new_path)
                print(f"Renamed '{file_path}' to '{new_path}'")
            except Exception as e:
                print(f"Error renaming '{file_path}': {e}")

# Pyramid视图函数，处理批量重命名请求
@view_config(route_name='rename_files', request_method='POST')
def rename_files_view(request):
    pattern = request.json.get('pattern', '')
    replacement = request.json.get('replacement', '')
    root_dir = request.json.get('root_dir', '')

    # 验证输入参数
    if not pattern or not replacement or not root_dir:
        return Response('Missing parameters', status=400)

    # 创建批量重命名工具实例
    renamer = BulkRenamer(root_dir)

    # 执行批量重命名操作
    renamer.rename_files(pattern, replacement)

    # 返回成功消息
    return Response('Files renamed successfully', status=200)

# 设置Pyramid配置和路由
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('rename_files', '/rename')
    config.scan()
    app = config.make_wsgi_app()
    return app

if __name__ == '__main__':
    main({})
