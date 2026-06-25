import secrets

from fastapi.security import HTTPBasic, HTTPBearer, OAuth2PasswordBearer
from pydantic import BaseModel

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

swagger_security = HTTPBasic()
bearer_security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")  # Для OAuth2 в Swagger


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
