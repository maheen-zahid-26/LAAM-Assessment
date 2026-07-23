import uuid

from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    base_price: Mapped[float] = mapped_column(Numeric, nullable=False)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    variants: Mapped[list["ProductVariant"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    price_adjustments: Mapped[list["PriceAdjustment"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    size: Mapped[str] = mapped_column(String, nullable=False)
    stock_qty: Mapped[int] = mapped_column(default=0)

    product: Mapped["Product"] = relationship(back_populates="variants")


class PriceAdjustment(Base):
    __tablename__ = "price_adjustments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    label: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)  
    amount: Mapped[float] = mapped_column(Numeric, nullable=False)
    is_percentage: Mapped[bool] = mapped_column(Boolean, default=False)

    product: Mapped["Product"] = relationship(back_populates="price_adjustments")


class DeliveryZone(Base):
    __tablename__ = "delivery_zones"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pincode_prefix: Mapped[str] = mapped_column(String, nullable=False)
    min_days: Mapped[int] = mapped_column(nullable=False)
    max_days: Mapped[int] = mapped_column(nullable=False)
    is_serviceable: Mapped[bool] = mapped_column(Boolean, default=True)
