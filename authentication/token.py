import jwt
import datetime

SECRET_KEY = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"

ACCESS_TOKEN_EXPIRATION_TIME_IN_MINUTES = 1
REFRESH_TOKEN_EXPIRATION_TIME_IN_MINUTES = 2


def generate_access_and_refresh_tokens(email):
    access_token_payload = {
        "exp": generate_access_token_expiration_time(),
        "email": email,
        "time": str(datetime.datetime.now())
    }
    refresh_token_payload = {
        "exp": generate_refresh_token_expiration_time(),
        "email": email,
        "time": str(datetime.datetime.now()),
    }
    access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm="HS256")

    return access_token, refresh_token


def token_is_valid(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        return False


def generate_access_token_expiration_time():
    scheduled = datetime.datetime.now() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME_IN_MINUTES)
    return int(scheduled.timestamp())


def generate_refresh_token_expiration_time():
    scheduled = datetime.datetime.now() + datetime.timedelta(minutes=2)
    return int(scheduled.timestamp())
