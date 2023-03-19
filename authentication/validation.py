"""
    Simple validation
"""


def validate_register_inputs(email, name, password):
    return (email and '@' in email) and name and (password and len(password) > 4)

def validate_login_inputs(email, password):
    return (email and '@' in email) and (password and len(password) > 4)