from flask import *
from authentication.authentication import register_print
from authentication.authentication import login_print
from authentication.users_db import init_users_db_if_needed

from authentication.activation import activation_print
from authentication.authorizationmiddleware import AuthorizationMiddleWare

app = Flask(__name__)

"""
    Set up auth middleware
"""
app.wsgi_app = AuthorizationMiddleWare(app.wsgi_app)

app.register_blueprint(register_print)
app.register_blueprint(login_print)

app.register_blueprint(activation_print)


@app.route("/")
def root():
    return "Server is running..."

if __name__ == '__main__':
    init_users_db_if_needed()
    app.run(debug=True)
