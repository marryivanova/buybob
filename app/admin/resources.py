from fastapi_admin.app import app
from fastapi_admin.resources import Dropdown, Field, Link, Model
from fastapi_admin.widgets import displays, inputs

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
            name="password", label="Пароль", display=displays.InputOnly(), input_=inputs.Password()
        ),
    ]


@app.register
class SupplierResource(Model):
    label = "Поставщики"
    icon = "fas fa-truck"
    model = Supplier
    search_fields = ["name", "inn"]
    fields = ["id", "name", "inn", "contact_name", "email", "phone"]


@app.register
class ProductResource(Model):
    label = "Товары"
    icon = "fas fa-box"
    model = Product
    search_fields = ["name"]
    fields = [
        "id",
        "name",
        "supplier",
        "category",
        "unit",
        "quantity",
        "price",
        "status",
        "expiry_date",
    ]


@app.register
class Content(Dropdown):
    label = "Каталог"
    icon = "fas fa-bars"

    class CategoryResource(Model):
        label = "Категории"
        model = Category
        fields = ["id", "name", "slug", "created_at"]

    resources = [CategoryResource]


@app.register
class ConfigResource(Model):
    label = "Настройки"
    model = Config
    icon = "fas fa-cogs"
    fields = ["id", "label", "key", "value", "status"]
