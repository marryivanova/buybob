from fastapi import HTTPException, Request
from fastapi_admin.app import app
from fastapi_admin.resources import Dropdown, Field, Link, Model
from fastapi_admin.widgets import displays, inputs
from starlette.datastructures import FormData
from tortoise.expressions import F
from tortoise.functions import Sum

from app.admin.display import StatusBadge
from app.admin.display.product_table import UnitBadge
from app.admin.enums import StatusEnum, UnitEnum
from app.admin.models import Category, Config, EmployeeModel, Product, Supplier

# TODO: Система складского учета
# @app.register
# class ProductResource(Link):
#     label = "Склад"
#     icon = "fas fa-star"
#     url = "/storage"


@app.register
class Dashboard(Link):
    label = "Дашборд"
    icon = "fas fa-home"
    url = "/admin"


@app.register
class EmployeeResource(Model):
    label = "Сотрудники"
    icon = "fas fa-users"
    model = EmployeeModel
    search_fields = ["username", "email", "full_name"]

    fields = [
        "id",
        Field(name="username", label="Логин"),
        Field(name="email", label="Почта", input_=inputs.Email()),
        Field(name="full_name", label="ФИО"),
        Field(
            name="password",
            label="Пароль",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
    ]


@app.register
class SupplierResource(Model):
    label = "Поставщики"
    icon = "fas fa-truck"
    model = Supplier
    search_fields = ["name", "inn"]

    fields = [
        "id",
        Field(name="name", label="Название компании"),
        Field(name="inn", label="ИНН"),
        Field(name="contact_name", label="Контактное лицо"),
        Field(name="email", label="Email"),
        Field(name="phone", label="Телефон"),
    ]


@app.register
class ProductResource(Model):
    label = "Товары"
    icon = "fas fa-box"
    model = Product
    search_fields = ["name"]

    fields = [
        "id",
        "name",
        Field(name="supplier_id", label="Поставщик", input_=inputs.ForeignKey(model=Supplier)),
        Field(name="category_id", label="Категория", input_=inputs.ForeignKey(model=Category)),
        Field(
            name="unit",
            label="Ед. изм.",
            input_=inputs.Enum(enum_type=str, enum=UnitEnum),
            display=UnitBadge(),
        ),
        Field(name="quantity", label="Количество", input_=inputs.Input(step="0.01")),
        Field(name="price", label="Цена за ед.", input_=inputs.Input(step="0.01")),
        Field(
            name="status",
            label="Статус",
            input_=inputs.Enum(enum_type=str, enum=StatusEnum),
            display=StatusBadge(),
        ),
        Field(name="expiry_date", label="Срок годности", input_=inputs.Date()),
    ]

    @classmethod
    async def resolve_data(cls, request: Request, data: FormData):
        ret, m2m_ret = await super().resolve_data(request, data)

        quantity = float(ret.get("quantity", 0))
        price = float(ret.get("price", 0))

        if quantity < 0:
            raise HTTPException(status_code=400, detail="Количество не может быть отрицательным")

        if price < 0:
            raise HTTPException(status_code=400, detail="Цена не может быть отрицательной")

        return ret, m2m_ret

    async def list(self, request: Request, page: int, page_size: int, filters: dict, sort: str):
        response = await super().list(request, page, page_size, filters, sort)

        summary = await Product.annotate(total=Sum(F("quantity") * F("price"))).first()

        total_value = summary.total if summary and summary.total else 0.0

        response.context.update(
            {
                "total_stock_value": f"{total_value:,.2f}",
            }
        )

        return response

    async def cell_attributes(self, request: Request, obj: dict, field: Field) -> dict:
        """
        Пример улучшения UI: подсвечиваем товары, которых мало (меньше 5 шт)
        """
        if field.name == "quantity" and obj.get("quantity", 0) < 5:
            return {"style": "color: red; font-weight: bold;"}
        return {}


@app.register
class Content(Dropdown):
    label = "Каталог"
    icon = "fas fa-bars"

    class CategoryResource(Model):
        label = "Категории"
        model = Category
        search_fields = ["name", "slug"]

        fields = [
            "id",
            Field(name="name", label="Название"),
            Field(name="slug", label="Описание"),
            Field(name="created_at", label="Дата создания", input_=inputs.Date()),
        ]

    resources = [CategoryResource]


@app.register
class ConfigResource(Model):
    label = "Настройки"
    model = Config
    icon = "fas fa-cogs"

    fields = [
        "id",
        "label",
        "key",
        "value",
        "status",
    ]
