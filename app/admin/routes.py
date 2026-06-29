from fastapi import Depends, HTTPException
from fastapi_admin.app import app
from fastapi_admin.depends import get_resources
from fastapi_admin.template import templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_404_NOT_FOUND

from app.admin.models import Config, EmployeeModel, Product


@app.get("/")
async def home(request: Request, resources=Depends(get_resources)):
    total_products = await Product.all().count()
    total_employees = await EmployeeModel.all().count()

    return templates.TemplateResponse(
        request,
        name="dashboard.html",
        context={
            "request": request,
            "resources": resources,
            "page_title": "Dashboard",
            "stats": {
                "products": total_products,
                "employees": total_employees,
            },
        },
    )


@app.put("/config/switch_status/{config_id}")
async def switch_config_status(request: Request, config_id: int):
    config = await Config.get_or_none(pk=config_id)
    if not config:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    config.status = not config.status
    await config.save(update_fields=["status"])
    return RedirectResponse(url=request.headers.get("referer"), status_code=HTTP_303_SEE_OTHER)
