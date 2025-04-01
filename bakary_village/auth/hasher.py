import bcrypt


class Hasher:

    def __init__(self, rounds=12):
        self.gensalt = bcrypt.gensalt(rounds=rounds)

    def hash_password(self, password: str):
        return bcrypt.hashpw(
            password=password.encode("utf-8"), salt=self.gensalt
        ).decode()

    def check_password(self, password: str, hashed_password: str):
        return bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=hashed_password.encode("utf-8"),
        )


hasher = Hasher()
