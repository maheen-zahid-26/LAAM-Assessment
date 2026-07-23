from typing import Literal

from pydantic import BaseModel

StockStatus = Literal["in_stock", "low_stock", "out_of_stock"]


class AvailabilityOut(BaseModel):
    size: str
    stock_qty: int
    status: StockStatus
