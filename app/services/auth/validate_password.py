from typing import Optional

import bcrypt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database.models.employees import Employee

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли пароль хешу."""
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_by_username(db: Session, username: str) -> Optional[Employee]:
    """Ищет пользователя по username в БД."""
    return db.query(Employee).filter(Employee.username == username).first()


async def authenticate_user(db: Session, username: str, password: str) -> Optional[Employee]:
    """Проверяет логин и пароль пользователя."""
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
