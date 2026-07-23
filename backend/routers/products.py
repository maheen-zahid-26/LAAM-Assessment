import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from repositories.product_repo import get_product_with_details, list_products
from schemas.product import (
    PriceBreakdownOut,
    PriceLineOut,
    ProductOut,
    ProductSummaryOut,
    VariantOut,
)
from services.pricing import Adjustment, compute_price

router = APIRouter(tags=["products"])


@router.get("/products", response_model=list[ProductSummaryOut])
async def get_products(db: AsyncSession = Depends(get_db)):
    products = await list_products(db)
    return [ProductSummaryOut.model_validate(p) for p in products]


@router.get("/products/{product_id}", response_model=ProductOut)
async def get_product(product_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    product = await get_product_with_details(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    adjustments = [
        Adjustment(
            label=a.label,
            type=a.type,
            amount=float(a.amount),
            is_percentage=a.is_percentage,
        )
        for a in product.price_adjustments
    ]
    breakdown = compute_price(float(product.base_price), adjustments)

    return ProductOut(
        id=product.id,
        title=product.title,
        brand=product.brand,
        category=product.category,
        base_price=float(product.base_price),
        image_url=product.image_url,
        variants=[VariantOut(size=v.size, stock_qty=v.stock_qty) for v in product.variants],
        price_breakdown=PriceBreakdownOut(
            base_price=breakdown.base_price,
            discounts=[PriceLineOut(label=d.label, amount=d.amount) for d in breakdown.discounts],
            fees=[PriceLineOut(label=f.label, amount=f.amount) for f in breakdown.fees],
            final_price=breakdown.final_price,
        ),
    )