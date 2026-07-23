from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import DeliveryZone


async def list_all_zones(db: AsyncSession) -> list[DeliveryZone]:
    # Small, mostly-static table — fetching all rows and matching in Python
    # (see services/delivery.py) keeps the matching logic pure and testable
    # without needing prefix-matching SQL.
    result = await db.execute(select(DeliveryZone))
    return list(result.scalars().all())
