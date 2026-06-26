from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.services.auth.token_generate import create_access_token
from app.services.auth.validate_password import hash_password
from database.core import Session, get_db
from database.models.employees import Employee

router = APIRouter(prefix="/api", tags=["Users"])


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    department_id: int


class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str
    department_id: int
    access_token: str


@router.post("/add-user", response_model=UserResponse)
async def add_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя в системе

    Параметры:
    ----------
    user_data : UserCreate
        Объект с данными нового пользователя:
        - username: str - уникальное имя пользователя (3-20 символов)
        - email: str - валидный email адрес
        - full_name: str - полное имя пользователя
        - password: str - пароль (минимум 8 символов)
        - department_id: int - ID отдела пользователя

    Возвращает:
    -----------
    UserResponse
        Объект с данными созданного пользователя:
        - username: str
        - email: str
        - full_name: str
        - department_id: int
        - access_token: str - JWT токен для авторизации

    Исключения:
    -----------
    HTTPException 400:
        - Если пользователь с таким username или email уже существует

    HTTPException 500:
        - При внутренних ошибках сервера

    Пример запроса:
    ---------------
    ```json
    {
        "username": "ivanov",
        "email": "ivanov@example.com",
        "full_name": "Иванов Иван",
        "password": "securepassword123",
        "department_id": 1
    }
    ```

    Пример ответа:
    --------------
    ```json
    {
        "username": "ivanov",
        "email": "ivanov@example.com",
        "full_name": "Иванов Иван",
        "department_id": 1,
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
    """

    existing_user = (
        db.query(Employee)
        .filter((Employee.username == user_data.username) | (Employee.email == user_data.email))
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists"
        )

    try:
        new_user = Employee(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            password_hash=hash_password(user_data.password),
            department_id=user_data.department_id,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        access_token = create_access_token(data={"sub": new_user.username})

        return UserResponse(
            username=new_user.username,
            email=new_user.email,
            full_name=new_user.full_name,
            department_id=new_user.department_id,
            access_token=access_token,
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}",
        )
