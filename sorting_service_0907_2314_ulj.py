# 代码生成时间: 2025-09-07 23:14:40
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import logging

# 设置日志记录器
log = logging.getLogger(__name__)

# 排序算法实现
def bubble_sort(arr):
    """冒泡排序算法实现"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        
    return arr

def insertion_sort(arr):
    """插入排序算法实现"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >=0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

def selection_sort(arr):
    """选择排序算法实现"""
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# Pyramid视图配置
@view_config(route_name='sort', renderer='json')
def sort_view(request):
    # 获取排序算法类型和待排序数组
    algorithm = request.matchdict.get("algorithm")
    numbers = request.json_body.get("numbers", [])
    
    # 参数校验
    if not algorithm or not isinstance(numbers, list) or not all(isinstance(x, (int, float)) for x in numbers):
        return Response(
            json_body={"error": "Invalid parameters"},
            status=400
        )
    
    try:
        # 根据算法类型调用对应的排序函数
        if algorithm == "bubble":
            sorted_numbers = bubble_sort(numbers)
        elif algorithm == "insertion":
            sorted_numbers = insertion_sort(numbers)
        elif algorithm == "selection":
            sorted_numbers = selection_sort(numbers)
        else:
            return Response(
                json_body={"error": "Unsupported algorithm"},
                status=400
            )
    except Exception as e:
        log.error(f"Error sorting numbers: {str(e)}")
        return Response(
            json_body={"error": "Error while sorting numbers