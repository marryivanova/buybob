from contextlib import asynccontextmanager
from pathlib import Path

import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, Request
from fastapi_admin.app import app as admin_app
from fastapi_admin.exceptions import (
    forbidden_error_exception,
    not_found_error_exception,
    server_error_exception,
    unauthorized_error_exception,
)
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from tortoise.contrib.fastapi import register_tortoise

from app.admin import settings
from app.admin.models import EmployeeModel
from app.admin.providers import LoginProvider
from app.services import api_router

BASE_DIR = Path(__file__).resolve().parent
ADMIN_TEMPLATES_DIR = BASE_DIR / "app" / "admin" / "templates"


def configure_logging() -> None:
    """Configure application logging."""
    logger.add(
        "app.log",
        rotation="10 MB",
        retention="30 days",
        encoding="utf-8",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )


def configure_exception_handlers() -> None:
    """Register exception handlers for admin app."""
    admin_app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
    admin_app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
    admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
    admin_app.add_exception_handler(HTTP_401_UNAUTHORIZED, unauthorized_error_exception)


def configure_middleware(app: FastAPI) -> None:
    """Register application middleware."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )


async def log_requests(request: Request, call_next):
    """Middleware for request logging."""
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


def configure_database(app: FastAPI) -> None:
    """Configure database connection."""
    register_tortoise(
        app,
        config=dict(
            connections={
                "default": "postgres://postgres:postgres@localhost:5432/contest",
            },
            apps={
                "models": {
                    "models": ["app.admin.models"],
                    "default_connection": "default",
                }
            },
        ),
        generate_schemas=True,
        add_exception_handlers=True,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    r = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        encoding="utf8",
    )
    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=[str(ADMIN_TEMPLATES_DIR)],
        favicon_url="https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/favicon.png",
        providers=[
            LoginProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg",
                admin_model=EmployeeModel,
            )
        ],
        redis=r,
    )
    yield


def create_app():
    configure_logging()

    app = FastAPI(
        title="Bob buy",
        description="E-commerce platform API",
        version="1.0.0",
        lifespan=lifespan,
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.middleware("http")(log_requests)
    configure_middleware(app)

    @app.get("/")
    async def index():
        return RedirectResponse(url="/admin")

    admin_app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
    admin_app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
    admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
    admin_app.add_exception_handler(HTTP_401_UNAUTHORIZED, unauthorized_error_exception)

    app.include_router(api_router)
    app.mount("/admin", admin_app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    configure_exception_handlers()

    configure_database(app)
    return app


app = create_app()

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        access_log=False,
    )
