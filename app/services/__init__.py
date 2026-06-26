from fastapi import APIRouter

from app.routers import auth, department, users

api_router = APIRouter(prefix="/v1")

api_router.include_router(auth.router)

api_router.include_router(users.router)


api_router.include_router(department.router)
