from config import settings


def classify_stock(stock_qty: int) -> str:
    """
    0            -> out_of_stock
    1..threshold -> low_stock
    threshold+   -> in_stock

    Threshold is centralized in settings so it's a one-line tuning knob
    rather than a magic number buried in logic.
    """
    if stock_qty <= 0:
        return "out_of_stock"
    if stock_qty <= settings.low_stock_max:
        return "low_stock"
    return "in_stock"
