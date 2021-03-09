import base64


def encrypt(string):
    return base64.b64encode(string.encode('utf-8', errors='strict'))


def decrypt(string):
    return base64.b64decode(string).decode('utf-8')


class RolePermissionDeniedException(Exception):
    pass
