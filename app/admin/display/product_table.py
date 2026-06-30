from starlette.requests import Request
from fastapi_admin.widgets.displays import Display
from enum import Enum


class BaseBadge(Display):
    """Базовый класс для всех бейджей"""

    async def render(self, request: Request, value: any):
        text = value.value if isinstance(value, Enum) else str(value)
        return self.generate_html(text)

    def generate_html(self, text: str):
        raise NotImplementedError


class StatusBadge(BaseBadge):
    def generate_html(self, text: str):
        colors = {
            "в наличии": "bg-success",
            "заказан": "bg-warning",
            "отгружен": "bg-primary",
            "списан": "bg-danger",
        }
        color_class = colors.get(text.lower(), "bg-secondary")
        return f'<span class="badge {color_class} text-white">{text}</span>'


class UnitBadge(BaseBadge):
    def generate_html(self, text: str):
        labels = {"кг": "кг", "литры": "л", "шт": "шт", "гр": "гр"}
        display_text = labels.get(text.lower(), text)

        return f"""
        <span style="border: 1px solid #6c757d; border-radius: 4px; padding: 2px 6px; 
                     font-size: 0.85em; color: #555; background: #eee; font-weight: 600;">
            {display_text}
        </span>
        """
