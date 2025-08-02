# 代码生成时间: 2025-08-03 04:40:08
import csv
from pyramid.view import view_config
from pyramid.response import Response
from excel_generator import generate_excel
def includeme(config):
    config.add_route('generate_excel', '/generate_excel')
    config.scan('.views')

def generate_excel(data):
    """Generates an Excel file based on provided data.
    
    :param data: A list of lists representing the rows and columns of the Excel sheet.
    :return: A bytes object representing the generated Excel file.
    """
    output = StringIO()
    csv_writer = csv.writer(output)
    for row in data:
        csv_writer.writerow(row)
    return output.getvalue()

@view_config(route_name='generate_excel', renderer='json')
def excel_view(request):
    """View function to handle the Excel generation request.
    
    :return: A Pyramid response object containing the generated Excel file.
    """
    try:
        data = request.json_body
        excel_content = generate_excel(data)
        response = Response(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            body=excel_content,
            headers=[('Content-Disposition', 'attachment; filename=generated_excel.xlsx')]
        )
        return response
    except Exception as e:
        return Response(
            json_body={'error': str(e)},
            status=500
        )

# Example usage of the above code
if __name__ == '__main__':
    from pyramid.config import Configurator
    from pyramid import paster
    config = Configurator()
    config.include('pyramid_jinja2')
    config.include('pyramid_mailer')
    config.include('pyramid_tm')
    config.include('.views')
    config.include('excel_generator')
    config.scan()
    app = config.make_wsgi_app()
    paster.service(app, {'config_uri': 'development.ini'})
