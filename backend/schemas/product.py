import uuid

from pydantic import BaseModel, ConfigDict


class VariantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    size: str
    stock_qty: int


class PriceLineOut(BaseModel):
    label: str
    amount: float


class PriceBreakdownOut(BaseModel):
    base_price: float
    discounts: list[PriceLineOut]
    fees: list[PriceLineOut]
    final_price: float


class ProductSummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    brand: str
    category: str
    base_price: float
    image_url: str | None


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    brand: str
    category: str
    base_price: float
    image_url: str | None
    variants: list[VariantOut]
    price_breakdown: PriceBreakdownOut