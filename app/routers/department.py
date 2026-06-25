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
