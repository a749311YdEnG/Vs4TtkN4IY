# 代码生成时间: 2025-09-04 09:15:50
from pyramid.view import view_config
def is_url_valid(url):
    """
    验证URL链接的有效性。
    
    参数:
    url (str): 待验证的URL链接。
    
    返回:
    bool: URL链接是否有效。
    """
    from urllib.parse import urlparse
    from urllib.request import urlopen
    try:
        # 解析URL
        result = urlparse(url)
        # 检查URL协议是否支持
        if result.scheme not in ['http', 'https']:
            return False
        # 检查URL是否可以访问
        with urlopen(url) as response:
            # 检查HTTP状态码
            if response.status == 200:
                return True
            else:
                return False
    except ValueError:
        # URL解析错误
        return False
    except Exception as e:
        # 其他错误
        print(f"Error: {e}")
        return False
def main():
    """
    程序入口函数。
    """
    url = input("请输入URL链接进行验证: ")
    if is_url_valid(url):
        print("URL链接有效。")
    else:
        print("URL链接无效。")

if __name__ == "__main__":
    main()
