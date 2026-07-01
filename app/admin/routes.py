from fastapi import Depends, HTTPException
from fastapi_admin.app import app
from fastapi_admin.depends import get_resources
from fastapi_admin.template import templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_404_NOT_FOUND
from tortoise.functions import Count, Sum

from app.admin.models import Category, Config, EmployeeModel, Product, Supplier


@app.get("/")
async def home(request: Request, resources=Depends(get_resources)):
    # 1. Основные цифры (KPI)
    total_products = await Product.all().count()
    total_employees = await EmployeeModel.all().count()
    total_category = await Category.all().count()
    total_suppler = await Supplier.all().count()

    # 2. Товары по категориям
    cat_stats = await Category.annotate(count=Count("products")).values("name", "count")
    by_category = dict(
        labels=[c["name"] for c in cat_stats],
        data=[c["count"] for c in cat_stats],
    )

    # 3. Товары по поставщикам
    sup_stats = await Supplier.annotate(count=Count("products")).values("name", "count")
    by_supplier = dict(
        labels=[s["name"] for s in sup_stats],
        data=[s["count"] for s in sup_stats],
    )

    # 4. Распределение по цене
    all_products = await Product.all().values("price")
    prices = [float(p["price"]) for p in all_products]
    by_price = dict(
        labels=["0-1000", "1000-5000", "5000+"],
        data=[
            len([p for p in prices if p < 1000]),
            len([p for p in prices if 1000 <= p < 5000]),
            len([p for p in prices if p >= 5000]),
        ],
    )

    # 5. Топ 5 товаров по количеству
    top_products = await Product.all().order_by("-quantity").limit(5).values("name", "quantity")
    by_count = dict(
        labels=[p["name"] for p in top_products],
        data=[float(p["quantity"]) for p in top_products],
    )

    chart_data = dict(
        by_category=by_category,
        by_price=by_price,
        by_count=by_count,
        by_supplier=by_supplier,
    )

    return templates.TemplateResponse(
        request,
        name="dashboard.html",
        context=dict(
            request=request,
            resources=resources,
            stats={
                "products": total_products,
                "employees": total_employees,
                "category": total_category,
                "supplier": total_suppler,
            },
            chart_data=chart_data,
        ),
    )


@app.put("/config/switch_status/{config_id}")
async def switch_config_status(request: Request, config_id: int):
    config = await Config.get_or_none(pk=config_id)
    if not config:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    config.status = not config.status
    await config.save(update_fields=["status"])
    return RedirectResponse(url=request.headers.get("referer"), status_code=HTTP_303_SEE_OTHER)
