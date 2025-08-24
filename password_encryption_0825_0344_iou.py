# 代码生成时间: 2025-08-25 03:44:57
import os
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound
from cryptography.fernet import Fernet

"""
密码加密解密工具，使用PYRAMID框架创建的程序。
该程序实现了通过HTTP请求进行密码加密和解密的功能。
"""

# 生成密钥
def generate_key():
    return Fernet.generate_key()

# 创建加密器
def create_encryptor(key):
    return Fernet(key)

# 加密函数
def encrypt_message(message, encryptor):
    return encryptor.encrypt(message.encode())

# 解密函数
def decrypt_message(encrypted_message, encryptor):
    decrypted_message = encryptor.decrypt(encrypted_message)
    return decrypted_message.decode()


# Pyramid的视图函数
@view_config(route_name='encrypt_password', renderer='json')
def encrypt_password(request):
    # 从请求中获取密码
    password = request.json.get('password')
    if not password:
        return Response('Password is required', status=400)

    # 密钥和加密器
    key = generate_key()
    encryptor = create_encryptor(key)
    encrypted_password = encrypt_message(password, encryptor)

    # 返回加密后的密码和密钥
    return {'encrypted_password': encrypted_password, 'key': key.decode()}


@view_config(route_name='decrypt_password', renderer='json')
def decrypt_password(request):
    # 从请求中获取密码和密钥
    encrypted_password = request.json.get('encrypted_password')
    key = request.json.get('key')
    if not encrypted_password or not key:
        return Response('Encrypted password and key are required', status=400)

    # 创建加密器
    encryptor = create_encryptor(key.encode())
    decrypted_password = decrypt_message(encrypted_password, encryptor)

    # 返回解密后的密码
    return {'decrypted_password': decrypted_password}
