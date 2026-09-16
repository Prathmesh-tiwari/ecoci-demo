"""UI layer: HTML rendering helpers."""

from __future__ import annotations

import html

BUTTON_CLASS = "btn btn-primary"


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def render_price(amount: float, currency: str = "GBP") -> str:
    symbols = {"GBP": "\u00a3", "USD": "$", "EUR": "\u20ac", "INR": "\u20b9"}
    symbol = symbols.get(currency, "")
    return f"{symbol}{amount:,.2f}"


def render_product_card(name: str, price: float, currency: str = "GBP") -> str:
    return (
        '<div class="product-card">'
        f"<h3>{escape(name)}</h3>"
        f'<span class="price">{escape(render_price(price, currency))}</span>'
        f'<button class="{BUTTON_CLASS}">Add to basket</button>'
        "</div>"
    )


def render_list(names: list[str]) -> str:
    items = "".join(f"<li>{escape(n)}</li>" for n in names)
    return f'<ul class="product-list">{items}</ul>'
