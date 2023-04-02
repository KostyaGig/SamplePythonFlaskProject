from flask import Blueprint, jsonify
from flask import request
from authentication.users_db import user_exists
from authentication.users_db import user_exists_not_considering_admin
from authentication.users_db import insert_user
from authentication.users_db import get_user_by_email
from authentication.admin import *
from authentication.activation import generate_activation_link_random_string
from authentication.activation import generate_text_for_activation_link
from authentication.validation import validate_register_inputs
from authentication.validation import validate_login_inputs
from authentication.token import generate_access_and_refresh_tokens

register_print = Blueprint('register', __name__)


@register_print.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        email = data.get("email", "")
        name = data.get("name", "")
        password = data.get("password", "")

        if not validate_register_inputs(email, name, password):
            return "Input data is not valid"

        if user_exists_not_considering_admin(email):
            return f"User with {email} email already exists! Please, login"

        hash_psw = hash_of(password)

        if is_admin(email, name, password):
            not_exists = not user_exists(email)
            if not_exists:
                insert_user(email, ADMIN_NAME, hash_psw, True, "", ADMIN_ROLE)
            return "You have registered as Admin"
        else:
            activation_link = generate_activation_link_random_string(email)
            insert_user(email, name, hash_psw, False, activation_link, "user")

            (access_token, refresh_token) = generate_access_and_refresh_tokens(email)

            return jsonify(
                tokens={
                    "access_token": access_token,
                    "refresh_token": refresh_token
                },
                activation_link_text=generate_text_for_activation_link(email)
            )
    except Exception as e:
        return f"Error occurred {e}"


login_print = Blueprint('login', __name__)


@login_print.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    email = data.get("email", "")
    password = data.get("password", "")

    if not validate_login_inputs(email, password):
        return "Input data is not valid"

    if not user_exists(email):
        return f"User by {email} has not been registered yet"

    (_, _, _, password_hash, _, role) = get_user_by_email(email)

    if check_psw(password, password_hash):
        (access_token, refresh_token) = generate_access_and_refresh_tokens(email)

        return jsonify(
            tokens={
                "access_token": access_token,
                "refresh_token": refresh_token
            },
            message=f"You have authorized as {role}"
        )
    else:
        return f"Email or password is not valid"
