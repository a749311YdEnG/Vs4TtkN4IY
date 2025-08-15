# 代码生成时间: 2025-08-15 08:49:28
import csv
import random
from datetime import datetime, timedelta
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# 测试数据生成器类
class TestDataGenerator:
    def __init__(self):
        # 数据库连接配置（示例）
        self.db_config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'password',
            'db': 'test_db'
        }

    def generate_test_data(self, num_records):
        """
        生成指定数量的测试数据

        :param num_records: 要生成的测试数据条数
        :return: 测试数据列表
        """
        test_data = []
        for _ in range(num_records):
            # 生成随机姓名
            name = self.generate_random_name()
            # 生成随机年龄
            age = random.randint(18, 80)
            # 生成随机创建日期
            creation_date = self.generate_random_date()
            test_data.append({'name': name, 'age': age, 'creation_date': creation_date})
        return test_data

    def generate_random_name(self):
        """
        生成随机姓名

        :return: 随机姓名
        """
        names = ['John', 'Alice', 'Bob', 'Carol', 'Dave']
        return random.choice(names)

    def generate_random_date(self):
        "