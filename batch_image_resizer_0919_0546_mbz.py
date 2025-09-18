# 代码生成时间: 2025-09-19 05:46:41
import os
from PIL import Image
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.config import Configurator
from pyramid.renderers import render_to_response

# 图片尺寸批量调整器
class ImageResizer:
    def __init__(self, source_folder, target_folder, size):
        self.source_folder = source_folder
        self.target_folder = target_folder
        self.size = size

    def resize_images(self):
        # 遍历源文件夹中的所有图片
        for filename in os.listdir(self.source_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # 打开图片
                with Image.open(os.path.join(self.source_folder, filename)) as img:
                    # 调整图片尺寸
                    img = img.resize(self.size, Image.ANTIALIAS)
                    # 保存调整后的图片到目标文件夹
                    target_path = os.path.join(self.target_folder, filename)
                    img.save(target_path)
                    print(f"Resized {filename} and saved to {target_path}")
            else:
                print(f"Skipped non-image file: {filename}")

# Pyramid视图函数
@view_config(route_name='resize_images', request_method='GET')
def resize_images_view(request):
    # 获取请求参数
    source_folder = request.params.get('source_folder')
    target_folder = request.params.get('target_folder')
    width = int(request.params.get('width'))
    height = int(request.params.get('height'))

    # 参数校验
    if not source_folder or not target_folder or width <= 0 or height <= 0:
        return Response("Invalid parameters", status=400)

    # 创建ImageResizer实例并调整图片尺寸
    resizer = ImageResizer(source_folder, target_folder, (width, height))
    resizer.resize_images()

    # 返回成功响应
    return Response("Images resized successfully", status=200)

# Pyramid配置函数
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('resize_images', '/resize')
    config.scan()
    return config.make_wsgi_app()

# 运行Pyramid应用
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main(global_config={}, **settings={'debug_all': True})
    server = make_server('0.0.0.0', 8080, app)
    print("Server started on port 8080")
    server.serve_forever()