"""Backend: price and tax calculation."""

from __future__ import annotations

from dataclasses import dataclass

TAX_RATES = {"IN": 0.18, "GB": 0.20, "US": 0.07, "DE": 0.19}


@dataclass(frozen=True)
class LineItem:
    sku: str
    unit_price: float
    quantity: int

    @property
    def subtotal(self) -> float:
        return round(self.unit_price * self.quantity, 2)


def tax_rate(country: str) -> float:
    if country not in TAX_RATES:
        raise ValueError(f"unsupported country: {country}")
    return TAX_RATES[country]


def apply_discount(subtotal: float, percent: float) -> float:
    if not 0 <= percent <= 100:
        raise ValueError("discount percent must be between 0 and 100")
    return round(subtotal * (1 - percent / 100.0), 2)


def order_total(items: list[LineItem], country: str, discount_percent: float = 0.0) -> float:
    subtotal = sum(item.subtotal for item in items)
    discounted = apply_discount(subtotal, discount_percent)
    return round(discounted * (1 + tax_rate(country)), 2)
