import sqlite3
from authentication.admin import ADMIN_ROLE

USERS_TABLE = "users"

users_connection = sqlite3.connect("authentication/Users.db", check_same_thread=False)
users_cursor = users_connection.cursor()


def init_users_db_if_needed():
    users_cursor.execute(f"CREATE TABLE IF NOT EXISTS {USERS_TABLE}("
                         f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                         f"email TEXT, "
                         f"name TEXT, "
                         f"password TEXT, "
                         f"is_active INTEGER, "
                         f"activation_link TEXT, "
                         f"role TEXT)")


def user_exists_not_considering_admin(email):
    return users_cursor.execute(
        f"SELECT * FROM {USERS_TABLE} WHERE email='{email}' AND role != '{ADMIN_ROLE}';"
    ).fetchone() is not None


def user_exists(email):
    return users_cursor.execute(
        f"SELECT * FROM {USERS_TABLE} WHERE email='{email}';"
    ).fetchone() is not None


def insert_user(email, name, hash_psw, is_active, activation_link, role):
    user = (email, name, hash_psw, is_active, activation_link, role)
    users_cursor.execute(
        f"INSERT INTO "
        f"{USERS_TABLE}(email, name, password, is_active, activation_link, role) "
        f"VALUES(?,?,?,?,?,?);",
        user)
    users_connection.commit()


def update_user(email, name, hash_psw, is_active, role):
    users_cursor.execute(f"UPDATE {USERS_TABLE} SET email='{email}',"
                         f"name='{name}',"
                         f"password='{hash_psw}',"
                         f"is_active={is_active},"
                         f"role='{role}' "
                         f"WHERE email='{email}';"
                         )
    users_connection.commit()


def get_user_by_email(email):
    return users_cursor.execute(
        f"SELECT email, name, password, is_active, role "
        f"FROM {USERS_TABLE} WHERE email='{email}';"
    ).fetchone()
