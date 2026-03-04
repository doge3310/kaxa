from bcrypt import hashpw, gensalt, checkpw
from requests import post


def hash_password(password: str):
    return hashpw(password.encode(), gensalt())


def verify_password(password: str, hash: str):
    return checkpw(password.encode(), hash.encode())
