import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from repositories.product_repo import get_product_basic, list_products_in_category
from schemas.alternatives import AlternativeOut
from services.matching import CandidateProduct, find_alternatives

router = APIRouter(tags=["alternatives"])


@router.get("/products/{product_id}/alternatives", response_model=list[AlternativeOut])
async def get_alternatives(
    product_id: uuid.UUID,
    exclude_size: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
):
    product = await get_product_basic(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    same_category = await list_products_in_category(db, product.category, product.id)

    candidates = [
        CandidateProduct(
            id=str(p.id),
            title=p.title,
            brand=p.brand,
            category=p.category,
            price=float(p.base_price),
            image_url=p.image_url,
            has_requested_size_in_stock=any(
                v.size == exclude_size and v.stock_qty > 0 for v in p.variants
            ),
        )
        for p in same_category
    ]

    matches = find_alternatives(
        product_id=str(product.id),
        category=product.category,
        price=float(product.base_price),
        candidates=candidates,
    )

    return [
        AlternativeOut(
            id=uuid.UUID(m.id),
            title=m.title,
            brand=m.brand,
            price=m.price,
            image_url=m.image_url,
            size_available=m.has_requested_size_in_stock,
        )
        for m in matches
    ]
