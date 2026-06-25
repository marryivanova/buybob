from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.http import HTTPBasicCredentials
import jwt
from pydantic import BaseModel


from app.services.auth.auth_config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    LoginRequest,
    Token,
    swagger_security,
    SECRET_KEY,
    ALGORITHM,
)
from app.services.auth.token_generate import create_access_token
from app.services.auth.validate_password import authenticate_user
from database.core import Session

router = APIRouter(prefix="/api", tags=["Auth"])


class TokenData(BaseModel):

    access_token: str
    token_type: str


@router.post("/login-swagger", status_code=status.HTTP_200_OK)
async def login_swagger(
    credentials: HTTPBasicCredentials = Depends(swagger_security), db: Session = Depends(Session)
):
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
async def login(request: LoginRequest, db: Session = Depends(Session)):
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
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return dict(message=f"Hello, {username}!")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
