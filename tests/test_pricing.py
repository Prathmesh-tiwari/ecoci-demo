import pytest

from shop.pricing import LineItem, apply_discount, order_total, tax_rate


def test_line_item_subtotal():
    assert LineItem("A1", 19.99, 3).subtotal == 59.97


def test_tax_rate_known_country():
    assert tax_rate("GB") == 0.20


def test_tax_rate_unknown_country():
    with pytest.raises(ValueError):
        tax_rate("ZZ")


def test_apply_discount():
    assert apply_discount(100.0, 25) == 75.0


def test_apply_discount_rejects_out_of_range():
    with pytest.raises(ValueError):
        apply_discount(100.0, 150)


def test_order_total_with_tax():
    items = [LineItem("A1", 10.0, 2), LineItem("B2", 5.0, 1)]
    assert order_total(items, "GB") == 30.0


def test_order_total_with_discount():
    items = [LineItem("A1", 50.0, 2)]
    assert order_total(items, "US", discount_percent=10) == 96.3


@pytest.mark.smoke
def test_smoke_import_and_basic_total():
    assert order_total([LineItem("X", 1.0, 1)], "IN") == 1.18
