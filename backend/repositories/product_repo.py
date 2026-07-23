import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from models import Product, ProductVariant


async def list_products(db: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.title)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_product_basic(db: AsyncSession, product_id: uuid.UUID) -> Product | None:
    """
    Product row only — no eager-loaded relations. Use this wherever an
    endpoint doesn't need variants/price_adjustments off the Product itself
    (e.g. it queries variants separately, or only needs category/base_price).
    Over a pooled remote connection (pgbouncer/Supabase), each extra
    selectinload is its own network round trip, so skipping unused ones
    matters a lot more than it would against a local DB.
    """
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_product_with_details(db: AsyncSession, product_id: uuid.UUID) -> Product | None:
    """
    Full product with variants + price_adjustments, for endpoints that need
    both. Uses joinedload (single JOIN query) rather than selectinload
    (which issues 2 extra round trips) since we're only ever fetching one
    product here.
    """
    stmt = (
        select(Product)
        .where(Product.id == product_id)
        .options(
            joinedload(Product.variants),
            joinedload(Product.price_adjustments),
        )
    )
    result = await db.execute(stmt)
    return result.unique().scalar_one_or_none()


async def get_variant(
    db: AsyncSession, product_id: uuid.UUID, size: str
) -> ProductVariant | None:
    stmt = select(ProductVariant).where(
        ProductVariant.product_id == product_id, ProductVariant.size == size
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def list_products_in_category(
    db: AsyncSession, category: str, exclude_id: uuid.UUID
) -> list[Product]:
    stmt = (
        select(Product)
        .where(Product.category == category, Product.id != exclude_id)
        .options(selectinload(Product.variants))
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())