from fastapi import Request
from fastapi_admin.app import app
from fastapi_admin.resources import Dropdown, Field, Link, Model
from fastapi_admin.widgets import displays, inputs

from app.admin.enums import StatusEnum
from app.admin.models import Category, Config, EmployeeModel, Product, Supplier


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
        "username",
        "email",
        "full_name",
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
        Field(
            name="name",
            label="Наименование",
        ),
        Field(
            name="supplier_id",
            label="Поставщик",
            input_=inputs.ForeignKey(model=Supplier),
        ),
        Field(
            name="category_id",
            label="Категория",
            input_=inputs.ForeignKey(model=Category),
        ),
        Field(
            name="unit",
            label="Единица измерения",
        ),
        Field(
            name="quantity",
            label="Количество",
            input_=inputs.Input(step="0.01"),
        ),
        Field(
            name="price",
            label="Цена за ед.",
            input_=inputs.Input(step="0.01"),
        ),
        Field(
            name="status", label="Статус товара", input_=inputs.Enum(enum_type=str, enum=StatusEnum)
        ),
        Field(
            name="expiry_date",
            label="Срок годности",
            input_=inputs.Date(),
        ),
    ]

    async def list(
        self,
        request: Request,
        page: int,
        page_size: int,
        filters: dict,
        sort: str,
    ):
        response = await super().list(request, page, page_size, filters, sort)

        all_products = await Product.all().values("quantity", "price")

        total_value = sum(float(product["quantity"] * product["price"]) for product in all_products)

        response.context.update(
            {
                "total_stock_value": f"{total_value:,.2f}",
            }
        )

        return response


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
            Field(name="slug", label="Slug"),
            Field(name="created_at", label="Дата создания"),
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
