from tortoise import Model, fields

from app.admin.enums import Status, StatusEnum, UnitEnum


class DepartmentModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)

    class Meta:
        table = "departments"

    def __str__(self):
        return self.name


class EmployeeModel(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True, verbose_name="Логин")
    email = fields.CharField(max_length=255, unique=True, verbose_name="Почта")
    full_name = fields.CharField(max_length=255, unique=True, verbose_name="ФИО")
    password = fields.CharField(
        max_length=255, source_field="password_hash", unique=True, verbose_name="Пароль"
    )

    department = fields.ForeignKeyField(
        "models.DepartmentModel",
        related_name="employees",
        null=True,
    )

    class Meta:
        table = "employees"

    def __str__(self):
        return self.full_name or self.username


class Supplier(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=200, verbose_name="Название компании")
    inn = fields.CharField(max_length=12, verbose_name="ИНН")
    contact_name = fields.CharField(max_length=100, verbose_name="Контактное лицо")
    email = fields.CharField(max_length=100, verbose_name="Почта")
    phone = fields.CharField(max_length=20, verbose_name="Номер телефона")

    class Meta:
        table = "suppliers"

    def __str__(self):
        return self.name


class Category(Model):
    id = fields.IntField(pk=True, verbose_name="Уникальный номер")
    slug = fields.CharField(max_length=200, verbose_name="Описание категории")
    name = fields.CharField(max_length=200, verbose_name="Наименование категории", unique=True)
    created_at = fields.DatetimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        table = "categories"

    def __str__(self):
        return self.name


class Product(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(
        max_length=200,
        verbose_name="Название",
    )

    supplier = fields.ForeignKeyField(
        "models.Supplier",
        related_name="products",
        verbose_name="Поставщик",
    )

    category = fields.ForeignKeyField(
        "models.Category",
        related_name="products",
        verbose_name="Категория",
        null=True,
    )

    unit = fields.CharEnumField(
        UnitEnum,
        default=UnitEnum.PCS,
        verbose_name="Мера измерения",
    )

    quantity = fields.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Количество",
    )

    price = fields.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Цена за ед.",
    )

    status = fields.CharEnumField(
        StatusEnum,
        default=StatusEnum.IN_STOCK,
        verbose_name="Статус",
    )

    expiry_date = fields.DateField(
        null=True,
        verbose_name="Срок годности",
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "products"

    def __str__(self):
        return self.name


class Config(Model):
    id = fields.IntField(pk=True)
    label = fields.CharField(max_length=200)
    key = fields.CharField(max_length=20, unique=True)
    value = fields.JSONField()
    status = fields.IntEnumField(Status, default=Status.on)

    class Meta:
        table = "configs"

    def __str__(self):
        return self.label
