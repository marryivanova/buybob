from enum import Enum, IntEnum


class ProductType(IntEnum):
    article = 1
    page = 2


class Status(IntEnum):
    on = 1
    off = 0


class Action(str, Enum):
    create = "create"
    delete = "delete"
    edit = "edit"


class UnitEnum(str, Enum):
    KG = "кг"
    LITERS = "литры"
    PCS = "шт"
    GRAMS = "гр"


class StatusEnum(str, Enum):
    IN_STOCK = "в наличии"
    ORDERED = "заказан"
    SHIPPED = "отгружен"
    WRITTEN_OFF = "списан"
