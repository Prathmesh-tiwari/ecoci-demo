# Usage

## Pricing

```python
from shop.pricing import LineItem, order_total

items = [LineItem("A1", 10.0, 2)]
order_total(items, "GB")   # 24.0
```

Supported tax jurisdictions: `IN`, `GB`, `US`, `DE`.

## Catalogue

```python
from shop.repository import Product, ProductRepository

repo = ProductRepository()
repo.add(Product("A1", "Blue Mug", 9.99, stock=5))
repo.reserve("A1", 2)      # 3 remaining
```

## Authentication

```python
from shop.auth import hash_password, verify_password

stored = hash_password("correct horse battery")
verify_password("correct horse battery", stored)   # True
```

Tokens expire after 15 minutes.

## Why this file matters to EcoCI

A pull request that only edits this file should be classified `documentation` and
should not trigger the security or database test suites. That is the cheapest and
most visible demonstration of the scheduler working.
