# 代码生成时间: 2025-09-12 22:18:29
# batch_file_renamer.py
# 这是一个使用PYRAMID框架创建的批量文件重命名工具

from pyramid.config import Configurator
# FIXME: 处理边界情况
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
import os
import re


# 定义一个错误处理函数
def handle_error(error):
    # 将错误信息返回给客户端
    return Response(str(error), content_type='text/plain', status=500)

# 文件重命名函数
def rename_files(directory, prefix, regex):
# 增强安全性
    # 检查目录是否存在
    if not os.path.exists(directory):
        raise ValueError("目录不存在")
    
    # 遍历目录中的文件
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # 检查是否为文件
        if os.path.isfile(filepath):
            # 使用正则表达式匹配文件名
            match = re.match(regex, filename)
            if match:
# 扩展功能模块
                # 生成新的文件名
                new_filename = f"{prefix}{filename}"
                new_filepath = os.path.join(directory, new_filename)
                # 重命名文件
                try:
                    os.rename(filepath, new_filepath)
                    print(f"文件 {filename} 已重命名为 {new_filename}")
                except OSError as error:
                    print(f"无法重命名文件 {filename}：{error}")
# NOTE: 重要实现细节

# Pyramid视图函数
@view_config(route_name='rename', renderer='json')
def rename_view(request):
    # 获取请求参数
    directory = request.params.get('directory')
    prefix = request.params.get('prefix', '')
    regex = request.params.get('regex', '.*')
    
    # 参数校验
    if not directory:
        return Response({"error": "缺少目录参数"}, content_type='application/json', status=400)
    
    # 调用文件重命名函数
    try:
        rename_files(directory, prefix, regex)
        return Response({"message": "文件重命名成功"}, content_type='application/json')
    except ValueError as error:
# 扩展功能模块
        return Response({"error": str(error)}, content_type='application/json', status=400)
    except Exception as error:
        return Response({"error": str(error)}, content_type='application/json', status=500)

# Pyramid配置函数
def main(global_config, **settings):
    """Assemble the Pyramid WSGI application."""
    config = Configurator(settings=settings)
    
    # 配置错误处理器
    config.scan('.batch_file_renamer')
    config.add_view(rename_view, route_name='rename')
# FIXME: 处理边界情况
    
    # 返回配置好的Pyramid应用
    return config.make_wsgi_app()
