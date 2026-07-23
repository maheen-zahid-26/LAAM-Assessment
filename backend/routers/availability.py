import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from repositories.product_repo import get_product_basic, get_variant
from schemas.availability import AvailabilityOut
from services.availability import classify_stock

router = APIRouter(tags=["availability"])


@router.get("/products/{product_id}/availability", response_model=AvailabilityOut)
async def get_availability(
    product_id: uuid.UUID,
    size: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
):
    product = await get_product_basic(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    variant = await get_variant(db, product_id, size)
    if variant is None:
        raise HTTPException(
            status_code=404, detail=f"Size '{size}' is not offered for this product"
        )

    return AvailabilityOut(
        size=variant.size,
        stock_qty=variant.stock_qty,
        status=classify_stock(variant.stock_qty),
    )
