import bcrypt

salt = bcrypt.gensalt(rounds=5)


def hash_of(str):
    return bcrypt.hashpw(bytes(str, "utf-8"), salt).decode("utf-8")


def check_psw(password, string_hash):
    return bcrypt.checkpw(bytes(password, "utf-8"), bytes(string_hash, "utf-8"))


def check_hash_psw_by_hash(password, hash):
    return hash_of(password) == hash
