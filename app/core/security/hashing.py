from passlib.context import CryptContext


ctx = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return ctx.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return ctx.verify(password, hashed_password)
