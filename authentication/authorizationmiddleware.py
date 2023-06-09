from werkzeug.wrappers import Request, Response
from authentication.token import token_is_valid, get_email_by_token
from authentication.admin import is_admin_email

require_auth_paths = set()
admin_paths = set()

class AuthorizationMiddleWare:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)

        if request.path not in require_auth_paths:
            return self.app(environ, start_response)

        split_token = request.headers.get("Authorization", " ").split(" ")

        if len(split_token) < 2:
            res = Response(
                "AccessToken is not found(try to Add \"Bearer\" before token)",
                mimetype="text/plain",
                status=401
            )
            return res(environ, start_response)

        token = split_token[1]

        (valid, message) = token_is_valid(token)
        if not valid:
            res = Response(
                message,
                mimetype="text/plain",
                status=401
            )
            return res(environ, start_response)

        if request.path in admin_paths:
            email = get_email_by_token(request.headers)
            if not(is_admin_email(email)):
                res = Response(
                    "You do not have enough rights to get to the endpoint",
                    mimetype="text/plain",
                    status=401
                )
                return res(environ, start_response)


        return self.app(environ, start_response)


"""
    Decorator for adding path to require_auth_paths set.
    You need it if there is need to check an user's authentication before getting into a route
    
    Pass path in format /{your_path}
"""


def require_auth(path):
    require_auth_paths.add(path)

    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator

def require_auth_as_admin(path):
    admin_paths.add(path)

    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator