import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from db import get_db
from repositories.delivery_repo import list_all_zones
from schemas.delivery import DeliveryEstimateOut, DeliveryResponse, DeliveryUnavailableOut
from services.delivery import DeliveryZone, estimate_delivery

router = APIRouter(tags=["delivery"])

# Pattern enforced at the query-param level -> malformed pincodes get a 422
# automatically, before any business logic runs.
PincodeParam = Annotated[str, Query(pattern=r"^\d{4,6}$")]


@router.get("/delivery/estimate", response_model=DeliveryResponse)
async def get_delivery_estimate(
    pincode: PincodeParam,
    product_id: uuid.UUID,  # accepted now for a stable contract; unused until
    # per-product handling time (e.g. made-to-order items) is modeled
    db: AsyncSession = Depends(get_db),
):
    zones = await list_all_zones(db)
    zone_dtos = [
        DeliveryZone(
            pincode_prefix=z.pincode_prefix,
            min_days=z.min_days,
            max_days=z.max_days,
            is_serviceable=z.is_serviceable,
        )
        for z in zones
    ]

    result = estimate_delivery(pincode, zone_dtos)

    if not result.serviceable:
        return DeliveryUnavailableOut(message=result.message or "Delivery info unavailable for this location")

    return DeliveryEstimateOut(
        min_days=result.min_days,
        max_days=result.max_days,
        estimated_date=result.estimated_date,
    )
