from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from database.core import Session, get_db
from database.models.department import Department

router = APIRouter(prefix="/api", tags=["Department"])


class DepartmentCreate(BaseModel):
    name: str


class DepartmentResponse(BaseModel):
    id: int
    name: str


@router.post("/department", response_model=DepartmentResponse)
async def add_department(department_data: DepartmentCreate, db: Session = Depends(get_db)):
    """
    Создание нового отдела в системе

    Параметры:
    ----------
    department_data : DepartmentCreate
        Объект с данными нового отдела:
        - name: str - Название отдела (должно быть уникальным, 2-50 символов)

    Возвращает:
    -----------
    DepartmentResponse
        Объект с данными созданного отдела:
        - id: int - Уникальный идентификатор отдела
        - name: str - Название отдела

    Исключения:
    -----------
    HTTPException 400:
        - Если отдел с таким названием уже существует

    HTTPException 500:
        - При внутренних ошибках сервера

    Пример запроса:
    ---------------
    ```json
    {
        "name": "Отдел разработки"
    }
    ```

    Пример ответа:
    --------------
    ```json
    {
        "id": 1,
        "name": "Отдел разработки"
    }
    """
    existing_user = db.query(Department).filter((Department.name == department_data.name)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is already such a department in the system.",
        )

    try:
        new_department = Department(name=department_data.name)
        db.add(new_department)
        db.commit()
        db.refresh(new_department)

        return DepartmentResponse(name=new_department.name, id=new_department.id)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating department: {str(e)}",
        )
