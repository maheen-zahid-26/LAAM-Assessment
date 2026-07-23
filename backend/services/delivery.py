from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class DeliveryZone:
    pincode_prefix: str
    min_days: int
    max_days: int
    is_serviceable: bool


@dataclass
class DeliveryResult:
    serviceable: bool
    min_days: int | None = None
    max_days: int | None = None
    estimated_date: str | None = None
    message: str | None = None


UNAVAILABLE_MESSAGE = "Delivery info unavailable for this location"


def estimate_delivery(
    pincode: str, zones: list[DeliveryZone], today: date | None = None
) -> DeliveryResult:
    """
    Matches a pincode against zone prefixes, longest-prefix-first so a more
    specific zone (e.g. '540') wins over a broader one (e.g. '5') if both
    are seeded. Returns an "unavailable" result rather than raising when
    nothing matches or the matched zone is explicitly not serviceable —
    that's a valid business outcome, not an error.
    """
    today = today or date.today()

    candidates = [z for z in zones if pincode.startswith(z.pincode_prefix)]
    if not candidates:
        return DeliveryResult(serviceable=False, message=UNAVAILABLE_MESSAGE)

    best = max(candidates, key=lambda z: len(z.pincode_prefix))

    if not best.is_serviceable:
        return DeliveryResult(serviceable=False, message=UNAVAILABLE_MESSAGE)

    estimated_date = (today + timedelta(days=best.max_days)).isoformat()
    return DeliveryResult(
        serviceable=True,
        min_days=best.min_days,
        max_days=best.max_days,
        estimated_date=estimated_date,
    )
