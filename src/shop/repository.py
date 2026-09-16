"""Database layer: an in-memory store with a migration-style schema version."""

from __future__ import annotations

from dataclasses import dataclass, field

SCHEMA_VERSION = 3


@dataclass
class Product:
    sku: str
    name: str
    price: float
    stock: int = 0


@dataclass
class ProductRepository:
    _rows: dict[str, Product] = field(default_factory=dict)

    def add(self, product: Product) -> None:
        if product.sku in self._rows:
            raise KeyError(f"duplicate sku {product.sku}")
        self._rows[product.sku] = product

    def get(self, sku: str) -> Product:
        try:
            return self._rows[sku]
        except KeyError as exc:
            raise KeyError(f"unknown sku {sku}") from exc

    def reserve(self, sku: str, quantity: int) -> int:
        product = self.get(sku)
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if product.stock < quantity:
            raise ValueError(f"insufficient stock for {sku}: {product.stock} < {quantity}")
        product.stock -= quantity
        return product.stock

    def search(self, term: str) -> list[Product]:
        needle = term.lower().strip()
        return sorted(
            (p for p in self._rows.values() if needle in p.name.lower()),
            key=lambda p: p.sku,
        )

    def count(self) -> int:
        return len(self._rows)
