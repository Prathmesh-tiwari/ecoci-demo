from shop.web.templates import render_list, render_price, render_product_card


def test_render_price_gbp():
    assert render_price(1234.5) == "\u00a31,234.50"


def test_render_price_inr():
    assert render_price(99.0, "INR") == "\u20b999.00"


def test_render_product_card_contains_name():
    html = render_product_card("Blue Mug", 9.99)
    assert "Blue Mug" in html and "product-card" in html


def test_render_product_card_escapes_html():
    html = render_product_card("<script>alert(1)</script>", 1.0)
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_render_list():
    assert render_list(["a", "b"]).count("<li>") == 2
