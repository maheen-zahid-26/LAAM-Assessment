from services.availability import classify_stock


def test_zero_stock_is_out_of_stock():
    assert classify_stock(0) == "out_of_stock"


def test_one_stock_is_low_stock():
    assert classify_stock(1) == "low_stock"


def test_threshold_boundary_is_low_stock():
    assert classify_stock(3) == "low_stock"  


def test_just_above_threshold_is_in_stock():
    assert classify_stock(4) == "in_stock"


def test_large_stock_is_in_stock():
    assert classify_stock(100) == "in_stock"


def test_negative_stock_treated_as_out_of_stock():
    assert classify_stock(-1) == "out_of_stock"
