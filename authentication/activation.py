import hashlib

from flask import Blueprint
from flask import request
from authentication.users_db import get_user_by_email
from authentication.users_db import update_user

"""
    Sample "http://127.0.0.1:5000/activate?email=example@gmail.com"
"""

activation_print = Blueprint('activation', __name__)


@activation_print.route("/activate")
def activate():
    email = request.args.get("email")
    if not email:
        return "An activation email is not found!"

    user_from_db_by_email = get_user_by_email(email)
    if user_from_db_by_email:
        (email, name, hash_psw, is_active, role) = user_from_db_by_email
        if is_active:
            return "You already activated the email"
        else:
            update_user(email, name, hash_psw.decode('UTF-8'), True, role)
            return f"Activation for {email} succeeded!"
    else:
        return f"User by {email} was not found"


def generate_activation_link_random_string(email):
    message_to_activate_link = generate_text_for_activation_link(email)
    return hashlib.sha256(message_to_activate_link.encode()).hexdigest()


def generate_text_for_activation_link(email):
    url = generate_url_activation_link(email)
    return f"Please click on the following link to activate your account: {url}"


def generate_url_activation_link(email):
    return f"http://127.0.0.1:5000/activate?email={email}"
