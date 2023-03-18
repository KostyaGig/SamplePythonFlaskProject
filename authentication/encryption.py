import bcrypt

salt = bcrypt.gensalt(rounds=5)


def hash_of(str):
    return bcrypt.hashpw(bytes(str, "utf-8"), salt)


def check_psw(password, hash):
    return bcrypt.checkpw(bytes(password, "utf-8"), hash)
