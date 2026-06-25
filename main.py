import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.services import api_router
from settings import settings

app = FastAPI(
    title="Bob buy",
    description="""
    ## Общее описание

    """,
    version="0.1.0",
    openapi_url="/openapi.json",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
    },
)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Hello World", "status": "ok"}


app.include_router(api_router)

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        access_log=False,
    )
