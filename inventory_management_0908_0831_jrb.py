# 代码生成时间: 2025-09-08 08:31:37
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPInternalServerError
import json
import logging


# 配置日志
logging.basicConfig(level=logging.INFO)


# 库存管理类
class InventoryManager:
    def __init__(self):
        # 初始化库存数据
        self.inventory = {}

    def add_item(self, item_id, quantity):
        """添加库存项
        Args:
            item_id (str): 物品ID
            quantity (int): 数量
        """
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity

    def remove_item(self, item_id, quantity):
        """移除库存项
        Args:
            item_id (str): 物品ID
            quantity (int): 数量
        """
        if item_id in self.inventory:
            if self.inventory[item_id] >= quantity:
                self.inventory[item_id] -= quantity
                if self.inventory[item_id] == 0:
                    del self.inventory[item_id]
            else:
                raise ValueError("库存不足")
        else:
            raise ValueError("物品不存在