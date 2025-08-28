# 代码生成时间: 2025-08-28 18:14:21
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import hashlib
import base64
import os

# Utility function to encrypt a password using SHA-256 and salt
def encrypt_password(password, salt=None):
    """Encrypt the password using SHA-256 and a salt.

    :param password: The password to encrypt
    :param salt: Optional salt to use, if None a new one will be generated
    :return: The encrypted password and salt
    """
    if salt is None:
        salt = os.urandom(16)  # Generate a new salt
    salted_password = password.encode() + salt
    return salt, hashlib.sha256(salted_password).hexdigest()

# Utility function to decrypt a password (verification)
def verify_password(password, salt, encrypted):
    """Verify a password against an encrypted one.

    :param password: The password to verify
    :param salt: The salt used during encryption
    :param encrypted: The encrypted password to compare against
    :return: True if the password matches, False otherwise
    """
    return encrypt_password(password, salt)[1] == encrypted


# Pyramid view function to handle encryption and decryption requests
@view_config(route_name='encrypt', request_method='POST', renderer='json')
def encrypt_view(request):
    """Encrypt a password and return the result.

    :return: A JSON response with the encrypted password and salt
    """
    password = request.json.get('password')
    if not password:
        return Response(json_body={'error': 'Missing password'}, status=400)

    salt, encrypted = encrypt_password(password)
    return {'password_encrypted': encrypted, 'salt': base64.b64encode(salt).decode()}

@view_config(route_name='decrypt', request_method='POST', renderer='json')
def decrypt_view(request):
    """Verify a password against an encrypted one.

    :return: A JSON response with the result of the verification
    """
    password = request.json.get('password')
    encrypted = request.json.get('encrypted')
    if not password or not encrypted:
        return Response(json_body={'error': 'Missing password or encrypted password'}, status=400)

    salt = base64.b64decode(request.json.get('salt', ''))
    if not salt:
        return Response(json_body={'error': 'Missing or invalid salt'}, status=400)

    is_valid = verify_password(password, salt, encrypted)
    return {'valid': is_valid}

# Pyramid configuration
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.add_route('encrypt', '/encrypt')
        config.add_route('decrypt', '/decrypt')
        config.scan()

if __name__ == '__main__':
    main({})