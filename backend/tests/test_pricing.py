from services.pricing import Adjustment, compute_price


def test_no_adjustments_returns_base_price_as_final():
    result = compute_price(1000, [])
    assert result.final_price == 1000
    assert result.discounts == []
    assert result.fees == []


def test_flat_discount_reduces_final_price():
    adjustments = [Adjustment(label="Clearance", type="discount", amount=200)]
    result = compute_price(1000, adjustments)
    assert result.discounts[0].amount == 200
    assert result.final_price == 800


def test_percentage_discount_computed_off_base_price():
    adjustments = [Adjustment(label="Sale", type="discount", amount=10, is_percentage=True)]
    result = compute_price(1000, adjustments)
    assert result.discounts[0].amount == 100
    assert result.final_price == 900


def test_fee_applied_after_discount_on_discounted_subtotal():
    adjustments = [
        Adjustment(label="Sale", type="discount", amount=10, is_percentage=True), 
        Adjustment(label="COD fee", type="fee", amount=10, is_percentage=True),   
    ]
    result = compute_price(1000, adjustments)
    assert result.discounts[0].amount == 100
    assert result.fees[0].amount == 90
    assert result.final_price == 990


def test_flat_fee_added_after_discount():
    adjustments = [
        Adjustment(label="Sale", type="discount", amount=200),
        Adjustment(label="Delivery", type="fee", amount=150),
    ]
    result = compute_price(1000, adjustments)
    assert result.final_price == 950


def test_zero_or_negative_adjustment_amount_is_skipped():
    adjustments = [
        Adjustment(label="Broken discount", type="discount", amount=0),
        Adjustment(label="Broken fee", type="fee", amount=-50),
    ]
    result = compute_price(1000, adjustments)
    assert result.discounts == []
    assert result.fees == []
    assert result.final_price == 1000


def test_discount_never_pushes_subtotal_below_zero():
    adjustments = [Adjustment(label="Huge discount", type="discount", amount=5000)]
    result = compute_price(1000, adjustments)
    assert result.final_price == 0
