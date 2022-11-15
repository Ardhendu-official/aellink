from passlib.context import CryptContext

psw_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str):  # type: ignore
        return psw_ctx.hash(password)


class HashVerify():
    def bcrypt_verify(password: str, hash_password: str):  # type: ignore
        return psw_ctx.verify(password, hash_password)
