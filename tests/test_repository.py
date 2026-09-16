import pytest

from shop.repository import SCHEMA_VERSION, Product, ProductRepository


@pytest.fixture()
def repo():
    r = ProductRepository()
    r.add(Product("A1", "Blue Mug", 9.99, stock=5))
    r.add(Product("B2", "Red Notebook", 4.50, stock=2))
    return r


def test_schema_version_pinned():
    assert SCHEMA_VERSION == 3


def test_add_and_get(repo):
    assert repo.get("A1").name == "Blue Mug"


def test_add_duplicate_rejected(repo):
    with pytest.raises(KeyError):
        repo.add(Product("A1", "Duplicate", 1.0))


def test_get_unknown(repo):
    with pytest.raises(KeyError):
        repo.get("NOPE")


def test_reserve_reduces_stock(repo):
    assert repo.reserve("A1", 2) == 3


def test_reserve_insufficient_stock(repo):
    with pytest.raises(ValueError):
        repo.reserve("B2", 99)


def test_reserve_rejects_non_positive(repo):
    with pytest.raises(ValueError):
        repo.reserve("A1", 0)


def test_search_is_case_insensitive(repo):
    assert [p.sku for p in repo.search("mug")] == ["A1"]


def test_count(repo):
    assert repo.count() == 2
