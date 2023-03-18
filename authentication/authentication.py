from flask import Blueprint, jsonify
from flask import request
from authentication.users_db import user_exists
from authentication.users_db import user_exists_not_considering_admin
from authentication.users_db import insert_user
from authentication.admin import *
from authentication.activation import generate_activation_link_random_string
from authentication.activation import generate_text_for_activation_link
from authentication.validation import validate_register
from authentication.token import generate_access_and_refresh_tokens

register_print = Blueprint('register', __name__)


@register_print.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        email = data["email"]
        name = data["name"]
        password = data["password"]

        if not validate_register(email, name, password):
            return "Data is not valid!"

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
            (access_token, refresh_token) = access_token, refresh_token

            return jsonify(
                tokens={
                    "access_token": access_token,
                    "refresh_token": refresh_token
                },
                activation_link_text=generate_text_for_activation_link(email)
            )
    except Exception as e:
        return f"Error occurred {e}"
