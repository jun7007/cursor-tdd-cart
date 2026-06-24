import pytest

from src.cart import subtotal

pytestmark = pytest.mark.entity


def test_inv1_single_item_subtotal():
    """INV-1: subtotal(items) == Σ(price × qty) — 단일 품목."""
    assert subtotal([{"price": 1000, "qty": 3}]) == 3000


def test_inv1_two_items_subtotal():
    """INV-1: subtotal(items) == Σ(price × qty) — 복수 품목."""
    items = [{"price": 1000, "qty": 3}, {"price": 2000, "qty": 2}]
    assert subtotal(items) == 7000


def test_inv1_interview_case_subtotal():
    """INV-1: subtotal(items) == Σ(price × qty) — 인터뷰 사례 (66,000원)."""
    items = [{"price": 12000, "qty": 3}, {"price": 30000, "qty": 1}]
    assert subtotal(items) == 66000
