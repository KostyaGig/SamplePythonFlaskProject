from authentication.encryption import hash_of
from authentication.encryption import check_psw

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_NAME = "admin"
ADMIN_ROLE = "admin"

ADMIN_PASSWORD_HASH = hash_of("admin")


def is_admin(email, name, password):
    return email == ADMIN_EMAIL and name == ADMIN_NAME and check_psw(password, ADMIN_PASSWORD_HASH)
