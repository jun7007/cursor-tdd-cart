import pytest

from src.cart import subtotal

pytestmark = pytest.mark.boundary


def test_e1_items_none_raises_type_error():
    """E-1: items is None → TypeError."""
    with pytest.raises(TypeError):
        subtotal(None)


def test_e2_negative_qty_includes_index():
    """E-2: 음수 qty → ValueError, 인덱스 포함."""
    with pytest.raises(ValueError, match="0"):
        subtotal([{"price": 1000, "qty": -1}])


def test_e2_negative_price_includes_index():
    """E-2: 음수 price → ValueError, 인덱스 포함."""
    with pytest.raises(ValueError, match="1"):
        subtotal([
            {"price": 1000, "qty": 1},
            {"price": -500, "qty": 2},
        ])
