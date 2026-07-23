from dataclasses import dataclass

from config import settings


@dataclass
class CandidateProduct:
    id: str
    title: str
    brand: str
    category: str
    price: float
    image_url: str | None
    has_requested_size_in_stock: bool


def find_alternatives(
    product_id: str,
    category: str,
    price: float,
    candidates: list[CandidateProduct],
    limit: int | None = None,
    tolerance: float | None = None,
) -> list[CandidateProduct]:
    """
    Deliberately simple rule-based matching (same category, price within
    +/- tolerance, has the requested size in stock) rather than a real
    recommender — documented as a scope cut in the README. Sorted by price
    proximity to the original so the closest substitutes surface first.
    """
    tolerance = tolerance if tolerance is not None else settings.alternatives_price_tolerance
    limit = limit if limit is not None else settings.alternatives_limit

    low = price * (1 - tolerance)
    high = price * (1 + tolerance)

    matches = [
        c
        for c in candidates
        if c.id != product_id
        and c.category == category
        and c.has_requested_size_in_stock
        and low <= c.price <= high
    ]

    matches.sort(key=lambda c: abs(c.price - price))
    return matches[:limit]
