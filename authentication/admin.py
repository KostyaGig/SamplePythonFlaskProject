from authentication.encryption import hash_of
from authentication.encryption import check_psw

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_NAME = "admin"
ADMIN_ROLE = "admin"

ADMIN_PASSWORD_HASH = str(hash_of("admin"))

"""
    In the application a sender of the emails and its receiver is Admin
"""
ADMIN_SENDER_MAIL = "pythonflasksample@gmail.com"
ADMIN_SENDER_LOGIN_PASSWORD = "dvpbkgvqsnfaijtl"

def is_admin(email, name, password):
    return email == ADMIN_EMAIL and name == ADMIN_NAME and check_psw(password, ADMIN_PASSWORD_HASH)


def is_admin_email(email):
    return email == ADMIN_EMAIL
