from datetime import timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.http import HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.auth.auth_config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    LoginRequest,
    Token,
    swagger_security,
)
from app.services.auth.token_generate import create_access_token
from app.services.auth.validate_password import authenticate_user
from database.core import get_db

router = APIRouter(prefix="/api", tags=["Auth"])


class TokenData(BaseModel):

    access_token: str
    token_type: str


@router.post("/login-swagger", status_code=status.HTTP_200_OK)
async def login_swagger(
    credentials: HTTPBasicCredentials = Depends(swagger_security), db: Session = Depends(get_db)
):
    """
    Аутентификация через Swagger UI (Basic Auth)

    Args:
        credentials: Данные для входа (username/password) из стандартного диалога авторизации Swagger
        db: Сессия базы данных

    Returns:
        TokenData: Объект с JWT-токеном

    Raises:
        HTTPException: 401 если неверные учетные данные
    """
    user = await authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    access_token = create_access_token(
        data=dict(sub=user.username),
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return TokenData(access_token=access_token, token_type="bearer")


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Стандартная аутентификация пользователя

    Args:
        request: Модель запроса с полями username и password
        db: Сессия базы данных

    Returns:
        Token: Объект с JWT-токеном

    Raises:
        HTTPException: 401 если неверные учетные данные
    """
    user = await authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(
        data=dict(sub=user.username),
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/api/protected")
async def protected_route(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/login"))):
    """
    Защищенный маршрут, требующий JWT-токена

    Args:
        token: JWT-токен из заголовка Authorization

    Returns:
        dict: Приветственное сообщение с именем пользователя

    Raises:
        HTTPException: 401 при ошибках валидации токена
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return dict(message=f"Hello, {username}!")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
