from typing import Literal, Union

from pydantic import BaseModel, Field


class DeliveryEstimateOut(BaseModel):
    serviceable: Literal[True] = True
    min_days: int
    max_days: int
    estimated_date: str  # ISO date, e.g. "2026-07-27"


class DeliveryUnavailableOut(BaseModel):
    serviceable: Literal[False] = False
    message: str = "Delivery info unavailable for this location"


DeliveryResponse = Union[DeliveryEstimateOut, DeliveryUnavailableOut]


class PincodeQuery(BaseModel):
    """Validates the pincode query param shape before it reaches business logic."""

    pincode: str = Field(pattern=r"^\d{4,6}$")
