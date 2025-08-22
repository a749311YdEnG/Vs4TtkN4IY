# 代码生成时间: 2025-08-23 04:41:39
import csv
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.config import Configurator
from pyramid.request import Request
from datetime import datetime
import xlsxwriter

# Excel表格自动生成器类
class ExcelGenerator:
    def __init__(self):
        pass

    # 生成Excel表格
    def generate_excel(self, data, filename):
        try:
            # 确保数据不为空
            if not data:
                raise ValueError('Data cannot be empty')

            # 创建Excel文件
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet()

            # 写入数据
            for i, row in enumerate(data):
                for j, value in enumerate(row):
                    worksheet.write(i, j, value)

            # 关闭Excel文件
            workbook.close()
            return f'Excel file {filename} generated successfully.'

        except Exception as e:
            return f'An error occurred: {e}'

# Pyramid视图函数
@view_config(route_name='generate_excel', renderer='json')
def generate_excel_view(request: Request):
    # 从请求中获取数据和文件名
    data = request.json.get('data', [])
    filename = request.json.get('filename', 'default.xlsx')

    # 实例化Excel生成器
    generator = ExcelGenerator()

    # 生成Excel文件
    result = generator.generate_excel(data, filename)

    # 返回结果
    return {'message': result}

# Pyramid配置
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('generate_excel', '/generate_excel')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    make_server('0.0.0.0', 6543, main).serve_forever()