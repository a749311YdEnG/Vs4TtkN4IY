# 代码生成时间: 2025-10-01 15:47:51
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import JSON

# 定义税务计算函数
def calculate_tax(income: float, deductions: float) -> float:
    """
    根据收入和扣除额计算税务。
    :param income: 收入金额
    :param deductions: 扣除额
    :return: 应缴税款
    """
    if income <= 0:
        raise ValueError("收入金额不能为负或零")
    net_income = income - deductions
    tax_rate = 0.2  # 假设税率为20%
    return net_income * tax_rate

# Pyramid视图函数，处理税务计算请求
@view_config(route_name='calculate_tax', renderer=JSON)
def tax_calculator(request):
    """
    接收请求并计算税务。
    :param request: Pyramid请求对象
    :return: 计算结果的JSON对象
    """
    try:
        income = float(request.matchdict['income'])
        deductions = float(request.matchdict['deductions'])
        tax = calculate_tax(income, deductions)
        return {'success': True, 'tax': tax}
    except ValueError as e:
        return {'success': False, 'message': str(e)}
    except Exception as e:
        return {'success': False, 'message': '未知错误'}

# 配置Pyramid应用程序
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.add_route('calculate_tax', '/calculate_tax/{income}/{deductions}')
        config.scan()

if __name__ == '__main__':
    main({})
