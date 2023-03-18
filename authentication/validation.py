"""
    Simple validation
"""


def validate_register(email, name, password):
    return (email and '@' in email) and name and (password and len(password) > 4)
